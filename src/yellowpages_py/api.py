import re
import requests
import urllib
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_contacts(search_term, website_filter=False):
    contacts = []
    url = f'https://www.yellowpages.ca/search/si/1/{search_term}/Montreal+QC'

    response = requests.get(url)

    if response.status_code == 200:
        parsed_html = BeautifulSoup(response.text, 'html.parser')

        pages = int(parsed_html.find(
            'span', class_='pageCount').contents[3].text.strip('\n'))

        for page in tqdm(range(1, pages + 1)):
            temp_contacts = []

            if page == 1:
                temp_contacts = get_page_contacts(
                    url, page, website_filter, parsed_html)
            else:
                temp_contacts = get_page_contacts(url, page, website_filter)

            for contact in temp_contacts:
                contacts.append(contact)

    return contacts


def get_page_contacts(url, page, website_filter=False, parsed_html=None):
    contacts = []

    def add_contact(listing):
        phone_elem = listing.find(
            'li', class_='mlr__submenu__item')

        if phone_elem:
            contacts.append({
                'name': listing.find('a', class_='jsListingName').text.replace(',', ';'),
                'phone': phone_elem.h4.text
            })

    def parse_listings(parsed_html):
        listings = parsed_html.find_all('div', class_='listing')

        for listing in listings:
            if website_filter:
                if not listing.find('li', class_='mlr__item--website'):
                    add_contact(listing)
            else:
                add_contact(listing)

    if not parsed_html:
        url = re.sub(r'si\/\d+\/', f'si/{page}/', url)

        response = requests.get(urllib.parse.quote_plus(url, safe=':/ +'))

        if response.status_code == 200:
            parse_listings(BeautifulSoup(response.text, 'html.parser'))

    else:
        parse_listings(parsed_html)

    return contacts


if __name__ == '__main__':
    print(f'\n{get_contacts("Alarm System", True)}\n')
