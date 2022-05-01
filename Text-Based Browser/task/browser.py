import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore

# write your code here
args = sys.argv
directory = ""

if len(args) == 2:
    directory = args[1]
    if not os.path.exists(directory):
        os.mkdir(directory)
    if not directory.endswith('\\'):
        directory += '\\'

url = ""
last_url = ""
stack = []
file = None

while url != "exit":
    url = input()
    if url == "back":
        if len(stack) > 0:
            print(stack.pop())
    elif url.find('.') < 0:
        print('Incorrect URL')
    elif url != "exit":
        if last_url != "":
            stack.append(last_url)

        if not url.startswith('https://'):
            url = 'https://' + url

        r = requests.get(url)
        if r:
            soup = BeautifulSoup(r.content, 'html.parser')
            tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
            if directory != "":
                filename = url[len('https://'):]
                print("filename: " + filename)
                index = filename.find('/')
                if index >= 0:
                    filename = filename[:index]
                print("Opening file: " + directory + filename)
                file = open(directory + filename, 'w', encoding="utf-8")

            for tag in tags:
                text = tag.get_text()
                if text.strip() != '':
                    if tag.name == 'a':
                        print(Fore.BLUE + text)
                    else:
                        print(text)
                    if file is not None:
                        file.write(text + '\n')

            if file is not None:
                file.close()
            last_url = r.text
        else:
            print('ERROR: ' + r.status_code)
