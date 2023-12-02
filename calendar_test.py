import json
import os
import pickle
import time

import googleapiclient
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_upcoming_events():
    creds = None
    if os.path.exists('cred/token.json'):
        with open('cred/token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cred/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('cred/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API to get the list of all calendars
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])

    # Now get all upcoming events from each calendar
    all_upcoming_events = []
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events_from_all_calendars = []

    for calendar in calendars:
        # print('Getting the upcoming events for calendar:', calendar['summary'])
        # print(calendar)
        events_result = service.events().list(
            calendarId=calendar['id'],
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        parse_date = lambda date: datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime(
            '%Y-%m-%d %H:%M:%S') if date is not None else None

        test = [{
            'event_id': event.get('id'),
            'title': event.get('summary'),
            'location': event.get('location'),
            'description': event.get('description'),
            'start_date': parse_date(event['start'].get('dateTime')),
            'end_date': parse_date(event['end'].get('dateTime')),
            'calendar': calendar['summary']} for event in events]  # TODO add calendar
        events_from_all_calendars.extend(test)

        all_upcoming_events.extend(events)

        # for event in events:
        #    start = event['start'].get('dateTime', event['start'].get('date'))
        #    print(start, event)

    return events_from_all_calendars


def create_events(event_list):
    ids = []
    for event in event_list:
        ids.append(
            create_event(event.get('title'), event.get('start_date'), event.get('end_date'), event.get('description'),
                         event.get('location'))
        )
    return f'Successfully created events with ids: {" ; ".join(ids)}'


def update_events(event_list):
    ids = []
    for event in event_list:
        ids.append(
            edit_event(
                event['event_id'],
                event.get('title'), event.get('start_date'), event.get('end_date'), event.get('description'),
                event.get('location')
            )
        )
    return f'Successfully updated events with ids: {" ; ".join(ids)}'


def remove_events(event_list):
    ids = []
    for event in event_list:
        ids.append(
            remove_event(event)
        )
    return f'Successfully removed events with ids: {" ; ".join(ids)}'


def create_event(title, datetime_str1, datetime_str2, location=None, description=None, calendar_id='primary'):
    datetime1 = datetime.datetime.strptime(datetime_str1, "%Y-%m-%d %H:%M:%S")
    datetime2 = datetime.datetime.strptime(datetime_str2, "%Y-%m-%d %H:%M:%S")

    creds = None
    if os.path.exists('cred/token.json'):
        with open('cred/token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cred/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('cred/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Create the event with the correct time zone for Poland
    event = {
        'summary': title,
        'start': {
            'dateTime': datetime1.isoformat(),
            'timeZone': 'Europe/Warsaw',
        },
        'end': {
            'dateTime': datetime2.isoformat(),
            'timeZone': 'Europe/Warsaw',
        },
        'location': location,
        'description': description,
    }

    # Insert the event
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    #print('Event created: %s' % (created_event.get('htmlLink')))
    return created_event.get('id')


def edit_event(event_id, new_title=None, datetime_str1=None, datetime_str2=None, new_description=None, new_location=None,
               calendar_id='primary'):
    datetime1 = datetime.datetime.strptime(datetime_str1,
                                           "%Y-%m-%d %H:%M:%S").isoformat() if datetime_str1 is not None else None
    datetime2 = datetime.datetime.strptime(datetime_str2,
                                           "%Y-%m-%d %H:%M:%S").isoformat() if datetime_str2 is not None else None

    creds = None
    if os.path.exists('cred/token.json'):
        with open('cred/token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cred/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('cred/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

    # Modify the desired fields of the event
    if new_title:
        event['summary'] = new_title
    if new_location:
        event['location'] = new_location
    if new_description:
        event['description'] = new_description
    if datetime1:
        event['start']['dateTime'] = datetime1
    if datetime2:
        event['end']['dateTime'] = datetime2

    # Update the event
    updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()

    #print('Event updated:', updated_event['summary'])
    return event_id


def remove_event(event_id, calendar='primary'):
    creds = None
    if os.path.exists('cred/token.json'):
        with open('cred/token.json', 'r') as token:
            creds = Credentials.from_authorized_user_info(json.load(token), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cred/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('cred/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Replace 'primary' with the calendar ID you're using if it's not the primary calendar
    # Replace 'eventId' with the ID of the event you want to delete
    try:
        service.events().delete(calendarId=calendar, eventId=event_id).execute()
        #print("Event deleted")
        return event_id
    except googleapiclient.errors.HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    #print(get_upcoming_events())
    datetime_str1 = "2023-11-26 12:00:00"
    datetime_str2 = "2023-11-26 18:30:00"
    task_id = create_event("test", datetime_str1, datetime_str2)
    task_id2 = create_event("test to remove", datetime_str1, datetime_str2)
    time.sleep(5)
    edit_event(task_id, new_title="test_edited")
    time.sleep(5)
    remove_event(task_id2)
    remove_event(task_id)
    get_upcoming_events()
