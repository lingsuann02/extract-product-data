import os

def get_files_in_folder(path):
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f != '.DS_Store' and not os.path.isdir(f)
    ]

def get_folders_in_folder(path):
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f != '.DS_Store' and os.path.isdir(f)
    ]