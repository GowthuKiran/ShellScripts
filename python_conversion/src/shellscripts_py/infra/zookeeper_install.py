from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

from shellscripts_py.common import run_command


@dataclass
class ZooKeeperInstallPlan:
    version: str
    install_dir: Path
    data_dir: Path
    user: str = "zookeeper"
    client_port: int = 2181
    commands: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"ZooKeeper plan: version={self.version}, install_dir={self.install_dir}, "
            f"data_dir={self.data_dir}, client_port={self.client_port}, commands={len(self.commands)}"
        )


def build_zookeeper_install_plan(version: str = "3.8.4", install_dir: str | Path = "/opt/zookeeper", data_dir: str | Path = "/var/lib/zookeeper", user: str = "zookeeper") -> ZooKeeperInstallPlan:
    install_path = Path(install_dir).expanduser()
    data_path = Path(data_dir).expanduser()
    commands = [
        "apt-get update -y",
        "apt-get install -y wget tar openjdk-11-jdk",
        f"useradd -r -s /sbin/nologin {user} || true",
        f"mkdir -p {install_path} {data_path}",
        f"chown -R {user}:{user} {install_path} {data_path}",
        f"bash -c 'wget -q https://downloads.apache.org/zookeeper/zookeeper-{version}/apache-zookeeper-{version}-bin.tar.gz -O /tmp/apache-zookeeper-{version}-bin.tar.gz'",
        f"bash -c 'tar -xzf /tmp/apache-zookeeper-{version}-bin.tar.gz -C /tmp'",
        f"bash -c 'mv /tmp/apache-zookeeper-{version}-bin/* {install_path}'",
        f"bash -c 'printf \"tickTime=2000\\ndataDir={data_path}\\nclientPort=2181\\ninitLimit=5\\nsyncLimit=2\\n\" > {install_path}/conf/zoo.cfg'",
        f"bash -c 'echo 1 > {data_path}/myid'",
    ]
    return ZooKeeperInstallPlan(version=version, install_dir=install_path, data_dir=data_path, user=user, commands=commands)


def install_zookeeper(version: str = "3.8.4", install_dir: str | Path = "/opt/zookeeper", data_dir: str | Path = "/var/lib/zookeeper", user: str = "zookeeper", dry_run: bool = False) -> ZooKeeperInstallPlan:
    plan = build_zookeeper_install_plan(version=version, install_dir=install_dir, data_dir=data_dir, user=user)
    if dry_run:
        return plan

    for command in plan.commands:
        run_command(command, check=True)
    return plan


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build and optionally execute a ZooKeeper install plan.")
    parser.add_argument("--version", default="3.8.4")
    parser.add_argument("--install-dir", default="/opt/zookeeper")
    parser.add_argument("--data-dir", default="/var/lib/zookeeper")
    parser.add_argument("--user", default="zookeeper")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    plan = install_zookeeper(version=args.version, install_dir=args.install_dir, data_dir=args.data_dir, user=args.user, dry_run=args.dry_run)
    print(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
