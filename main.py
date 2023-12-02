import os
import random
import time
from pprint import pprint

import openai
from openai._types import NOT_GIVEN
from todoist_api_python.api import TodoistAPI
import json

from calendar_test import get_upcoming_events, create_events, update_events, remove_events
from message_bases import initial_conversation_for_picker_generator, get_organiser_tools, FunctionNames, \
    get_tool_choice_dict, get_noter_tools, initial_conversation_for_noter_generator
from stable_utils import get_gpt_tasks, get_todoist_tasks, add_prompt, EstimationModels, \
    create_tool_call
from speech_to_text import record_and_transcribe, only_transcribe
from text_to_speach import voice_to_speech
from todo_integration_utils import parse_todo, remove_todos, update_todos

with open('cred/additional_keys.json', 'r') as file:
    keys = json.load(file)

# Access the keys
gpt_key = keys['gpt_key']
api = TodoistAPI(keys['todoist_api_token'])

USER = 'user'
ASSISTANT = 'assistant'


def create_tool_response(tool_call_id, function_name, response):
    return {
        "tool_call_id": tool_call_id,
        "role": "tool",
        "name": function_name,
        "content": response,
    }


def execute_function_call(tool_call, obsidian_path=''):
    # print(tool_call.json())
    if tool_call.function.name == FunctionNames.add_todos.value:
        query = json.loads(tool_call.function.arguments)["new_todos"]
        results = parse_todo(api, gpt_project, query)
        return results
    elif tool_call.function.name == FunctionNames.get_todos.value:
        return json.dumps(get_todoist_tasks(api, gpt_project))
    elif tool_call.function.name == FunctionNames.remove_todos.value:
        return remove_todos(api,
                            gpt_project,
                            json.loads(tool_call.function.arguments)["todos_to_remove"])
    elif tool_call.function.name == FunctionNames.update_todos.value:
        return update_todos(api,
                            gpt_project,
                            json.loads(tool_call.function.arguments)["updated_todos"])
    elif tool_call.function.name == FunctionNames.update_todos.value:
        return update_todos(api,
                            gpt_project,
                            json.loads(tool_call.function.arguments)["updated_todos"])
    elif tool_call.function.name == FunctionNames.get_events.value:
        return json.dumps(get_upcoming_events())

    elif tool_call.function.name == FunctionNames.add_events.value:
        return create_events(json.loads(tool_call.function.arguments)["events_to_add"])

    elif tool_call.function.name == FunctionNames.update_events.value:
        return update_events(json.loads(tool_call.function.arguments)["events_to_update"])

    elif tool_call.function.name == FunctionNames.remove_events.value:
        return remove_events(json.loads(tool_call.function.arguments)["events_to_remove"])

    elif tool_call.function.name == FunctionNames.get_200_random_obsidian_notes.value:
        return get_random_obsidian_notes(obsidian_path, min(200, get_obsidian_notes_n(obsidian_path)))

    elif tool_call.function.name == FunctionNames.get_obsidian_notes_number.value:
        return str(get_obsidian_notes_n(obsidian_path))

    else:
        results = f"Error: function {tool_call.function.name} does not exist"
    return results


def get_obsidian_notes_n(obsidian_path):
    entries = os.listdir(obsidian_path)
    files = [entry for entry in entries if os.path.isfile(os.path.join(obsidian_path, entry))]
    return len(files)


def get_random_obsidian_notes(obsidian_path, n):
    entries = os.listdir(obsidian_path)
    files = [entry for entry in entries if os.path.isfile(os.path.join(obsidian_path, entry))]
    files = random.sample(files, n)
    files_dict = []
    for i in files:
        with open(os.path.join(obsidian_path, i)):
            files_dict.append({"fileName": i, "content": i})
    return json.dumps(files_dict)


projects = api.get_projects()
gpt_project = [i for i in projects if i.name == "GPT"][0]


def generic_tool_conversation(conversation_source, initial_generator, get_tools, conversation_pre_seed,
                              final_output_handler, task_executor=execute_function_call,
                              response_format=NOT_GIVEN):
    conversation, SYSTEM_MESSAGE = initial_generator()

    openai.api_key = gpt_key

    # here can be a loop?
    user_input = conversation_source()

    conversation_pre_seed(conversation, task_executor=task_executor)
    add_prompt(conversation, user_input, USER)

    done = False

    while not done:
        chat = openai.chat.completions.create(
            model=EstimationModels.gpt_4_turbo.value,
            messages=[*conversation],
            max_tokens=3000,
            temperature=0.5,
            tools=get_tools() if get_tools() != [] else NOT_GIVEN,
            response_format=response_format
        )

        conversation.append(chat.choices[0].message)
        tool_calls = chat.choices[0].message.tool_calls
        if tool_calls is not None:
            for i, b in enumerate(tool_calls):
                response = task_executor(chat.choices[0].message.tool_calls[i])
                conversation.append(
                    create_tool_response(
                        chat.choices[0].message.tool_calls[i].id,
                        chat.choices[0].message.tool_calls[i].function.name,
                        response
                    )
                )
        if chat.choices[0].message.content and chat.choices[0].finish_reason == 'stop':
            final_output_handler(chat.choices[0].message.content)
            done = True
    time.sleep(1)


def add_noter_pre_seed(conversation, task_executor):
    conversation.append(
        create_tool_call(tool_call_id='call_qqqqqqqqqqqqqqqqqqqqqqqq',
                         function_name=FunctionNames.get_obsidian_notes_number.value,
                         function_args={}))
    conversation.append(
        create_tool_response(
            conversation[-1].tool_calls[0].id,
            conversation[-1].tool_calls[0].function.name,
            task_executor(conversation[-1].tool_calls[0])
        )
    )

    conversation.append(  # TODO this probably will not be needed
        create_tool_call(tool_call_id='call_gggggggggggggggggggggggg',
                         function_name=FunctionNames.get_200_random_obsidian_notes.value,
                         function_args={}))
    conversation.append(
        create_tool_response(
            conversation[-1].tool_calls[0].id,
            conversation[-1].tool_calls[0].function.name,
            task_executor(conversation[-1].tool_calls[0])
        )
    )


def add_organiser_pre_seed(conversation, task_executor):
    conversation.append(
        create_tool_call(tool_call_id='call_tttttttttttttttttttttttt', function_name=FunctionNames.get_todos.value,
                         function_args={}))
    conversation.append(
        create_tool_response(
            conversation[-1].tool_calls[0].id,
            conversation[-1].tool_calls[0].function.name,
            task_executor(conversation[-1].tool_calls[0])
        )
    )

    conversation.append(
        create_tool_call(tool_call_id='call_cccccccccccccccccccccccc', function_name=FunctionNames.get_events.value,
                         function_args={}))
    conversation.append(
        create_tool_response(
            conversation[-1].tool_calls[0].id,
            conversation[-1].tool_calls[0].function.name,
            execute_function_call(conversation[-1].tool_calls[0])
        )
    )


def run_organiser(conversation_source):
    generic_tool_conversation(conversation_source, initial_conversation_for_picker_generator, get_organiser_tools,
                              add_organiser_pre_seed, final_output_handler=voice_to_speech)


def save_note(note, notes_path, parent_path):
    with open(f'{notes_path}/{note["fileName"]}', 'w') as f:
        f.write(note["content"])
        f.write(f"\n [[{parent_path}|Source Transcription]]")


def noter_final_generator(notes_path, parent_path):
    def noter_final_handler(output):
        output_dict = json.loads(output)

        for note in output_dict["notes"]:
            save_note(note, notes_path, parent_path)

        voice_to_speech(output_dict["summaryMessage"])

    return noter_final_handler


def run_noter(conversation_source, notes_path, parent_path):  # need to clean this
    generic_tool_conversation(conversation_source, initial_conversation_for_noter_generator, get_noter_tools,
                              add_noter_pre_seed,
                              task_executor=lambda tool_call: execute_function_call(tool_call,
                                                                                    obsidian_path=notes_path),
                              final_output_handler=noter_final_generator(notes_path, parent_path),
                              response_format={"type": "json_object"})


def backuped(transcribtion, bck_path):
    with open(bck_path, "w") as f:
        f.write(transcribtion)
    return transcribtion


def get_saved_transcription(path):
    with open(path) as f:
        file_contents = f.read()
    return file_contents


class ConversationSources:
    text_input = input
    live_recording = lambda: record_and_transcribe('pl')
    saved_recording = lambda path, lang='pl', bck_path=None: \
        lambda: only_transcribe(lang, path=path) if bck_path is None else (
            backuped(only_transcribe(lang, path=path), bck_path))
    saved_transcription = lambda file_path: lambda: get_saved_transcription(file_path)


if __name__ == '__main__':
    # print(get_gpt_tasks(api, gpt_project))
    run_organiser(ConversationSources.live_recording)
