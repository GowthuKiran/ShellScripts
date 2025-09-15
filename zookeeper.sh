#!/bin/bash
# Script to install and configure Apache ZooKeeper on Linux
# Tested on Ubuntu/CentOS with Java 11+

set -e

ZOOKEEPER_VERSION="3.8.4"
INSTALL_DIR="/opt/zookeeper"
DATA_DIR="/var/lib/zookeeper"
USER="zookeeper"
CLIENT_PORT=2181

echo "=== Installing dependencies ==="
if [ -x "$(command -v apt)" ]; then
    sudo apt update -y
    sudo apt install -y wget tar openjdk-11-jdk
elif [ -x "$(command -v yum)" ]; then
    sudo yum install -y wget tar java-11-openjdk
else
    echo "Unsupported package manager!"
    exit 1
fi

echo "=== Creating user and directories ==="
sudo useradd -r -s /sbin/nologin $USER || true
sudo mkdir -p $INSTALL_DIR $DATA_DIR
sudo chown -R $USER:$USER $INSTALL_DIR $DATA_DIR

echo "=== Downloading ZooKeeper $ZOOKEEPER_VERSION ==="
cd /tmp
wget -q https://downloads.apache.org/zookeeper/zookeeper-$ZOOKEEPER_VERSION/apache-zookeeper-$ZOOKEEPER_VERSION-bin.tar.gz
tar -xzf apache-zookeeper-$ZOOKEEPER_VERSION-bin.tar.gz
sudo mv apache-zookeeper-$ZOOKEEPER_VERSION-bin/* $INSTALL_DIR
sudo chown -R $USER:$USER $INSTALL_DIR

echo "=== Configuring zoo.cfg ==="
cat <<EOF | sudo tee $INSTALL_DIR/conf/zoo.cfg
tickTime=2000
dataDir=$DATA_DIR
clientPort=$CLIENT_PORT
initLimit=5
syncLimit=2
EOF

echo "=== Setting server ID ==="
echo "1" | sudo tee $DATA_DIR/myid
sudo chown -R $USER:$USER $DATA_DIR

echo "=== Creating systemd service ==="
cat <<EOF | sudo tee /etc/systemd/system/zookeeper.service
[Unit]
Description=Apache ZooKeeper
After=network.target
Wants=network.target

[Service]
Type=simple
User=$USER
Group=$USER
ExecStart=$INSTALL_DIR/bin/zkServer.sh start-foreground
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

echo "=== Reloading systemd and starting ZooKeeper ==="
sudo systemctl daemon-reload
sudo systemctl enable zookeeper
sudo systemctl start zookeeper

echo "=== Checking ZooKeeper status ==="
sudo systemctl status zookeeper --no-pager
