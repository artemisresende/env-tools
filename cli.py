import click
import system


@click.group()
def cli():
    """
    Development Toolkit that provides tools for JavaScript and Python applications.
    """
    pass


@cli.command()
@click.option("--dev", help="Flag to install development dependencies.")
def setup(dev: bool = False):
    """
    Install infrastructure dependencies and update the system.
    :return:
    """
    click.echo("Installing dependencies...")
    system.install_dependencies(dev)

    update()


@cli.command()
def update():
    """
    Update packages via topgrade.
    """
    click.echo("Updating the system...")
    system.update()


@cli.command()
@click.argument("engine", default="podman-docker", type=click.STRING)
def enable_containers(engine):
    """
    Enable an OCI-compatible engine for running containers.
    """
    click.echo(f"Installing Container Engine ({engine})...")
    system.install(packages=[engine])


@cli.command()
@click.argument("version", type=click.STRING)
def install_python(version):
    """
    Install a given version of Python via asdf runtime manager.
    """
    system.install_python(version)


@cli.command()
@click.argument("domain", type=click.STRING)
@click.argument("email", type=click.STRING)
def get_cert(domain, email):
    """
    Get an SSL/TLS certificate for a given domain via Linode API.

    :param email: e-mail required by Certbot
    :param domain: domain to generate certificate of
    """
    system.request_linode_ssl_cert(domain, email)
