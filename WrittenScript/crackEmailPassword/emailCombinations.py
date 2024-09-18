import itertools
import string

characters = string.ascii_letters + string.digits  + '@'
length = 5

for i in range(2, length):
    # print(i)
    for combination in itertools.product(characters, repeat=length):
        print(''.join(combination))
        print(combination)




# import subprocess

# command = 'chrome.exe -remote-debugging-port=9222 -user-data-dir="F:\chromeData" --remote-allow-origins=*'
# result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# print(result.stdout.decode())