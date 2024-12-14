import click
import os


def install_dependencies(dev: bool = False):
    """
    Install dependencies on an environment with bash.
    :param dev:
    :return:
    """
    click.echo("Installing Homebrew...")
    # https://brew.sh/
    os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    os.system('echo "eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"" >> ~/.bashrc')

    click.echo("Installing Updater Tool (topgrade)...")
    os.system('brew install topgrade')

    if dev:
        click.echo("Installing Runtime Manager (asdf)...")
        # https://asdf-vm.com/guide/getting-started.html
        os.system('brew install asdf')
        os.system('printf "\n. \"$(brew --prefix asdf)/libexec/asdf.sh\"" >> ~/.bashrc')
        os.system('printf "\n. \"$(brew --prefix asdf)/etc/bash_completion.d/asdf.bash\"" >> ~/.bashrc')

    click.echo("Installing Python Tools...")
    os.system('curl -fsSL https://bootstrap.pypa.io/get-pip.py | python3')  # https://pip.pypa.io/en/stable/installation/

    if dev:
        os.system('pip install poetry')

    click.echo("Installing SSL/TLS Certificate Providers...")
    os.system('pip install certbot python3-certbot-dns-linode')  # Certbot
    # local certificate provider


def install_python(version: str):
    """
    Install Python via asdf.

    :param version: a Python runtime version
    """
    assert version

    click.echo(f"Installing Python {version}...")
    os.system('asdf plugin-add python')
    os.system(f'asdf install python latest:{version}')
    os.system(f'asdf global python latest:{version}')


def update():
    """
    Update the system via topgrade.
    """
    click.echo("Update the system")
    os.system("topgrade")


def install(packages: list[str]):
    """
    Install a package using the default system package manager.
    It supports apt, dnf, yum and apk.

    :param packages: list of packages to be installed
    """
    import re

    # Get the list of packages as string
    # noinspection RegExpSingleCharAlternation,RegExpRedundantEscape
    packages_str = re.sub(r"(\[|\]|\"|\'|,)", "", str(packages))  # "['aaa', 'bbb', 'ccc']" -> "aaa bbb ccc"

    # Detect the package manager
    package_manager = None
    if os.system("which apt > /dev/null 2>&1") == 0:
        package_manager = "apt"
    elif os.system("which dnf > /dev/null 2>&1") == 0:
        package_manager = "dnf"
    elif os.system("which yum > /dev/null 2>&1") == 0:
        package_manager = "yum"
    elif os.system("which apk > /dev/null 2>&1") == 0:
        package_manager = "apk"

    if package_manager is None:
        click.echo(f"Unsupported package manager. Please install {packages_str} manually.")
        return

    # Run command
    match package_manager:
        case "apt":
            os.system(f"sudo apt install -y {packages_str}")
        case "dnf":
            os.system(f"sudo dnf install -y {packages_str}")
        case "yum":
            os.system(f"sudo yum install -y {packages_str}")
        case "apk":
            os.system(f"sudo apk add {packages_str}")


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
