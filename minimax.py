import random, sys
from word_association import *

word_association = WordAssociation()

def minimax(blue_words, red_words, beige_words, black_words, turn):
    # this is some representation of the board that will be passed in. For now, I am just hard coding this
    if len(black_words) == 0:
        return [-sys.maxsize - 1, "", 0]
    if turn == "blue":
        if len(blue_words) == 0:
            return [sys.maxsize, "", 0]
        elif len(red_words) == 0:
            return [-sys.maxsize - 1, "", 0]
    if turn == "red":
        if len(red_words) == 0:
            return [sys.maxsize, "", 0]
        elif len(blue_words) == 0:
            return [-sys.maxsize - 1, "", 0]
    similar_words = {}
    word_colors = {}

    # For each word on the board, the following gets the most similar words to the board word
    for blue_word in blue_words:
        similar_words[blue_word] = word_association.ratings(blue_word, 0.05)
        word_colors[blue_word] = "blue"

    for red_word in red_words:
        similar_words[red_word] = word_association.ratings(red_word, 0.05)
        word_colors[red_word] = "red"

    for beige_word in beige_words:
        similar_words[beige_word] = word_association.ratings(beige_word, 0.05)
        word_colors[beige_word] = "beige"

    for black_word in black_words:
        similar_words[black_word] = word_association.ratings(black_word, 0.05)
        word_colors[black_word] = "black"
    
    # for key in similar_words:
    #    print(key, " (", word_colors[key], "): ", similar_words[key])

    # Dictionary to hold the usability score of each of the potential clues
    clue_scores = {}
    # Dictionary to hold the words this clue is associated with
    clue_use_cases = {}
    # Dictionary to hold the number of board words this would check off for the user
    clue_positive_uses = {}

    for board_word in word_colors:
        if word_colors[board_word] == turn:
            for clue in similar_words[board_word]:
                clue_scores[clue] = clue_scores.get(clue, 0) + 3 * similarity(clue, board_word)
                clue_positive_uses[clue] = clue_positive_uses.get(clue, 0) + 1
                if clue not in clue_use_cases:
                    clue_use_cases[clue] = []
                clue_use_cases[clue].append([board_word, similarity(clue, board_word)])
        elif word_colors[board_word] == "beige":
            for clue in similar_words[board_word]:
                clue_scores[clue] = clue_scores.get(clue, 0) - 1 * similarity(clue, board_word)
                if clue not in clue_use_cases:
                    clue_use_cases[clue] = []
                clue_use_cases[clue].append([board_word, similarity(clue, board_word)])
        elif word_colors[board_word] == "black":
            for clue in similar_words[board_word]:
                clue_scores[clue] = clue_scores.get(clue, 0) - 100 * similarity(clue, board_word)
                if clue not in clue_use_cases:
                    clue_use_cases[clue] = []
                clue_use_cases[clue].append([board_word, similarity(clue, board_word)])
        else:
            for clue in similar_words[board_word]:
                clue_scores[clue] = clue_scores.get(clue, 0) - 3 * similarity(clue, board_word)
                if clue not in clue_use_cases:
                    clue_use_cases[clue] = []
                clue_use_cases[clue].append([board_word, similarity(clue, board_word)])
    #print("clue scores:")
    #for key in clue_scores:
    #    print(key, ": ", clue_scores[key])
    
    #print("clue use cases:")
    #for key in clue_use_cases:
    #    print(key, ": ", clue_use_cases[key])

    #print("clue scores:")
    for key in clue_scores:
        if key in clue_positive_uses:
            clue_scores[key] = clue_scores[key] * clue_positive_uses[key]
        else:
            clue_scores[key] = -1000
        #print(key, ": ", clue_scores[key])

    #print("sorted:")
    sorted_dict = dict(sorted(clue_scores.items(), key=lambda item: item[1], reverse=True)[:5])
    #for key in sorted_dict:
    #    print(key, ": ", sorted_dict[key])

    best_clue = ""
    best_clue_num = 0
    score = sys.maxsize
    for clue in sorted_dict:
        if sorted_dict[clue] <= 0:
            break
        target_number = clue_positive_uses[clue]
        sorted_associations = sorted(clue_use_cases[clue], key=lambda x: x[1], reverse=True)
        #print(sorted_associations)
        new_red = red_words[:]
        new_beige = beige_words[:]
        new_blue = blue_words[:]
        new_black = black_words[:]
        #print(blue_words)
        #print(red_words)
        #print(beige_words)
        #print(black_words) 
        # Looping through the words associated with a clue
        for i in range(len(sorted_associations)):
            if word_colors[sorted_associations[i][0]] == turn:
                if word_colors[sorted_associations[i][0]] == "blue":
                    new_blue.remove(sorted_associations[i][0])
                else:
                    new_red.remove(sorted_associations[i][0])
            else:
                if word_colors[sorted_associations[i][0]] == "blue":
                    new_blue.remove(sorted_associations[i][0])
                elif word_colors[sorted_associations[i][0]] == "red":
                    new_red.remove(sorted_associations[i][0])
                elif word_colors[sorted_associations[i][0]] == "beige":
                    new_beige.remove(sorted_associations[i][0])
                elif word_colors[sorted_associations[i][0]] == "black":
                    new_black.remove(sorted_associations[i][0])
                break
        #print("CLUE IS: ", clue)
        #print(new_blue)
        #print(new_red)
        #print(new_beige)
        #print(new_black)
        # recursed output is going to give you the best score for the other player
        if turn == "red":
            turn = "blue"
        else:
            turn = "red"
        recursed_output = minimax(new_blue, new_red, new_beige, new_black, turn)
        if score > recursed_output[0]:
            score = recursed_output[0]
            best_clue = clue
            best_clue_num = clue_positive_uses[clue]
        return [score, best_clue, best_clue_num]

def main():
    blue_words = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    red_words = ["j", "k", "l", "m", "n", "o", "p", "q"]
    beige_words = ["r", "s", "t", "u", "v", "w", "x"]
    black_words = ["y"]
    turn = "blue"
    maxing = True
    output = minimax(blue_words, red_words, beige_words, black_words, turn)
    print("OUTPUT IS: ", output)

if __name__ == "__main__":
    main()