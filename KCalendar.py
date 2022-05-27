from __future__ import print_function

from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import mwclient

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Creates the start and enddate in the correct UTC format
def getdate(myevent):
    date = (myevent['title']['DateTime UTC']).split(" ")
    mydate = [int(i) for i in date[0].split("-")]
    mytime = [int(i) for i in date[1].split(":")]
    startdate = datetime(mydate[0], mydate[1], mydate[2], mytime[0], mytime[1], mytime[2], 0)
    enddate = startdate + timedelta(hours=1)

    return startdate.isoformat(), enddate.isoformat()

# Does what its name suggests
def generate_google_event(title, startdate, enddate):
    event = {
        'summary': title,
        'start': {
            'dateTime': startdate,
            'timeZone': 'Europe/Paris',
        },
        'end': {
            'dateTime': enddate,
            'timeZone': 'Europe/Paris',
        },
    }
    return event

def main():
    existing = False
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Lol Fandom API
        # The Cargo query only includes the upcoming KC matches
        # The api doesn't really use the correct UTC format that's why there is a (str) cast and a specification of
        # the wanted format
        site = mwclient.Site('lol.fandom.com', path='/')
        response = site.api('cargoquery',
                            limit='max',
                            tables="MatchSchedule=MS",
                            fields="MS.Team1, MS.Team2, MS.DateTime_UTC",
                            where="(MS.Team1 = 'Karmine Corp' OR MS.Team2 = 'Karmine Corp') AND MS.DateTime_UTC >= '" + (str)(
            datetime.today().strftime("%Y-%m-%d %H:%M:%S"))+"'",
                            order_by="MS.DateTime_UTC"
                            )

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming already existing game events')

        events_result = service.events().list(calendarId='qhhbqgs8a0gsgfpmcrepnilc90@group.calendar.google.com',
                                              timeMin=now,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        # goes through all events and check that it does not already exist in the calendar if it does not,
        # then it adds it
        for KCevents in response.popitem()[1]:
            startdate, enddate = getdate(KCevents)
            title = KCevents['title']['Team1'] + " vs " + KCevents['title']['Team2']

            for existing_event in events:
                if existing_event['start']['dateTime'] == (startdate + "+02:00"):
                    existing = True
                    break
                else:
                    existing = False
            if not existing:
                event = service.events().insert(calendarId='qhhbqgs8a0gsgfpmcrepnilc90@group.calendar.google.com',
                                               body=generate_google_event(title,startdate,enddate)).execute()
                print('Event created: %s' % (event.get('htmlLink')))

        if not events:
            print('No upcoming events found.')
            return

        # CAUTION !!!
        # The following lines empty the calendar when executed
        #for event in events:
        #    service.events().delete(calendarId='qhhbqgs8a0gsgfpmcrepnilc90@group.calendar.google.com',eventId=event[
        #    'id']).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
