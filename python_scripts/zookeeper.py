#!/usr/bin/env python3
from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path


ZOOKEEPER_VERSION = "3.8.4"
INSTALL_DIR = "/opt/zookeeper"
DATA_DIR = "/var/lib/zookeeper"
USER = "zookeeper"
CLIENT_PORT = 2181


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    print("=== Installing dependencies ===")
    if shutil.which("apt"):
        run(["sudo", "apt", "update", "-y"])
        run(["sudo", "apt", "install", "-y", "wget", "tar", "openjdk-11-jdk"])
    elif shutil.which("yum"):
        run(["sudo", "yum", "install", "-y", "wget", "tar", "java-11-openjdk"])
    else:
        print("Unsupported package manager!")
        return 1

    print("=== Creating user and directories ===")
    subprocess.run(["sudo", "useradd", "-r", "-s", "/sbin/nologin", USER], check=False)
    run(["sudo", "mkdir", "-p", INSTALL_DIR, DATA_DIR])
    run(["sudo", "chown", "-R", f"{USER}:{USER}", INSTALL_DIR, DATA_DIR])

    print(f"=== Downloading ZooKeeper {ZOOKEEPER_VERSION} ===")
    os.chdir("/tmp")
    archive = f"apache-zookeeper-{ZOOKEEPER_VERSION}-bin.tar.gz"
    run(["wget", "-q", f"https://downloads.apache.org/zookeeper/zookeeper-{ZOOKEEPER_VERSION}/{archive}"])
    run(["sudo", "mkdir", "-p", INSTALL_DIR])
    run(["sudo", "tar", "-xzf", archive, "--strip-components=1", "-C", INSTALL_DIR])
    run(["sudo", "chown", "-R", f"{USER}:{USER}", INSTALL_DIR])

    zoo_cfg = f"""tickTime=2000
dataDir={DATA_DIR}
clientPort={CLIENT_PORT}
initLimit=5
syncLimit=2
"""
    cfg_path = Path("/tmp/zoo.cfg")
    cfg_path.write_text(zoo_cfg, encoding="utf-8")
    run(["sudo", "cp", str(cfg_path), f"{INSTALL_DIR}/conf/zoo.cfg"])

    myid = Path("/tmp/myid")
    myid.write_text("1\n", encoding="utf-8")
    run(["sudo", "cp", str(myid), f"{DATA_DIR}/myid"])
    run(["sudo", "chown", "-R", f"{USER}:{USER}", DATA_DIR])

    service = f"""[Unit]
Description=Apache ZooKeeper
After=network.target
Wants=network.target

[Service]
Type=simple
User={USER}
Group={USER}
ExecStart={INSTALL_DIR}/bin/zkServer.sh start-foreground
Restart=on-failure
RestartSec=5
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
"""
    service_path = Path("/tmp/zookeeper.service")
    service_path.write_text(service, encoding="utf-8")
    run(["sudo", "cp", str(service_path), "/etc/systemd/system/zookeeper.service"])

    print("=== Reloading systemd and starting ZooKeeper ===")
    run(["sudo", "systemctl", "daemon-reload"])
    run(["sudo", "systemctl", "enable", "zookeeper"])
    run(["sudo", "systemctl", "start", "zookeeper"])
    run(["sudo", "systemctl", "status", "zookeeper", "--no-pager"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
