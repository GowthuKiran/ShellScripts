from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

from shellscripts_py.common import run_command


@dataclass
class TomcatInstallPlan:
    version: str
    install_dir: Path
    user: str = "tomcat"
    java_home: str | None = None
    commands: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Tomcat plan: version={self.version}, install_dir={self.install_dir}, user={self.user}, "
            f"commands={len(self.commands)}"
        )


def build_tomcat_install_plan(version: str = "9.0.89", install_dir: str | Path = "/opt/tomcat", user: str = "tomcat") -> TomcatInstallPlan:
    install_path = Path(install_dir).expanduser()
    java_home = "/usr/lib/jvm/java-11-openjdk"
    commands = [
        "apt-get update -y",
        "apt-get install -y wget curl tar default-jdk",
        f"useradd -m -U -d {install_path} -s /bin/false {user}",
        f"mkdir -p {install_path}",
        f"bash -c 'wget -O /tmp/apache-tomcat-{version}.tar.gz https://downloads.apache.org/tomcat/tomcat-9/v{version}/bin/apache-tomcat-{version}.tar.gz'",
        f"bash -c 'tar -xzf /tmp/apache-tomcat-{version}.tar.gz -C {install_path} --strip-components=1'",
        f"chown -R {user}:{user} {install_path}",
        f"bash -c 'echo \"JAVA_HOME={java_home}\" > /etc/environment'",
    ]
    return TomcatInstallPlan(version=version, install_dir=install_path, user=user, java_home=java_home, commands=commands)


def install_tomcat(version: str = "9.0.89", install_dir: str | Path = "/opt/tomcat", user: str = "tomcat", dry_run: bool = False) -> TomcatInstallPlan:
    plan = build_tomcat_install_plan(version=version, install_dir=install_dir, user=user)
    if dry_run:
        return plan

    for command in plan.commands:
        run_command(command, check=True)
    return plan


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build and optionally execute a Tomcat install plan.")
    parser.add_argument("--version", default="9.0.89")
    parser.add_argument("--install-dir", default="/opt/tomcat")
    parser.add_argument("--user", default="tomcat")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    plan = install_tomcat(version=args.version, install_dir=args.install_dir, user=args.user, dry_run=args.dry_run)
    print(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
