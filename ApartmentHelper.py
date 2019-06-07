import json
import time

from selenium import webdriver

#  Opens Chrome to start the process of gathering data
inputs = dict()

#  City format: (city, ST)
inputs['location'] = "Grove City, OH"
inputs['Zip Code'] = 43123

#  Open json file containing weather object
with open('ApartmentHelper.json') as f:
    Data = json.load(f)

#  dictionary to hold all values of the weather for location
information = {'weather': {}, 'areaVibe': {}}



def main():

    #  Opens up chrome and goes to weatherspark to gather historical weather data

    driver = webdriver.Chrome("D:\chromedriver_win32/chromedriver.exe")
    driver.get("https://weatherspark.com/")
    driver.maximize_window()

    assert "The Typical Weather Anywhere on Earth - Weather Spark" in driver.title
    #  enters the location of the city
    elem = driver.find_element_by_xpath("//input[@title = 'Enter City or Airport']")
    elem.clear()
    elem.send_keys(inputs['location'])
    time.sleep(1)
    #  clicks the value of the first location (hopefully the correct location)
    elem = driver.find_element_by_xpath("//div[@class = 'LiveSearch-options LiveSearch-FrontPage-options']/div[@data-index = '0']")
    elem.click()
    time.sleep(1)

    for val in Data['weather']:
        get_value_xpath(driver, information['weather'], val, Data['weather'][val])

    for val in information['weather']:
        print(val + ': ' + information['weather'][val])


    #  This section will go to Areavibe and gather demographics for the city


    cityUrl = inputs['location'].split(", ")[0]
    cityUrl = cityUrl.replace(' ', '+')
    cityUrl = cityUrl.lower()
    driver.get("https://www.areavibes.com/ax_search_full/?query=" + cityUrl)

    city = inputs['location'].split(", ")[0]
    state = inputs['location'].split(", ")[1]
    areaVibeLocation = json.loads(driver.find_element_by_tag_name("body").text)
    for val in areaVibeLocation:
        stateCheck = val['state_abbr']
        cityCheck = val['city']
        if stateCheck == state and cityCheck == city:
            lat = val['lat']
            lon = val['lon']
            break

    driver.get("https://www.areavibes.com/" + cityUrl +"-" + state.lower() + "/livability/?ll=" + str(lat) + "+" + str(lon))

    for val in Data['areaVibe']:
        get_value_xpath(driver, information['areaVibe'], val, Data['areaVibe'][val])

    for val in information['areaVibe']:
        print(val + ': ' + information['areaVibe'][val])

    driver.quit()


#  Gathers the value of the text at the specific xpath location and appends it to the dictionary
def get_value_xpath(driver, dictionary, key, xpath):
    elem = driver.find_element_by_xpath(xpath).text
    dictionary[key] = elem



if __name__ == "__main__":
    main()
