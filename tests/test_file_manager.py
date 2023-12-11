import pytest

from file_manager import file_reader, file_writer


@pytest.fixture
def csv_file(tmp_path):
    # Create a temporary CSV file for testing
    file_path = tmp_path / "test.csv"
    with open(file_path, "w") as f:
        f.write("Name,Location\n")
        f.write("Company A,New York\n")
        f.write("Company B,San Francisco\n")
    return file_path

def test_file_reader(csv_file):
    # Test file_reader function
    expected_result = [["Company A", "New York"], ["Company B", "San Francisco"]]
    assert file_reader(csv_file) == expected_result

def test_file_writer(csv_file):
    # Test file_writer function
    headers = ["Name", "Location"]
    companies = [["Company A", "New York"], ["Company B", "San Francisco"]]
    file_writer(csv_file, headers, companies)

    # Read the written file and compare its contents
    with open(csv_file, "r") as f:
        assert f.read() == "Name,Location\nCompany A,New York\nCompany B,San Francisco\n"