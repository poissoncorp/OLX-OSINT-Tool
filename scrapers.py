from requests import post, get
from json import loads
from tqdm import tqdm
from requests import get
from bs4 import BeautifulSoup as bs


def autocomplete(region):
    r = post('https://www.olx.pl/ajax/geo6/autosuggest/', data={'data': region})
    return loads(r.text)['data']


def get_pages(city_id):
    r = bs(
        post('https://www.olx.pl/oferty/', data={'search[city_id]': city_id}).text,
        features='html.parser',
    )

    pages = []
    for page in r.find('div', {'class': 'pager'}).find_all('a')[:-1]:
        pages.append(page['href'])
    pages.append(pages[0].split('?')[0])

    return pages


def scrap_offers_urls(pages):
    offers = []
    list(map(lambda page: bs(get(page).text, features='html.parser').find_all('div', {}),pages))
    for page in pages:
        r = bs(get(page).text, features='html.parser')

        for offer in r.find_all('div', {'class': 'offer-wrapper'}):
            url = offer.find('a')['href']
            if 'olx.pl/d/oferta' in url:
                offers.append(url)

    return offers


def scrap_offers(offers_urls):
    sellers = []

    for i in tqdm(range(len(offers_urls)), desc='Scraping..'):
        r = bs(get(offers_urls[i]).text, features='html.parser')
        card = r.find('div', {'data-cy': 'seller_card'})

        seller = {
            'name': card.find('h2').text,
            'offers': [offers_urls[i]],
            'fb_connected': False,
            'avatar': None,
            'last_online': card.find('span').text.replace('Ostatnio online ', ''),
        }

        if card.find('a'):
            seller['url'] = 'https://www.olx.pl' + card.find('a')['href']
        else:
            seller['url'] = None

        for img in card.find_all('img'):
            if 'Facebook' in img['alt']:
                seller['fb_connected'] = True
            elif 'avatar' in img['alt']:
                seller['avatar'] = img['src']

        seller['registered_since'] = [
            i for i in card.find_all('div') if 'Na OLX od' in i.text
        ][-1].text.replace('Na OLX od ', '')

        sellers.append(seller)

    sellers_fixed = []

    for seller in sellers:
        if seller['url']:
            for duplicate in [i for i in sellers if i['url'] == seller['url']]:
                if duplicate['offers'][0] not in seller['offers']:
                    seller['offers'].append(duplicate['offers'][0])
                sellers.remove(duplicate)
        else:
            # amogus 😳😳
            for sus in [i for i in sellers if i['name'] == seller['name']]:
                if sus['registered_since'] == seller['registered_since']:
                    if sus['last_online'] == seller['last_online']:
                        if sus['offers'][0] not in seller['offers']:
                            seller['offers'].append(sus['offers'][0])
                        sellers.remove(sus)
        sellers_fixed.append(seller)

    return sellers_fixed
