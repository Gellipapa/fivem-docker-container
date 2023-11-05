import os
import subprocess
from pathlib import Path

import docker
from tqdm import tqdm

from fivem_server_manager.utils import get_artifact_version, get_existing_server_folders, \
    get_server_folders, selection_menu, stop_other_fivem_server_containers
from fivem_server_manager.settings import WORKING_DIR, _LOCALE


def main():
    server_folder_names = [folder.name for folder in get_existing_server_folders()]
    print(_LOCALE("SELECT_SERVER_TO_START"))
    selected_server = selection_menu(_LOCALE('CHOICE'), server_folder_names)
    artifact_version = get_artifact_version(get_server_folders() / Path(selected_server))

    os.environ['FIVEM_SERVER_NAME'] = selected_server
    os.environ['ARTIFACT_VERSION'] = artifact_version
    stop_other_fivem_server_containers()
    try:
        subprocess.run(["docker-compose", "--project-name", selected_server, "up"], check=True)
    except KeyboardInterrupt:
        subprocess.run(["docker-compose", "down"])


if __name__ == "__main__":
    main()
