# python3
"""Generate TSV for Anki Flash cards from Via Russian Conversation practice notes.

Optional Flags:
leave_caps: Leave capitalization (Will format Proper Nouns).
"""

import re

class Flashcard:
  "Flash Card Class"

  def __init__(self):
    self.line = None
    self.russian = None
    self.english = None
    self.date = None
    self.tutor = None
    self.junk = None
    self.header = None
    self.errors = []

  
  def set_up(self, line, header):
    self.line = line
    self.header = header
    self.create_sides()



  def create_sides(self):

    sides = self.line.split('-')

    if len(sides) == 2:
      if normalizer.is_cyrillic(sides[0]) and normalizer.is_latin(sides[1]):
        self.russian = sides[0]
        self.english = sides[1]
      elif normalizer.is_cyrillic(sides[1]) and normalizer.is_latin(sides[0]):
        self.russian = sides[1]
        self.english = sides[0]
        
        print(self.russian, '; ', self.english)
      else:
        self.junk = True
        self.errors.append("Can't separate English from Russian")
    self.junk = True
    self.errors.append('Wrong number of sides')
  


class Generator:
  def __init__(self):
    self.card_deck = []


  def generate_flashcards(self, path):
    with open(path, 'r', encoding='utf-8') as f:

      lines = [line for line in f.read().splitlines() if line.strip() != '']
      for line in lines:
        if normalizer.is_lesson_header(line):
          header = line
        else:
          header = None

          card = Flashcard()
          card.set_up(line, header)
          self.card_deck.append(card)


      print(len(self.card_deck))



class Normalizer():
  def __init__(self):
    self.cyrllic = '[а-яА-Я]'
    self.latin = '[a-zA-Z]'
    self.punctuation = r'[\+!?\.\s-]'
    self.lesson_header = r'(?P<day>[0-9]{,2})\s.*(?P<month>[a-zA-Z])\s.*(?P<year>20[0-9]{,2})\s.*(?P<tutor>[a-zA-Z])'

  def is_cyrillic(self, string):
    return bool(re.search(self.cyrllic, string))

  def is_latin(self, string):
    return bool(re.search(self.latin, string))

  def is_lesson_header(self, string):
    return bool(re.match(self.lesson_header, string))



#path = r'C:\Users\Joel\Documents\GitHub\tools\via_russian_flashcard_maker\conversation.txt'
path = r'./via_russian_flashcard_maker/conversation.txt'

normalizer = Normalizer()
generator = Generator()
generator.generate_flashcards(path)
