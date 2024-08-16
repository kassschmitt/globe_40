import pytest
import vcr
import logging
from pathlib import Path
from globe40.reanalysis_retriever import ReanalysisRetriever

# Configure vcrpy
vcr_config = {
    "record_mode": "once",  # 'once' will record the call once and use the cassette for future tests
    "cassette_library_dir": "cassettes",
    "decode_compressed_response": True,
}

# Initialize VCR
vcr = vcr.VCR(**vcr_config)


@pytest.fixture
def retriever():
    import cdsapi

    client = cdsapi.Client()
    return ReanalysisRetriever(client)


@vcr.use_cassette("retrieve_reanalysis_grib.yaml")
def test_retrieve_reanalysis_grib_success(retriever, tmp_path):
    """Test a successful data retrieval."""
    year = "2024"
    month = "01"
    day_range = ["01", "02"]
    timesteps_key = "6_hourly"
    variable_set_key = "mslp"
    leg_name = "test_leg"
    area = [50, -10, 40, 10]
    output_dir = tmp_path  # Use tmp_path for temporary directory

    retriever.retrieve_reanalysis_grib(
        year=year,
        month=month,
        day_range=day_range,
        timesteps_key=timesteps_key,
        variable_set_key=variable_set_key,
        leg_name=leg_name,
        area=area,
        output_dir=str(output_dir),
    )

    output_filename = f"G40_{leg_name}__{variable_set_key}__{year}_{month}__{timesteps_key}.grib"
    expected_path = output_dir / output_filename
    assert expected_path.exists()


@vcr.use_cassette("retrieve_reanalysis_grib_failure.yaml")
def test_retrieve_reanalysis_grib_failure(retriever, caplog):
    """Test the failure case for data retrieval."""
    # Simulate an API failure in the cassette by modifying the cassette file manually if needed
    # Here we assume the cassette is correctly set to record a failure

    year = "2023"
    month = "02"
    day_range = ["29"]
    timesteps_key = "6_hourly"
    variable_set_key = "mslp"
    leg_name = "test_leg"
    area = [50, -10, 40, 10]
    output_dir = "./test_output"

    with caplog.at_level(logging.ERROR):
        retriever.retrieve_reanalysis_grib(
            year=year,
            month=month,
            day_range=day_range,
            timesteps_key=timesteps_key,
            variable_set_key=variable_set_key,
            leg_name=leg_name,
            area=area,
            output_dir=output_dir,
        )

    assert "Error: Failed to retrieve data." in caplog.text
