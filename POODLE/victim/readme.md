build image: docker build -t victim-demo .
run container: docker run --link server-demo:server-demo victim-demo