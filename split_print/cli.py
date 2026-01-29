"""
Command-line interface for PDF splitting tool.
"""

import sys
from pathlib import Path

import click

from .splitter import split_pdf_file


@click.command()
@click.argument(
    'input_file',
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
@click.option(
    '-o', '--output',
    type=click.Path(dir_okay=False, writable=True),
    help='Output file path (default: {input}_split.pdf)',
)
@click.option(
    '--overlap',
    type=float,
    default=0.0,
    help='Overlap between pages in millimeters (default: 0)',
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    help='Enable verbose output',
)
def main(input_file: str, output: str, overlap: float, verbose: bool) -> None:
    """
    Split tall PDFs into printable A4-sized pages.

    Takes a vertically long PDF and splits it into standard A4 pages
    (210mm × 297mm) that can be easily printed.

    Example:

        split-print input.pdf -o output.pdf
    """
    try:
        output_path = split_pdf_file(
            input_path=input_file,
            output_path=output,
            overlap_mm=overlap,
            verbose=verbose
        )

        click.echo(f"✓ PDF split successfully!")
        click.echo(f"Output saved to: {output_path}")

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
