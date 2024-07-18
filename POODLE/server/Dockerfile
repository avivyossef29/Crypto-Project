# Use an older base image with OpenSSL that supports SSLv3
FROM ubuntu:14.04

# Install Apache and OpenSSL
RUN apt-get update && \
    apt-get install -y apache2 openssl

# Enable SSL and install mod_ssl
RUN a2enmod ssl

# Set the ServerName globally
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Copy the SSL configuration file
COPY ./httpd-ssl.conf /etc/apache2/sites-available/default-ssl.conf

# Copy the SSL certificates
COPY ./server.crt /etc/ssl/certs/server.crt
COPY ./server.key /etc/ssl/private/server.key

# Enable the SSL site
RUN a2ensite default-ssl

# Expose port 443 for SSL
EXPOSE 443

# Start Apache in the foreground
CMD ["apachectl", "-D", "FOREGROUND"]