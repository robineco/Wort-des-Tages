from requests.exceptions import ConnectionError
from termcolor import colored
from bs4 import BeautifulSoup
import requests

len_of_longest_text = 5


def create_frequency(full, empty):
    word_frequency = ''
    for _ in range(full):
            word_frequency += '▮'
        
    for _ in range(empty):
        word_frequency += '▯'
    
    return word_frequency


def update_longest_text(text):
    global len_of_longest_text
    if len(text) > len_of_longest_text:
        len_of_longest_text = len(text)


def print_seperator():
    minus = ''
    for _ in range(16 + len_of_longest_text):
        minus += '-'
    print(colored(minus, 'yellow'))


def main():
    try:
        baseurl = 'https://www.duden.de'
        word_of_the_day_url = '/wort-des-tages'

        response = requests.get(baseurl + word_of_the_day_url)

        soup = BeautifulSoup(response.text, "html.parser")

        block = soup.find(id='block-wordoftheday').find('a').attrs['href']
        word_url = baseurl + block

        response = requests.get(word_url, "html.parser")
        soup = BeautifulSoup(response.text, "html.parser")

        
        word = soup.find("span", {"class": "lemma__main"}).text
        word = word.replace('\u00AD', '')
        update_longest_text(word)

        wordfrequency = ''
        try:
            full = len(soup.find("span", {"class": "shaft__full"}).text)
            empty = len(soup.find("span", {"class": "shaft__empty"}).text)
            wordfrequency = create_frequency(full, empty)
        except AttributeError:
            wordfrequency = 'nicht verfügbar'
        
        spelling = ''
        try:
            spelling = soup.find(id='rechtschreibung').find('dd').text
        except AttributeError:
            spelling = 'nicht verfügbar'
        update_longest_text(spelling)

        meaning = ''
        try:
            meaning = soup.find(id='bedeutung').find('p').text
        except AttributeError:
            meaning = 'nicht verfügbar'
        update_longest_text(meaning)

        origin = ''
        try:
            origin = soup.find(id='herkunft').find('p').text
        except AttributeError:
            origin = 'nicht verfügbar'
        update_longest_text(origin)

        print_seperator()
        print(colored('Wort des Tages: ', 'green') + colored(word, 'cyan'))
        print(colored('Häufigkeit:     ', 'green') + colored(wordfrequency, 'cyan'))
        print(colored('Worttrennung:   ', 'green') + colored(spelling, 'cyan'))
        print(colored('Bedeutung:      ', 'green') + colored(meaning, 'cyan'))
        print(colored('Herkunft:       ', 'green') + colored(origin, 'cyan'))
        print_seperator()

    except ConnectionError:
        print(colored('No Internet Connection', 'red', attrs=['bold', 'blink']))

if __name__ == "__main__":
    main()
