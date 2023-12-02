import datetime
import json
from enum import Enum

picker_message_base_old = f"Today is {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. You are a helpful assistant and you should behave as one with general knowledge and complex reasoning, "
"You must always follow strict rules for your messages format. If think my input doesn't describe tasks anough you should still try to do your job."
"Whats more you have to proactively come up with tasks which are as small and detailed as possible that should be added to my todolist and "
"add, update, remove, complete them only using commands, and strict format "
"that is shown bellow:\n"
"1. !Very important! You always should write all messages in format:\n"
"MESSAGE_SECTION: message to user (may be in Polish or English just as user messages)\n"
"CODE_SECTION: EXECUTE_COMMAND command_name command_arg;\n"
"2. !Important! Do not list my tasks in MESSAGE_SECTION, all suggestions for todolist have to be in CODE_SECTION. When you menage my todolist tasks for me you have to type: \n"
"To add task in todolist type EXECUTE_COMMAND add_todo task_name\n"
"To update task in todolist type EXECUTE_COMMAND update_todo task_name\n"
"To remove task in todolist type EXECUTE_COMMAND remove_todo task_name\n"
"To complete task in todolist type EXECUTE_COMMAND complete_todo task_name\n"
"To do nothing DO_NOTHING\n"
"in the CODE_SECTION part."
"For example if you think I should clean my room type:\n"
"MESSAGE_SECTION: In you have a dirty room it may be an obstacle to tomorrow tasks. Adding cleaning room to todolist\n"
"CODE_SECTION: EXECUTE_COMMAND add_todo \"Clean room\";\n"
"Other example if you think I should buy eggs type :\n"
"MESSAGE_SECTION: I added buying eggs to your todolist \n"
"CODE_SECTION: EXECUTE_COMMAND add_todo \"Buy eggs\";\n"

picker_message_base_old_old = ("You are a helpful assistant and you "
                               "should behave as one with general knowledge and complex reasoning. "
                               "You will hear different inputs from heard conversations, my internal self talk, "
                               "lectures to direct instructions. "
                               "You must always follow strict rules for your messages format. "
                               "If think my input doesn't describe tasks enough you should still try to do your job."
                               "Whats more you have to proactively come up with tasks which are as small and detailed"
                               "as possible that should be added to my todolist and "
                               "add, update, remove, complete them only using add_todos function, remove_todos, get_todos"
                               " and specified strict format")

noter_message_base = ("You will get an input a text, then divide the text I will provide into as much as you can obsydian markdown atomic notes, "
                      "so the notes exhaust the topic, "
                      "using data from the text and your general knowledge. You should output data in json format useing the following schema: "
                      '`{"notes": [{fileName: "some file name beeing the title at the same time.md", "content": "NOTE_CONTENT"}], '
                      '"summaryMessage": "Message summarizing what you generated"}` .'
                      "The generated notes will be added to Obsidian vault."
                      "Each of the notes content (NOTE_CONTENT) should be capturing a single, clear narrative idea or concept related to the topic being researched, "
                      "adhering to the principles of Andy Matuschak's note-taking methodology. "
                      "Each atomic note must include sufficient detail and information relevant to the topic "
                      "and meet the following criteria: information relevance, reliability, clear structure, "
                      "detail, documentation, updating, accessibility, integration with other information, "
                      "accuracy, and critical evaluation of information. Pleas link notes with "
                      "[[linked_fileName.md|custom display text]] and make sure that every generated "
                      "has at least one link to something. The structure of each atomic NOTE_CONTENT "
                      "should have 2 parts:"
                      "The first part 'IDEEA,' must be a narrative text about the main idea or concept, "
                      "and the second part, 'Details,' should contain all the details of the main idea or concept. "
                      "The notes may contain subheadings, bullet points, or enumeration of details if necessary, "
                      "but each note must not deviate from capturing a single, "
                      "clear narrative idea and must avoid including multiple ideas or tangential information. "
                      "Finally, based on the content of each note, suggest a relevant title for each atomic note "
                      "created, with a maximum length of 70 characters and no symbols or colons. "
                      "After title also place relevant links if you couldn't find place for them in the text. "
                      "When you create some link if you haven't already provide note of that file name make sure "
                      "to generate linked note.")

picker_message_base = ("You are a helpful assistant and you "
                       "should behave as one with general knowledge and complex reasoning, "
                       "You must always follow strict rules for your messages format. "
                       "If think my input doesn't describe tasks enough you should still try to do your job."
                       "Whats more you have to proactively try to refine my todo list removing duplicate "
                       "tasks, merge, split, or add new. "
                       "You should add, update, remove, complete them only using add_todos function, remove_todos, "
                       "get_todos, update_todos"
                       " and specified strict format. "
                       "Don't remove (or update with data loss) any task "
                       "unless it is  already contained in one of the other new tasks,"
                       " or I explicitly tell you to remove something. "
                       "You will get all of my tasks in get_todos and all of them are important so make sure to not "
                       "remove anything even if they are unrelated to current context you got as they are all relevant"
                       "to my other plans, "
                       "and are not done yet (unless I explicitly say that something is already done). "
                       "After that if some tasks are or make sense to be time "
                       "specific they have some (start and end datetime)"
                       "you can menage my calendar. "
                       "You can do it with add_events, update_events, remove_events, get_events. "
                       "You can only modify my 'fotoblsks@gmail.com' calendar but all calendars events are valid you "
                       "just cant modify them, But you should still try to resolve events conflicts "
                       "between different calendars, tho it's better to not resolve conflict "
                       "than to not add calendar event."
                       " Don't remove (or update with data loss) any event "
                       "unless I explicitly tell you that I won't do some event, or that it's canceled. "
                       "You will get all of my events in get_events and all of them are important so make sure to not "
                       "remove anything even if they are unrelated to current context you got, as they are all relevant"
                       "to my other plans (unless I explicitly say that something I will not do or is cancelled). "
                       "Our interaction will look like this: "
                       "1. I will provide you with some text (heard conversations, my internal self talk, "
                       "lectures to direct instructions). "
                       "2. You will get_todos. "
                       "3. You will get_events. "
                       "4. You will update my todolist with chain of todolist operations. "
                       "5. You will update my calendar with chain of calendar events operations. "
                       "6. After you are done and only then you will tell me what you done. "
                       "!IMPORTANT you should only write text to me after you done all operations for given input in my"
                       "calendar and todolist")


# "that is shown bellow:\n"
# "1. !Very important! You always should write all messages in format:\n"
# "MESSAGE_SECTION: message to user (may be in Polish or English just as user messages)\n"
# "CODE_SECTION: EXECUTE_COMMAND command_name command_arg;\n"
# "2. !Important! Do not list my tasks in MESSAGE_SECTION, all suggestions for todolist have to be in CODE_SECTION. When you menage my todolist tasks for me you have to type: \n"
# "To add task in todolist type EXECUTE_COMMAND add_todo task_name\n"
# "To update task in todolist type EXECUTE_COMMAND update_todo task_name\n"
# "To remove task in todolist type EXECUTE_COMMAND remove_todo task_name\n"
# "To complete task in todolist type EXECUTE_COMMAND complete_todo task_name\n"
# "To do nothing DO_NOTHING\n"
# "in the CODE_SECTION part."
# "For example if you think I should clean my room type:\n"
# "MESSAGE_SECTION: In you have a dirty room it may be an obstacle to tomorrow tasks. Adding cleaning room to todolist\n"
# "CODE_SECTION: EXECUTE_COMMAND add_todo \"Clean room\";\n"
# "Other example if you think I should buy eggs type :\n"
# "MESSAGE_SECTION: I added buying eggs to your todolist \n"
# "CODE_SECTION: EXECUTE_COMMAND add_todo \"Buy eggs\";\n"


def initial_conversation_for_cleaner_generator(tasks=None):
    SYSTEM_MESSAGE = {"role": "system",
                      "content": picker_message_base
                      }
    conversation = [
        SYSTEM_MESSAGE,
    ]
    return conversation, SYSTEM_MESSAGE


def initial_conversation_for_picker_generator(tasks=None):
    SYSTEM_MESSAGE = {"role": "system",
                      "content": picker_message_base
                      }
    conversation = [
        SYSTEM_MESSAGE,
    ]
    return conversation, SYSTEM_MESSAGE


def initial_conversation_for_noter_generator(tasks=None):
    SYSTEM_MESSAGE = {"role": "system",
                      "content": noter_message_base
                      }
    conversation = [
        SYSTEM_MESSAGE,
    ]
    return conversation, SYSTEM_MESSAGE


def initial_conversation_for_picker_generator_old(tasks):
    SYSTEM_MESSAGE = {"role": "system",
                      "content": picker_message_base
                      }
    conversation = [
        SYSTEM_MESSAGE,
        {"role": "user", "content": picker_message_base
         },
        {"role": "assistant", "content": "MESSAGE_SECTION: Hello, how can I assist you?\n"
                                         "CODE_SECTION: DO_NOTHING;\n",
         },
        {"role": "user",
         "content": f"TODOLIST_STATE: todolist={json.dumps(tasks)}\n"
                    f"USER_MESSAGE:  Add \"test\" and test2 to my todolist.",
         },

        {"role": "assistant", "content": "MESSAGE_SECTION: I added \"test\" and \"test2\" to your todolist.\n"
                                         "CODE_SECTION: EXECUTE_COMMAND add_todo \"test\"; "
                                         "EXECUTE_COMMAND add_todo \"test2\";\n"
         },
        {"role": "user",
         "content": f'TODOLIST_STATE: '
                    f'todolist={json.dumps([*tasks, {"name": "test", "done": False}, {"name": "test2", "done": False}])}\n'
                    f'USER_MESSAGE: Remove test and test2 from my todolist.'},
        {"role": "assistant",
         "content": "MESSAGE_SECTION: I removed \"test\" and \"test2\" from your todolist.\n"
                    "CODE_SECTION: EXECUTE_COMMAND remove_todo \"test\"; EXECUTE_COMMAND remove_todo \"test2\";\n"
         },
    ]
    return conversation, SYSTEM_MESSAGE


class FunctionNames(Enum):
    get_todos = 'get_todos'
    add_todos = 'add_todos'
    update_todos = 'update_todos'
    remove_todos = 'remove_todos'

    get_events = 'get_events'
    add_events = 'add_events'
    update_events = 'update_events'
    remove_events = 'remove_events'

    get_obsidian_notes_number = 'get_obsidian_notes_number'
    search_obsidian_notes_for_string = 'search_obsidian_notes_for_string'
    get_linked_obsidian_notes = 'get_linked_obsidian_notes'
    get_obsidian_notes = 'get_obsidian_notes'
    get_200_random_obsidian_notes = 'get_200_random_obsidian_notes'


def get_organiser_tools():
    todoist_tools = [
        {"type": "function", "function": {
            "name": FunctionNames.get_todos.value,
            "description": "Get todos from todolist",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        }},
        {"type": "function", "function": {
            "name": FunctionNames.add_todos.value,
            "description": "Add todo to todolist",
            "parameters": {
                "type": "object",
                "properties": {
                    "new_todos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Name of the task"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Details of the task"
                                },
                                "priority": {
                                    "type": "number",
                                    "description": "Task priority from 1 (normal, default value) to 4 (urgent)."
                                },
                            }
                        }
                    }
                }

            },
        }},
        {"type": "function", "function": {
            "name": FunctionNames.remove_todos.value,
            "description": "Remove todos from todolist",
            "parameters": {
                "type": "object",
                "properties": {
                    "todos_to_remove": {  # add todoname to it to avoid accidents
                        "type": "array",
                        "items": {
                            "type": "number",
                            "description": "Id of the task to remove",
                        }
                    }
                }
            },
        }},
        {"type": "function", "function": {
            "name": FunctionNames.update_todos.value,
            "description": "Update todos from todolist",
            "parameters": {
                "type": "object",
                "properties": {
                    "updated_todos": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "task_id": {
                                    "type": "string",
                                    "description": "Id of task to update"
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Updated name of the task"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Updated details of the task"
                                },
                                "priority": {
                                    "type": "number",
                                    "description": "Updated task priority from 1 (normal, default value) to 4 (urgent)."
                                },
                            }
                        }
                    }
                }

            },
        }},
    ]

    calendar_tools = lambda calendar: [
        {"type": "function", "function": {
            "name": FunctionNames.get_events.value,
            "description": "Get all calendars events",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        }},
        {
            "type": "function", "function": {
            "name": FunctionNames.add_events.value,
            "description": f"Add calendar events to {calendar} calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "events_to_add": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "Event title"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Event location"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Event description"
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Event start date in format yyyy-mm-dd HH:MM:SS example: 2023-11-26 18:30:00"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "Event end date in format yyyy-mm-dd HH:MM:SS example: 2023-11-26 20:30:00"
                                },
                            }
                        }
                    }
                }
            },
        }},
        {"type": "function", "function": {
            "name": FunctionNames.update_events.value,
            "description": f"Update calendar events to {calendar} calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "events_to_update": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "event_id": {
                                    "type": "string",
                                    "description": "Id of event to update"
                                },
                                "title": {
                                    "type": "string",
                                    "description": "Updated title of the event"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "Updated location of the event"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Updated description of the event"
                                },
                                "start_date": {
                                    "type": "string",
                                    "description": "Updated start date of the event in format yyyy-mm-dd HH:MM:SS example: 2023-11-26 18:30:00"
                                },
                                "end_date": {
                                    "type": "string",
                                    "description": "Updated end date of the event in format yyyy-mm-dd HH:MM:SS example: 2023-11-26 20:30:00"
                                },
                            }
                        }
                    }
                }
            },
        }},
        {"type": "function", "function": {
            "name": FunctionNames.remove_events.value,
            "description": f"Remove calendar event to {calendar} calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "events_to_remove": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Id of event to remove"

                        }
                    }
                }
            },
        }}
    ]
    return [
        *todoist_tools,
        *calendar_tools('fotoblysk@fejm.pl')
    ]


def get_noter_tools():
    obsidian_tools = [
        {"type": "function", "function": {
            "name": FunctionNames.get_obsidian_notes_number.value,
            "description": "Get number of obsidian notes",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        }},
        {
            "type": "function", "function": {
            "name": FunctionNames.get_200_random_obsidian_notes.value,
            "description": f"Get 200 random obsidian notes",
            "parameters": {
                "type": "object",
                "properties": {
                }
            },
        }}

    ]
    return [
        *obsidian_tools,
    ]


def get_tool_choice_dict(funciton_name):
    return {"type": "function", "function": {"name": funciton_name}}
