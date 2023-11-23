#import numpy.core.multiarray
from io import BytesIO
import sys
# from sys import argv
from time import sleep
from PIL import ImageFilter
import requests
# import shutil
from PIL import Image
import numpy as np
from selenium import webdriver
import pytesseract
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import random
import configparser
# import io
# import cv2

uname = None
passwd = None

config = configparser.ConfigParser()
config.read('config.ini')

if len(sys.argv) > 1:
    uname = sys.argv[1]
    passwd = sys.argv[2]
else:
    uname = config.get("UserData","UserName")
    passwd = config.get("UserData","Password")

# options = ChromeOptions()
# options.add_argument("--start-maximized")
browser = webdriver.Chrome()
browser.maximize_window()
browser.implicitly_wait(5)


browser.get("https://lms"+str(random.randint(1, 10))+ ".uk.ac.ir")
WebDriverWait(browser, 20).until(EC.url_contains("mainpage.aspx"))
browser.find_element_by_id(
    "ctl00_PortalMasterPageStandardHeader_LoginStatusMainL").click()
img = None
try:
    while EC.url_contains('loginPage.aspx'):
        arr = None
        arr2 = None
        captcha = browser.find_element_by_id("ctl00_mainContent_myRadCaptcha_CaptchaImageUP")

        src = captcha.get_attribute('src')

        r = requests.get(src, stream=True)


        if r.status_code == 200:
            r.raw.decode_content = True
            try:
                image = Image.open(BytesIO(r.content))
                grayscale = image.convert("L")
                arr = np.array(grayscale)
            except Exception as e:
                print(e)

    #Convert image to black and white:

        for i in range(0,len(arr)):
            for j in range(0,len(arr[i])):
                if arr[i][j] >= 155:
                    arr[i][j] = 255
                else:
                    arr[i][j] = 0

    #Clear the edges where there is no text:

        for i in range(0, len(arr)):
            for j in range(0, len(arr[i])):
                if (i < 6 or j < 6) or (i > len(arr) - 6 or j > len(arr[i]) -6):
                    arr[i][j] = 255

                    
        for i in range(0, len(arr)):
            for j in range(0, len(arr[i]), int(len(arr[i])/5)):
                # if (i < 8 or j < 8) or (i > len(arr) - 8 or j > len(arr[i]) - 8):
                arr[i][j] = 255
                arr[i][j - 1] = 255
                arr[i][j + 1] = 255
                arr[i][j - 2] = 255
                arr[i][j + 2] = 255

    #Remove black dots from image

        for count in range(0,5):
            arr2 = arr
            for margin in range(1,5):
                for i in range(margin, len(arr)-margin):
                    for j in range(margin, len(arr[i])-margin):
                        if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255 and arr2[i-margin][j-margin] == 255 and arr2[i-margin][j+margin] == 255 and arr2[i+margin][j+margin] == 255 and arr2[i+margin][j-margin] == 255:
                            arr[i][j] = 255

        arr2 = arr

        for count in range(0,10):
            arr2 = arr
            margin = 3
            for i in range(margin, len(arr)-margin):
                for j in range(margin, len(arr[i])-margin):
                    if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255:
                        arr[i][j] = 255

        arr2 = arr

        for count in range(0, 10):
            arr2 = arr
            for margin in range(1, 6):
                for i in range(margin, len(arr)-margin):
                    for j in range(margin, len(arr[i])-margin):
                        if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255 and arr2[i-margin][j-margin] == 255 and arr2[i-margin][j+margin] == 255 and arr2[i+margin][j+margin] == 255 and arr2[i+margin][j-margin] == 255:
                            arr[i][j] = 255

        arr2 = arr

        for count in range(0, 5):
            arr2 = arr
            margin = 3
            for i in range(margin, len(arr)-margin):
                for j in range(margin, len(arr[i])-margin):
                    if arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255 and arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255:
                        arr[i][j] = 255
        
        arr2 = arr

        for count in range(0, 10):
            arr2 = arr
            margin = 1
            for i in range(margin, len(arr)-margin):
                for j in range(margin, len(arr[i])-margin):
                    if (arr2[i-margin][j] == 255 and arr2[i+margin][j] == 255) or (arr2[i][j-margin] == 255 and arr2[i][j+margin] == 255):
                        arr[i][j] = 255

        arr2 = arr

        margin = 1
        for i in range(margin, len(arr)-margin):
            for j in range(margin, len(arr[i])-margin):
                if arr2[i-margin][j] == 0 and arr2[i+margin][j] == 0 and arr2[i][j-margin] == 0 and arr2[i][j+margin] == 0 and arr2[i-margin][j-margin] == 0 and arr2[i-margin][j+margin] == 0 and arr2[i+margin][j+margin] == 0 and arr2[i+margin][j-margin] == 0:
                    arr[i][j] = 0

        img = Image.fromarray(arr)
        img = img.resize((600,200))
        img = img.filter(ImageFilter.BoxBlur(4))
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        img = img.filter(ImageFilter.GaussianBlur)
        img = img.filter(ImageFilter.UnsharpMask)
        # img = img.filter(ImageFilter.MedianFilter)
        # img2 = cv2.adaptiveThreshold(arr,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,0)
        # img2 = cv2.blur(img2,(5,5))
        # cv2.imshow("test",img2)
        # img = cv2.blur(img,(5,5))
        # img.save('out.png')
        # img.show()
        captchaText = pytesseract.image_to_string(
            img, config='--psm 8 outputbase digits')
        print(captchaText)
        if len(captchaText) == 7:
            print('login')
            if EC.presence_of_element_located((By.ID,"LoginButton")):
                try:
                    username = browser.find_element_by_id('UserName')
                    password = browser.find_element_by_id('Password')
                    captchaBox = browser.find_element_by_id(
                        'ctl00_mainContent_myRadCaptcha_CaptchaTextBox')
                    submit = browser.find_element_by_id("LoginButton")

                    username.clear()
                    username.send_keys(uname)

                    password.clear()
                    password.send_keys(passwd)

                    captchaBox.clear()
                    captchaBox.send_keys(captchaText)

                    submit.click()
                except Exception as e:
                    browser.refresh()

        else:
            browser.find_element_by_id(
                'ctl00_mainContent_myRadCaptcha_CaptchaLinkButton').click()
            sleep(2)
except Exception as e:
    print(e)
quit()
