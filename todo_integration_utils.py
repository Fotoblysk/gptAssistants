import json


def parse_todo(api, gpt_project, new_todos):
    ids = []
    for i in new_todos:
        task = api.add_task(
            content=i.get("name"),
            description=i.get("description"),
            priority=i.get("priority"),
            project_id=gpt_project.id)
        ids.append(task.id)
    return f"Todos with id's {' ; '.join(ids)} added successfully to todoist"


def remove_todos(api, gpt_project, removed_todos):
    ids = []
    for i in removed_todos:
        #print(f"removing todo {i}")
        api.delete_task(i, project_id=gpt_project.id)
        ids.append(str(i))
    return f"Todos with id's {' ; '.join(ids)} removed successfully from todoist"


def update_todos(api, gpt_project, updated_todo):
    ids = []
    for i in updated_todo:
        #print(f"updating todo {i}")
        api.update_task(task_id=i.get("task_id"),
                        content=i.get("name"),
                        description=i.get("description"),
                        priority=i.get("priority"),
                        project_id=gpt_project.id)
        ids.append(i.get("task_id"))
    return f"Todos with id's {' ; '.join(ids)} updated in todoist"
