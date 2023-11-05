# SPDX-FileCopyrightText: 2023-present Matt Jadud <matthew.jadud@gsa.gov>
#
# SPDX-License-Identifier: Unlicense
import click
from wbc.renderer.render import render

from wbc.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="wbc")
def wbc():
    click.echo("Hello world!")