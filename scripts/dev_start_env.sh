sudo docker-up
echo 'docker is up'
docker stop local-redis
docker rm local-redis
docker run --name local-redis -p 6379:6379 -d redis