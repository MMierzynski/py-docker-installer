import os
from core.project_config import ProjectConfig

class Server(object):

    def __init__(self, project_config):
        self.project_config = project_config
    

    def start(self):
        project_compose_filepath = self.project_config.get_project_compose_path()
        project_compose_file = self.project_config.get_project_compose_file()
        project_root_dir_path = self.project_config.get_project_root_path()
        cwd = os.getcwd()

        if os.path.exists(project_root_dir_path):
            if os.path.exists(project_compose_filepath):

                if cwd != os.path.dirname(project_compose_filepath): 
                     os.chdir(os.path.dirname(project_compose_filepath))
                
                docker_compose_command = 'docker-compose -f ' + project_compose_file + ' up -d'
                print("INFO: Starting server...")
                if self.project_config.is_build_required():
                    docker_compose_command += ' --build'

                print(os.system(docker_compose_command))
                os.chdir(cwd)
            else:
                print("ERROR: Cannot start server - docker-compose.yml file does not exists.")
        else:
            print("ERROR: Cannot start server - Root project directory does not exists.")

    def stop(self):
        project_compose_filepath = self.project_config.get_project_compose_path()
        project_compose_file = self.project_config.get_project_compose_file()
        project_root_dir_path = self.project_config.get_project_root_path()
        cwd = os.getcwd()

        if os.path.exists(project_root_dir_path):
            if os.path.exists(project_compose_filepath):
                if cwd != os.path.dirname(project_compose_filepath): 
                     os.chdir(os.path.dirname(project_compose_filepath))
                
                print(os.system('docker-compose down'))
                os.chdir(cwd)
            else:
                print("ERROR: Cannot stop server - docker-compose.yml file does not exists.")
        else:
            print("ERROR: Cannot stop server - Root project directory does not exists.")