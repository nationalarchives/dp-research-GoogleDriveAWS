#!/usr/bin/Python3

folder_id = input('Enter the URL of the Google folder which is the parent of all files and folder to transfer: ')  # takes the Google URL
folder_id = folder_id.rsplit('/', 1)[-1]  # strips rest of url to keep just the Google ID

import Google_API_Metadata

folder_list = []

if __name__ == '__main__':
    print('Collecting folder id list')
    Google_API_Metadata.get_root_folder(folder_id, folder_list)
    Google_API_Metadata.get_all_folders(folder_list)
    Google_API_Metadata.merge(folder_list, folder_id)
    print('Generating file metadata list')
    Google_API_Metadata.get_file_list()
print('Files Transferred')
print('done!')