build image: docker build -t victim-demo .
run container: docker run --link server-demo:server-demo victim-demo

docker rm -f victim-demo ; docker build -t victim-demo . ; docker run --rm --network=custom_network --name victim-demo victim-demo ; docker image prune -f