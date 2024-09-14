# Traktor Collection Manager

## Project Overview

The Traktor Collection Manager is a tool designed to help DJs manage their music collections within Traktor DJ software. It provides functionality to export collection data, compare it with other sources (like Shazam libraries), and analyze track information.

## Main Features

- Export Traktor collection data to CSV files
- Compare Traktor collections with external libraries (e.g., Shazam)
- Identify downloaded tracks
- Analyze track metadata and key information

## Getting Started

### Step 1: Clone the Repository

Clone this repository to your local machine:
`git clone https://github.com/yourusername/Traktor-Collection-Manager.git`
`cd Traktor-Collection-Manager`

### Step 2: Set Up the Environment

Run the initialization script:
`./first_run.sh`
This will create a virtual environment, update PIP, and install all required dependencies.

### Step 3: Prepare Sample Data

Replace the sample data files with your own:

- Replace `sample_shazamlibrary.csv` with your actual Shazam library CSV, which you can download logging in at Shazam website

### Step 4: Export Traktor Collection Data

Run `build_csv.py` to create a CSV file named `traktor_collection_[UNIXtimestamp].csv`. This script:

- Uses TraktorBuddy to read data from `collection.nml`. It will find the file using the path according to your Traktor installation.
- Generates a customized CSV file with enhanced track information
- Adds three new columns for different Camelot Wheel key notations
- Facilitates harmonic mixing by including these key variations

### Step 5: Compare Traktor and External Libraries

Run `compare_csv.py` to analyze your collections. This script:

- Compares the exported Traktor collection CSV with your external library CSV (e.g., Shazam)
- Creates a new column called __Downloaded__
- Marks tracks that have already been downloaded
- Generates a new `fixed_shazamlibrary.csv` file with the comparison results and fixed columns order

__Important Note:__ Before running `compare_csv.py`, ensure you've correctly specified the path to the `traktor_collection_[UNIXtimestamp].csv` file generated in Step 4 within the script.

## Project Structure

- `build_csv.py`: Script to export Traktor collection data
- `compare_csv.py`: Script to compare Traktor collections with external libraries
- `traktorbuddy_example.py`: Example script demonstrating TraktorBuddy usage
- `sample_shazamlibrary.csv`: Sample external library CSV file
- `requirements.txt`: List of project dependencies
- `.gitignore`: File specifying which files should not be tracked by Git

## Dependencies

This project relies on:

- Python
- pandas
- TraktorBuddy (Third-Party library for interacting with Traktor DJ software)

## Usage Tips

- Regularly update your Traktor collection CSV to reflect changes in your library
- Use the comparison feature to identify tracks you already have downloaded
- Leverage the Camelot Wheel key information for harmonic mixing

## Contributing

Contributions are welcome! Please submit pull requests or issues on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
