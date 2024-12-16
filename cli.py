import os
from typing import Optional

import click

import system
from system import PackageManager


@click.group()
def cli():
    """
    Toolkit that helps the installation and configuration of Linux machines for development and execution of applications and OCI-Containers.
    """
    pass

@cli.command()
def setup():
    """
    Prepare the system by installing dependencies and updating all packages. May require a reboot.
    """
    click.echo("Installing dependencies...")
    click.echo("[1/3] Homebrew")
    _install("brew")

    click.echo("[2/3] Updater Tool")
    _install("topgrade")

    click.echo("[3/3] Certbot")
    _install("certbot")

    click.echo("Installing Runtimes...")
    click.echo("[1/1] Python")
    _install("python", "3.10")

    _update()

def _update():
    click.echo("Updating the system...")
    os.system("topgrade")

@cli.command()
def update():
    """
    Update packages via topgrade.
    """
    _update()

@cli.command()
@click.argument("engine", default="podman-docker", type=click.STRING)
def enable_containers(engine):
    """
    Enable an OCI-compatible engine for running resources.
    """
    click.echo(f"Installing Container Engine ({engine})...")
    _install(engine)

def _install(package: str, version: Optional[str] = None):
    import sys

    match package:
        case "python":
            package = "python latest"

            if version:
                package += f":{version}"

            if not sys.version.startswith(version):  # Check if python is already installed
                system.install(package, pkg_manager=system.PackageManager.ASDF,
                               pre_commands=["asdf plugin-add python"],
                               post_commands=["asdf global python latest:{version}"])

            # PIP (https://pip.pypa.io/en/stable/installation/)
            system.install(pkg="pip", pkg_manager=None,
                           pre_commands=['curl -fsSL https://bootstrap.pypa.io/get-pip.py | python3'])

            # Poetry
            system.install("poetry", pkg_manager=PackageManager.PIP)
        case "brew":
            # https://brew.sh/
            click.echo("ping")
            system.install(pkg=package, pkg_manager=None,
                           pre_commands=[
                               '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'],
                           post_commands=['echo "eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"" >> ~/.bashrc'])
        case "asdf":
            # https://asdf-vm.com/guide/getting-started.html
            system.install(pkg=package, pkg_manager=PackageManager.BREW,
                           post_commands=[
                               'printf "\n. \"$(brew --prefix asdf)/libexec/asdf.sh\"" >> ~/.bashrc',
                               'printf "\n. \"$(brew --prefix asdf)/etc/bash_completion.d/asdf.bash\"" >> ~/.bashrc'
                           ])
        case "topgrade":
            system.install("topgrade", PackageManager.BREW)
        case "certbot":
            system.install("python3-certbot-dns-linode")
        case _:
            system.install(package)

@cli.command()
@click.argument("package", type=click.STRING)
def install(package):
    """
    Install a given package. Support "[package name]:[version]" syntax.
    """
    version: Optional[str]

    try:
        package, version = package.split(":")
    except ValueError:
        version = None

    _install(package, version)

@cli.command()
@click.argument("domain", type=click.STRING)
@click.argument("email", type=click.STRING)
def get_cert(domain, email):
    """
    Get an SSL/TLS certificate for a given domain via Linode API.
    """
    system.request_linode_ssl_cert(domain, email)
