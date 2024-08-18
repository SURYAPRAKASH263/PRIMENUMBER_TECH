import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://hprera.nic.in/PublicDashboard'

def get_page_content(url):
    response = requests.get(url, verify=False)
    return response.content

def get_project_links(content, num_projects=6):
    soup = BeautifulSoup(content, 'html.parser')
    
    projects_section = soup.find('div', {'id': 'collapseOne1'})
    
    if not projects_section:
        projects_section = soup.find_all('a', string='View Details')

    project_links = projects_section.find_all('a', href=True) if projects_section else []
    
    links = ['https://hprera.nic.in' + link['href'] for link in project_links[:num_projects]]
    return links

def get_project_details(project_url):
    content = get_page_content(project_url)
    soup = BeautifulSoup(content, 'html.parser')
    details = {}

    details['GSTIN No'] = soup.find('span', {'id': 'GSTIN'}).text.strip() if soup.find('span', {'id': 'GSTIN'}) else 'N/A'
    details['PAN No'] = soup.find('span', {'id': 'PAN'}).text.strip() if soup.find('span', {'id': 'PAN'}) else 'N/A'
    details['Name'] = soup.find('span', {'id': 'Name'}).text.strip() if soup.find('span', {'id': 'Name'}) else 'N/A'
    details['Permanent Address'] = soup.find('span', {'id': 'Address'}).text.strip() if soup.find('span', {'id': 'Address'}) else 'N/A'
    
    return details

def main():
    content = get_page_content(url)
    project_links = get_project_links(content)
    
    projects_details = []
    for link in project_links:
        details = get_project_details(link)
        projects_details.append(details)
    
    return projects_details

project_details = main()
print(project_details)
