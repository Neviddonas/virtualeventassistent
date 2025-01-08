from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup


def get_link_workingnommads(address, links, driver):
    driver.get(address)
    
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

def get_link_remoteok(address, links, driver):
    driver.get(address)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for tr in soup.find_all("tr", attrs={'data-slug': True}):
        if 'events' in tr['data-slug'].lower():  # Check if "events" is in the text of the <tr>
            data_url = tr.find("a", class_ = "no-border tooltip")
            if data_url:
                links.append("https://remoteok.com" + data_url["href"])
    return links

def scrape_job_listings():
    options = Options()
    options.add_argument("--headless")  # Enable headless mode explicitly
    driver = webdriver.Firefox(options = options)        
    links = []
    workingnomads = ["https://www.workingnomads.com/jobs?category=management&tag=event-manager",
                     "https://www.workingnomads.com/jobs?category=management&tag=event-planning",
                     "https://www.workingnomads.com/jobs?category=management&tag=virtual-event-coordinator",
                     "https://www.workingnomads.com/jobs?category=management&tag=online-event-manager",
                     "https://www.workingnomads.com/jobs?category=management&tag=digital-event-coordinator",
                     "https://www.workingnomads.com/jobs?category=management&tag=event-marketing-specialist",
                     "https://www.workingnomads.com/jobs?category=management&tag=virtual-event-production",
                     "https://www.workingnomads.com/jobs?category=management&tag=event-support-specialist",
                     "https://www.workingnomads.com/jobs?category=management&tag=event-operations",
                     "https://www.workingnomads.com/jobs?category=management&tag=virtual-engagement-coordinator"]

    for search in workingnomads:
        links = get_link_workingnommads(search, links, driver)

    remoteok = ["https://remoteok.com/remote-marketing-jobs"]
#    for search in remoteok:
#        links = get_link_remoteok(search, links, driver)
        
    links = list(set(links))
    with open("results.html", "w") as file:
        file.write("<html><body><h1>Scraper Results</h1>")

        for link in links:
            file.write(f'<a href="{link}">{link}</a><br>')

        file.write("</body></html>")
    driver.quit()
    
scrape_job_listings()
