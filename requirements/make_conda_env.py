import os
import sys
from copy import deepcopy

import click
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq as CS


@click.command()
@click.option(
    "-s",
    "--sections",
    default="main,tests,dev,docs",
    help="Dependency sections to include in the produced environment.yml file. "
         "Default: 'main,tests,dev,docs'",
)
@click.option("-i", "--input-dir", default=".", help="Path to input directory.")
@click.option("-o", "--output", default=None, help="Path to output file.")
@click.option("-q", "--quiet", is_flag=True, help="Suppress terminal output.")
def cli(sections, input_dir, output, quiet):
    # Set YAML parameters
    yaml = YAML(typ="rt")  # Round-trip mode allows for comment insertion
    indent_offset = 2
    yaml.indent(offset=indent_offset)

    # Load environment file template
    with open(os.path.join("requirements", "environment.in")) as f:
        env_yml = yaml.load(f.read())

    # Extract dependency section contents
    sections = [x.strip() for x in sections.split(",")]
    section_indices = {}
    dep_list = deepcopy(env_yml["dependencies"]) if "dependencies" in env_yml else []
    i = len(dep_list)

    for section in sections:
        section_indices[section] = i
        with open(os.path.join("requirements", f"{section}.in")) as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    dep_list.append(line.strip())
                    i += 1

    # Format dependency list
    lst = CS(dep_list)

    for section, i in section_indices.items():
        lst.yaml_set_comment_before_after_key(i, section, indent_offset)

    env_yml["dependencies"] = lst

    # Output to terminal
    if not quiet:
        yaml.dump(env_yml, sys.stdout)

    # Output to file
    if output is not None:
        with open(output, "w") as outfile:
            if not quiet:
                print()
            print(f"Saving to {output}")
            yaml.dump(env_yml, outfile)


if __name__ == "__main__":
    cli()
