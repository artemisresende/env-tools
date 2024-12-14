# Environment Toolkit

Toolkit that helps the installation and configuration of Linux machines[^1] for development and execution of applications and OCI-Containers.

It installs, as dependencies:
* [Homebrew](https://brew.sh/), as Package Manager (General)
* [asdf](https://asdf-vm.com/), as Runtime Manager
* [topgrade](https://github.com/topgrade-rs/topgrade), as Package Updater
* [pip](https://pypi.org/project/pip/), as Package Manager (Python)
* [poetry](https://python-poetry.org/), as Python Packaging and Dependency Manager
* [certbot](https://github.com/certbot/certbot) and [python3-certbot-dns-linode](https://certbot-dns-linode.readthedocs.io/en/stable/index.html), as SSL/TLS certificate provider.

Optionally:
* Install [Podman](https://podman.io/) with Docker aliases as Container Runtime.
* Generate an SSL/TLS certificate via Certbot and Linode.
* Update all packages via [topgrade](https://github.com/topgrade-rs/topgrade)

[^1] It supports Linux Machines with Bash and one of the following package managers: `apt`, `dnf`, `yum` or `apk`. **Tested only on Debian-based machines.**

## Installation

TBD

## Getting Started

Run `env-tools setup` to install dependencies and update the system.

> Note that `setup` will ask for privileged permissions via `sudo`.

Afterward, you can run any other command as you might need.

```
Usage: env-tools [OPTIONS] COMMAND [ARGS]...

  Development Toolkit that provides tools for JavaScript and Python
  applications.

Options:
  --help  Show this message and exit.

Commands:
  enable-containers  Enable an OCI-compatible engine for running containers.
  get-cert           Get an SSL/TLS certificate for a given domain via...
  install-python     Install a given version of Python via asdf runtime...
  setup              Install infrastructure dependencies and update the...
  update             Update packages via topgrade.
```

### Installing Python

`$ env-tools install-python [VERSION]`

### Enabling Containers

`$ env-tools enable-containers`

### Get SSL/TLS certificates

`$ env-tools get-cert [DOMAIN] [EMAIL]`

### Update the system

`$ env-tools update`

> Note that `update` will ask for privileged permissions via `sudo`.
 