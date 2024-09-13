docker run --rm --network=custom_network --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW attacker-demo  

docker rm -f attacker-demo ; docker build -t attacker-demo . ; docker run --rm --network=custom_network --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW
--name attacker-demo attacker-demo  ; docker image prune -f