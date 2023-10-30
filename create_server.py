import os
import sys
import subprocess
import requests
import json
from pathlib import Path


folders = []
for entry in os.scandir("./"):
    if entry.is_dir() and (entry.name != '[cfxserver]' and entry.name != 'sql_scripts'):
        folders.append(entry.name)

while True:
    new_folder_name = input("Kérem, adjon meg egy mappanevet: ")
    if new_folder_name in folders:
        print("Ez a mappanév már szerepel a listában. Kérem, adjon meg másikat.")
    else:
        break


registry_url = "https://registry.hub.docker.com/v2/repositories/traskin/fxserver/tags/"
params = {
    "ordering": "last_updated",
    "page_size": 10
}

response = requests.get(registry_url, params=params)

if response.status_code == 200:
    tags = response.json()['results']
    for tag in tags:
        print(f"Tag: {tag['name']}, Last Updated: {tag['last_updated']}")
else:
    print("Failed to fetch tags:", response.status_code, response.text)

os.environ['VAR'] = new_folder_name
selected_artifact_input = input("Milyen artifact verziót szeretnél használni add meg vagy hagyd üresen: ")
os.environ['ARTIFACT'] = selected_artifact_input

path = Path.cwd() / new_folder_name

if not path.exists():
    path.mkdir(parents=True)
    print(f"Folder '{new_folder_name}' created successfully at {path}")
else:
    print(f"Folder '{new_folder_name}' already exists at {path}")


if selected_artifact_input:
    with open(f'./{new_folder_name}/artifact_version.txt', 'w') as file:
        file.write(os.environ['ARTIFACT'])
    docker_build_command = f"docker-compose build"
    subprocess.run(docker_build_command.split(), check=True)
docker_command = f" docker-compose --project-name {new_folder_name} up"
try:
    process = subprocess.run(docker_command.split(), check=True)
except KeyboardInterrupt:
    subprocess.run("docker-compose down".split())
    print("A program futása megszakadt!")
    