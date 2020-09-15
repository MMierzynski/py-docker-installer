import os
import yaml
import json

class ProjectConfig(object):

    def __init__(self, filepath):
        pass
        self.filepath = filepath
        self.__config = dict()
    

    def parse(self):
        if os.path.exists(self.filepath) and os.path.isfile(self.filepath):
            ext = os.path.splitext(self.filepath)[1]
            if ext == '.yml' or ext == '.yaml':
                with open(self.filepath, 'r') as yaml_stream:
                    try:
                        self.__config = yaml.safe_load(yaml_stream)
                    except yaml.YAMLError as exc:
                        print(exc)
                        self.__config = dict()

                    self.__validate()

                    if not self.is_valid:
                        self.__config = dict()
            else:
                print("WARRNING: Cannot load configuration. Wrong file extension: "+ext)
        else:
            print("WARRNING: Configuration filepath does not exists or is not a file.")
    
            
    def get_repository(self):
        if self.is_valid:
            return self.__config['project']['repository']
        return ''
    

    def get_project_root_path(self):
        if self.is_valid:
            return self.__config['project']['root_dir']
        return ''
    

    def get_project_www_path(self):
        if self.is_valid:
            return os.path.join(self.__config['project']['root_dir'], self.__config['project']['www_dir'])
        return ''


    def get_project_compose_path(self):
        if self.is_valid:
            return os.path.join(self.__config['project']['root_dir'], self.__config['project']['compose_file'])
        return ''

    def get_project_compose_file(self):
        if self.is_valid:
            return self.__config['project']['compose_file']
        return ''

    def is_force_instalation(self):
        if 'force' in self.__config['project'].keys():
            return self.__config['project']['force']
        else:
            return False
            

    def is_build_required(self):
        if 'build' in self.__config['project'].keys():
            return self.__config['project']['build']
        else:
            return False

    
    def get_repository_branch(self):
        if 'branch' in self.__config['project'].keys():
            return self.__config['project']['branch']
        else:
            return 'master'


    def get_project_env(self):
        if 'env' in self.__config['project'].keys():
            return self.__config['project']['env']
        else:
            return list()
    

    def get_project_str_env(self):
        if 'env' in self.__config['project'].keys():
            config_envs = self.__config['project']['env']
            env_list = list()

            for env in config_envs:
                key, value = list(env.items())[0]
                env_list.append("{}={}".format(key, value))
            
            return env_list
        else:
            return list()
    

    def get_files(self): 
        if self.is_valid:
            if 'files' in self.__config['project'].keys():
                return self.__config['project']['files']
        return dict();

    def __validate(self):
        is_valid = False
        if len(self.__config) > 0:
            check_args = [
                {'project': ['repository', 'branch', 'root_dir', 'root_dir', 'compose_file']}, # required key and fields
                #{'server': ['config_source', 'config_target']} # key is not required, but when key exists the fields are requied
            ]

            for index, arg in enumerate(check_args):
                if index == 0:
                    is_valid = self.__check_argument(arg)
                else:
                    is_valid = self.__check_argument(arg, 'project', False)
                
                if not is_valid:
                    break
        else:
            print("WARNING: Config is empty.")
        self.is_valid = is_valid


    def __check_argument(self, arg, prev_key = None, key_req = True):
        arg_key = list(arg.keys())[0]
          
        if prev_key != None:
            haystack = self.__config[prev_key]
        else:
            haystack = self.__config
                
        if arg_key in haystack:
            arg_fields = list(arg.values())[0]
            
            for field in arg_fields:
                if field not in haystack[arg_key]:
                    print("WARNING: Field '{}' not found in section '{}'.".format(field, arg_key))
                    return False
            return True
        else:
            if key_req:
                print("WARNING: Section '{}' not found".format(arg_key))
                return False
            return True