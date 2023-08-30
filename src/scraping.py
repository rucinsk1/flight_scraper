import pandas as pd
import os


from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.webdriver.common.by import By




if __name__ == '__main__':
    
    driver = webdriver.Chrome()

    home = 'WAW'
    dest = 'PAR'
    start = '2023-11-24'
    end = '2023-11-27'
    url = str('https://www.kayak.pl/flights/{}-{}/{}/{}?sort=price_a'.format(home, dest, start, end))

    driver.get(url)
    # popup_window = '//*[@id="portal-container"]/div/div[2]/div/div/div[1]/div/span/button'
    # driver.find_element(by=By.XPATH, value = popup_window).click()
    
    flight_rows = driver.find_elements(by=By.XPATH, value="//div[@class='nrc6-inner']")
    print(flight_rows)
    
    prices = []
    airlines = []
    first_flight_stops = []
    return_flight_stops = []
    hand_luggage = []
    checked_luggage = []
    first_way_hours = []
    return_way_hours = []
    full_time = []
    for element in flight_rows:
        elementHTML =  element.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')
        
        #price
        temp_price = elementSoup.find("div", {"class" : "nrc6-price-section"})
        price = temp_price.find("div", {"class" : "f8F1-price-text"})
        prices.append(price.text)

        #airline
        airline = elementSoup.find("div", {"class" : "J0g6-operator-text"})
        airlines.append(airline.text)
        print(type(elementSoup))
        
        #stops
        ways = elementSoup.find_all("li", {"class" : "hJSA-item"})
        if len(ways) != 2:
            raise Exception(f"found only {len(ways)} ways (should be 2)")
        elif isinstance(ways[0], Tag) and isinstance(ways[1], Tag):
            first_stops = ways[0].find("span", {"class" : "JWEO-stops-text"})
            back_stops = ways[1].find("span", {"class" : "JWEO-stops-text"})
            first_flight_stops.append(first_stops.text)
            return_flight_stops.append(back_stops.text)
        else:
            first_flight_stops.append("error")
            return_flight_stops.append("error")
        
        #luggage
        luggages = elementSoup.find_all("div",{"class" : "ac27-fee-box"})
        if len(ways) != 2:
            raise Exception(f"found only {len(luggages)} luggages (should be 2)")
        elif isinstance(luggages[0], Tag) and isinstance(luggages[1], Tag):
            hand = luggages[0].find_all("div", {"class": "ac27-inner"})[1]
            luggage = luggages[1].find_all("div", {"class": "ac27-inner"})[1]
            hand_luggage.append(hand.text)
            checked_luggage.append(luggage.text)
        else:
            hand_luggage.append("error")
            luggages.append("error")
        
        #time schedule
        schedule = elementSoup.find_all("div", {"class" : "vmXl vmXl-mod-variant-large"})
        if len(schedule) != 2:
            raise Exception(f"found only {len(schedule)} schedules(should be 2)")
        elif isinstance(schedule[0], Tag) and isinstance(schedule[1], Tag):
            first = schedule[0].find_all("span")
            first_way_hours.append(f"{first[0].text}-{first[2].text}")
            ret = schedule[1].find_all("span")
            return_way_hours.append(f"{ret[0].text}-{ret[2].text}")
        else:
            first_way_hours.append("error")
            return_way_hours.append("error")
            print(type(schedule[0]))
        
        
        #travel_time
        
        
    print(prices)
    print(airlines)
    print(first_flight_stops)
    print(return_flight_stops)
    print(hand_luggage)
    print(checked_luggage)
    print(first_way_hours)
    print(return_way_hours)
    
    data = {
        "price" : prices,
        "airline" : airlines,
        "first_way_hours" : first_way_hours,
        "first_way_stops" : first_flight_stops,
        "return_way_hours" : return_way_hours,
        "return_stops" : return_flight_stops,
        "hand_luggage" : hand_luggage,
        "checked_luggage" : checked_luggage
    }
    
    df = pd.DataFrame(data)

    print(df)
        #luggage
        # h_luggage = temp_price.find("div", {"class" : "ac27-inner"})
        # n_luggage = temp_price.find("div", {"class" : "ac27-inner"})
        
    sleep(100000)
    
    #nrc6-inner
    
    print("test")