import argparse
import sys
import os
import yaml
from core.project_config import ProjectConfig
from core.project import Project
from core.server import Server


parser = argparse.ArgumentParser(description='')
parser.add_argument('-c', '--config',  type=str, help='Absolute path to config file', required=False)

if __name__ == '__main__':
    args = parser.parse_args()

    config = ProjectConfig(args.config)
    config.parse()

    print("=" * 33 + " CONFIGURATION " + "=" * 32)
    print("REPOSITORY: " + config.get_repository())
    print("BRANCH: " + config.get_repository_branch())
    print("PROJECT ROOT: " + config.get_project_root_path())
    print("WWW DIRECTORY: " + config.get_project_www_path())
    print("COMPOSE PATH: " + config.get_project_compose_path())

    project = Project(config)
    server = Server(config)
    print()

    print("=" * 31 + " STOPPING PROJECT " + "=" * 31)
    server.stop()
    print()

    print("=" * 31 + " CREATING PROJECT " + "=" * 31)
    project.create_project()
    print()

    print("=" * 31 + " CLONING PROJECT " + "=" * 32)
    project.clone_repository()
    print()

    print("=" * 30 + " CREATING .ENV FILE " + "=" * 30)
    project.create_dot_env_file()
    print()

    print("=" * 32 + " COPYING FILES " + "=" * 33)
    project.copy_files()
    print()

    print("=" * 31 + " STARTING PROJECT " + "=" * 31)
    server.start()
    print()

    print("=" * 35 + " FINISHED " + "=" * 34)