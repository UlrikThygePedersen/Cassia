import pytest
import pandas as pd  # type:ignore
from pathlib import Path
from cassia.cassia import Cassia

# Base directory path
BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def load_vessels():
    """Fixture to load vessels data."""
    vessels_csv_path = BASE_DIR / "assets/vessels.csv"
    vessels_df = pd.read_csv(vessels_csv_path)
    return vessels_df


@pytest.fixture(scope="session")
def load_ports():
    """Fixture to load ports data."""
    ports_csv_path = BASE_DIR / "assets/ports.csv"
    ports_df = pd.read_csv(ports_csv_path)
    return ports_df


@pytest.fixture(scope="session")
def load_tide_heights():
    """Fixture to load tide heights data."""
    tide_heights_csv_path = BASE_DIR / "assets/tide_heights.csv"
    tide_heights_df = pd.read_csv(tide_heights_csv_path)
    return tide_heights_df


@pytest.fixture(scope="session")
def cassia_instance(load_vessels, load_ports, load_tide_heights):
    """Fixture to initialize the Cassia instance."""
    # Assuming Cassia uses these dataframes internally
    cassia = Cassia()
    return cassia
