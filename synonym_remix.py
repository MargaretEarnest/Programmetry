import random
import re
from PyDictionary import PyDictionary
import nltk
from pattern.en import conjugate, lemma, lexeme, PRESENT, SG, singularize, pluralize


# Capitalized elements in the title must be made lowercase if you want them to replaced with a synonym
inputText = """
poem goes here
poem continued"""

wordMap = []
synWordTypes = ["JJ", "JJR", "JJS", "NN", "NNS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
noEdit = ["be", "am", "is", "are", "was", "were", "being", "been", "not", "as", "then", "other"]

dictionary = PyDictionary()

# gets synonyms for the word passed in and attempts to format them to the correct tense or number
def getSynonyms(word, part):
    synonyms = []
    wordToTry = lemma(word) if part[0] == 'V' else word
    synList = dictionary.synonym(wordToTry)
    if synList is None:
        return [word]
    for syn in synList:
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


# Only run on first time running the program to avoid output every time
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

lines = []
splitLines = inputText.splitlines()

# for each like, replaces a word with a synonym if it is a fitting
# part of speech and it's not on the noEdit list and it has synonyms
for line in splitLines:
    text = nltk.word_tokenize(line)
    lines.append([])
    for token in nltk.pos_tag(text):
        if synWordTypes.count(token[1]) > 0 and noEdit.count(token[0].lower()) == 0 and getSynonyms(token[0], token[1]) != []:
            wordList = getSynonyms(token[0], token[1])
            random.shuffle(wordList)
            lines[-1].append(wordList[0])
        else:
            lines[-1].append(token[0])
    # prints out a progress tracker because this program takes forever to run sometimes
    print("Finished line " + str(len(lines) - 1) + "/" + str(len(splitLines) - 1) + "...")

# formates the lines list into text, handling most weird punctuation spacing
paragraph = ""
for line in lines:
    paragraph += re.sub(r'\s([’?.!,;:“”"](?:\s|$))', r'\1', " ".join(line).replace(" ,", ",")) + "\n"

# prints the poem / story
print("\n" + ("~" * 30))
print(paragraph)

