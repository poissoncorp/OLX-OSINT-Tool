from scrapers import *
from utils import *
from json import dumps
from time import time

def get_region():
    while True:
        region_to_search = out('?', 'Region to search')
        regions_found = autocomplete(region_to_search)

        if len(regions_found):
            out('I', 'Found regions')

            i = 0
            for region in regions_found:
                out('I', region['text'], 4, i)
                i += 1
            out('I', 'Search another region', 4, 'S')

            region_to_search = out('?', 'Pick a region from above')
            try:
                if int(region_to_search) in range(i):
                    region_id = regions_found[int(region_to_search)]['id']
                    break
                else:
                    out('E', 'Region outside of range')
            except:
                if region_to_search != 'S':
                    out('E', 'Unknown region')
        else:
            out('W', 'Region not found!', 4)
    return region_id

if __name__ == '__main__':
    region_id = get_region()
    pages = get_pages(region_id)
    out('I', 'Found ' + str(len(pages)) + ' pages of results')
    if out('?', 'Do you want to proceed? (y/n)') not in ['y', 'Y']:
        exit()
    offers_urls = scrap_offers_urls(pages)
    out('I', 'Found ' + str(len(offers_urls)) + ' offers')
    sellers = scrap_offers(offers_urls)
    out('I', 'Found ' + str(len(sellers)) + ' unique sellers')

    file_path = 'olx_sellers_' + str(time()).split('.')[0] + '.json'
    with open(file_path, 'a') as file:
        file.write(dumps(sellers))
    out('I', 'Exported sellers info to the ' + file_path + ' file')
