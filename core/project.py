import os
import shutil
from core.project_config import ProjectConfig

class Project(object):
    def __init__(self, project_config):
        self.project_config = project_config

    def create_project(self):
        if self.project_config.is_valid:
            project_root_dir_path = self.project_config.get_project_root_path()
            if not os.path.exists(project_root_dir_path):
                print("INFO: Project root directory directory not found. It will be created...")
                os.makedirs(project_root_dir_path)
            else:
                print("INFO: Project root directory already exists.")
        else:
            print("ERROR: Cannot create project - project configuration is not valid.")

    
    def clone_repository(self):
        project_root_dir_path = self.project_config.get_project_root_path()
        if os.path.exists(project_root_dir_path):
            if self.project_config.is_force_instalation():
                print("INFO: FORCE INSTALLATION - the whole content of project root directory will be removed.")
                for root, dirs, files in os.walk(project_root_dir_path, topdown=False):
                    for filename in files:
                        os.remove(os.path.join(root, filename))
                    for dirname in dirs:
                        os.rmdir(os.path.join(root, dirname))

            root_list_dir = os.listdir(project_root_dir_path)
            root_dir_items_count = len(root_list_dir)

            if root_dir_items_count == 0:
                print("INFO: Cloning repository to project root directory...")
                os.chdir(project_root_dir_path)
                print(os.system('git clone ' + self.project_config.get_repository() + ' .'))

                repository_branch = self.project_config.get_repository_branch()
                if repository_branch != 'master':
                    print("INFO: Checking out repository to {}.".format(repository_branch))
                    print(os.system('git checkout {}'.format(repository_branch)))
            else:
                print("WARNING: Cannot clone repository - root directory not empty.")
        else:
            print("ERROR: Cannot clone repository - root project directory does not exists.")


    def create_dot_env_file(self):
        print("INFO: Creating .env file for the project...")
        project_root_dir_path = self.project_config.get_project_root_path()
        if os.path.exists(project_root_dir_path):
            os.chdir(project_root_dir_path)
            dot_env_filepath = os.path.join(project_root_dir_path, '.env')
            if not os.path.exists(dot_env_filepath):
                project_envs = self.project_config.get_project_str_env()
                if len(project_envs) > 0:
                    with open(dot_env_filepath, 'w') as dot_env_file:
                        project_envs = [line + '\n' for line in project_envs]
                        dot_env_file.writelines(project_envs)
                else:
                    print("WARNING: Cannot create .env file - no envs in config file.")
            else:
                print("WARNING: Cannot create .env file - already exists.")
        else:
            print("ERROR: Cannot create .env file - root project directory does not exists.")

    
    def copy_files(self):
        files_to_copy = self.project_config.get_files()
        if len(files_to_copy) > 0:
            print("INFO: Copying files to project...")
            
            project_root_dir_path = self.project_config.get_project_root_path()
            if os.path.exists(project_root_dir_path):
                for key, item in files_to_copy.items():
                    item_keys = item.keys()
                    if 'source' in item_keys and 'target' in item_keys:
                        if  os.path.exists(item['source']):
                            if os.path.exists(item['target']):
                                os.remove(item['target'])

                            print("INFO: Copying {}...".format(key))
                            result = shutil.copy2(item['source'], item['target'], follow_symlinks=True)
                            if result == item['target']:
                                print("INFO: File {} has been copied succesfully.".format(key))
                            else:
                                print("ERROR: Error during copying {}".format(key))
                        else:
                            print("ERROR: Cannot copy file {} - source file does not exists.".format(key))
                    else:
                        print("ERROR: Cannot copy files - missing source or target property in {}.".format(key))
            else:
                print("ERROR: Cannot copy files - root project directory does not exists.")
        else:
            print("INFO: Nothing to copy.")
        
