import random
import tkinter as tk
from collections import defaultdict

class Codenames:
    def __init__(self):
        self.total_cards = []
        self.cards_left = {}
        self.turn = 'blue'
        self.triesLeft = 3 # TODO: don't hardcode this
        self.generate_board()
        self.call_AI()

    def generate_board_words(self):
        with open("wordbank.txt") as file:
            word_bank = file.read().splitlines()
        words = random.sample(word_bank, 25)

        # Blue will always go first, which puts red at a disadvantage, which is why there is 1 less card for red
        word_colors = 9 * ['blue'] + 8 * ['red'] + 7 * ['beige'] + ['black']
        random.shuffle(word_colors)

        return list(zip(words, word_colors))

    def group_words_by_color(self, board_words):
        grouped_words = defaultdict(list)
        for word, color in board_words:
            grouped_words[color].append(word)
        return grouped_words

    def disable_board(self):
        for x in range(5):
            for y in range(5):
                self.total_cards[x][y].button.configure(state=tk.DISABLED)

    def check_results(self, color, word):
        self.cards_left[color].remove(word)

        # Check if they selected the assassin word
        if color == 'black':
            if self.turn == 'blue':
                self.display_winner('red')
            else:
                self.display_winner('blue')

        # Check if they've found all of their words
        elif len(self.cards_left['blue']) == 0:
            self.display_winner('blue')
        elif len(self.cards_left['red']) == 0:
            self.display_winner('red')
        # Check if their turn should end
        elif color != self.turn or self.triesLeft == 0:
            if self.turn == 'blue':
                self.turn = 'red'
                self.title.config(text="Red's turn!", fg='red')
            else:
                self.turn = 'blue'
                self.title.config(text="Blue's turn!", fg='blue')
            self.call_AI()

        else:
            self.triesLeft-=1

    def display_winner(self, winning_color):
        self.disable_board()
        self.title.config(text=winning_color.capitalize() + " wins!", fg=winning_color)

    def build_gui(self, board_words):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Codenames")
        self.play_area = tk.Frame(self.root, width=300, height=300, bg='white')
        self.play_area.pack(pady=(100, 10), padx=10)

        self.title = tk.Label(self.root, text="Blue's turn!", font=('Arial', 25), bg='white', fg='blue')
        self.title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        class Card:
            def __init__(self, x, y, counter, play_area, check_results):
                self.x = x
                self.y = y
                self.play_area = play_area
                self.check_results = check_results
                self.word = board_words[counter][0]
                self.color = board_words[counter][1]
                self.button = tk.Button(self.play_area, text=self.word, width=20, height=5, command=self.reveal_color)
                self.button.grid(row=x, column=y)
                self.revealed = False

            def reveal_color(self):
                if not self.revealed:
                    self.button.configure(highlightbackground=self.color)
                    self.revealed = True
                    self.check_results(self.color, self.word)

        total_iterations = 0
        for x in range(5):
            row_cards = []
            for y in range(5):
                new_card = Card(x, y, total_iterations, self.play_area, self.check_results)
                row_cards.append(new_card)
                total_iterations+=1
            self.total_cards.append(row_cards)

    def generate_board(self):
        board_words = self.generate_board_words()
        self.cards_left = self.group_words_by_color(board_words)
        print(self.cards_left)
        self.build_gui(board_words)
        self.root.mainloop()

    def call_AI(self):
        # TODO: call AI to retrieve clue for self.turn + number of words relevant to that clue
        # set triesLeft equal to that number
        # display all of this info above the board
        return
if __name__ == '__main__':
    Codenames()
