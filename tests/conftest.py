from __future__ import annotations

import pytest
import stamina


@pytest.fixture(autouse=True, scope="session")
def deactivate_retries() -> None:
    stamina.set_active(False)
