all: server

server: server.c
	gcc -o server server.c -I/usr/local/ssl/include -L/usr/local/ssl/lib -lssl -lcrypto
