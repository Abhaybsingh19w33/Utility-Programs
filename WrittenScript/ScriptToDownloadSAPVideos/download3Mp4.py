# !pip install requests
# !pip install bs4
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
  
def get_links_and_download(url):           
    links = []
    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text)
    
    for link in soup.find_all('a'):
        temp = link.get('href')
        if not temp == '':
            links.append(link.get('href'))
        
    tempLen = len(links)
    for i in links:
        print(i)

    for i in tqdm (range (tempLen), desc="Downloading...",ascii=False, ncols=75):                              
        print("\n",links[i])
        temp = links[i].split('.')
        
        if temp[-1] == 'mp4':
            downloadfile(links[i], url + links[i])
        elif temp[-1] == 'vtt':
            tempUrl = links[i]
            links[i] = links[i].replace(' ', '%20')
            downloadfile(tempUrl, url + links[i])
        elif temp[-1] == 'srt':
            tempUrl = links[i]
            links[i] = links[i].replace(' ', '%20')
            downloadfile(tempUrl, url + links[i])
    print("Downloaded")
    print(len(links))

def get_links_and_download_with_file(url,path):           
    links = []
    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text)
    
    for link in soup.find_all('a'):
        temp = link.get('href')
        if not temp == '':
            links.append(link.get('href'))
        
    tempLen = len(links)
    for i in links:
        print(i)

    for i in tqdm (range (tempLen), desc="Downloading...",ascii=False, ncols=75):                              
        print("\n", links[i])
        if links[i][-4] != '.':
            continue

        temp = links[i].split('.')
        
        if temp[-1] == 'mp4':
            downloadfile(links[i], url + links[i], path)
        elif temp[-1] == 'vtt':
            tempUrl = links[i]
            links[i] = links[i].replace(' ', '%20')
            downloadfile(tempUrl, url + links[i], path)
        elif temp[-1] == 'srt':
            tempUrl = links[i]
            links[i] = links[i].replace(' ', '%20')
            downloadfile(tempUrl, url + links[i], path)
        elif temp[-1] == 'txt':
            tempUrl = links[i]
            links[i] = links[i].replace(' ', '%20')
            downloadfile(tempUrl, url + links[i], path)
        else :
            tempUrl = links[i]
            links[i] = links[i].replace(' ', '%20')
            downloadfile(tempUrl, url + links[i], path)
        
    print("Downloaded")
    print(len(links))

def downloadfile(name,url,path):
#     name=name+".mp4"
    r=requests.get(url)
    # print( "****Connected****")
    # name = path + name
    path = path + '\\' + name
    print("\n******************************")
    print("name ",name)
    print("path ",path)
    print("******************************\n")
    # f=open(name,'wb')
    f=open(path,'wb')
    print ("Downloading....." )
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print ("Done")
    f.close()

def get_links(url):           
    links = []
    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text)
    
    for link in soup.find_all('a'):
        temp = link.get('href')
        if not temp == '':
            links.append(link.get('href'))

    return links

# error
url = 'https://hservers.org/sapvt/ABAP/SAP%20ABAP%20OO%20ALV/'
# url = 'https://hservers.org/sapvt/ABAP/SAP%20ABAP%20ALV/'
url_list = []

cwd = os.getcwd()

folderName = getFolderName(url)
print("--------------------------------------------------")
print("current working directory ",cwd)
print("Folder Name               ",folderName)
print("--------------------------------------------------")
path = os.path.join(cwd, folderName)
# print("path ", path)
# print("--------------------------------------------------")

if not os.path.exists(path):
    os.mkdir(path)

url_list = get_links(url)

