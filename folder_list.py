import os
import sys
import subprocess
import docker
from tqdm import tqdm

client = docker.from_env()
container_list = [
    container
    for container in client.containers.list()
    if container.attrs['Name'] not in ["/pgadmin","/postgres"]
]

folder_path = "./"
folders = []

for entry in os.scandir(folder_path):
    if entry.is_dir() and (entry.name != '[cfxserver]' and entry.name != 'sql_scripts'):
        folders.append(entry.name)

print("A mappák a következők:")
for i in range(len(folders)):
    print(f"{i+1}. {folders[i]}")


if len(folders) == 0:
    print("Nincs még szerver mappa! Futtasd a create_server.bat-ot!")
else:
    while True:
        sys.stdout.write("Kérlek válassz egy mappát (1-{}): ".format(len(folders)))
        sys.stdout.flush()
        selected_folder_num = int(sys.stdin.readline().rstrip())
        if selected_folder_num < 1 or selected_folder_num > len(folders):
            print("A megadott szám nem érvényes. Kérem, próbálja újra.")
            continue
            
        selected_folder_name = folders[selected_folder_num - 1]
        break
try:
    with open(f'./{selected_folder_name}/artifact_version.txt', 'r') as file:
        os.environ['ARTIFACT'] = file.readline()
except FileNotFoundError:
    os.environ['ARTIFACT'] = "latest"

print("A kiválasztott mappa neve:", selected_folder_name)
os.environ['VAR'] = selected_folder_name

if len(container_list) > 0:
    print("Futó docker containerek:", *[container.attrs["Name"] for container in container_list])
    for container in tqdm(container_list, desc = "Futó docker containerek leállítása folyamatban", unit = "container"):
        container.stop()

docker_command = f" docker-compose --project-name {selected_folder_name} up"

try:
    process = subprocess.run(docker_command.split(), check=True)
except KeyboardInterrupt:
    subprocess.run("docker-compose down".split())
    os.system("exit /B")
    print("A program futása megszakadt! A container leállításra került!")