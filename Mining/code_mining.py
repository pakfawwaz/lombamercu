

from selenium import webdriver
from selenium.common import exceptions
import sys
import time
import csv
import io
def scrape(url):
    


    driver = webdriver.Chrome('E:/chromedriver')


    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    try:
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    try:
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    print("> JUDUL: " + title + "\n")
    print("> USERNAME & KOMENTAR:")
    
             
    for username, comment in zip(username_elems, comment_elems):
        print(username.text + ":")
        print(comment.text + "\n")
    with io.open('youtube18.csv', 'w', newline='', encoding="utf-16") as file:
         writer = csv.writer(file, quoting=csv.QUOTE_ALL)
         writer.writerow(["Username", "Comment"])
         for username, comment in zip(username_elems, comment_elems):
             writer.writerow([username.text, comment.text])

    driver.close()

if __name__ == "__main__":
    scrape(sys.argv[1])
