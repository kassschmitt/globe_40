import geojson as gj
import csv
import argparse
import os


def process_row_into_area_feature(row):
    """
    Function that processes a row into a bounding box feature
    """
    l = int(row["bb_left"])
    b = int(row["bb_bottom"])
    r = int(row["bb_right"])
    t = int(row["bb_top"])
    return gj.Feature(
        geometry=gj.Polygon([[(l, t), (l, b), (r, b), (r, t), (l, t)]]),
        properties={
            "title": "{}".format(row["leg_name"]),
            "description": "{} to {}".format(row["start_city"], row["finish_city"]),
            "stroke": row["leg_color_code"],
            "fill": row["leg_color_code"],
        },
    )


def process_row_into_point_feature(row):
    """
    Function that processes a row into a point feature
    """
    lat = float(row["start_lat"])
    lon = float(row["start_lon"])
    return gj.Feature(
        geometry=gj.Point((lon, lat)),
        properties={
            "title": "{}".format(row["start_city"]),
            "description": "{} to depart {} on {}".format(
                row["leg_name"], row["start_city"], row["start_date"]
            ),
        },
    )


def process_tsv(input_file, output_file):
    """
    Reads a TSV file and processes each row.
    """
    feature_list = []
    with open(input_file, mode="r", newline="", encoding="utf-8") as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")

        # Iterate over each row in the TSV file
        for row in reader:
            feature_list.append(process_row_into_area_feature(row))
            feature_list.append(process_row_into_point_feature(row))

    # Create the GeoJSON FeatureCollection
    feature_collection = gj.FeatureCollection(feature_list)

    # Write the GeoJSON data to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        gj.dump(feature_collection, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process a TSV file into a GeoJSON FeatureCollection."
    )
    parser.add_argument("input_file", help="Path to the input TSV file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Derive the output file name
    input_file = args.input_file
    output_file = os.path.splitext(input_file)[0] + ".geojson"

    # Process the TSV file and generate the GeoJSON output
    process_tsv(input_file, output_file)
    print(f"GeoJSON data has been written to {output_file}")
