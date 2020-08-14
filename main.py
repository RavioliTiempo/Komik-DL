from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from zipfile import ZipFile
import time, os, requests, re
from requests.exceptions import MissingSchema

browser = webdriver.Firefox()
browser.install_addon('H:\\Projects\\Comic-DL\\uBlock0_1.29.1b1.firefox.signed.xpi', temporary=True)
comicUrl = input('Comic Url: (ID NEEDED!)')
#comicUrl = 'https://readcomiconline.to/Comic/Doctor-Aphra/Issue-22?id=137588' # The ID is NEEDED
# Parsing the url for title
comicName = comicUrl.split('/')
comicName = comicName[4] + '?' + comicName[5]
comicName = comicName.split('?')
Zipname = comicName[0] + ' - ' + comicName[1] + '.zip'
cbzName = comicName[0] + ' - ' + comicName[1] + '.cbz'
comicUrl = comicUrl + '&readType=1&quality=hq'


browser.get(comicUrl)
time.sleep(30)

# divImage > p > img > src
print('Finding Image \n')

comicZip = ZipFile(Zipname, 'w')

imgcount = 1
while imgcount <= 100:
    # Just bruteforces the possible amount of pages
    imglink = "/html/body/div[1]/div[4]/div[5]/p[%s]/img" % (imgcount)
    #print(imglink)
    try:
        imglink = browser.find_element_by_xpath(imglink).get_attribute('src')
    except NoSuchElementException:
        comicZip.close()
        # Rename the zip to a cbz
        print("Converting to CBZ")
        os.rename(Zipname, cbzName)
        browser.close()
    try:
        imgres = requests.get(imglink)
    except MissingSchema:
        print('Thats it. No pages left')
    
    # print(imglink)
    if imgcount < 10:
        imgname = "0" + str(imgcount)
        print('Downloading page #: %s' % (imgcount))
        imgname = imgname + '.jpg'
        imgfile = open('%s' % (imgname), 'wb')
        
        for chunk in imgres.iter_content(10000):
            imgfile.write(chunk)
        imgfile.close()
        comicZip.write(imgname)
    elif imgcount >= 10:
        imgname = str(imgcount)
        print('Downloading Page #: %s' % (imgcount))
        imgname = imgname + '.jpg'
        imgfile = open('%s' % (imgname), 'wb')
        for chunk in imgres.iter_content(10000):
            imgfile.write(chunk)
        imgfile.close()
        comicZip.write(imgname)
    
    imgcount = imgcount + 1
