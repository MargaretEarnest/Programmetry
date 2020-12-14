#!/usr/bin/python

# Random Sentences reimplementation
# copyright (c) 2016 Nick Montfort <nickm@nickm.com>
# based on a 1961 program by Victor H. Yngve
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
#
# Updated 31 May 2018 to add compatibility with Python 3 (Python 2 still works)

"""Engineer Small has a little train.
The engine is black and shiny.
He keeps it oiled and polished.
Engineer Small is proud of his little engine.
The engine has a bell and a whistle.
It has a sand-dome.
It has a headlight and a smokestack.
It has four big driving wheels.
It has a firebox under its boiler.
When the water in the boiler is heated, it makes steam."""
import random
import time
from random import choice

# <distance-sentence> | <observation-sentence> | <env-sentence> | <gather-sentence> | <hug-sentence> | <dance-sentence> | <movement-sentence>
grammar = \
    """       <sentence> ::= <distance-sentence> | <observation-sentence> | <env-sentence> | <gather-sentence> | <hug-sentence> | <dance-sentence> | <movement-sentence>
     <distance-sentence> ::= " she" <distance-verb> " me with her" <beckoner>
  <observation-sentence> ::= " there is a" <adj-descriptor> <state-noun> " to her" <appearance-noun>
          <env-sentence> ::= " the" <env-noun> <env-verb> <env-prep>
       <gather-sentence> ::= " we" <gather-verb> <gather-prep> " and" <gather-activity>
         <distance-verb> ::= " reaches for" | " beckons to" | " stops" | " greets"
          <hug-sentence> ::= <hug-phrase> <object-pronoun> <hug-prep>
        <dance-sentence> ::= " we" <dance-phrase> " until" <dance-end>
     <movement-sentence> ::= <movement-phrase> " to" <object-pronoun>
             <body-part> ::= " hands" | " arms" | " eyes" | " face" | " heart" | " mouth"
       <appearance-noun> ::= " look" | " stare" | " eyes" | " stance" | " disposition" | " voice" | " appearance"
              <beckoner> ::= <body-part> | <appearance-noun>
        <adj-descriptor> ::= " familiar" | " certain" | " comforting" | " shifting" | " stable"
            <state-noun> ::= " intensity" | " love" | " calmness" | " radiance" | " peace" | " understanding"
              <env-noun> ::= " duststorm" | " wind" | " storm" | " snowstorm" | " fog" | " chaos" | " darkness" | " noise" | " rain" | " thunder"
              <env-verb> ::= " lessens" | " settles" | " grows" | " picks up" | " ceases" | " stops" | " explodes" | " continues"
        <object-pronoun> ::= " her" | " me" | " us"
       <subject-pronoun> ::= " she" | " I" | " we"
            <possessive> ::= " her" | " my" | " our"
              <env-prep> ::= " around" <object-pronoun> | " above" <object-pronoun> | " between us" | " in the distance" | " within" <object-pronoun>
           <gather-verb> ::= " dance" | " sit" | " stand" | " wait" | " rest" | " drift" | " walk" | " run"
           <gather-prep> ::= " under the stars" | " under the sun" | " under the moon" | " by the sea" | " in a forest" | " through a desert"
       <gather-activity> ::= " watch waves lap the shore" | " breathe in the night air" | " soak in heat" | " dance in the moonlight" | " sway with the breeze" | " laugh at birds" | " soak in the sea" | " wade through tall grass" 
              <hug-verb> ::= " take" | " hold" | " hug"
              <hug-prep> ::= " to" <object-pronoun> | " to" <possessive> " chest" | " in" <possessive> " arms" | " in" <possessive> " embrace"
            <hug-phrase> ::= " I" <hug-verb> | " we" <hug-verb> | " she" <hug-verb> "s" 
            <dance-verb> ::= " twirl" | " spin" | " step" | " whirl" | " sashay" | " circle" | " spiral" | " swing" | " slide"
          <dance-phrase> ::= <dance-verb> " and" <dance-verb> | <dance-verb> <dance-maybe> "," <dance-verb> ", and" <dance-verb> 
           <dance-maybe> ::= "," <dance-verb> <dance-maybe> | "" 
             <dance-end> ::= " we're exhausted" | " morning touches the sky" | " we spin out of control" | " the world stands still" | " everything dissolves" 
         <movement-verb> ::= " run" | " dash" | " come" | " walk"
       <movement-phrase> ::= " I" <movement-verb> | " she" <movement-verb> "s" | " we" <movement-verb> """

count = 0

lines = []
for line in grammar.split('\n'):
    lines.append(line.strip())

rule = {}
for line in lines:
    left_side, right_side = line.split(' ::= ')
    rule[left_side] = right_side.split(' | ')

for left_side in rule:
    new_right_side = []
    for option in rule[left_side]:
        tokens = []
        while len(option) > 0:
            target = '"'
            if option[0] == '<':
                target = '>'
            last = option.find(target, 1)
            tokens.append(option[0:last + 1])
            option = option[last + 1:].strip()
        new_right_side.append(tokens)
    rule[left_side] = new_right_side

original = __doc__.split('\n')


# Using these strings one can, for instance, check to see how long
# it takes to generate each of the original sentences. Nothing is done
# with them in the program as first released, however.

def expand(token):
    if token[0] == '"':
        return [token[1:-1]]
    else:
        right_side = rule[token]
        option = choice(right_side)
        if token == '<sentence>':
            rule['<sentence>'].remove(option)
        result = []
        for t in option:
            result = result + expand(t)
        return result

random.shuffle(rule['<sentence>'])
print("This Person does not Exist")
print()

while len(rule['<sentence>']) > 0:
    count = count + 1
    parts = expand('<sentence>')
    while '' in parts:
        parts.remove('')
    sentence = ''.join(parts) + '.'
    sentence = sentence[1].upper() + sentence[2:]
    print(sentence.replace("dashs", "dashes"))
    # time.sleep(3)
print("I feel known.")
