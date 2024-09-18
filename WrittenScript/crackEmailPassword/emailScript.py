from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


chromedata = 'F:/chromedata'
# chrome.exe –remote-debugging-port=9222 –user-data-dir=F:\chromeData
path = 'C:/Program Files/Google/Chrome/Application'
# Initialize the webdriver and open a website
driver = webdriver.Chrome()
driver.get("https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%3Ftab%3Drm%26ogbl&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%3Ftab%3Drm%26ogbl&osid=1&passive=1209600&service=mail&ifkv=AQMjQ7RLPsVdmPI163VdIU6mSwkOCcHiTVqRqmv881UgmqTuY34b3RXME5itDHYUNYX6pJBlCMFI&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward&TL=ADBc5UNwsbNIX5kFPvkb_Wfd4PRBT1JpyhNTtbbUFOq5G3mUt35SjxQmCdjfO5xY")

# Find the input field element and enter data
input_field = driver.find_element("xpath", '//*[@id="identifierId"]')
# input_field.send_keys("180303105323@paruluniversity.ac.in")
input_field.send_keys("abhaybsingh19w33@gmail.com")

# Press the "Enter" key
input_field = driver.find_element("xpath", '//*[@id="identifierNext"]/div/button/span')
input_field.click()

# wait for passsword screen to come
time.sleep(4)

input_field = driver.find_element("xpath", '//*[@id="password"]/div[1]/div/div[1]/input')
password = 'Asdfgh@1234'
input_field.send_keys(password)

# Press the "Enter" key
input_field = driver.find_element("xpath", '//*[@id="passwordNext"]/div/button/span')
input_field.click()

# wait for passsword screen to come
time.sleep(4)

input_field = driver.find_element("xpath", '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/section/div/div/section/header/div/h2/span')

# wait for passsword screen to come
time.sleep(4)
# input_field.click()
# Close the webdriver
driver.close()