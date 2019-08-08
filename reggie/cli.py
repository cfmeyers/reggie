# -*- coding: utf-8 -*-

"""Console script for reggie."""
import sys
import click
from reggie.reggie import sniff_out_dependencies


@click.command()
@click.argument('target_script_path', type=str)
@click.argument('dir_path', type=str)
def main(target_script_path, dir_path):
    """Console script for reggie."""
    sniff_out_dependencies(target_script_path, dir_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
