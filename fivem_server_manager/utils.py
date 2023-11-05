from datetime import datetime
from pathlib import Path
from typing import List, Sequence, Tuple

import docker
import requests
from tqdm import tqdm

from fivem_server_manager.settings import DEFAULT_ARTIFACT_VERSION, SERVER_FOLDER, WORKING_DIR, \
    _LOCALE


def get_artifact_version(server_folder: Path) -> str:
    artifact_version_path = server_folder / Path('artifact_version.txt')
    try:
        with open(artifact_version_path, 'r') as file:
            return file.readline()
    except FileNotFoundError:
        return DEFAULT_ARTIFACT_VERSION


def set_artifact_version(server_folder: Path, artifact_version: str) -> None:
    artifact_version_path = server_folder / Path('artifact_version.txt')
    with open(artifact_version_path, 'w') as file:
        file.write(artifact_version)


def fetch_available_manifest_versions() -> None | List[Tuple[str, datetime]]:
    registry_url = "https://registry.hub.docker.com/v2/repositories/traskin/fxserver/tags/"
    params = {
        "ordering": "last_updated",
        "page_size": 10
    }
    response = requests.get(registry_url, params=params)
    if response.status_code == 200:
        tags = response.json()['results']
        return [
            (tag["name"], datetime.fromisoformat(tag["last_updated"].split('.')[0]))
            for tag in tags
        ]
    return None

def get_server_folders() -> Path:
    server_folders = Path(WORKING_DIR) / Path(SERVER_FOLDER)
    server_folders.mkdir(parents=True, exist_ok=True)
    return server_folders


def get_new_folder_from_input() -> Path:
    existing_folder_names = get_existing_server_folders()

    new_folder_name = input(_LOCALE("ENTER_FOLDER_NAME"))
    if new_folder_name not in existing_folder_names:
        new_folder_path = get_server_folders() / Path(new_folder_name)
        new_folder_path.mkdir(parents=True, exist_ok=False)
        return new_folder_path
    print(_LOCALE("FOLDER_NAME_ALREADY_EXISTS"))
    get_new_folder_from_input()


def get_existing_server_folders() -> List[Path]:
    return [
        folder for folder in get_server_folders().iterdir() if folder.is_dir()
    ]


def pretty_print_artifact_versions(
    available_artifact_versions: List[Tuple[str, datetime]]
) -> None:
    formatted_list = [
        [version[0], version[1].strftime("%Y-%m-%d %H:%M:%S")]
        for version in available_artifact_versions
    ]
    longest_line = max(
        max(len(version_str), len(version_date)) for version_str, version_date in formatted_list
    )
    print(f"{'VERSION':<{longest_line}} | {'DATE':<{longest_line}}")
    for version_str, version_date in formatted_list:
        print(f"{version_str:<{longest_line}} | {version_date:<{longest_line}}")

def selection_menu(text: str, options: Sequence[str]) -> str:
    while True:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

        try:
            choice = int(input(text))
            return options[choice - 1]
        except (ValueError, IndexError):
            print(_LOCALE("INVALID_OPTION_CHOICE"))


def stop_other_fivem_server_containers() -> None:
    client = docker.from_env()
    # Shutdown currently running other fivem servers
    server_folder_names = [folder.name for folder in get_existing_server_folders()]
    other_fivem_containers = [
        container
        for container in client.containers.list()
        if container.labels["com.docker.compose.project"] in server_folder_names
    ]
    if other_fivem_containers:
        for container in tqdm(
            other_fivem_containers,
            desc=_LOCALE("SHUTTING_DOWN_OTHER_FIVEM_SERVERS"),
            unit="container"
        ):
            container.stop()
