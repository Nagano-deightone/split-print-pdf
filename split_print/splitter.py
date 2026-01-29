"""
Core PDF splitting logic.
"""

import math
from pathlib import Path
from typing import Optional

from pypdf import PdfReader, PdfWriter, PageObject, Transformation

from .constants import A4_HEIGHT_PT, A4_WIDTH_PT, MM_TO_PT


class PDFSplitter:
    """Handles splitting of tall PDFs into A4-sized pages."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")

    def split_pdf(
        self,
        input_path: str,
        output_path: str,
        page_height: float = A4_HEIGHT_PT,
        overlap_mm: float = 0.0
    ) -> None:
        """
        Split a PDF into pages of specified height.

        Args:
            input_path: Path to input PDF file
            output_path: Path to output PDF file
            page_height: Target page height in points (default: A4 height)
            overlap_mm: Overlap between pages in millimeters (default: 0)

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If PDF is invalid or corrupted
        """
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        overlap_pt = overlap_mm * MM_TO_PT

        self._log(f"Reading PDF: {input_path}")
        try:
            reader = PdfReader(input_path)
        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}")

        writer = PdfWriter()
        total_pages_created = 0

        self._log(f"Processing {len(reader.pages)} pages from input PDF")

        for page_num, page in enumerate(reader.pages, 1):
            # Get original page dimensions
            mediabox = page.mediabox
            page_width = float(mediabox.width)
            original_height = float(mediabox.height)

            self._log(f"Page {page_num}: {page_width:.1f}pt × {original_height:.1f}pt")

            # Check if page needs splitting
            if original_height <= page_height:
                # Page fits within target height, add as-is
                writer.add_page(page)
                total_pages_created += 1
                self._log(f"  → Added as single page (fits within {page_height:.1f}pt)")
            else:
                # Calculate number of splits needed
                num_splits = math.ceil(original_height / page_height)
                self._log(f"  → Splitting into {num_splits} pages")

                for split_index in range(num_splits):
                    # Calculate crop boundaries
                    # PDF coordinates: origin at bottom-left, y-axis points up
                    lower_y = original_height - ((split_index + 1) * page_height) - overlap_pt
                    upper_y = original_height - (split_index * page_height)

                    # Ensure we don't go below the page bottom
                    lower_y = max(0, lower_y)

                    # Create a new page with the cropped content
                    new_page = PageObject.create_blank_page(
                        width=page_width,
                        height=min(page_height, upper_y - lower_y)
                    )

                    # Copy content from original page
                    new_page.merge_page(page)

                    # Crop to the desired section
                    new_page.mediabox.lower_left = (0, lower_y)
                    new_page.mediabox.upper_right = (page_width, upper_y)

                    writer.add_page(new_page)
                    total_pages_created += 1

                    actual_height = upper_y - lower_y
                    self._log(f"    Split {split_index + 1}/{num_splits}: y={lower_y:.1f} to {upper_y:.1f} (height={actual_height:.1f}pt)")

        # Write output PDF
        self._log(f"Writing output to: {output_path}")
        self._log(f"Total pages created: {total_pages_created}")

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        self._log("Done!")


def split_pdf_file(
    input_path: str,
    output_path: Optional[str] = None,
    overlap_mm: float = 0.0,
    verbose: bool = False
) -> str:
    """
    Convenience function to split a PDF file.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file (default: {input}_split.pdf)
        overlap_mm: Overlap between pages in millimeters (default: 0)
        verbose: Enable verbose logging

    Returns:
        Path to the output file
    """
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_split.pdf")

    splitter = PDFSplitter(verbose=verbose)
    splitter.split_pdf(input_path, output_path, overlap_mm=overlap_mm)

    return output_path
