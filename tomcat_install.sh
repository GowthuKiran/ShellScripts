#!/bin/bash
# Script to install Apache Tomcat on a Linux server
# Tested on CentOS/RHEL and Ubuntu/Debian

TOMCAT_VERSION=9.0.89
TOMCAT_USER=tomcat
INSTALL_DIR=/opt/tomcat

echo "### Updating system packages..."
if [ -f /etc/debian_version ]; then
    sudo apt update -y
    sudo apt install -y wget curl tar default-jdk
elif [ -f /etc/redhat-release ]; then
    sudo yum install -y wget curl tar java-11-openjdk-devel
else
    echo "Unsupported Linux distribution"
    exit 1
fi

echo "### Creating Tomcat user..."
sudo useradd -m -U -d $INSTALL_DIR -s /bin/false $TOMCAT_USER

echo "### Downloading Apache Tomcat..."
cd /tmp
wget https://downloads.apache.org/tomcat/tomcat-9/v$TOMCAT_VERSION/bin/apache-tomcat-$TOMCAT_VERSION.tar.gz

echo "### Installing Tomcat..."
sudo mkdir -p $INSTALL_DIR
sudo tar -xvzf apache-tomcat-$TOMCAT_VERSION.tar.gz -C $INSTALL_DIR --strip-components=1

echo "### Setting permissions..."
sudo chown -R $TOMCAT_USER:$TOMCAT_USER $INSTALL_DIR

echo "### Creating systemd service..."
sudo bash -c "cat > /etc/systemd/system/tomcat.service <<EOF
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

User=$TOMCAT_USER
Group=$TOMCAT_USER

Environment=\"JAVA_HOME=/usr/lib/jvm/java-11-openjdk\"
Environment=\"CATALINA_PID=$INSTALL_DIR/temp/tomcat.pid\"
Environment=\"CATALINA_HOME=$INSTALL_DIR\"
Environment=\"CATALINA_BASE=$INSTALL_DIR\"
Environment=\"CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC\"

ExecStart=$INSTALL_DIR/bin/startup.sh
ExecStop=$INSTALL_DIR/bin/shutdown.sh

[Install]
WantedBy=multi-user.target
EOF"

echo "### Reloading systemd and starting Tomcat..."
sudo systemctl daemon-reload
sudo systemctl enable tomcat
sudo systemctl start tomcat

echo "### Tomcat installation complete!"
echo "Access it at: http://<your_server_ip>:8080"
