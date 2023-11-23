import json
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('ignore-ssl-errors')
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(5)
browser.maximize_window()

imagePointer = 0
imageUrls = []
#browser.get("https://www.google.com/search?q=نقش+های+اسلیمی+ایرانی&tbm=isch&ved=2ahUKEwjHppjz7oDvAhWL34UKHe7pD20Q2-cCegQIABAA&oq=نقش+های+اسلیمی+ایرانی&gs_lcp=CgNpbWcQA1CCkDZYgpA2YNSTNmgAcAB4AIABnwOIAZ8DkgEDNC0xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=R2g1YIfnAou_lwTu07_oBg&bih=1299&biw=2708&client=opera-gx&hl=en")
browser.get("https://www.google.com/search?q=%D9%86%D9%82%D8%B4%20%D9%87%D8%A7%DB%8C%20%D8%A7%D8%B3%D9%84%DB%8C%D9%85%DB%8C%20%D8%A7%DB%8C%D8%B1%D8%A7%D9%86%DB%8C&tbm=isch&hl=en&tbs=rimg:CT6XkwxCQO_1ZYZfDNT10xEz7&bih=1299&biw=2708&client=opera-gx&sa=X&ved=0CBsQuIIBahcKEwiQ6eaGh4PvAhUAAAAAHQAAAAAQBg")
images = browser.find_elements_by_class_name("rg_i")
try:
  for j in range(200):
    for i in range(imagePointer,len(images)):
      image = images[i]
      browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth',block:'start'});", image)
      # WebDriverWait(browser, 200).until(
      #         EC.element_to_be_clickable((By.XPATH, "//img[@class='rg_i',@src='"+image.get_attribute("src")+"']")))
      # image.click()
      # sleep(0.3)
      for k in range(100):
        try:
          image.click()
          break
        except :
          pass
      imageUrl = browser.find_elements_by_class_name(
          "n3VNCb")[0].get_attribute("src")
      imageUrls.append(imageUrl)
    imagePointer = len(images)
    sleep(2)
    images = browser.find_elements_by_class_name("rg_i")
    print("images len = " + str(len(images))+", # images url = " + str(len(imageUrls)) + ", j = " + str(j))
except Exception as e:
  print(e)
with open("./imageUrls_"+str(time.time())+"_imgNum_"+str(len(imageUrls))+".json","w") as f:
  json.dump(imageUrls,f)