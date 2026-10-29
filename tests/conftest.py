from pathlib import Path

import pytest

from erp_spec_forge.loader import load

SPECS = Path(__file__).resolve().parents[1] / "specs"


@pytest.fixture(scope="session")
def system():
    return load(SPECS)
