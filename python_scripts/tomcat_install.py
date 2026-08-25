#!/usr/bin/env python3
from __future__ import annotations
import os
import shutil
import subprocess
from pathlib import Path


TOMCAT_VERSION = "9.0.89"
TOMCAT_USER = "tomcat"
INSTALL_DIR = "/opt/tomcat"


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def resolve_java_home() -> str:
    java_bin = shutil.which("java")
    if not java_bin:
        return "/usr/lib/jvm/java-11-openjdk"
    resolved = Path(java_bin).resolve()
    return str(resolved.parent.parent)


def main() -> int:
    print("### Updating system packages...")
    if Path("/etc/debian_version").exists():
        run(["sudo", "apt", "update", "-y"])
        run(["sudo", "apt", "install", "-y", "wget", "curl", "tar", "default-jdk"])
    elif Path("/etc/redhat-release").exists():
        run(["sudo", "yum", "install", "-y", "wget", "curl", "tar", "java-11-openjdk-devel"])
    else:
        print("Unsupported Linux distribution")
        return 1

    print("### Creating Tomcat user...")
    run(["sudo", "useradd", "-m", "-U", "-d", INSTALL_DIR, "-s", "/bin/false", TOMCAT_USER])

    print("### Downloading Apache Tomcat...")
    os.chdir("/tmp")
    archive = f"apache-tomcat-{TOMCAT_VERSION}.tar.gz"
    run(["wget", f"https://downloads.apache.org/tomcat/tomcat-9/v{TOMCAT_VERSION}/bin/{archive}"])

    print("### Installing Tomcat...")
    run(["sudo", "mkdir", "-p", INSTALL_DIR])
    run(["sudo", "tar", "-xvzf", archive, "-C", INSTALL_DIR, "--strip-components=1"])

    print("### Setting permissions...")
    run(["sudo", "chown", "-R", f"{TOMCAT_USER}:{TOMCAT_USER}", INSTALL_DIR])

    java_home = resolve_java_home()
    service = f"""[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking
User={TOMCAT_USER}
Group={TOMCAT_USER}
Environment=\"JAVA_HOME={java_home}\"
Environment=\"CATALINA_PID={INSTALL_DIR}/temp/tomcat.pid\"
Environment=\"CATALINA_HOME={INSTALL_DIR}\"
Environment=\"CATALINA_BASE={INSTALL_DIR}\"
Environment=\"CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC\"
ExecStart={INSTALL_DIR}/bin/startup.sh
ExecStop={INSTALL_DIR}/bin/shutdown.sh

[Install]
WantedBy=multi-user.target
"""
    service_path = Path("/tmp/tomcat.service")
    service_path.write_text(service, encoding="utf-8")
    run(["sudo", "cp", str(service_path), "/etc/systemd/system/tomcat.service"])

    print("### Reloading systemd and starting Tomcat...")
    run(["sudo", "systemctl", "daemon-reload"])
    run(["sudo", "systemctl", "enable", "tomcat"])
    run(["sudo", "systemctl", "start", "tomcat"])

    print("### Tomcat installation complete!")
    print("Access it at: http://<your_server_ip>:8080")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
