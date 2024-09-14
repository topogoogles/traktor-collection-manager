import pandas as pd
import TraktorBuddy
import time

collection = TraktorBuddy.Collection()

# Build the contents of the library csv using the collection data
artist_list = []
title_list = []
bpm_list = []
key_list = []
location_list = []

for track in collection.tracks():
    artist_list.append(track.artist())
    title_list.append(track.title())
    bpm_list.append(track.bpm())
    key_list.append(track.key())
    location_list.append(track.location())

# print(
#     f"artist: {artist_list[999]}\ntitle: {title_list[999]}\nbpm: {bpm_list[999]}\nkey: {key_list[999]}"
# )

# Create the Pandas Dataframe using the library contents
library_df = pd.DataFrame(
    {
        "Artist": artist_list,
        "Title": title_list,
        "BPM": bpm_list,
        "Key": key_list,
        "Location": location_list,
    }
)

# Set display option (this doesn't affect CSV output)
pd.options.display.float_format = "{:.2f}".format

# Round BPM column before saving
library_df["BPM"] = library_df["BPM"].round(2)


# Fix the 'Location' column to a cleaner 'Folder' column
def folder_extractor(location):
    parts = str(location).split("/")
    return parts[-2] if len(parts) > 0 else "Unknown"


library_df["Folder"] = library_df["Location"].apply(folder_extractor)

# Fix the 'Key' column to two separated ones: 'Key' and 'OpenKey'
major_minor_keys = [
    "C",
    "G",
    "D",
    "A",
    "E",
    "B",
    "F#",
    "Db",
    "Ab",
    "Eb",
    "Bb",
    "F",
    "Am",
    "Em",
    "Bm",
    "F#m",
    "C#m",
    "G#m",
    "D#m",
    "Bbm",
    "Fm",
    "Cm",
    "Gm",
    "Dm",
]
openkey_major_minor_keys = [
    "1d",
    "2d",
    "3d",
    "4d",
    "5d",
    "6d",
    "7d",
    "8d",
    "9d",
    "10d",
    "11d",
    "12d",
    "1m",
    "2m",
    "3m",
    "4m",
    "5m",
    "6m",
    "7m",
    "8m",
    "9m",
    "10m",
    "11m",
    "12m",
]
mixedinkey_major_minor_keys = [
    "8B",
    "9B",
    "10B",
    "11B",
    "12B",
    "1B",
    "2B",
    "3B",
    "4B",
    "5B",
    "6B",
    "7B",
    "8A",
    "9A",
    "10A",
    "11A",
    "12A",
    "1A",
    "2A",
    "3A",
    "4A",
    "5A",
    "6A",
    "7A",
]
musickey_list = []
openkey_list = []
mixedinkey_list = []

notation_vars = ["Gb", "C#", "G#", "D#", "A#", "Gbm", "Dbm", "Abm", "Ebm", "A#m"]
notation_fixed = ["F#", "Db", "Ab", "Eb", "Bb", "F#m", "C#m", "G#m", "D#m", "Bbm"]

# Make the 'Key' column correspond with musical key notation
for item in library_df["Key"]:
    if item is not None:
        # Replace OpenKey for Music notation
        if item in openkey_major_minor_keys:
            item_index = openkey_major_minor_keys.index(item)
            item = major_minor_keys[item_index]
        # Replace Mixed in Key for Musical notation
        if item in mixedinkey_major_minor_keys:
            item_index = mixedinkey_major_minor_keys.index(item)
            item = major_minor_keys[item_index]
        # Replace notation variation for fixed
        if item in notation_vars:
            item_index = notation_vars.index(item)
            item = notation_fixed[item_index]
        # Fill the 'musickey_list', 'openkey_list' and 'mixedinkey_list' arrays
        new_item_index = major_minor_keys.index(item)
        musickey_list.append(major_minor_keys[new_item_index])
        openkey_list.append(openkey_major_minor_keys[new_item_index])
        mixedinkey_list.append(mixedinkey_major_minor_keys[new_item_index])
    else:
        musickey_list.append(item)
        openkey_list.append(item)
        mixedinkey_list.append(item)

# Create the new keys columns in the dataframe
library_df["MusicKey"] = musickey_list
library_df["OpenKey"] = openkey_list
library_df["MixedInKey"] = mixedinkey_list

# Ignore the original 'Key' and 'Location' columns
columns_to_keep = [col for col in library_df.columns if col not in ["Key", "Location"]]
# Define the desired order of columns
desired_order = [
    "Artist",
    "Title",
    "Folder",
    "BPM",
    "MusicKey",
    "OpenKey",
    "MixedInKey",
]
# Reorder the columns
library_df = library_df[
    desired_order + [col for col in columns_to_keep if col not in desired_order]
]

""" Print some part of the dataframe for testing
print(
    library_df.loc[
        70:120,
        ["Artist", "Title", "BPM", "MusicKey", "OpenKey", "MixedInKey"],
    ]
)
"""

# Generate the Unix timestamp
timestamp = int(time.time())

# Construct the filename
filename = f"traktor_collection_{timestamp}.csv"

# Save tthe dataframe to a CSV file
library_df[desired_order].to_csv(
    filename,
    index=False,
    encoding="utf-8",  # Specify encoding if needed
    sep=",",  # Default separator is comma
    quotechar='"',  # Default quote character is double quote
)
