﻿# Idcardgenerator

# Student Management Application Setup Guide

This guide provides step-by-step instructions to set up the **Student Management Application** on a new system. The app helps manage student data for classes 1 to 12, generate ID cards and fee receipts, and categorize students by class.

## Requirements

Before setting up the application, ensure you have the following installed:

- Python 3.8+ (Ensure you have `pip` installed)
- SQLite (for the database)
- Flask (for the web framework)
- FPDF (for generating PDFs)

## Setup Instructions

### 1. Clone or Download the Project

First, clone the project repository or download the source files.

### 1. Download and Install SQLite

You need to download and set up SQLite before running the application. Download SQLite from the link below:

[Download SQLite](https://www.sqlite.org/2024/sqlite-tools-win-x64-3460100.zip)

#### Setting Up SQLite Environment Variable

After downloading SQLite:

1. Extract the downloaded zip file to a folder, e.g., `C:\sqlite`.
2. Add the folder path to your system's `PATH` environment variable.

   - On **Windows**:
     - Search for "Environment Variables" in the start menu.
     - Under **System Variables**, select `Path` and click **Edit**.
     - Click **New**, and add the path to the SQLite folder, e.g., `C:\sqlite`.
     - Click **OK** to save the changes.
   - On **macOS/Linux**:
     - Add the following to your `.bashrc` or `.zshrc` file:
       ```bash
       export PATH=$PATH:/path/to/sqlite
       ```

```bash
git clone https://github.com/Aloneking789/idcardgenerator.git

pip install -r requirements.txt

flask run

```
