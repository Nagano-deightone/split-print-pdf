"""
Batch processing CLI for splitting multiple PDFs.
"""

import sys
from pathlib import Path
from typing import List

import click

from .splitter import split_pdf_file


@click.command()
@click.argument(
    'input_files',
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
@click.option(
    '-o', '--output-dir',
    type=click.Path(file_okay=False, writable=True),
    help='Output directory for split PDFs (default: same as input)',
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
@click.option(
    '--continue-on-error',
    is_flag=True,
    help='Continue processing even if some files fail',
)
def main(
    input_files: tuple,
    output_dir: str,
    overlap: float,
    verbose: bool,
    continue_on_error: bool
) -> None:
    """
    Split multiple tall PDFs into printable A4-sized pages.

    Process multiple PDF files at once. Input files can be specified
    individually or using shell wildcards.

    Examples:

        batch-split-print file1.pdf file2.pdf file3.pdf

        batch-split-print ~/Downloads/*.pdf

        batch-split-print *.pdf -o ~/Desktop/output/

        batch-split-print *.pdf --overlap 5 -v
    """
    # Create output directory if specified
    output_path = None
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        click.echo(f"Output directory: {output_path}")

    total_files = len(input_files)
    successful = 0
    failed = 0
    failed_files: List[str] = []

    click.echo(f"Processing {total_files} file(s)...\n")

    for idx, input_file in enumerate(input_files, 1):
        input_path = Path(input_file)

        # Determine output path
        if output_path:
            output_file = str(output_path / f"{input_path.stem}_split.pdf")
        else:
            output_file = str(input_path.parent / f"{input_path.stem}_split.pdf")

        # Progress indicator
        click.echo(f"[{idx}/{total_files}] Processing: {input_path.name}")

        try:
            split_pdf_file(
                input_path=str(input_file),
                output_path=output_file,
                overlap_mm=overlap,
                verbose=verbose
            )

            click.echo(f"  ✓ Success: {Path(output_file).name}")
            successful += 1

        except Exception as e:
            click.echo(f"  ✗ Failed: {e}", err=True)
            failed += 1
            failed_files.append(input_path.name)

            if not continue_on_error:
                click.echo("\nStopping due to error. Use --continue-on-error to process remaining files.", err=True)
                sys.exit(1)

        if verbose:
            click.echo()  # Empty line for readability

    # Summary
    click.echo("\n" + "=" * 50)
    click.echo("SUMMARY")
    click.echo("=" * 50)
    click.echo(f"Total files: {total_files}")
    click.echo(f"Successful:  {successful}")
    click.echo(f"Failed:      {failed}")

    if failed_files:
        click.echo("\nFailed files:")
        for filename in failed_files:
            click.echo(f"  - {filename}")
        sys.exit(1)
    else:
        click.echo("\n✓ All files processed successfully!")


if __name__ == '__main__':
    main()
