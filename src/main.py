from scraping import scrape

if __name__ == '__main__':
    
    home = 'WAW'
    dest = 'PAR'
    start = '2023-11-24'
    end = '2023-11-27'
    url = str('https://www.kayak.pl/flights/{}-{}/{}/{}?sort=price_a'.format(home, dest, start, end))
    
    scrape(url)