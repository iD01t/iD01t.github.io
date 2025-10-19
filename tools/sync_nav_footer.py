import os
import re
from bs4 import BeautifulSoup

def sync_nav_and_footer(source_html, target_html):
    """
    Synchronizes the header and footer from a source HTML file to a target HTML file.

    This function extracts the <header> and <footer> sections from the source file
    and replaces the corresponding sections in the target file. It uses BeautifulSoup
    for reliable HTML parsing and preserves the original structure of the target file.

    Args:
        source_html (str): The file path of the source HTML file (e.g., "index.html").
        target_html (str): The file path of the target HTML file to be updated.
    """
    try:
        # Read the source file (index.html)
        with open(source_html, 'r', encoding='utf-8') as f:
            source_content = f.read()
        source_soup = BeautifulSoup(source_content, 'html.parser')

        # Extract the header and footer from the source
        source_header = source_soup.find('header')
        source_footer = source_soup.find('footer')

        if not source_header:
            print(f"Warning: <header> not found in {source_html}. Trying <nav> instead.")
            source_header = source_soup.find('nav')

        if not source_header:
            print(f"Error: Neither <header> nor <nav> found in {source_html}. Aborting for this file.")
            return

        if not source_footer:
            print(f"Error: <footer> not found in {source_html}. Aborting for this file.")
            return

        # Read the target file
        with open(target_html, 'r', encoding='utf-8') as f:
            target_content = f.read()
        target_soup = BeautifulSoup(target_content, 'html.parser')

        # Find the header and footer in the target
        target_header = target_soup.find('header')
        if not target_header:
            # Fallback to finding <nav> if <header> is not present
            target_header = target_soup.find('nav')

        target_footer = target_soup.find('footer')

        # Replace the header and footer in the target
        if target_header:
            target_header.replace_with(source_header)
        else:
            print(f"Warning: No <header> or <nav> found in {target_html}. Header not replaced.")
            # If no header/nav, we might need to decide on a course of action,
            # like inserting it after the opening <body> tag. For now, we'll just warn.

        if target_footer:
            target_footer.replace_with(source_footer)
        else:
            print(f"Warning: No <footer> found in {target_html}. Footer not replaced.")

        # Write the modified content back to the target file
        with open(target_html, 'w', encoding='utf-8') as f:
            f.write(str(target_soup))

        print(f"Successfully synced {target_html} with {source_html}")

    except FileNotFoundError:
        print(f"Error: File not found. Make sure both {source_html} and {target_html} exist.")
    except Exception as e:
        print(f"An error occurred while processing {target_html}: {e}")

def find_html_files(root_dir):
    """
    Finds all HTML files in a directory, excluding specified subdirectories.
    """
    html_files = []
    # Excluded directories
    excluded_dirs = {'.git', '.github', 'tools', 'jules-scratch', 'ebooks', 'audiobooks'}
    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from the search
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

if __name__ == "__main__":
    # The script should be run from the root of the repository.
    # The source file is assumed to be 'index.html' in the root.
    source_file = "index.html"

    # Get all HTML files in the current directory and subdirectories
    html_files_to_sync = find_html_files(".")

    # Remove the source file from the list of files to be synced
    if source_file in html_files_to_sync:
        html_files_to_sync.remove(source_file)

    for target_file in html_files_to_sync:
        sync_nav_and_footer(source_file, target_file)

    print("\nSynchronization process complete.")
