#!/usr/bin/env python3
"""Hangman game """

import random
import sys
import unidecode

DEFAULT_SIZE = 5
DEFAULT_TRIES = 5

class Words:
    def __init__(self, filename='noun.csv', size=None):
        # Initialize Words object with optional filename and size parameters
        
        self.size = size

        with open('noun.csv', 'r', encoding='utf-8') as fp:
            lines = fp.readlines()

        lines.pop()  # Remove header
        lines = [row.split(',')[0] for row in lines]  # Take the first column of the list
        lines = [unidecode.unidecode(word) for word in lines]  # Remove all accents

        lines = list(filter(lambda x: len(x) == size, lines))

        if not lines:
            print('No words of specified length found.')
            quit()

        lines = [line.upper() for line in lines if line.isalpha()]
        self.words = lines


    def __next__(self):
        # Return a random word from the list of words
        return random.choice(self.words)

    def __iter__(self):
        # Return the iterator object
        return self

class Hangman:
    def __init__(self, word, tries):
        # Initialize Hangman object with word and tries parameters
        
        self.word = word
        self.tries = tries
        self.guessed_letters = []
    
    def guess(self, char):
        # Guess a letter in the word
        
        # Validate input
        while not char.isalpha() or len(char) > 1:
            print('Please enter only one letter!')
            char = input('> ').upper()

        # Decrease tries if the guessed letter is not in the word
        if char not in self.word:
            self.tries -= 1
        else:
            # Add the guessed letter to the list of guessed letters
            self.guessed_letters.append(char.upper())

        return self.tries
    
    def get_word(self):
        # Return the current status of the word with guessed letters revealed
        
        return tuple(c if c in self.guessed_letters else '_' for c in self.word)
    
    def get_status(self): 
        # Return the status of the game
        
        if self.tries == 0:
            print('Game over. The word was:', self.word)
            return 'lost'
        elif all(c in self.guessed_letters for c in self.word):
            print(' '.join(self.word))
            print('Congratulations! You won.')
            return 'won'
        else:
            return 'ongoing'

def read_arguments():
    # Read command line arguments using sys.argv
    
    tries = DEFAULT_TRIES
    word_length = DEFAULT_SIZE

    if len(sys.argv) > 1:
        try:
            tries = int(sys.argv[1])
        except ValueError:
            print("Invalid value for number of tries. Using default value.")

    if len(sys.argv) > 2:
        try:
            word_length = int(sys.argv[2])
        except ValueError:
            print("Invalid value for word length. Using default value.")

    return tries, word_length

if __name__ == '__main__':
    tries, word_length = read_arguments()

    words = Words(size=word_length)

    continue_game = 'y'

while continue_game == 'y':
    hangman = Hangman(next(words), tries)

    while hangman.get_status() == 'ongoing':
        print(' '.join(hangman.get_word()))
        char = input('> ')
        tries_left = hangman.guess(char.upper())
        print(f'Tries left: {tries_left}')

    print('Would you like to play again? (y/n)')

    continue_game = input('> ').lower()
    while continue_game not in ('y', 'n'):
        print('Would you like to play again? (y/n)')
        continue_game = input('> ').lower()