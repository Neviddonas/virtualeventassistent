from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import sending_email


def get_link_workingnommads(address, links, driver):
    driver.get(address)    
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup_h4 = soup.find_all("h4", class_="hidden-xs")
    hrefs = []
    for h4 in soup_h4:
        href = h4.find("a", class_="open-button")["href"]
        hrefs.append("https://www.workingnomads.com" + href)
    for ref in hrefs:
        driver.get(ref)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        href = soup.find("a", class_="apply-now")["href"]
        
        driver.get("https://www.workingnomads.com" + href)
        final_url = driver.current_url
        links.append(final_url)
    return links

def get_link_nodesk(address, links, driver):
    driver.get(address)
    time.sleep(2)
    
    jobs = driver.find_elements(By.CSS_SELECTOR, '#hits .ais-Hits-item')
    hrefs = []
    for job in jobs:
        link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        hrefs.append(link)
    for ref in hrefs:
        driver.get(ref)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        app_link = soup.find("a", href=True, string=lambda s: s and "Apply" in s)
        if app_link:
            link = app_link['href']
            clean_url = link.split('?')[0]
        links.append(clean_url)
    return links

def scrape_job_listings():
    options = Options()
    options.add_argument("--headless")  # Enable headless mode explicitly
    driver = webdriver.Firefox(options = options)        
    links = []
    search_terms = ["event manager", "event planning", "virtual event coordinator",
                    "online event manager", "digital event coordinator",
                    "event marketing specialist", "virtual event production",
                    "event support specialist", "event operations", "virtual engagement coordinator"]
    
    for search in search_terms:
        link = f"https://www.workingnomads.com/jobs?category=management&tag={search.replace(' ', '-')}"
        links = get_link_workingnommads(link, links, driver)


    for search in search_terms:
        link = f"https://nodesk.co/remote-jobs/?query={search.replace(' ', '%20')}"
        links = get_link_nodesk(link, links, driver)
        
    links = list(set(links))
    with open("results.html", "w") as file:
        file.write("<html><body><h1>Scraper Results</h1>")

        for link in links:
            file.write(f'<a href="{link}">{link}</a><br>')

        file.write("</body></html>")
    driver.quit()
    
scrape_job_listings()
sending_email.send_email()
