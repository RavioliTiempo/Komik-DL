from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from zipfile import ZipFile
import time, os, requests, re, glob
from requests.exceptions import MissingSchema

browser = webdriver.Firefox()
browser.install_addon('H:\\Projects\\Comic-DL\\uBlock0_1.29.1b1.firefox.signed.xpi', temporary=True)
#comicUrl = input('Comic Url: (ID NEEDED!)')

# TODO: Add img file cleanup after each issue

def comicDL(comicUrl):
    # Parsing the url for title
    comicName = comicUrl.split('/')
    comicName = comicName[4] + '?' + comicName[5]
    comicName = comicName.split('?')
    Zipname = comicName[0] + ' - ' + comicName[1] + '.zip'
    cbzName = comicName[0] + ' - ' + comicName[1] + '.cbz'
    comicUrl = comicUrl + '&readType=1&quality=hq'
    browser.get(comicUrl)
    time.sleep(30)
    print('Finding Image \n')
    comicZip = ZipFile(Zipname, 'w')
    imgcount = 1
    while imgcount <= 300: # Just bruteforces the possible amount of pages        
        imglink = "/html/body/div[1]/div[4]/div[5]/p[%s]/img" % (imgcount) # The XPath for the page img.
        imgname = "%03d" % (imgcount)
        imgname = str(imgname) + '.jpg'
        try:
            imglink = browser.find_element_by_xpath(imglink).get_attribute('src')
        except NoSuchElementException:
            comicZip.close()
            # Rename the zip to a cbz
            print("Converting to CBZ")
            os.rename(Zipname, cbzName)
            print('Cleaning up.')
            for pageImg in glob.glob('*.jpg'):
                os.remove(pageImg)
           # browser.close()
            break
        try:
            imgres = requests.get(imglink)
        except MissingSchema:
            print('Thats it. No pages left')
        
        # print(imglink)
        
        print('Downloading page #: %s' % (imgcount))
        imgname = imgname + '.jpg'
        imgfile = open('%s' % (imgname), 'wb')
        for chunk in imgres.iter_content(10000):
            imgfile.write(chunk)
        imgfile.close()
        comicZip.write(imgname)    
        imgcount = imgcount + 1

def comicSeries(pageUrl):
    browser.get(pageUrl)
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
            #browser.close()
            break
        linkcount = linkcount + 1
    
    for link in comicList:
        comicDL(link)




# Download the series
#comicSeries('https://readcomiconline.to/Comic/Darth-Vader-2017')

# Download single issue
comicDL('https://readcomiconline.to/Comic/Darth-Vader-2017/TPB-2?id=133671')
