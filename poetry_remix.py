import random
from curses.ascii import isalpha

import spacy

# The poem to be remixed
poem = """
"""

wordPool = dict()
lines = str.splitlines(poem)
structure = []
# Parts of speech placed in this array will be shuffled around, so with "NOUN"
# here, only nouns will be shuffled
mixable = []

# All part of speech options: ["ADJ", "ADP", "ADV", "AUX", "CONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB"]

# Descent
# fullMixable = ["ADJ", "ADP", "ADV", "AUX", "CONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "SCONJ", "SYM", "VERB"]
# random.shuffle(fullMixable)
# skip = len(lines) // len(fullMixable) + 1

# Adds words to the word pool by part of speech
def addWordToPool(newWord, newPart):
    if list(wordPool.keys()).count(newPart) == 0:
        wordPool[newPart] = [newWord]
    else:
        wordPool[newPart].append(newWord)


if __name__ == '__main__':
    nlp = spacy.load("en_core_web_sm")

    docs = []

    # Handles contractions by merging contraction parts with original word
    for line in lines:
        doc = nlp(line)
        t = 0
        while t < len(doc):
            token = doc[t]
            if "’" in token.text:
                with doc.retokenize() as retokenizer:
                    attrs = {"POS": doc[token.i - 1].pos_}
                    retokenizer.merge(doc[(token.i - 1):(token.i + 1)], attrs)
            t += 1
        docs.append(doc)

    i = 0
    # Defines the poem structure by putting words into the structure array bit by bit and adding mixable word types
    # to their respective word pools
    for line in lines:
        doc = docs[i]
        i += 1
        # Descent
        # if i % skip == 0:
        #     mixable.append(fullMixable.pop())
        parts = []
        if len(line) > 0:
            for token in doc:
                if mixable.count(token.pos_) > 0:
                    parts.append([token.pos_, token.text[0].isupper()])
                    addWordToPool(token.text.lower(), token.pos_)
                else:
                    parts.append([token.text, None])
        structure.append(parts)

    # Word pools are shuffled to mix up mixable words
    for part in wordPool:
        random.shuffle(wordPool[part])

    # Words are re-inserted into the poem structure, with non-mixable words retaining their order and mixable
    # words being taken out of their respective word pools
    for line in structure:
        newLine = ""
        for part in line:
            if not part[1] is None:
                word = wordPool[part[0]].pop()
                if part[1]:
                    word = word.capitalize()
                newLine += " " + word
            else:
                newLine += (" " if isalpha(part[0][0]) else "") + part[0]
        print(newLine.strip())
