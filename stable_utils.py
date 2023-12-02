import json
from enum import Enum

from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_message_tool_call import Function


class EstimationModels(Enum):
    gpt_4_turbo = "gpt-4-1106-preview"  # 0.01/0.03
    gpt_4__vision_turbo = "gpt-4-1106-vision-preview"  # 0.01/0.03
    gpt_3_5_turbo = "gpt-3.5-turbo-1106"  # 0.01/0.03

#def print_debug_information(total_tokens, new_message_tokens):
#    print(f'TODOIST tasks: {get_gpt_tasks()}')
#    print(f'New message tokens: \t{new_message_tokens}')
#    print(f'Conversation tokens: \t{total_tokens}')

def get_gpt_tasks(api, gpt_project):
    tasks = api.get_tasks()
    gpt_tasks = [i for i in tasks if i.project_id == gpt_project.id]
    return gpt_tasks

def get_todoist_tasks(api, gpt_project):  # TODO limit usage of api
    return [
        {"id": i.id, "parent_id": i.parent_id, "name": i.content, "description": i.description, "priority": i.priority,
         "done": i.is_completed} for i in
        get_gpt_tasks(api, gpt_project) if not i.is_completed]

def add_prompt(conversation: list, content: str, role: str):
    conversation.append({"content": content, "role": role})

def create_tool_call(tool_call_id, function_name, function_args):
    return ChatCompletionMessage(content=None, role='assistant', tool_calls=[
        ChatCompletionMessageToolCall(id=tool_call_id,
                                      function=Function(arguments=json.dumps(function_args), name=function_name),
                                      type="function")
    ])
