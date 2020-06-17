from requests.exceptions import ConnectionError
from termcolor import colored
from bs4 import BeautifulSoup
import requests

lenOfLongestText = 5


def createFrequency(full, empty):
    wordFrequency = ''
    for i in range(full):
            wordFrequency += '▮'
        
    for i in range(empty):
        wordFrequency += '▯'
    
    return wordFrequency


def updateLongestText(text):
    global lenOfLongestText
    if len(text) > lenOfLongestText:
        lenOfLongestText = len(text)


def printSeperator():
    minus = ''
    for i in range(16 + lenOfLongestText):
        minus += '-'
    print(colored(minus, 'yellow'))


def main():
    try:
        baseUrl = 'https://www.duden.de'
        wordOfTheDayUrl = '/wort-des-tages'

        response = requests.get(baseUrl + wordOfTheDayUrl)

        soup = BeautifulSoup(response.text, "html.parser")

        block = soup.find(id='block-wordoftheday').find('a').attrs['href']
        wordUrl = baseUrl + block

        response = requests.get(wordUrl, "html.parser")
        soup = BeautifulSoup(response.text, "html.parser")

        
        word = soup.find("span", {"class": "lemma__main"}).text
        word = word.replace('\u00AD', '')
        updateLongestText(word)

        full = len(soup.find("span", {"class": "shaft__full"}).text)
        empty = len(soup.find("span", {"class": "shaft__empty"}).text)
        wordFrequency = createFrequency(full, empty)
        
        rechtschreibung = soup.find(id='rechtschreibung').find('dd').text
        updateLongestText(rechtschreibung)
        bedeutung = soup.find(id='bedeutung').find('p').text
        updateLongestText(bedeutung)
        herkunft = soup.find(id='herkunft').find('p').text
        updateLongestText(herkunft)

        printSeperator()
        print(colored('Wort des Tages: ', 'green') + colored(word, 'cyan'))
        print(colored('Häufigkeit:     ', 'green') + colored(wordFrequency, 'cyan'))
        print(colored('Worttrennung:   ', 'green') + colored(rechtschreibung, 'cyan'))
        print(colored('Bedeutung:      ', 'green') + colored(bedeutung, 'cyan'))
        print(colored('Herkunft:       ', 'green') + colored(herkunft, 'cyan'))
        printSeperator()

    except ConnectionError as e:
        print(colored('No Internet Connection', 'red', attrs=['bold', 'blink']))

if __name__ == "__main__":
    main()
