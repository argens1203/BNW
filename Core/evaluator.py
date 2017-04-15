from keras.models import load_model
import numpy as np
from othello import State

size = 8
minimum = -100
maximum = 100
neutral = 0

class Evaluator ():

    def __init__ (self, valueNN, border = "False", corner = "False", liberty = "False"):
        self.valueNN = load_model (valueNN)
        self.border = border
        self.corner = corner
        self.liberty = liberty
        return

    def evaluate (self, state, player):
        
        if state.player == 0:
            score = player * (state.bc - state.wc)
            if score > 0:
                return maximum
            if score == 0:
                return neutral
            if score < 0:
                return minimum

        NN = []
        NN.append (self.convertToNN (state.mirrored (), player))
        X = np.asarray (NN)
        value = self.valueNN.predict (X)
        return value [0][0]

    def convertToNN (self, board, player):
        input_NN = []
        white = []
        black = []
        empty = []

        if self.border or self.corner:
            border = []

        if self.liberty:
            moves = []

        for i in range (size):
            row_white = []
            row_black = []
            row_empty = []

            if self.border or self.corner:
                row_border = []

            if self.liberty:
                row_total = []

            for j in range (size):

                if self.border == True:
                    if i == 0 or j == 0 or i == size-1 or j == size-1:
                        row_border.append (1)
                    else:
                        row_border.append (0)
                else:
                    if self.corner == True:
                        row_border.append (0)

                piece = board [i][j] * player
                if piece == 0:
                    row_empty.append (1)
                    row_black.append (0)
                    row_white.append (0)
                    if self.liberty:
                        row_total.append (0)
                else:
                    if piece == 1:
                        row_empty.append (0)
                        row_black.append (1)
                        row_white.append (0)
                        if self.liberty:
                            row_total.append (1)
                    else:
                        row_empty.append (0)
                        row_black.append (0)
                        row_white.append (1)
                        if self.liberty:
                            row_total.append (-1)

            empty.append (row_empty)
            white.append (row_white)
            black.append (row_black)

            if self.border or self.corner:
                border.append (row_border)
            if self.liberty:
                moves.append (row_total)

        if self.corner:
            border [0][0] = border [0][size - 1] = border [size - 1][0] = border [size - 1][size - 1] = 4
            border [0][1] = border [1][0] =  border [1][1] = -1
            border [0][size - 2] = border [1][size - 1] =  border [1][size - 2] = -1
            border [size - 2][0] = border [size - 1][1] =  border [size - 2][1] = -1
            border [size - 2][size - 1] = border [size - 1][size - 2] = border [size - 1][size - 1] =  -1

        e = np.asarray (empty)
        w = np.asarray (white)
        bl = np.asarray (black)

        input_NN.append (e)
        input_NN.append (w)
        input_NN.append (bl)

        if self.border or self.corner:
            bd = np.asarray (border)
            input_NN.append (bd)
        
        if self.liberty:
            state = State (board = moves)
            for i in range (size):
                for j in range (size):
                    moves [i][j] = 0

            for (x, y, _) in state.validMoves:
                moves [x][y] = 1

            mv = np.asarray (moves)
            input_NN.append (mv)

        # print ("e", e.shape)
        # print ("w", w.shape)
        # print ("bl", bl.shape)

        # b = np.asarray (board)
        # print ("b.shape", b.shape)
        return input_NN