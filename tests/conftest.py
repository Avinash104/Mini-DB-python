import pytest
from database import Database
from datasets import load_test_data

@pytest.fixture
def test_db():
    db = Database()
    load_test_data(db)
    return db