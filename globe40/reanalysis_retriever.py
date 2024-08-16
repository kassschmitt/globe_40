import cdsapi
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ReanalysisRetriever:
    TIMESTEPS = {
        "hourly": ["{:02d}:00".format(h) for h in range(24)],
        "3_hourly": ["{:02d}:00".format(h) for h in range(0, 24, 3)],
        "4_hourly": ["{:02d}:00".format(h) for h in range(0, 24, 4)],
        "6_hourly": ["{:02d}:00".format(h) for h in range(0, 24, 6)],
        "12_hourly": ["{:02d}:00".format(h) for h in range(0, 24, 12)],
        "daily_noon": ["12:00"],
        "daily_midnight": ["00:00"],
        "sched_hours": ["{:02d}:00".format(h) for h in [3, 7, 10, 13, 16, 20]],
    }

    VARIABLE_SETS = {
        "ten_metre_wind": ["10m_u_component_of_wind", "10m_v_component_of_wind"],
        "mslp": ["mean_sea_level_pressure"],
        "waves": ['mean_wave_direction', 'mean_wave_period', 'significant_height_of_combined_wind_waves_and_swell']
    }

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def retrieve_reanalysis_grib(
        self,
        year,
        month,
        day_range,
        timesteps_key,
        variable_set_key,
        leg_name,
        area,
        output_dir,
    ):
        variable_set = self.VARIABLE_SETS[variable_set_key]
        timesteps = self.TIMESTEPS[timesteps_key]

        # Create the output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        output_filename = (
            f"G40_{leg_name}__{variable_set_key}__{year}_{month}__{timesteps_key}.grib"
        )
        full_output_path = output_path / output_filename

        try:
            # Perform the retrieval
            self.client.retrieve(
                "reanalysis-era5-single-levels",
                {
                    "product_type": "reanalysis",
                    "variable": variable_set,
                    "year": year,
                    "month": month,
                    "day": day_range,
                    "area": area,
                    "time": timesteps,
                    "format": "grib",
                },
                str(full_output_path),  # convert Path object to string
            )
            self.logger.info(f"Success: Data retrieved and saved to {full_output_path}")
        except Exception as e:
            # Report error
            self.logger.error(f"Error: Failed to retrieve data. {e}")


# Example usage
if __name__ == "__main__":
    client = cdsapi.Client()
    retriever = ReanalysisRetriever(client)
    leg_name = "test_leg"
    retriever.retrieve_reanalysis_grib(
        year="2023",
        month="08",
        day_range=["01", "02", "03"],
        timesteps_key="6_hourly",
        variable_set_key="mslp",
        leg_name=leg_name,
        area=[50, -10, 40, 10],  # [North, West, South, East]
        output_dir="./gribs/{}".format(leg_name),
    )
