# Apollo

Apollo is a Python-based music downloader and organizer designed to automate the retrieval, tagging, and sorting of music files. 
It uses Selenium to search for and download tracks, and leveraging YouTube Music metadata for accurate tagging and organization.

## Features

- **Automated Downloading**: Searches for music based on input from a text file and downloads the best available version.
- **Optimal File Selection**: Identifies the highest bitrate available and retrieves the most suitable file.
- **Metadata Tagging**: Uses YouTube Music data to assign correct title, artist, album, release date, and artwork.
- **Structured File Organization**: Renames and moves files to maintain a clean and organized music library.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required dependencies, installable via pip:

  ```bash
  pip install requests selenium edgedriver-autoinstaller eyed3 ytmusicapi
