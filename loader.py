import csv
import requests
from bs4 import BeautifulSoup


def find_linkedin_url(company_name):
    """
    Searches for the LinkedIn URL of a given company name.

    Args:
      company_name: The name of the company to search for.

    Returns:
      The URL of the company's LinkedIn page, or None if not found.
    """
    # Construct the search URL
    search_url = (
        f"https://www.linkedin.com/search/results/companies/?keywords={company_name}"
    )

    # Send a GET request to the search URL
    response = requests.get(search_url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "lxml")

    # Find the first company result
    company_result = soup.find("span", class_="entity-result__title-text")

    print(company_result)
    # Extract the LinkedIn URL if found
    if company_result:
        linkedin_url = company_result.find("a")["href"]
        if "/company/" in linkedin_url:
            return linkedin_url

    # No LinkedIn URL found
    return None


def main():
    # Read the CSV file
    with open("companies.csv", "r") as f:
        reader = csv.reader(f)
        companies = list(reader)

    # Find and write LinkedIn URLs
    with open("linkedin_urls.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Company Name", "LinkedIn URL"])

        for company_name in companies:
            linkedin_url = find_linkedin_url(company_name[0])
            writer.writerow([company_name[0], linkedin_url])


if __name__ == "__main__":
    main()
