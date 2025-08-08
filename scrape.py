from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Proxy authentication credentials
AUTH = 'brd-customer-hl_46b3b75b-zone-ai_scraprer:vdmz6b74jt0o'

# Proxy WebDriver endpoint URL
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'


def scrape_website(website):
    """
    Launches a remote Chrome browser via proxy, navigates to the given website,
    takes a screenshot, and returns the page HTML source.
    """
    print("Launching Chrome browser...")

    with Remote(SBR_WEBDRIVER, options=ChromeOptions()) as driver:
        driver.get(website)
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html


def extract_body_content(html_content):     
    """
    Extracts the <body> content from the given HTML using BeautifulSoup.
    Returns the body as a string if found.
    """

    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)



def clean_body_content(body_content):
    """
    Removes <script> and <style> tags from the body content,
    then returns cleaned text with whitespace stripped.
    """
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content



def split_dom_content(dom_content, max_length=6000):
    """
    Splits the DOM content string into chunks of max_length characters.
    Returns a list of string chunks.
    """
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length) 
    ]
