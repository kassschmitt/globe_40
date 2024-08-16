import geojson as gj
import csv
import argparse
import cdsapi
import globe40.reanalysis_retriever as rr
from globe40.utils import extend_interval, get_days_in_interval


def process_row_into_area(row):
    """
    Processes the bounding box information into an area list.
    """
    l = float(row["bb_left"])
    b = float(row["bb_bottom"])
    r = float(row["bb_right"])
    t = float(row["bb_top"])
    return [t, l, b, r]


def process_row_into_intervals(
    row, percentage_to_change, days_either_end, year_shifts=[-6, -5, -4, -3, -2]
):
    """
    Extends the interval based on the given percentage and days padding.
    """
    start_date = row["start_date"]
    end_date = row["approx_finish_date"]
    for ys in year_shifts:
        yield extend_interval(
            start_date, end_date, percentage_to_change, days_either_end, ys
        )


def generate_rows(input_file):
    """
    Reads rows from a TSV file as dictionaries.
    """
    with open(input_file, mode="r", newline="", encoding="utf-8") as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter="\t")
        for row in reader:
            yield row


def process_row(retriever, row, percentage_to_change, days_either_end):
    """
    Processes each row and yields the required information for retrieval.
    """
    area = process_row_into_area(row)
    leg_name = row["leg_name"]
    for extended_start_date, extended_end_date in process_row_into_intervals(
        row, percentage_to_change, days_either_end
    ):

        for year, month, days in get_days_in_interval(
            extended_start_date, extended_end_date
        ):
            yield {
                "year": year,
                "month": month,
                "days": days,
                "leg_name": leg_name,
                "area": area,
                "output_dir": f"./gribs/{leg_name}",
            }


def fetch_grib_data(retriever, row_data, timesteps_key, variable_set_key):
    """
    Fetches GRIB data based on the processed row data.
    """
    retriever.retrieve_reanalysis_grib(
        year=row_data["year"],
        month=row_data["month"],
        day_range=row_data["days"],
        timesteps_key=timesteps_key,
        variable_set_key=variable_set_key,
        leg_name=row_data["leg_name"],
        area=row_data["area"],
        output_dir=row_data["output_dir"],
    )
    print(
        f"Fetched GRIB data for {row_data['year']}-{row_data['month']} {row_data['days']} {row_data['area']} into {row_data['output_dir']}"
    )


def process_tsv(
    input_file, percentage_to_change, days_either_end, timestep_key, variable_set_key
):
    """
    Reads a TSV file and processes each row using generators.
    """
    client = cdsapi.Client()
    retriever = rr.ReanalysisRetriever(client)

    # Use generators to process and fetch data
    for row in generate_rows(input_file):
        for row_data in process_row(
            retriever, row, percentage_to_change, days_either_end
        ):
            fetch_grib_data(retriever, row_data, timestep_key, variable_set_key)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process a TSV file into a collection of gribfiles."
    )
    parser.add_argument("input_file", help="Path to the input TSV file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Define parameters for interval adjustment
    percentage_to_change = 25
    days_either_end = 14
    timesteps_key = "6_hourly"
    variable_set_key = "waves"
    # Process the TSV file
    process_tsv(
        args.input_file,
        percentage_to_change,
        days_either_end,
        timesteps_key,
        variable_set_key,
    )
