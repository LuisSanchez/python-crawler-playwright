from file_manager import file_reader
from linkedin_scrapper import scrape_linkedin


def start():
    companies = file_reader()
    # Replace with your LinkedIn credentials
    username = ""
    password = ""
    scrape_linkedin(companies, username, password)


if __name__ == "__main__":
    start()
