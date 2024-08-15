import geojson as gj
import csv

def process_row_into_area_feature(row):
    """
    Function that processes a row into a bounding box feature
    """
    l = int(row['bb_left'])
    b = int(row['bb_bottom'])
    r = int(row['bb_right'])
    t = int(row['bb_top'])
    return gj.Feature(geometry=gj.Polygon([[(l,t), (l,b), (r,b), (r,t), (l,t)]]), properties={"title": "{}".format(row['leg_name']), "description": "{} to {}".format(row['start_city'], row['finish_city']), "stroke": row['leg_color_code'], "fill": row['leg_color_code']})

def process_row_into_point_feature(row):
    """
    Function that processes a row into a point feature
    """
    lat = float(row['start_lat'])
    lon = float(row['start_lon'])    
    return gj.Feature(geometry=gj.Point((lon, lat)), properties={"title": "{}".format(row['start_city']), "description": "{} to depart {} on {}".format(row['leg_name'], row['start_city'], row['start_date_time_utc'])})

def process_tsv(file_path):
    """
    Reads a TSV file and processes each row.
    """
    feature_list = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        
        # Iterate over each row in the TSV file
        for row in reader:
            feature_list.append(process_row_into_area_feature(row))
            feature_list.append(process_row_into_point_feature(row))            
    feature_collection = gj.FeatureCollection(feature_list)
    print(gj.dumps(feature_collection))

if __name__ == "__main__":
    # Replace 'your_file.tsv' with the path to your TSV file
    tsv_file_path = 'globe_40_legs_2026.tsv'
    process_tsv(tsv_file_path)




