from typing import List

from bs4 import BeautifulSoup
from file_manager import file_reader, file_writer
from playwright.sync_api import sync_playwright, Page

# Slow down the script by 2 seconds to make it easier to follow and avoid getting blocked
SLOW_MO = 2000
LINKEDIN_URL = "https://www.linkedin.com"
DEFAULT_HEADERS = ["Company Name", "LinkedIn URL"]


def find_linkedin_urls(page: Page, companies: List[List[str]]) -> List[List[str]]:
    """
    Finds the LinkedIn URLs for a list of companies.

    Args:
        page (Page): The Playwright Page object.
        companies (List[List[str]]): A list of company names and keywords.

    Returns:
        List[List[str]]: A list of company names and their corresponding LinkedIn URLs.
    """

    results = []
    for csv_row in companies:
        company = csv_row[0]
        keywords = csv_row[1].replace(" ", ",").lower()

        # Construct the search URL
        search_url = (
            f"{LINKEDIN_URL}/search/results/companies/?keywords={company},{keywords}"
        )
        resp = page.goto(search_url)
        page.wait_for_load_state("domcontentloaded")

        if resp.status == 200:
            # Parse the HTML content
            soup = BeautifulSoup(page.content(), "lxml")

            # Find the first company result
            company_result = soup.find("span", class_="entity-result__title-text")

            # Extract the LinkedIn URL if found
            if company_result:
                linkedin_url = company_result.find("a")["href"]
                if "/company/" in linkedin_url:
                    results.append([company, linkedin_url])

    return results


def find_company_employees(page: Page, linkedin_urls: str) -> List[str]:
    """
    Finds and retrieves information about employees of a company from LinkedIn.

    Args:
        page (Page): The page object used for web scraping.
        linkedin_urls (str): A list of LinkedIn URLs for different companies.

    Returns:
        List[str]: A list of company information, including company name, LinkedIn URL, and number of employees.
    """
    employees = []

    for csv_row in linkedin_urls:
        company_info = []
        company = csv_row[0]
        linkedin_url = csv_row[1]

        resp = page.goto(f"{linkedin_url}people/")
        page.wait_for_load_state("domcontentloaded")
        if resp.status == 200:
            # Parse the HTML content
            soup = BeautifulSoup(page.content(), "lxml")

            employees_count = soup.find(
                "span",
                class_="t-normal t-black--light link-without-visited-state link-without-hover-state",
            ).text.strip()
            company_info = [company, linkedin_url, employees_count]

            associated_members_div = soup.find(
                "div", class_="org-people__header-spacing-carousel"
            )
            if associated_members_div:
                associated_members = associated_members_div.find(
                    "h2", class_="text-heading-xlarge"
                ).text.strip()
                company_info.append(associated_members)

            employees.append(company_info)

    return employees


def scrape_linkedin(companies, username, password) -> None:
    """
    Logs into LinkedIn using the provided username and password,
    scrapes company URLs, saves them to a CSV file, and then
    scrapes company employees and saves them to another CSV file.

    Args:
        companies (list): List of company names to search for.
        username (str): LinkedIn username.
        password (str): LinkedIn password.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(slow_mo=SLOW_MO)
        context = browser.new_context()
        page = context.new_page()

        page.goto(f"{LINKEDIN_URL}/login")
        page.fill('input[name="session_key"]', username)
        page.fill('input[name="session_password"]', password)
        page.click('button[type="submit"]')

        # Wait for the login process to complete
        page.wait_for_load_state("domcontentloaded")

        # Check if login was successful
        if page.url == f"{LINKEDIN_URL}/feed/":
            company_urls = find_linkedin_urls(page=page, companies=companies)
            file_writer(
                file_name="linkedin_urls.csv",
                headers=DEFAULT_HEADERS,
                companies=company_urls,
            )
            linkedin_urls = file_reader(file_name="linkedin_urls.csv")
            company_employees = find_company_employees(
                page=page, linkedin_urls=linkedin_urls
            )
            file_writer(
                file_name="company_employees.csv",
                headers=DEFAULT_HEADERS + ["Employee Count", "Associated Members"],
                companies=company_employees,
            )
            print(
                "Scraping completed!, please check the linkedin_urls.csv and company_employees.csv files."
            )
        else:
            print("Login failed!")

        browser.close()
