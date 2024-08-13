import geojson as gj
import csv
import re

def convert_to_decimal(coord_str):
    """
    Converts a latitude or longitude string in the format '47° 15.00’ N' or '122° 30.00’ W' to a decimal value.
    
    Args:
        coord_str (str): The coordinate string to convert.
    
    Returns:
        float: The coordinate in decimal degrees.
    
    Raises:
        ValueError: If the input string is not in the expected format.
    """
    # Define the regular expression for the expected format
    pattern = r"^\s*(\d{1,3})°\s*([\d.]+)’\s*([NSEW])\s*$"
#    pattern = r"^\s*(\d{1,3})°\s*([\d.]+)′\s*([NSEW])\s*$"
    
    # Attempt to match the input string with the regex
    match = re.match(pattern, coord_str)
    
    if not match:
        raise ValueError(f"Input string '{coord_str}' is not in the expected format.")

    # Extract the degrees, minutes, and direction from the matched groups
    degrees = float(match.group(1))
    minutes = float(match.group(2))
    direction = match.group(3)
    
    # Convert minutes to decimal and add to degrees
    decimal = degrees + (minutes / 60)
    
    # Adjust for the direction
    if direction in ['S', 'W']:
        decimal *= -1
    
    return "{:.3f}".format(decimal)


def process_row(row):
    """
    Example function that processes a row from the TSV file.
    """
    columns_to_modify = ['start_lat', 'start_lon', 'finish_lat', 'finish_lon']
    new_row = {}
    for key, value in row.items():
        if key in columns_to_modify:
            new_row[key] = convert_to_decimal(value)
        else:
            new_row[key] = value
    print("\t".join(new_row.values()))

def process_tsv(file_path):
    """
    Reads a TSV file and processes each row.
    """
    feature_list = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        header = reader.fieldnames
        if header:
            print("\t".join(header))        
        # Iterate over each row in the TSV file
        for row in reader:
            process_row(row)

# Example usage
if __name__ == "__main__":
    # Replace 'your_file.tsv' with the path to your TSV file
    tsv_file_path = 'globe_40_legs_2026.tsv'
    process_tsv(tsv_file_path)




