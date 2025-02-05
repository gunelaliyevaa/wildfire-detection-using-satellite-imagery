import os
import pandas as pd
import csv
import shutil


def combine_csv_files(input_folder, output_folder, output_filename="combined.csv"):
    """Combines all CSV files in a folder into one."""
    output_file = os.path.join(output_folder, output_filename)
    os.makedirs(output_folder, exist_ok=True)
    combined_df = pd.DataFrame()

    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            df = pd.read_csv(file_path)
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df.to_csv(output_file, index=False)
    print(f"Combined file saved at: {output_file}")
    return output_file


def merge_photo_urls(csv_file1, csv_file2, output_file, placeholder_photo_url):
    """Merges wildfire coordinate CSV with photo URLs."""
    df1 = pd.read_csv(csv_file1)
    df2 = pd.read_csv(csv_file2)
    df1.rename(columns={'LONGITUDE': 'longitude', 'LATITUDE': 'latitude'}, inplace=True)
    merged_df = pd.merge(df2, df1[['longitude', 'latitude', 'PHOTO_URL']], how='left', on=['latitude', 'longitude'])
    merged_df['PHOTO_URL'] = merged_df['PHOTO_URL'].fillna(placeholder_photo_url)
    merged_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved at: {output_file}")
    return output_file


def remove_invalid_photos(input_file, output_file, placeholder_photo_url):
    """Removes rows where PHOTO_URL contains a placeholder image."""
    df = pd.read_csv(input_file)
    filtered_df = df[df['PHOTO_URL'] != placeholder_photo_url]
    filtered_df.to_csv(output_file, index=False)
    print(f"Invalid photos removed. Cleaned file saved at: {output_file}")
    return output_file


def extract_coordinates_from_photos(folder_path, output_csv, invalid_folder):
    """Extracts coordinates from image filenames and saves them in a CSV."""
    os.makedirs(invalid_folder, exist_ok=True)
    data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".png"):
            try:
                base_name = os.path.splitext(file_name)[0]
                latitude, longitude, _ = base_name.split('_')
                data.append([float(longitude), float(latitude), os.path.join(folder_path, file_name)])
            except ValueError:
                print(f"Invalid file name: {file_name}. Moving to {invalid_folder}")
                shutil.move(os.path.join(folder_path, file_name), os.path.join(invalid_folder, file_name))

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["LONGITUDE", "LATITUDE", "PHOTO_URL"])
        writer.writerows(data)

    print(f"CSV file created: {output_csv}")
    return output_csv


def main():
    # Define paths
    input_folder = "CSV_FilesFolders/All4CSVofGit"
    output_folder = "CSV_FilesFolders/J1_VIIRS_COMBINED_CSVs"
    placeholder_photo_url = "CSV_FilesFolders/PlaceholderNotFound.png"

    # Step 1: Combine CSV files
    combined_csv = combine_csv_files(input_folder, output_folder)

    # Step 2: Merge with Photo URLs
    csv_with_photos = merge_photo_urls(
        "CSV_FilesFolders/CoordinateCSVFolder/photo coordinates copy.csv",
        combined_csv,
        os.path.join(output_folder, "updated_file2.csv"),
        placeholder_photo_url
    )

    # Step 3: Remove Invalid Photo URLs
    cleaned_csv = remove_invalid_photos(csv_with_photos, "CSV_FilesFolders/J1_VIIRS_COMBINED_CSVs/updated_file3.csv",
                                        placeholder_photo_url)

    # Step 4: Extract Coordinates from Photos
    extract_coordinates_from_photos(
        "CSV_FilesFolders/PhotoFile4Wildfire",
        os.path.join(output_folder, "coordinates.csv"),
        "CSV_FilesFolders/InvalidPhotoName"
    )


if __name__ == "__main__":
    main()
