#docker build -t client_image .
#docker run --rm -t --name client_container --network=host client_image

FROM ubuntu:16.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for Firefox
RUN apt-get update && apt-get install -y \
    wget \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libxrender1 \
    libasound2 \
    bzip2 \
    ca-certificates \
    libdbus-glib-1-2 \
    libgtk2.0-0 \
    libx11-6 \
    libnss3-tools \
    sqlite3 \
    xvfb

# Download and install Firefox 7 from Mozilla's archive
RUN wget https://ftp.mozilla.org/pub/firefox/releases/7.0/linux-x86_64/en-US/firefox-7.0.tar.bz2 -O /tmp/firefox7.tar.bz2 && \
    tar -xjf /tmp/firefox7.tar.bz2 -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm /tmp/firefox7.tar.bz2

# Copy the self-signed certificate into the container
COPY server.crt /root/server.crt
# Create a Firefox profile directory
RUN mkdir -p /root/.mozilla/firefox/test-profile
# Initialize the NSS database for the Firefox profile
RUN certutil -N -d /root/.mozilla/firefox/test-profile --empty-password
# Import the self-signed certificate into the Firefox profile
RUN certutil -A -n "My Self-Signed Cert" -t "CT,," -i /root/server.crt -d /root/.mozilla/firefox/test-profile

# Copy the local JDK Linux file (jdk-7-linux-x64.tar.gz) into the Docker image
COPY jdk-7-linux-x64.tar.gz /tmp/jdk7.tar.gz
# Install Java 7 manually from the local file
RUN tar -xzf /tmp/jdk7.tar.gz -C /opt/ && \
    rm /tmp/jdk7.tar.gz && \
    ln -s /opt/jdk1.7.0/bin/java /usr/bin/java
# Link the Java plugin (libnpjp2.so) to Firefox's plugins directory
RUN mkdir -p /opt/firefox/plugins && \
    ln -s /opt/jdk1.7.0/jre/lib/amd64/libnpjp2.so /opt/firefox/plugins/


# Set the JAVA_HOME environment variable
ENV JAVA_HOME=/opt/jdk1.7.0
ENV PATH=$JAVA_HOME/bin:$PATH

# Import the certificate into the Java truststore
RUN keytool -import -alias server-cert -file /root/server.crt -keystore $JAVA_HOME/jre/lib/security/cacerts -storepass changeit -noprompt

# Set the working directory
WORKDIR /root

CMD ["bash", "-c", "Xvfb :99 -ac & export DISPLAY=:99 && firefox --no-remote --profile /root/.mozilla/firefox/test-profile https://127.0.0.3:443 & firefox_pid=$! && sleep 2 && pkill -f 'firefox --no-remote' && wait $firefox_pid; export DISPLAY=:99 && firefox --no-remote --profile /root/.mozilla/firefox/test-profile http://127.0.0.3:8080"]

#CMD ["bash", "-c", "Xvfb :99 -ac & export DISPLAY=:99 && firefox --no-remote --profile /root/.mozilla/firefox/test-profile http://127.0.0.3:8080"]
#CMD ["/bin/bash"]
#Xvfb :99 -ac &
#export DISPLAY=:99