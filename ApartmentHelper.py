import time

from selenium import webdriver

#  Opens Chrome to start the process of gathering data
inputs = {}
inputs['location'] = "Grove City, Ohio"
inputs['Zip Code'] = 43123



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
    #clicks the value of the first location (hopefully the correct location)
    elem = driver.find_element_by_xpath("//div[@class = 'LiveSearch-options LiveSearch-FrontPage-options']/div[@data-index = '0']")
    elem.click()
    time.sleep(1)

    #  dictionary to hold all values of the weather for location
    weather = {}

    get_value_xpath(driver, weather, 'Location Description', "//div[@class = 'Section-body charts_only_do_hide'][1]//p[1]")
    get_value_xpath(driver, weather, 'Best Tourism Time', "//div[@class = 'Section-body charts_only_do_hide'][1]//p[2]")

    get_value_xpath(driver, weather, 'Warm Season', "//div[@class = 'Section-body charts_only_do_hide'][2]/p[1]")
    get_value_xpath(driver, weather, 'Cold Season', "//div[@class = 'Section-body charts_only_do_hide'][2]/p[2]")

    get_value_xpath(driver, weather, 'Wet Season', "//div[@class = 'Section-body charts_only_do_hide'][4]/p[2]")
    get_value_xpath(driver, weather, 'Dry Season', "//div[@class = 'Section-body charts_only_do_hide'][4]/p[3]")
    get_value_xpath(driver, weather, 'Snowfall', "//div[@class = 'Section-body charts_only_do_hide'][4]/p[10]")
    get_value_xpath(driver, weather, 'Humidity', "//div[@class = 'Section-body charts_only_do_hide'][6]/p[3]")
    get_value_xpath(driver, weather, 'Surface Layout', "//div[@class = 'Section-body charts_only_do_hide'][11]/p[3]")




    print(weather)
    for val in weather:
        print(val + ': ' + weather[val])

    driver.quit()


#  Gathers the value of the text at the specific xpath location and appends it to the dictionary
def get_value_xpath(driver, dictionary, key, xpath):
    elem = driver.find_element_by_xpath(xpath).text
    dictionary[key] = elem


if __name__ == "__main__":
    main()
