import os
import json
import paramiko
from pathlib import Path

path_file_config_key = Path(os.getenv('PATH_FILE_CONFIG_KEY'))
path_file_config_aws = Path(os.getenv('PATH_FILE_CONFIG_BREAKER_AWS'))

with path_file_config_key.open('r') as file:
    dict_config_key = json.load(file)

client_ssh = paramiko.SSHClient()
client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
client_ssh.connect(
    hostname=dict_config_key['hostname'], 
    port=dict_config_key['port'], 
    username=dict_config_key['username'],
    password=dict_config_key['password'])   

# now do the test steps remotely
str_path_file_config_remote = '/home/jaap/breaker/config.cfg'
str_path_dir_code_remote = '/home/jaap/breaker/breaker_discord'
name = 'breaker_discord'
name_dockerfile = 'dockerfile_' + name
name_image = 'image_' + name
name_container = 'container_' + name


command =  'rm -Rf ' + str_path_dir_code_remote
stdin, stdout, stderr = client_ssh.exec_command(command)
print(stdout.readlines())
print(stderr.readlines())


command =  'git clone https://github.com/kozzion/breaker_discord ' + str_path_dir_code_remote
stdin, stdout, stderr = client_ssh.exec_command(command)
print(stdout.readlines())
print(stderr.readlines())

# stop container
command =  'docker stop ' + name_container
stdin, stdout, stderr = client_ssh.exec_command(command)
print(stdout.readlines())
print(stderr.readlines())

# unname old container
command =  'docker rm ' + name_container
stdin, stdout, stderr = client_ssh.exec_command(command)
print(stdout.readlines())
print(stderr.readlines())

# unname old image
command =  'docker rmi ' + name_image
stdin,stdout,stderr=client_ssh.exec_command(command)
print(stdout.readlines())
print(stderr.readlines())

# build new image
command =  'docker build'
command += ' -t ' + name_image
command += ' -f ' + str_path_dir_code_remote + '/docker/' + name_dockerfile
command += ' .'
print(command)
stdin,stdout,stderr=client_ssh.exec_command(command)
print(stdout.readlines())
print(stderr.readlines())

#run new image
#TODO move these back to config
command =  'docker run'
command += ' -e AWS_ACCESS_KEY_ID="' + os.environ['AWS_ACCESS_KEY_ID'] + '"'
command += ' -e AWS_SECRET_ACCESSS_KEY="' + os.environ['AWS_SECRET_ACCESSS_KEY'] + '"'
command += ' --name ' + name_container
command += ' --mount type=bind,source=' + str_path_file_config_remote + ',target=/config/config.cfg,readonly' 
command += ' ' + name_image
stdin,stdout,stderr=client_ssh.exec_command(command)
print(stdout.readlines())
print(stderr.readlines())