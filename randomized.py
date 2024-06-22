import random
from word_association import *

word_association = WordAssociation()

top_clues = 3
epsilon = 0.001
e = 3 # Engineers be like:

class Board:
    def __init__(self, words, turn, clue_words=None):
        self.remaining_words = words.copy()
        self.turn = turn
        # TODO clue history as to avoid giving the same clue twice

        if clue_words is not None:
            self.clue_words = clue_words
        else:
            self.clue_words = set()
            for word in self.remaining_words:
                self.clue_words |= set(word_association.ratings(word[0], epsilon))

    def clue_quality(self, clue):
        word_associations = []
        for word in self.remaining_words:
            word_associations.append(word + (word_association.similarity(word[0], clue[0]),))
        word_associations = sorted(word_associations, key=lambda x: x[2], reverse=True)

        for word in word_associations[:clue[1]]:
            if word[1] != self.turn or word[2] == 0:
                return 0
        return word_associations[clue[1] - 1][2] * clue[1] # TODO better score

    def clue_candidates(self):
        clues = []
        for clue_word in self.clue_words:
            for i in range(1, min(10, len(self.remaining_words))):
                quality = self.clue_quality((clue_word, i))
                if quality > 0:
                    clues.append((clue_word, i, quality))
                else:
                    break
        return sorted(clues, key=lambda x: x[2], reverse=True)[:top_clues]

    def pick_clue(self, clue_candidates):
        return random.choices(clue_candidates, weights=[clue[2] for clue in clue_candidates])[0]

    def count_color_words(self, color):
        c = 0
        for word in self.remaining_words:
            if word[1] == color:
                c += 1
        return c

    def play_word(self, board_word):
        for i, word in enumerate(self.remaining_words):
            if word[0] == board_word:
                del self.remaining_words[i]
                if word[1] == 'black':
                    return 'blue' if self.turn == 'red' else 'red'
                elif word[1] == 'beige':
                    self.turn = 'blue' if self.turn == 'red' else 'red'
                    return 'skip'
                elif self.count_color_words('red') == 0:
                    return 'red'
                elif self.count_color_words('blue') == 0:
                    return 'blue'
                elif word[1] != self.turn:
                    self.turn = 'blue' if self.turn == 'red' else 'red'
                    return 'skip'
                break
        return None # Indicates that more guesses can be made

    def pick_board_word(self, clue):
        word_associations = []
        for word in self.remaining_words:
            word_associations.append(word_association.similarity(word[0], clue[0]))
        return random.choices(self.remaining_words, weights=[weight ** e for weight in word_associations])[0][0]

    def simulate_field_operative(self, clue):
        board_word = self.pick_board_word(clue)
        result = self.play_word(board_word)
        if result == 'skip':
            return None
        elif result is None:
            if clue[1] == 1:
                self.turn = 'blue' if self.turn == 'red' else 'red'
                return None
            return self.simulate_field_operative((clue[0], clue[1] - 1))
        else:
            return result

    def simulate_turn(self):
        clue_candidates = self.clue_candidates()
        clue = self.pick_clue(clue_candidates)
        return self.simulate_field_operative(clue)

    def simulate_game(self, first_clue=None):
        result = self.simulate_field_operative(first_clue) if first_clue is not None else None
        while result is None:
            result = self.simulate_turn()
            print(result)
        return result

    def clue_win_rate(self, clue, samples=20):
        wins = 0
        for _ in range(samples):
            self_copy = Board(self.remaining_words, self.turn, self.clue_words)
            result = self_copy.simulate_game(clue)
            if result == self.turn:
                wins += 1
        return wins / samples

    def best_clue(self):
        clue_candidates = self.clue_candidates()
        print(clue_candidates)
        clue_win_rates = [self.clue_win_rate(clue) for clue in clue_candidates]
        max_win_rate = -1
        max_index = -1
        for i, win_rate in enumerate(clue_win_rates):
            if win_rate > max_win_rate:
                max_win_rate = win_rate
                max_index = i
        return clue_candidates[max_index]

with open("wordbank.txt") as file:
    word_bank = file.read().splitlines()
random.seed(12341234)
words = random.sample(word_bank, 25)
words = [word.lower() for word in words]
# Blue will always go first, which puts red at a disadvantage, which is why there is 1 less card for red
word_colors = 9 * ['blue'] + 8 * ['red'] + 7 * ['beige'] + ['black']
random.shuffle(word_colors)
board = Board(list(zip(words, word_colors)), 'red')
print(board.remaining_words)
print(board.best_clue())
