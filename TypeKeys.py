# import win32com.client as comclt
# wsh= comclt.Dispatch("WScript.Shell")
# wsh.AppActivate("Notepad") # select another application
# wsh.SendKeys("a") # send the keys you want

import time
import random
from pynput.keyboard import Controller

keyboard = Controller()  # Create the controller

def type_string_with_delay(string):
    for character in string:  # Loop over each character in the string
        keyboard.type(character)  # Type the character
        delay = random.uniform(0, 2)  # Generate a random number between 0 and 10
        time.sleep(delay)  # Sleep for the amount of seconds generated


loopCount = 0
while loopCount < 10000 :
    print('typing')
    type_string_with_delay("This is my string typed with a delay")
else :
    loopCount = 0
