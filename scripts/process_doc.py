"""
Utility script for processing documents with IntelliDoc.

This module defines functions to process individual files or entire directories.
It can be invoked manually or integrated into automated workflows.
"""

from __future__ import annotations

import os
from typing import Iterable


def process_single_document(file_path: str) -> None:
    """Simulate processing a single document.

    Currently, this function prints status messages.  In future versions it will
    call the IntelliDoc API or run local AI models.

    Args:
        file_path: Path to the document to process.
    """
    print(f"Starting processing for {file_path}…")
    # TODO: Add document processing logic here
    print(f"Finished processing for {file_path}.")


def process_all_documents_in_directory(directory: str, extensions: Iterable[str] | None = None) -> None:
    """Process all documents in a directory with specified extensions.

    Args:
        directory: Path to a directory containing documents.
        extensions: Optional iterable of file extensions (e.g., {".txt", ".md"}).
    """
    if extensions is None:
        extensions = {".txt"}
    for filename in os.listdir(directory):
        if any(filename.endswith(ext) for ext in extensions):
            file_path = os.path.join(directory, filename)
            process_single_document(file_path)


if __name__ == "__main__":
    # Example usage: process all .txt files in the current directory
    process_all_documents_in_directory(os.getcwd())
