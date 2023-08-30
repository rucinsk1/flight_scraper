import pandas as pd
import os

from typing import Tuple, List
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.webdriver.common.by import By

def scrape(url : str) -> None:
    
    data = {
        "price" : [],
        "airlines" : [],
        "first_way_hours" : [],
        "first_way_airports" : [],
        "first_way_stops" : [],
        "return_way_hours" : [],
        "return_way_airports" : [],
        "return_way_stops" : [],
        "hand_luggage" : [],
        "checked_luggage" : []   
    }
    
    
    driver = webdriver.Chrome()
    driver.get(url)
    sleep(5)
    popup_window =  '//div[@class = "Py0r-button-content"]'#'//*[@id="portal-container"]/div/div[2]/div/div/div[1]/div/span/button'
    driver.find_element(by=By.XPATH, value = popup_window).click()
    
    flight_options = driver.find_elements(by=By.XPATH, value='//div[@class="nrc6-inner"]') #/"
    
    for element in flight_options:
        elementHTML =  element.get_attribute('outerHTML')
        element_soup = BeautifulSoup(elementHTML, 'html.parser')
        
        #price
        data["price"].append(scrape_price_from_element(element_soup))
        
        #airline
        data["airlines"].append(scrape_airlines_from_element(element_soup))
        
        #stops
        stops = scrape_stops_from_element(element_soup)
        data["first_way_stops"].append(stops[0])
        data["return_way_stops"].append(stops[1])
        
        #luggage
        luggages = scrape_luggage_from_element(element_soup)
        data["hand_luggage"].append(luggages[0])
        data["checked_luggage"].append(luggages[0])

        #time schedule
        schedule = scrape_schedule_from_element(element_soup)
        data["first_way_hours"].append(schedule[0])
        data["return_way_hours"].append(schedule[1])
        
        #Airports
        airports = scrape_airports_from_element(element_soup)
        data["first_way_airports"].append(airports[0])
        data["return_way_airports"].append(airports[1])
        
    df = pd.DataFrame(data)

    print(df)
    sleep(100000)

def scrape_price_from_element(element_soup : BeautifulSoup) -> str:
    
    temp_price = element_soup.find("div", {"class" : "nrc6-price-section"})
    price = temp_price.find("div", {"class" : "f8F1-price-text"})
    return price.text

def scrape_airlines_from_element(element_soup : BeautifulSoup) -> str:
    
    airline = element_soup.find("div", {"class" : "J0g6-operator-text"})    
    return airline.text

def scrape_stops_from_element(element_soup : BeautifulSoup) -> Tuple[str, str]:
    
    ways = element_soup.find_all("li", {"class" : "hJSA-item"})
    if len(ways) != 2:
        raise Exception(f"found only {len(ways)} ways (should be 2)")
    elif isinstance(ways[0], Tag) and isinstance(ways[1], Tag):
        first_stops = ways[0].find("span", {"class" : "JWEO-stops-text"})
        back_stops = ways[1].find("span", {"class" : "JWEO-stops-text"})
        
        return (first_stops.text, back_stops.text)
    else:
        return ('error', 'error')
    
def scrape_luggage_from_element(element_soup : BeautifulSoup) -> Tuple[str, str]:
    
    luggages = element_soup.find_all("div",{"class" : "ac27-fee-box"})
    if len(luggages) != 3:
        raise Exception(f"found only {len(luggages)} luggages (should be 3)")
    elif isinstance(luggages[0], Tag) and isinstance(luggages[1], Tag):
        hand = luggages[0].find_all("div", {"class": "ac27-inner"})[1]
        luggage = luggages[1].find_all("div", {"class": "ac27-inner"})[1]
        
        return (hand.text, luggage.text)
    else:
        return ('error', 'error')

def scrape_schedule_from_element(element_soup : BeautifulSoup) -> Tuple[str, str]:
    
    schedule = element_soup.find_all("div", {"class" : "vmXl vmXl-mod-variant-large"})
    if len(schedule) != 2:
        raise Exception(f"found only {len(schedule)} schedules(should be 2)")
    elif isinstance(schedule[0], Tag) and isinstance(schedule[1], Tag):
        first = schedule[0].find_all("span")
        ret = schedule[1].find_all("span")
        
        return (f"{first[0].text}-{first[2].text}", f"{ret[0].text}-{ret[2].text}")
    else:
        return ('error', 'error')

def scrape_airports_from_element(element_soup : BeautifulSoup) -> Tuple[str, str]:
    
    airports = element_soup.find_all("span", {"class" : "EFvI-ap-info"})
    ports = []
    
    for airport in airports:
        elems = airport.find_all("span")
        text = ''
        for elem in elems:
            text += elem.text + ' '
    
        ports.append(text[:-1])
    first_airports = ports[0] + ' -> ' + ports[1]
    return_airports = ports[2] + ' -> ' + ports[3]
    return (first_airports, return_airports)
