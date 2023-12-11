# [Telescope](https://telescopepartners.com/) Assignment

Given a CSV file of company names, create a script that can find LinkedIn URLs for those companies. The LinkedIn URLs should be stored as a CSV file. Once that is done, extend the script using Playwright browser to find the employee count from LinkedIn.

## Needed libraries

First install the following libraries on your virtual env.
To create a virtual env type the following:

```python
python -m venv vtel
```

### Then install using the following command:

```
pip install -r requirements.txt
```

#### This program uses the following libraries:

- playwright
- pytest-playwright
- pytest
- beautifulsoup4
- lxml

### Run tests

Run the following command in your terminal:

```python
pytest
```

## How to use the program?

You need to add a **valid username and password** to login successfully and access the feed and people url paths.
This can be added on the `start.py` file.

Once the credentials have been added, go to the root directory and run:

```
python start.py
```

### The program does the following steps:

- Read a `companies.csv` file where the companies are stored with a column called **keywords** to add more accurancy.
- With that list, a login to LinkedIn will be attempted.
- With the session on the page with the headless browser, a new request for each company will be done.
- If the company is found, it will be added on a new list.
- All the company LinkedIn links will be added on the `linkedin_urls.csv` file.
- Using this last file, a new request will be done for each company to find the employees and associated members, once found, they will be appended to a new list.
- A new file called `company_employees.csv` will be created with this information.

## Things to consider

- Avoid making too many requests or you will get a challenge. Last one was by voice and then a puzzle, any challenge to prove that you're a human.
- A proxy could be used but it will increase the complexity of this challenge.
- Use .env or yaml file to store credentials.
- This script uses basic web scraping techniques and might not work perfectly if LinkedIn changes their website structure. Maybe a dedicated web scraping library like Scrapy for more robust and reliable scraping would be recommended.
