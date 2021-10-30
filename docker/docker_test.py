import os
name = 'breaker_discord'
name_dockerfile = 'dockerfile_' + name
name_image = 'image_' + name
name_container = 'container_' + name

# stop container


# unname old container
command =  'docker rm ' + name_container
os.system(command)

# unname old image
command =  'docker rm ' + name_image
os.system(command)

# build new image
command =  'docker build'
command += ' -t ' + name_image
command += ' -f ' + name_dockerfile
command += ' build' # TODO remove this
os.system(command)

#run new image
command =  'docker run'
command += ' -e PATH_FILE_CONFIG_BREAKER="config.cfg"'
command += ' -e PATH_FILE_CONFIG_BREAKER="config.cfg"'
command += ' --name ' + name_container
command += ' ' + name_image
os.system(command)


# -e POSTGRES_ENV_POSTGRES_USER='bar' \
# -e POSTGRES_ENV_DB_NAME='mysite_staging' \
# -e POSTGRES_PORT_5432_TCP_ADDR='docker-db-1.hidden.us-east-1.rds.amazonaws.com' \
# -e SITE_URL='staging.mysite.com' \
# -p 80:80 \
# --link redis:redis \  
# --name container_name dockerhub_id/image_name
# command =  'docker scan image_breaker_discord'
# os.system(command)
# command += ' -t image_breaker_discord'
# command += ' -f dockerfile_breaker_discord'
# command += ' build'
