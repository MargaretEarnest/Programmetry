import random
import re
import textwrap
from PyDictionary import PyDictionary
import nltk
from pattern.en import conjugate, lemma, lexeme, PRESENT, SG, singularize, pluralize

print("A fourth grader's first essay")
print()

# Note: capitalizing the first word will prevent it from generating synonyms due
# to restrictions on proper nouns
inputSentence = "A blessing in disguise. "
wordMap = dict()
synWordTypes = ["JJ", "JJR", "JJS", "NN", "NNS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

dictionary = PyDictionary()

# returns a unique list of synonyms for the given word, hopefully fomatted to the
# same tense or number as the original
def getSynonyms(word, part):
    synonyms = []
    wordToTry = lemma(word) if part[0] == 'V' else word
    synList = dictionary.synonym(wordToTry)
    if synList is None:
        return [word]
    for syn in synList:
        if " " not in syn:
            if part == "VB" or part == "VBP":
                synonyms.append(lemma(syn))
            elif part == "VBD" and len(lexeme(syn)) > 3:
                synonyms.append(lexeme(syn)[3])
            elif part == "VBG" and len(lexeme(syn)) > 0:
                synonyms.append(lexeme(syn)[0])
            elif part == "VBN" and len(lexeme(syn)) > 3:
                synonyms.append(lexeme(syn)[-1])
            elif part == "VBZ" and len(lexeme(syn)) > 1:
                synonyms.append(lexeme(syn)[1])
            elif part == "NN" and syn[-2:] != "ss":
                synonyms.append(singularize(syn))
            elif part == "NNS":
                synonyms.append(pluralize(syn))
            else:
                synonyms.append(syn)
    return list(set(synonyms))


# Only run on first time running the program to avoid output
# every time
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

# gets synonyms for each word
text = nltk.word_tokenize(inputSentence)
for token in nltk.pos_tag(text):
    if synWordTypes.count(token[1]) > 0:
        wordList = getSynonyms(token[0], token[1])
        random.shuffle(wordList)
        wordMap[token[0]] = wordList

# finds the word with the least synonyms out of those
# in appropriate parts of speech
smallest = None
for wordList in wordMap:
    if smallest is None or len(wordMap[wordList]) < len(smallest):
        smallest = wordMap[wordList]

# puts the paragraph back together choosing random synonyms for
# appropriate words
sentenceTemp = inputSentence.split(" ")
paragraph = inputSentence
for i in range(len(smallest)):
    sentence = ""
    for word in sentenceTemp:
        noPunc = re.sub(r'[^\w\s]', '', word)
        if noPunc in wordMap:
            sentence += wordMap[noPunc].pop() + " "
        else:
            sentence += word + " "
    paragraph += sentence.strip().capitalize() + ". "

print(textwrap.fill(paragraph, width=70))

