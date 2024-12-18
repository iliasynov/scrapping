from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    browser = playwright. chromium. launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.docstring.fr/scraping/")
    button = page.get_by_role("button", name="Récupérer les livres secrets")
    if button:
        button.click()

    page.wait_for_timeout(10000)

    browser.close()
