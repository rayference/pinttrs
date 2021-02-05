import os

import click
from setuptools.config import read_configuration


@click.command()
@click.option(
    "-s",
    "--sections",
    default="main,tests,dev,docs",
    help="Dependency sections to include in the produced environment.yml file. "
    "Default: 'main,tests,dev,docs'",
)
@click.option("-i", "--input", default="setup.cfg", help="Path to setup.cfg file.")
@click.option(
    "-o",
    "--output-dir",
    default="./requirements",
    help="Path to output directory.",
)
@click.option("-q", "--quiet", is_flag=True, help="Suppress terminal output.")
def cli(sections, input, output_dir, quiet):
    if not quiet:
        print(f"Reading dependencies from {input}")

    setup_config = read_configuration(input)
    sections = [x.strip() for x in sections.split(",")]

    for section in sections:
        if not quiet:
            print(f"Processing section '{section}'")

        if section == "main":
            packages = setup_config["options"]["install_requires"]
        else:
            packages = setup_config["options"]["extras_require"][section]

        if not quiet:
            print(f"Writing to {os.path.join(output_dir, f'{section}.in')}")
        with open(os.path.join(output_dir, f"{section}.in"), "w") as f:
            f.write("\n".join(packages))
            f.write("\n")


if __name__ == "__main__":
    cli()
