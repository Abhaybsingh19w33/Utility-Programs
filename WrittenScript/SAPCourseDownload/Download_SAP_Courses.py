import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

def printLine():
    print("--------------------------------------------------------------------------------------------")

def getFolderName(url):
    url = url.replace('%20',' ')
    url = url.split('/')
    if url[-1] == '':
        return url[-2]
    else :
        return url[-1]

def downloadfile(name,url,path):
    print("\n in downloadfile function ---> ", url)
    r=requests.get(url)

    path = path + '\\' + name
    printLine()
    print("name ",name)
    print("path ",path)
    printLine()
    
    f=open(path,'wb')
    print ("Downloading....." )
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print ("Done")
    f.close()

def get_links(path, url, tree_spaces_input = "", tree_spaces = ""):    
    links = []
    
    if tree_spaces_input == '':
        tree_spaces = "\t"
    else: 
        tree_spaces = tree_spaces_input + tree_spaces       

    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text, 'html.parser')
    
    for link in soup.find_all('a'):
        temp = link.get('href')

        # repeatetive urls
        if not temp == '' and not temp == ( url + '/') and temp not in [ "https://hservers.org/",
                                                                         "https://hservers.org/sapvt/",     
                                                                         "https://hservers.org/sapvt/ABAP/" ] :
            
            links.append(link.get('href'))
            # print("-------------------------treeSpaces\tspaces", tree_spaces , "spaces")
            print("path",tree_spaces,temp)
            
            if temp[-1] == '/':
                # not any links yet
                pass
            else:
                tempPath = path + "\\" +temp
                print("Total path",tree_spaces,tempPath)
                
                # if path not exist then create it
                if not os.path.exists(tempPath):
                    os.mkdir(tempPath)

                temp = temp.replace(" ", "%20")
                tempUrl = url + temp
                # printLine()
                # print("tempUrl", tempUrl)
                # printLine()

                get_links_and_download_with_file(tempUrl, tempPath)
                
                get_links(tempPath, tempUrl, tree_spaces_input = "\t", tree_spaces = tree_spaces)
                # get_links_and_download_with_file(url, path)

def get_links_and_download_with_file(url,path):     
    printLine()
    print("in get_links_and_download_with_file function ",url)
    print("in get_links_and_download_with_file function ",path)
    printLine()

    links = []
    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text, 'html.parser')
    printLine()
    print(soup)
    printLine()
    # for link in soup.find_all('li'):
    #     a = link.find_all('div')
    #     for a0 in a:
    #         a1 = link.find_all('a')
    #         for a2 in a1:
    #             if 'href' in a2.attrs:
    #                 url = a2.get('href')
    #                 print("url--->>",url)
    #     print("link--->>",link)
        
        
        # print("--->>",link.get('div'))
        # # temp = link.get('href')
        # temp = link.text
        # if not temp == '':
        #     # links.append(link.get('href'))
        #     links.append(link.text)
        
    # tempLen = len(links)
    # for i in links:
    #     print("--->>",i)

    # for i in tqdm (range (tempLen), desc="Downloading...",ascii=False, ncols=75):                              
    #     # print("\n", links[i])
    #     if not links[i] == '' and not links[i] == ( url + '/') and links[i] not in [ "https://hservers.org/",                                                                      "https://hservers.org/sapvt/ABAP/" ] :
    #         continue            

    #     if links[i][-4] != '.':
    #         print("-- not doc file -->", links[i])
    #         continue

    #     print("--doc file -->", links[i])
    #     temp = links[i].split('.')
        
    #     if temp[-1] == 'NET':
    #         continue
    #     if temp[-1] == 'mp4':
    #         downloadfile(links[i], url + links[i], path)
    #     elif temp[-1] == 'vtt':
    #         tempUrl = links[i]
    #         links[i] = links[i].replace(' ', '%20')
    #         downloadfile(tempUrl, url + links[i], path)
    #     elif temp[-1] == 'srt':
    #         tempUrl = links[i]
    #         links[i] = links[i].replace(' ', '%20')
    #         downloadfile(tempUrl, url + links[i], path)
    #     elif temp[-1] == 'txt':
    #         tempUrl = links[i]
    #         links[i] = links[i].replace(' ', '%20')
    #         downloadfile(tempUrl, url + links[i], path)
    #     else :
    #         tempUrl = links[i]
    #         links[i] = links[i].replace(' ', '%20')
    #         downloadfile(tempUrl, url + links[i], path)
    
    print("endof get_links_and_download_with_file function ")
    print("=============================================================")

# url = 'https://hservers.org/sapvt/ABAP/'
# url = 'https://hservers.org/sapvt/ABAP/Use%20SAP%20BRFplus%20Like%20a%20Pro/1.%20Introduction/1.%20Course%20Introduction.mp4'
url = "https://hservers.org/sapvt/ABAP/ABAP%20Basic%20Course/"
# get folder name from URL
folderName = getFolderName(url)

path = os.path.join("F:\\SAP_HSERVER\\", folderName)

# if path not exist then create it
if not os.path.exists(path):
    os.mkdir(path)

printLine()
print("path\t\t",path)
printLine()

get_links(path, url)