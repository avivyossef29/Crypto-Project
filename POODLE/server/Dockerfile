# Use an older base image with OpenSSL that supports SSLv3
FROM ubuntu:14.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y apache2 openssl python3 python3-pip

RUN pip3 install --index-url https://pypi.python.org/simple/ --upgrade pip3

RUN pip3 install --upgrade setuptools

# Install Flask
RUN pip3 install flask


# Enable SSL and install mod_ssl
RUN a2enmod ssl

# Set the ServerName globally
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Copy the SSL configuration file
COPY ./httpd-ssl.conf /etc/apache2/sites-available/default-ssl.conf

# Copy the SSL certificates
COPY ./server.crt /etc/ssl/certs/server.crt
COPY ./server.key /etc/ssl/private/server.key

# Copy the Flask app
COPY ./server.py /server.py

# Enable the SSL site
RUN a2ensite default-ssl

# Expose port 443 for SSL
EXPOSE 443

# Start Apache in the foreground and the Flask app
CMD ["bash", "-c", "apachectl -D FOREGROUND & python /server.py"]