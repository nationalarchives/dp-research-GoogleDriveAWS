import get_credentials

import httplib2

from apiclient import discovery

import pandas as pd

import Google_AWS_Download


all_folders = []
file_list = []

def get_root_folder(folder_id, folder_list): #get's folder list from original root folder

    credentials = get_credentials.get_credentials()

    http = credentials.authorize(httplib2.Http())

    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(q="mimeType = 'application/vnd.google-apps.folder' and '"+folder_id+"' in parents",

        pageSize=1000, fields="nextPageToken, files(id, mimeType)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()

    folders = results.get('files', [])

    if not folders:
        print('No folders found.')

    else:
        for folder in folders:
            id = folder.get('id')
            folder_list.append(id)


def get_all_folders(folder_list): #creates list of all sub folder under root, keeps going until no folders underneath

    for folder in folder_list:
        additional_folders = []
        credentials = get_credentials.get_credentials()

        http = credentials.authorize(httplib2.Http())

        service = discovery.build('drive', 'v3', http=http)
        results = service.files().list(
            q="mimeType = 'application/vnd.google-apps.folder' and '" +folder+ "' in parents",

            pageSize=1000, fields="nextPageToken, files(id, mimeType)", supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        items = results.get('files', [])

        for item in items:
            id = item.get('id')
            additional_folders.append(id)
        if not additional_folders:
            pass
        else:
            all_folders.extend(additional_folders)
            folder_list = additional_folders
            get_all_folders(folder_list)


def merge(folder_list, folder_id): #merges sub folder list with full list
    global full_list
    full_list = all_folders + folder_list
    full_list.append(folder_id)


def get_file_list(): #runs over each folder generating file list, for files over 1000 uses nextpagetoken to run additional requests, picks up metadata included in the request
    for folder in full_list:
        credentials = get_credentials.get_credentials()

        http = credentials.authorize(httplib2.Http())

        service = discovery.build('drive', 'v3', http=http)

        page_token = None
        while True:
            results = service.files().list(
                q="'" + folder + "' in parents",

                pageSize=1000, fields="nextPageToken, files(name, md5Checksum, mimeType, size, createdTime, modifiedTime, id, parents, trashed)", pageToken=page_token, supportsAllDrives=True, includeItemsFromAllDrives=True).execute()

            items = results.get('files', [])
            for item in items:
                name = item['name']

                checksum = item.get('md5Checksum')

                size = item.get('size', '-')

                id = item.get('id')

                mimeType = item.get('mimeType', '-')

                createdTime = item.get('createdTime', 'No date')

                modifiedTime = item.get('modifiedTime', 'No date')

                parents = item.get('parents')

                trashed = item.get('trashed')


                file_list.append([name, checksum, mimeType, size, createdTime, modifiedTime, id, parents, trashed])

            page_token = results.get('nextPageToken', None)
            if page_token is None:
                break
    files = pd.DataFrame(file_list,columns=['file_name', 'checksum_md5', 'mimeType', 'size', 'date_created', 'date_last_modified', 'google_id', 'google_parent_id', 'trashed'])
    files.drop(files[files['trashed'] == True].index, inplace=True)  # removes files which have True listed in trashed, these are files which had been moved to the recycle bin
    print('Starting file transfer')
    Google_AWS_Download.downloadFileList(files)