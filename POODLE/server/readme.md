build image: docker build -t server-demo .
run container: docker run -d -p 443:443 --name server-demo server-demo
test server: openssl s_client -connect localhost:443 -ssl3


docker rm -f server-demo ; docker build -t server-demo . ; docker run -d -p 443:443 --name server-demo server-demo ; docker image prune -f
