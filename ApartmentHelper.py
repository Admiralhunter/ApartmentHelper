import json
import sys
import time

from selenium import webdriver

#  Open json file containing all necessary objects with associated XPath's
with open('ApartmentHelper.json') as f:
    Data = json.load(f)

#  Dictionary to hold all values of the data
information = {'weather': {}, 'areaVibe': {}}
#  Dictionary for all necessary inputs
inputs = Data['inputs']



def main():
    #  Opens up chrome and goes to weatherspark to gather historical weather data

    driver = webdriver.Chrome("D:\chromedriver_win32/chromedriver.exe")
    driver.get("https://weatherspark.com/")
    driver.maximize_window()
    assert "The Typical Weather Anywhere on Earth - Weather Spark" in driver.title

    #  Enters the location of the city
    elem = driver.find_element_by_xpath("//input[@title = 'Enter City or Airport']")
    elem.clear()
    elem.send_keys(inputs['location'])
    time.sleep(0.5)
    #  Clicks the value of the first location (hopefully the correct location)
    elem = driver.find_element_by_xpath("//div[@class = 'LiveSearch-options LiveSearch-FrontPage-options']/div[@data-index = '0']")
    elem.click()
    time.sleep(0.5)

    #  Iterates through all keys of the weather object and inputs the value
    for val in Data['weather']:
        get_value_xpath(driver, information['weather'], val, Data['weather'][val])

    #  TODO Remove once debugging not required
    for val in information['weather']:
        print(val + ': ' + information['weather'][val])



    #  This section will go to Areavibe and gather demographics for the city

    cityUrl = inputs['location'].split(", ")[0]
    cityUrl = cityUrl.replace(' ', '+')
    cityUrl = cityUrl.lower()
    driver.get("https://www.areavibes.com/ax_search_full/?query=" + cityUrl)

    #  Checks to ensure that the city is in the correct state and then assigns lat and lon
    city = inputs['location'].split(", ")[0]
    state = inputs['location'].split(", ")[1]
    state = state.upper()
    areaVibeLocation = json.loads(driver.find_element_by_tag_name("body").text)
    lat = "NA"
    lon = "NA"
    for val in areaVibeLocation:
        stateCheck = val['state_abbr']
        cityCheck = val['city']
        if stateCheck == state and cityCheck == city:
            lat = val['lat']
            lon = val['lon']
            break

    #  If the lat or lon could not be determine then exit the program and output an error
    if lat == "NA" or lon == "NA":
        driver.quit()
        sys.exit("The latitude or longitude could not be retrieved.")

    #  Goes to proper page on areavibe to start getting data
    driver.get("https://www.areavibes.com/" + cityUrl +"-" + state.lower() + "/livability/?ll=" + str(lat) + "+" + str(lon))

    #  iterates through all keys of the areaVibe object and inputs the value
    for val in Data['areaVibe']:
        get_value_xpath(driver, information['areaVibe'], val, Data['areaVibe'][val])

    #  TODO Remove once debugging not required
    for val in information['areaVibe']:
        print(val + ': ' + information['areaVibe'][val])

    #  Close browser once finished
    driver.quit()


#  Gathers the value of the text at the specific xpath location and appends it to the dictionary
def get_value_xpath(driver, dictionary, key, xpath):
    elem = driver.find_element_by_xpath(xpath).text
    dictionary[key] = elem



if __name__ == "__main__":
    main()
