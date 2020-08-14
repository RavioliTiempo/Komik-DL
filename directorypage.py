import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

pageurl = "https://readcomiconline.to/Comic/Darth-Vader"

# /html/body/div[1]/div[5]/div[1]/div[3]/div[2]/div/table/tbody/tr[3]/td[1]/a
# Grab the links to each comic from the directory page.

browser = webdriver.Firefox()
browser.install_addon('H:\\Projects\\Comic-DL\\uBlock0_1.29.1b1.firefox.signed.xpi', temporary=True)

browser.get(pageurl)
time.sleep(20)
comicList = []

linkcount = 3
while linkcount <= 100:
    comicLink = '/html/body/div[1]/div[5]/div[1]/div[3]/div[2]/div/table/tbody/tr[%s]/td[1]/a' % (linkcount)
    try:
        comicLink = browser.find_element_by_xpath(comicLink).get_attribute('href')
        comicList.append(comicLink)
        #print(comicLink)
    except NoSuchElementException:
        print('No more links :(')
        browser.close()
        break
    linkcount = linkcount + 1

print(comicList)
print(len(comicList))

# Incorporate this code with the single comic code so it function together
# make the other code into a function
