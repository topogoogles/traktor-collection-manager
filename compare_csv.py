"""
This script compares 'shazamlibrary.csv' and 'traktor_collection_[UNIXtimestamp].csv' files,
finds the already downloaded tracks and exports a new 'fixed_shazamlibrary.csv' file with 
the changes
"""

import pandas as pd
from datetime import datetime
import re


def fix_shazam_library(input_filename, output_filename):
    # Read the original CSV file
    df = pd.read_csv(input_filename, skiprows=1)

    # Reorder the columns
    df = df[["TagTime", "Artist", "Title", "URL", "TrackKey"]]

    # Add a new 'Downloaded' column with all False values
    df["Downloaded"] = False

    # Export the new DataFrame to a CSV file
    df.to_csv(output_filename, index=False)

    print(f"Fixed Shazam library CSV file created: {output_filename}")


# Usage example
input_file = "sample_shazamlibrary.csv"  # Replace with your own "shazamlibrary.csv"
output_file = "fixed_shazamlibrary.csv"

fix_shazam_library(input_file, output_file)


# Regex to extract 'year' folder values from the traktor collection
def extract_year(text):
    match = re.search(r"\b\d{4}\b", text)
    return int(match.group()) if match else None


def compare_traktor_shazam(traktor_df, shazam_df):
    # Extract year from Folder in traktor_df
    traktor_df["Folder_Year"] = traktor_df["Folder"].apply(extract_year)

    # Convert TagTime to datetime objects and extract year
    shazam_df["TagTime"] = pd.to_datetime(shazam_df["TagTime"])
    shazam_df["Year"] = shazam_df["TagTime"].dt.year

    # Sort both DataFrames by Year, Artist, and Title
    traktor_df = traktor_df.sort_values(by=["Folder_Year", "Artist", "Title"])
    shazam_df = shazam_df.sort_values(by=["Year", "Artist", "Title"])

    # Merge the DataFrames
    merged_df = pd.merge(
        traktor_df,
        shazam_df[["Year", "Artist", "Title"]],
        left_on=["Folder_Year", "Artist", "Title"],
        right_on=["Year", "Artist", "Title"],
        suffixes=("_traktor", "_shazam"),
        indicator=True,
    )

    # Filter for matches
    matched_df = merged_df[merged_df["_merge"] == "both"]

    return matched_df


# Function to change 'downloaded' values to True if exist in matched_df
def update_downloaded_status(matched_df, shazamlibrary_file):
    # Read the secondary Shazam library CSV
    shazamlibrary_df = pd.read_csv(shazamlibrary_file)

    # Create a set of matched tracks for efficient lookup
    matched_tracks = set(zip(matched_df["Artist"], matched_df["Title"]))

    # Update the 'Downloaded' column
    shazamlibrary_df["Downloaded"] = shazamlibrary_df.apply(
        lambda row: True if (row["Artist"], row["Title"]) in matched_tracks else False,
        axis=1,
    )

    # Export the updated DataFrame to CSV
    shazamlibrary_df.to_csv(shazamlibrary_file, index=False)

    print(f"Updated '{shazamlibrary_file}' with downloaded status")


# Workflow:
# Load your DataFrames
traktor_df = pd.read_csv(
    "traktor_collection_1725549724.csv"
)  # Replace with your own "traktor_collection_[UNIXtimestamp].csv"
shazam_df = pd.read_csv(
    "sample_shazamlibrary.csv", skiprows=1
)  # Replace with your own "shazamlibrary.csv"

# Perform the comparison
result_df = compare_traktor_shazam(traktor_df, shazam_df)

# Update downloaded status in secondary Shazam library
update_downloaded_status(result_df, "fixed_shazamlibrary.csv")

# Display results
print(result_df)

# Optional: Filter for specific years
"""
start_year = 2020
end_year = 2022

filtered_result = result_df[
    (result_df["Folder_Year"] >= start_year) & (result_df["Folder_Year"] <= end_year)
]

print(filtered_result)
"""
