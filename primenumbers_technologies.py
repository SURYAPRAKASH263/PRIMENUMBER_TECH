import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL of the site to scrape
url = 'https://hprera.nic.in/PublicDashboard'

# Function to get the content of the page
def get_page_content(url):
    response = requests.get(url, verify=False)
    return response.content

# Function to parse the main page and get project links
def get_project_links(content, num_projects=6):
    soup = BeautifulSoup(content, 'html.parser')
    
    # Modify this part based on actual site structure
    projects_section = soup.find('div', {'id': 'collapseOne1'})
    
    # If the section is not found, try another approach
    if not projects_section:
        projects_section = soup.find_all('a', string='View Details')

    project_links = projects_section.find_all('a', href=True) if projects_section else []
    
    links = ['https://hprera.nic.in' + link['href'] for link in project_links[:num_projects]]
    return links

# Function to get project details from a project page
def get_project_details(project_url):
    content = get_page_content(project_url)
    soup = BeautifulSoup(content, 'html.parser')
    details = {}

    # Extract required details
    details['GSTIN No'] = soup.find('span', {'id': 'GSTIN'}).text.strip() if soup.find('span', {'id': 'GSTIN'}) else 'N/A'
    details['PAN No'] = soup.find('span', {'id': 'PAN'}).text.strip() if soup.find('span', {'id': 'PAN'}) else 'N/A'
    details['Name'] = soup.find('span', {'id': 'Name'}).text.strip() if soup.find('span', {'id': 'Name'}) else 'N/A'
    details['Permanent Address'] = soup.find('span', {'id': 'Address'}).text.strip() if soup.find('span', {'id': 'Address'}) else 'N/A'
    
    return details

# Main function to get details of the first 6 projects
def main():
    content = get_page_content(url)
    project_links = get_project_links(content)
    
    projects_details = []
    for link in project_links:
        details = get_project_details(link)
        projects_details.append(details)
    
    return projects_details

# Run the main function and print the details
project_details = main()
print(project_details)
