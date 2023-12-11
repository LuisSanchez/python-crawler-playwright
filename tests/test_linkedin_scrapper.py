import pytest
from playwright.sync_api import sync_playwright
from linkedin_scrapper import (
    find_linkedin_urls,
    find_company_employees,
)


class MockURLContent:
    def __call__(self):
        return """
        <html>
            <body>
                <span class="entity-result__title-text"><a href="/company/linkedin_url1">Company A</a></span>
            </body>
        </html>
    """


class MockEmployeesContent:
    def __call__(self):
        return """
        <html>
            <body>
                <span class="t-normal t-black--light link-without-visited-state link-without-hover-state">100</span>
                <div class="org-people__header-spacing-carousel">
                    <h2 class="text-heading-xlarge">10</h2>
                </div>
                <span class="t-normal t-black--light link-without-visited-state link-without-hover-state">200</span>
                <div class="org-people__header-spacing-carousel">
                    <h2 class="text-heading-xlarge">20</h2>
                </div>
            </body>
        </html>
    """


class MockResponse:
    def __init__(self, status=200):
        self.status = status


@pytest.fixture
def mock_page():
    # Create a mock Playwright Page object
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()


def test_find_linkedin_urls(mock_page):
    companies = [["Company A", "keyword1"]]
    expected_result = [["Company A", "/company/linkedin_url1"]]
    mock_page.content = MockURLContent()
    mock_page.goto = lambda x: MockResponse()  # Mock the response object
    actual_result = find_linkedin_urls(mock_page, companies)
    assert actual_result == expected_result


def test_find_company_employees(mock_page):
    TEST_URL = "https://url_test.com/"
    linkedin_urls = [["Company A", TEST_URL]]
    expected_result = [["Company A", TEST_URL, "100", "10"]]
    mock_page.content = MockEmployeesContent()
    mock_page.goto = lambda x: MockResponse()  # Mock the response object
    actual_result = find_company_employees(mock_page, linkedin_urls)
    assert actual_result == expected_result
