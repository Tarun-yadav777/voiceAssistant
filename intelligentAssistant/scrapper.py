from selenium import webdriver
import time

URL = 'https://www.india.gov.in/my-government/schemes?_ga=2.168990825.979707816.1640763068-1270151582.1640763068'


def scrapperFunction(keyword):
    driver = webdriver.Chrome()
    driver.get(URL)

    driver.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div[3]/div/div/div/div[2]/form/div/div/div/div[1]/div/div/input').send_keys(
        keyword)
    driver.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div[3]/div/div/div/div[2]/form/div/div/div/div[2]/input').click()
    time.sleep(10)
    element = driver.find_element_by_xpath(
        '/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div[2]/div/div[3]/div/div/div/div[3]/div/ul')
    links = element.find_elements_by_tag_name('a')
    linkList = []

    for link in links:
        linkList.append(link.get_attribute('href'))

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    schemes = {}
    for link in linkList:
        driver.get(link)
        heading = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div/div/div[1]/div/div/div/div/ol/li/h3').text
        info = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[2]/div/section/div/div/div/div/div/div/div[1]/div/div/div/div/ol/li/div[2]/div/p').text
        schemes[heading] = [info, link]
    driver.quit()
    return schemes


