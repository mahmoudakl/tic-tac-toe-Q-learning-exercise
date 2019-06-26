import random
import numpy as np

from functools import reduce


class Game:

    def __init__(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.actions = self.get_free_spots()

    def print_board(self):
        print '    0   1   2\n'
        for i, row in enumerate(self.board):
            print '%i  ' % i,
            for item in row:
                print '%s  ' % item,
            print '\n'

    def reset(self):
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    def get_free_spots(self):
        free = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    free.append((i, j))

        return free

    def move(self, key, action=None, mode='agent'):
        if mode == 'random':
            free_spots = self.get_free_spots()
            action = random.choice(free_spots)
            self.board[action[0]][action[1]] = key
        else:
            row = action[0]
            col = action[1]
            self.board[row][col] = key

    def check_for_win(self, key):
        # Check Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == key:
            return True, self.board[0][0]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] == key:
            return True, self.board[0][2]

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == key:
                return True, self.board[i][0]
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] == key:
                return True, self.board[0][i]

        return False

    def check_for_draw(self):
        if any('-' in x for x in self.board):
            return False

        return True

    def get_state(self):
        flat_state = reduce(lambda x, y: x + y, self.board)
        return ''.join(flat_state)

    def play(self, mode='random'):
        player_turn = False if np.random.random() < 0.5 else True

        while True:
            self.print_board()
            if player_turn:
                move = input("Player's turn. Select a row and column in the format row,col:")
                try:
                    row, col = int(move[0]), int(move[1])
                except ValueError:
                    print "Invalid input"
                    continue

                if row not in range(3) or col not in range(3) or not self.board[row][col] == '-':
                    print "Invalid move"
                    continue

                player_turn = not player_turn
                self.board[row][col] = 'X'

            else:
                print "Opponent's turn."
                if mode == 'random':
                    self.move('O', mode='random')

                player_turn = not player_turn

            # Check if the game has ended
            if self.check_for_win('X'):
                self.print_board()
                print "Game Over. Human player won!!"
                break
            elif self.check_for_draw():
                self.print_board()
                print "Game Over. Draw!!"
                break
            elif self.check_for_win('O'):
                self.print_board()
                print "Game Over. Your opponent won"
                break
