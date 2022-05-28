# KCalendar
Python program which adds events corresponding to the upcoming Karmine Corp LoL matches to a specified GCalendar.

# How to use it ?
## Prerequisites
To run this script, you need the following prerequisites:

- For the [Google Calendar API prerequisites](https://developers.google.com/calendar/api/quickstart/python)
  - Python 2.6 or greater
  - The [pip](https://pypi.python.org/pypi/pip) package management tool
  - A Google Cloud Platform project with the API enabled. To create a project and enable an API, refer to [Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)
      Note: For this script, you are enabling the "Google Calendar API"
  - Authorization credentials for a desktop application. To learn how to create credentials for a desktop application, refer to [Create credentials](https://developers.google.com/workspace/guides/create-credentials)
  - A Google account with Google Calendar enabled
- For the [Leaguepedia API](https://lol.fandom.com/wiki/Help:Leaguepedia_API)
  - [mwclient](https://mwclient.readthedocs.io/en/latest/user/index.html): Lightweight python client

## Setting up
In 3 steps:
1. Add your credentials.json file in the same folder as KCalendar.py
2. Run the script for the first time to link your Google Account
3. Go to your task scheduler (Windows) and add a recurring run of your script. To learn how to do this, refer to [this video](https://www.youtube.com/watch?v=4n2fC97MNac&t=441s)

That's it :)
