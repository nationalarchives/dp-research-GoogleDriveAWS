#!/usr/bin/Python3

import os

from oauth2client import client

from oauth2client import tools

from oauth2client.file import Storage

import httplib2


# If modifying these scopes, delete your previously saved credentials

# at ~/.credentials/drive-python-quickstart.json

SCOPES = 'https://www.googleapis.com/auth/drive.readonly' #allows read access to metadata and files

CLIENT_SECRET_FILE = 'credentials.json'

APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.



    If nothing has been stored, or if the stored credentials are invalid,

    the OAuth2 flow is completed to obtain the new credentials.



    Returns:

        Credentials, the obtained credential.

    """

    home_dir = os.path.expanduser('~')

    credential_dir = os.path.join(home_dir, '.credentials2')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    credential_path = os.path.join(credential_dir,

                                   'drive-python-quickstart.json')

    store = Storage(credential_path)

    credentials = store.get()

    if not credentials or credentials.invalid:

        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

        flow.user_agent = APPLICATION_NAME

        if flags:

            credentials = tools.run_flow(flow, store, flags)

        else:  # Needed only for compatibility with Python 2.6

            credentials = tools.run(flow, store)

        print('Storing credentials to ' + credential_path)

    return credentials