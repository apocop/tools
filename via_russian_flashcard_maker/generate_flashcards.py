# python3
"""Generate TSV for Anki Flash cards from Via Russian Conversation practice notes."""

import re

class Flashcard:
  "Flash Card Class"

  def __init__(self):
    self.line = None
    self.russian = None
    self.english = None
    self.date = None
    self.tutor = None
    self.junk = False
    self.header = None
    self.errors = []
    self.sides = []


  def fill_out(self, line, header):
    """Fill out a new flash card"""
    self.line = line
    self.header = header
    self.create_sides()
    self.generate_tags()

  def create_sides(self):

    self.sides = self.line.split('-')
    if len(self.sides) == 2:
      if normalizer.is_cyrillic(self.sides[0]) and normalizer.is_latin(self.sides[1]):
        self.russian = self.sides[0].strip()
        self.english = self.sides[1].strip()
      elif normalizer.is_cyrillic(self.sides[1]) and normalizer.is_latin(self.sides[0]):
        self.russian = self.sides[1].strip()
        self.english = self.sides[0].strip()
      else:
        self.junk = True
        self.errors.append("Can't separate English from Russian")
    elif len(self.sides) != 2:
      self.junk = True
      self.errors.append(f'Card needs 2 sides, but has {len(self.sides)}.')

  def generate_tags(self):
    if self.header:
      match = re.match(normalizer.lesson_header, self.header)
      if match:
        self.date = f"{match.group('month')} {match.group('day')},{match.group('year')}"
        self.tutor = match.group('tutor')
    else:
      self.errors.append('Card has no header')

class Generator:
  def __init__(self):
    self.card_deck = []
    self.junk_deck = []
    self.last_header = None

  def print_report(self):
    """Print a final report about the cards."""

    print('--- Flash Card Maker ---')
    print(f'Total number of cards created: {len(self.card_deck)}')
    print(f'Unused lines of text: {len(self.junk_deck)}')

  def cards_to_tsv(self, path):
    """Export valid flashcards to TSV"""
  
    flashcards = ''
    for card in self.card_deck:
      flashcards += f'{card.english}\t{card.russian}\ttags:{card.date} {card.tutor}\n'
    with open(path, 'w', encoding='utf-8') as f:
      f.write(flashcards)


  def generate_flashcards(self, path):
    with open(path, 'r', encoding='utf-8') as f:
      lines = [line for line in f.read().splitlines() if line.strip() != '']
    for line in lines:
      if normalizer.is_lesson_header(line):
        self.last_header = line
      else:
        card = Flashcard()
        card.fill_out(line, self.last_header)
        if card.junk:
          self.junk_deck.append(card)
        else:
          self.card_deck.append(card)

    self.print_report()
    self.print_junk_cards()

  
  def print_junk_cards(self):


    for junk in self.junk_deck:
      print(f'Line: "{junk.line}"')
      print(f'Russian: "{junk.russian}"')
      print(f'English: "{junk.english}"')
      print(f'Sides: {junk.sides}')
      print(f'Date: {junk.date}')
      print(f'Tutor: {junk.tutor}')
      print(f'Error: {junk.errors}\n')


class Normalizer():
  def __init__(self):
    self.cyrllic = '[а-яА-Я]'
    self.latin = '[a-zA-Z]'
    self.punctuation = r'[\+!?\.\s-]'
    self.lesson_header = r'(?P<day>[0-9]{,2})\s*(?P<month>[a-zA-Z]*)\s.*(?P<year>20[0-9]{,2})\s*(?P<tutor>[a-zA-Z]+)'

  def is_cyrillic(self, string):
    return bool(re.search(self.cyrllic, string))

  def is_latin(self, string):
    return bool(re.search(self.latin, string))

  def is_lesson_header(self, string):
    return bool(re.match(self.lesson_header, string))

  def normalize(self, string):
    pass


path = r'./via_russian_flashcard_maker/conversation.txt'
export_path = r'./via_russian_flashcard_maker/cards.tsv'
normalizer = Normalizer()
generator = Generator()
generator.generate_flashcards(path)
generator.cards_to_tsv(export_path)
