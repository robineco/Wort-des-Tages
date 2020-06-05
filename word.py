from requests.exceptions import ConnectionError
from termcolor import colored
from bs4 import BeautifulSoup
import requests

try:
    url = 'https://www.duden.de/wort-des-tages'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    block = soup.find(id='block-wordoftheday').findAll('a')
    word = block[0].contents[0]
    info = block[1].contents[0][:-2]


    minus = ''
    for i in range(16 + len(info)):
        minus += '-'

    print(colored(minus, 'yellow'))
    print(colored('Wort des Tages: ', 'green') + colored(word, 'cyan', attrs=['bold']) + '\n' + colored('Wortart:        ', 'green') + colored(info, 'cyan'))
    print(colored(minus, 'yellow'))
except ConnectionError as e:
    print(colored('No Internet Connection', 'red', attrs=['bold', 'blink']))
