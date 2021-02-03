# python3
"""Generate TSV for Anki Flash cards from Via Russian Conversation practice notes.

Optional Flags:
leave_caps: Leave capitalization (Will format).
"""

import re

class Flashcard:
  "Flash Card Class"

  def __init__(self, line, header):
    self.line = line
    self.Russian = None
    self.English = None
    self.date = None
    self.tutor = None
    self.junk = None
    self.header = header

  
  def set_up(self):
    pass


class Generator:
  def __init__(self):
    self.normalizer = Normalizer()
    self.card_deck = []


  def generate_flashcards(self, path):
    with open(path, 'r', encoding='utf-8') as f:
      lines = [line for line in f.read().splitlines() if line != '']
      for line in lines:
        if self.normalizer.is_lesson_header(line):
          header = line
        else:
          header = None
        header = line
        card = Flashcard(line, header)
        self.card_deck.append(card)


      print(len(self.card_deck))


class Normalizer():
  def __init__(self):
    self.cyrllic = '[а-яА-Я]'
    self.latin = '[a-zA-Z]'
    self.punctuation = r'[\+!?\.\s-]'
    self.lesson_header = r'(?P<day>[0-9]{,2})\s.*(?P<month>[a-zA-Z])\s.*(?P<year>20[0-9]{,2})\s.*(?P<tutor>[a-zA-Z])'

  def is_cyrillic(self, string):
    return bool(re.search('[а-яА-Я]', string))

  def is_latin(self, string):
    return bool(re.search('[a-ZA-Z]', string))

  def is_lesson_header(self, string):
    return bool(re.match(self.lesson_header, string))



path = r'C:\Users\Joel\Documents\GitHub\tools\via_russian_flashcard_maker\conversation.txt'

generator = Generator()
generator.generate_flashcards(path)
