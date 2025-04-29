import os
import shutil
path = "C:\\Code\\ResearchProjectArtefacts\\ResearchProjectArtefacts\\file_organizer\\test_directory"


def get_dirs(path):
    dirs = os.listdir(path)
    dirs= [d for d in dirs if os.path.isdir(path +'/'+d)]
    #print(*directories, sep="\n")
    return dirs


def get_files(path):
    files = os.listdir(path)
    files = [f for f in files if os.path.isfile(path+'/'+f)]
    #print(*files, sep="\n")
    return files


def create_sub_dirs(path):
    files = get_files(path)
    

    for f in files:
        dir_name = os.path.splitext(f)[0]
        full_dir_path = os.path.join(path, dir_name)
        file_full_path = os.path.join(path, f)
        if not os.path.exists(full_dir_path):
            try:
                os.mkdir(full_dir_path)
            except PermissionError:
                print("No permission error")
                continue
        else:
            print(f"Directory path already exists {dir_name}")
        
        try:
            shutil.move(file_full_path, full_dir_path)
        except Exception as e:
            print(f"failed to move file {f} to {full_dir_path}: {e}")
        



create_sub_dirs(path)