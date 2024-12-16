from enum import Enum
from typing import Optional

import click
import os


def is_executable_available(executable: str) -> bool:
    """Check if an executable is available at runtime."""
    return os.system(f"which {executable} > /dev/null 2>&1") == 0


class PackageManager:
    BREW = "brew"
    ASDF = "asdf"
    PIP = "pip"
    APT = "apt"
    DNF = "dnf"
    YUM = "yum"
    APK = "apk"

    @classmethod
    def system(cls):
        for pkg in [cls.APT, cls.DNF, cls.YUM, cls.APK]:
            if is_executable_available(pkg):
                return pkg


def setup_git(name: str, email: str, default_branch: str = "main"):
    """
    Setup Git information.

    :param name: name used in commit messages
    :param email: email used in commit messages
    :return:
    """
    if is_executable_available("git"):
        os.system(f"git config --global init.defaultBranch {default_branch}")
        os.system(f"git config --global user.name {name}")
        os.system(f"git config --global user.email {email}")
    else:
        raise RuntimeError("Git is not available at runtime.")

def install(pkg: str,
            pkg_manager: Optional[PackageManager] = PackageManager.system(),
            pre_commands: Optional[list[str]] = None,
            post_commands: Optional[list[str]] = None):
    """
    Install a package using one of the available package managers.

    :param pkg: package name
    :param pkg_manager: package manager, e.g. 'apt'
    :param pre_commands: commands to be executed before installation
    :param post_commands: commands to be executed after installation
    :return: None
    """

    queue: list[str] = []
    use_sudo: bool = True

    if pre_commands:
        queue += pre_commands

    cmd: Optional[str] = None
    match pkg_manager:
        case PackageManager.APT | PackageManager.DNF | PackageManager.YUM:
            cmd = f"{pkg_manager} install -y {pkg}"
        case PackageManager.APK:
            cmd = f"apk add {pkg}"
        case PackageManager.BREW | PackageManager.ASDF | PackageManager.PIP:
            cmd = f"{pkg_manager} install {pkg}"
            use_sudo = False
        case _:
            pass

    if cmd:
        if use_sudo:
            cmd = f"sudo {cmd}"

        queue += [cmd]

    if post_commands:
        queue += post_commands

    for cmd in queue:
        if os.system(cmd):
            break


def request_linode_ssl_cert(domain: str, email: str, wildcard: bool = True):
    """
    Request a Certbot certificate for the specified domain names using Linode DNS plugin.

    :param domain: Domain name to generate a certificate for.
    :param email: The email address to use for registration and recovery.
    :param wildcard: Generate a wildcard certificate. Defaults to False.
    :return: None
    """
    import os
    from pathlib import Path

    # Check/create credentials file
    linode_credential_path = "/etc/letsencrypt/linode.ini"
    if not Path(linode_credential_path).exists():
        click.echo(f"Unable to find Linode at {linode_credential_path}.")
        click.echo("Provide a Linode API Key: ")
        stdin = click.get_text_stream('stdin')
        api_key = stdin.read()
        os.system(f'sudo printf "dns_linode_key = {api_key}\ndns_linode_version = 4\n" > {linode_credential_path}')

    # Create a certbot command
    cmd = (f"sudo certbot certonly --email {email} --agree-tos --non-interactive"
           " --dns-linode --dns-linode-credentials /etc/letsencrypt/linode.ini"
           " --dns-linode-propagation-seconds 120")

    # Add the domains
    if wildcard:
        # Generate a wildcard certificate
        cmd += f" --domain *.{domain}"
    else:
        # Generate a regular certificate
        cmd += f" --domain {domain}"

    # Run the Certbot command
    os.system(cmd)
