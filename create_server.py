import os
import sys
import subprocess


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


os.environ['VAR'] = new_folder_name
docker_command = f" docker-compose --project-name {new_folder_name} up"
try:
    process = subprocess.run(docker_command.split(), check=True)
except KeyboardInterrupt:
    subprocess.run("docker-compose down".split())
    print("A program futása megszakadt!")
