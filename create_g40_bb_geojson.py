import geojson as gj
import csv

def process_row_into_feature(row):
    """
    Example function that processes a row from the TSV file.
    """
    l = int(row['bb_left'])
    b = int(row['bb_bottom'])
    r = int(row['bb_right'])
    t = int(row['bb_top'])
    return gj.Feature(geometry=gj.Polygon([[(t,l), (b,l), (b,r), (t,r)]]))

def process_tsv(file_path):
    """
    Reads a TSV file and processes each row.
    """
    feature_list = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        
        # Iterate over each row in the TSV file
        for row in reader:
            feature_list.append(process_row_into_feature(row))
    feature_collection = gj.FeatureCollection(feature_list)
    print(gj.dumps(feature_collection))

# Example usage
if __name__ == "__main__":
    # Replace 'your_file.tsv' with the path to your TSV file
    tsv_file_path = 'globe_40_legs_2026.tsv'
    process_tsv(tsv_file_path)




