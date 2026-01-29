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
        page_width: float = A4_WIDTH_PT,
        overlap_mm: float = 0.0
    ) -> None:
        """
        Split a PDF into A4-sized pages, scaling down if necessary.

        Args:
            input_path: Path to input PDF file
            output_path: Path to output PDF file
            page_height: Target page height in points (default: A4 height)
            page_width: Target page width in points (default: A4 width)
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
        self._log(f"Target page size: {page_width:.1f}pt × {page_height:.1f}pt (A4)")

        for page_num, page in enumerate(reader.pages, 1):
            # Get original page dimensions
            mediabox = page.mediabox
            original_width = float(mediabox.width)
            original_height = float(mediabox.height)

            self._log(f"\nPage {page_num}: {original_width:.1f}pt × {original_height:.1f}pt")
            self._log(f"  = {original_width/MM_TO_PT:.1f}mm × {original_height/MM_TO_PT:.1f}mm")

            # Calculate scaling factor to fit within A4 width
            scale_x = page_width / original_width
            scale_y = 1.0  # We'll handle height by splitting

            # Use the smaller scale to ensure it fits
            scale_factor = min(scale_x, 1.0)

            scaled_width = original_width * scale_factor
            scaled_height = original_height * scale_factor

            if scale_factor < 1.0:
                self._log(f"  → Scaling to {scale_factor:.2%} to fit A4 width")
                self._log(f"  → Scaled size: {scaled_width:.1f}pt × {scaled_height:.1f}pt")
                self._log(f"    = {scaled_width/MM_TO_PT:.1f}mm × {scaled_height/MM_TO_PT:.1f}mm")

            # Calculate number of vertical splits needed
            num_splits = math.ceil(scaled_height / page_height)
            self._log(f"  → Splitting into {num_splits} page(s)")

            for split_index in range(num_splits):
                # Calculate the vertical section in scaled coordinates
                top_y_scaled = scaled_height - (split_index * page_height)
                bottom_y_scaled = max(0, scaled_height - ((split_index + 1) * page_height) - overlap_pt)
                section_height_scaled = top_y_scaled - bottom_y_scaled

                # Convert back to original coordinates
                top_y_orig = top_y_scaled / scale_factor
                bottom_y_orig = bottom_y_scaled / scale_factor

                # Create output page
                output_page = PageObject.create_blank_page(
                    width=scaled_width,
                    height=section_height_scaled
                )

                # Copy the original page
                output_page.merge_page(page)

                # Crop to the section (in original coordinates)
                output_page.mediabox.lower_left = (0, bottom_y_orig)
                output_page.mediabox.upper_right = (original_width, top_y_orig)

                # Scale down if needed
                if scale_factor < 1.0:
                    output_page.scale_by(scale_factor)

                writer.add_page(output_page)
                total_pages_created += 1

                self._log(f"    Page {split_index + 1}/{num_splits}: {scaled_width:.1f}pt × {section_height_scaled:.1f}pt")

        # Write output PDF
        self._log(f"\nWriting output to: {output_path}")
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
