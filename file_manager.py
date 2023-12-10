import csv
from typing import List


def file_reader(file_name: str = "companies.csv") -> List[str]:
    """
    Read a CSV file and return its contents as a list of strings.

    Args:
        file_name (str): The name of the CSV file to read.

    Returns:
        List[str]: The contents of the CSV file, excluding the header row.
    """
    companies = []
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        companies = list(reader)

    return companies[1:]  # Skip header row


def file_writer(file_name: str, headers: List[str], companies: List[List[str]]) -> None:
    """
    Write the headers and company information to a CSV file.

    Args:
        file_name (str): The name of the CSV file to write.
        headers (List[str]): The list of header names.
        companies (List[List[str]]): The list of company information.
    """
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for company_info in companies:
            writer.writerow(company_info)
