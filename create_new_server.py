import os
import subprocess

from fivem_server_manager.settings import SERVER_FOLDER, WORKING_DIR, _LOCALE
from fivem_server_manager.utils import fetch_available_manifest_versions, \
    get_new_folder_from_input, pretty_print_artifact_versions, set_artifact_version, \
    stop_other_fivem_server_containers


def main():
    new_folder = get_new_folder_from_input()
    print(_LOCALE("AVAILABLE_ARTIFACT_VERSIONS"))
    available_artifact_versions = fetch_available_manifest_versions()
    if available_artifact_versions is not None:
        pretty_print_artifact_versions(available_artifact_versions)
    else:
        print(_LOCALE("ERROR_FETCHING_ARTIFACT_VERSIONS"))
    selected_artifact_version = input(_LOCALE("SELECT_ARTIFACT_VERSION"))

    os.environ['FIVEM_SERVER_NAME'] = new_folder.name
    os.environ['ARTIFACT_VERSION'] = selected_artifact_version

    set_artifact_version(new_folder, selected_artifact_version)

    stop_other_fivem_server_containers()
    subprocess.run(["docker-compose", "build"], check=True)
    try:
        subprocess.run(
            ["docker-compose", "--project-name", new_folder.name, "up"],
            check=True
        )
    except KeyboardInterrupt:
        subprocess.run(["docker-compose", "down"])


if __name__ == "__main__":
    main()
