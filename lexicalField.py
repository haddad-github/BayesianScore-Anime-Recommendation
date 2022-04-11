import requests
import csv
from pattern3.text.en import pluralize

#Scrape all related words to the given word
def scrape(word):
    url = 'https://relatedwords.org/api/related'
    payload = {'term':word}
    jsonData = requests.get(url, params=payload).json()
    if not jsonData:
        raise Exception("The word you're looking for cannot be found")
    else:
        return jsonData

#Make a word plural
def makePlural(word):
    return pluralize(word)

#Generate a lexical field of the 5 top related words to the given word (including their plural form)
def generateLexicon(word):
    word = word.lower()

    jsonData = scrape(word)

    wordLexicalField = [word, makePlural(word)]
    for i in range(5):
        try:
            wordLexicalField.append(jsonData[i]['word'])
            wordLexicalField.append(makePlural(jsonData[i]['word']))
        except:
            raise Exception("Word has too little related words")
            break

    return wordLexicalField