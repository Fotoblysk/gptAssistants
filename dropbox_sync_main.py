import time
from shutil import copyfile

import inotify.adapters
import json
import os
import threading
import queue

from main import run_organiser, ConversationSources, run_noter

LOCAL_DROPBOX_DIR = '/home/fotoblysk/Dropbox/Recorders'  # Local Dropbox directory to monitor
LOCAL_STATUS_FILE = '/home/fotoblysk/Dropbox/processedStatus.json'  # Local JSON file to store processed status
TRANS_LOCATION_BASE = '/home/fotoblysk/Dropbox/Obsydian/RawTranscriptions'
REC_LOCATION_BASE = '/home/fotoblysk/Dropbox/Obsydian/RawRecordings'
NOTER_LOCATION = '/home/fotoblysk/Dropbox/Obsydian/GPTNotes'


def update_processed_status(file_name, status):
    if os.path.exists(LOCAL_STATUS_FILE):
        with open(LOCAL_STATUS_FILE, 'r') as f:
            status_data = json.load(f)
    else:
        status_data = {}

    status_data[file_name] = status

    with open(LOCAL_STATUS_FILE, 'w') as f:
        json.dump(status_data, f, indent=4)


def process_file(file_path):
    # Your custom function to process the file
    print(f"Processing file: {file_path}")
    # try:
    # backup old
    copyfile(file_path, os.path.join(REC_LOCATION_BASE, file_path.split("/")[-1]))

    run_organiser(ConversationSources.saved_recording(
        file_path,
        bck_path=f'{TRANS_LOCATION_BASE}/{file_path.split("/")[-1]}.md'))

    run_noter(ConversationSources.saved_transcription(f'{TRANS_LOCATION_BASE}/{file_path.split("/")[-1]}.md'),
              NOTER_LOCATION,
              f'{TRANS_LOCATION_BASE}/{file_path.split("/")[-1]}.md')

    # Update the status to True after processing False if processing failed
    update_processed_status(file_path, True)
    # except Exception as e:
    #    print(f'Failed to process file {file_path}, e: {e}')
    update_processed_status(file_path, False)


def monitor_dropbox_dir():
    i = inotify.adapters.Inotify()
    i.add_watch(LOCAL_DROPBOX_DIR)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        # Check for 'IN_CLOSE_WRITE' event to ensure the file write is completed
        if ('IN_CLOSE_WRITE' in type_names
                or 'IN_MOVED_TO' in type_names):  # Dropbox uses IN_CLOSE_NOWRITE so we monitor IN_MOVED_TO,
            # could also IN_MODIFY (it also uses that)
            file_path = os.path.join(path, filename)
            # Check if the file has already been processed
            if not os.path.exists(LOCAL_STATUS_FILE) or file_path not in json.load(open(LOCAL_STATUS_FILE)):
                task_queue.put(file_path)


def execute_tasks_from_queue():
    while True:
        time.sleep(1)
        file_path = task_queue.get()
        print(f'working on task {file_path}')
        process_file(file_path)
        task_queue.task_done()


def process_existing_files(process_failed=False):
    # Process all existing files in the directory
    for root, dirs, files in os.walk(LOCAL_DROPBOX_DIR):
        for filename in files:
            file_path = os.path.join(root, filename)
            # Check if the file has already been processed
            if (not os.path.exists(LOCAL_STATUS_FILE) or
                    (file_path not in json.load(open(LOCAL_STATUS_FILE)) or
                     (process_failed is True and json.load(open(LOCAL_STATUS_FILE))[file_path] is False))):
                task_queue.put(file_path)


if __name__ == '__main__':
    task_queue = queue.Queue()

    print("existing process")
    PROCESS_OLD = True
    if PROCESS_OLD:
        process_existing_files(process_failed=True)

    task_executor = threading.Thread(target=execute_tasks_from_queue, daemon=True)
    print("over ex process")
    task_executor.start()

    print("new process")
    monitor_dropbox_dir()
    print("new process end")
