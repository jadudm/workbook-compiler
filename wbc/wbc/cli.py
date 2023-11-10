import click
import sys
import importlib.util

from wbc.parser.parse import parse
from wbc.renderer.render import render


def load_code(name, file):
    module_name = f"wbc.helpers"
    spec = importlib.util.spec_from_file_location(module_name, file)
    from_spec = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = from_spec
    spec.loader.exec_module(from_spec)
    return from_spec


@click.command()
@click.argument("input", required=True, type=click.Path(exists=True))
@click.argument("output", required=True, type=click.Path(exists=False))
@click.option(
    "--functions",
    required=False,
    type=click.Path(exists=True),
    help="Python functions to load for workbook population",
)
def cli(input, output, functions):
    """Convert INPUT JSonnet spec into OUTPUT workbook.

    Default output format is `xlsx`.
    """

    # wbc workbook
    wbcwb = parse(input)

    # openpxl workbook
    if functions:
        m = load_code("functions", functions)
        # print(m.random_uei(3))
        setattr(wbcwb, "functions", m)
    else:
        setattr(wbcwb, "functions", None)

    pxlwb = render(wbcwb)
    pxlwb.save(output)


if __name__ == "__main__":
    cli()
