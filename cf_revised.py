import itertools
import copy
from collections import defaultdict
from pprint import pprint
import random
#import strats as s
        
'''this file contains the board class, whose methods will be called in the strategies file cf_strats_redone. you can also
play a two-player, human vs. human game in this file.'''

## add weights to the no-gos in the utility estimator
## make it so that the first open three in a given column is weighted higher

class Board(object):
    def __init__(self, player1, player2, height=6, width=7):
        self.arr = [[0 for i in range(7)] for j in range(6)]
        self.open_cols = range(7)
        self.moves = []
        self.moves_dict = defaultdict(int)
        self.player1 = player1
        self.player2 = player2
        self.height = height
        self.width = width
        self.available_fours_all = self.build_available_four_strings_all()
        self.available_fours_no_columns = self.build_available_four_strings_no_columns()

    def build_available_four_strings_no_columns(self):
        '''a list. each entry is a list of four indices making a possible connect four'''
        fours = []
        ## rows
        for row in range(self.height):
            for col in range(self.width - 3):
                fours.append([(row, col+i) for i in range(4)])
        # ## columns
        # for row in range(self.height - 3):
        #     for col in range(self.width):
        #         fours.append([(row+i, col) for i in range(4)])
        ## nw diagonals
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                fours.append([(row+i, col+i) for i in range(4)])
        ## ne diagonals
        for row in range(self.height - 3, self.height):
            for col in range(self.width - 3):
                fours.append([(row-i, col+i) for i in range(4)])
        assert len(fours) == 69 - 21
        return fours

    def build_available_four_strings_all(self):
        fours = self.build_available_four_strings_no_columns()
        ## add columns
        for row in range(self.height - 3):
            for col in range(self.width):
                fours.append([(row+i, col) for i in range(4)])
        assert len(fours) == 69
        return fours


    def opposite_player(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def numMoves(self):
        total = 0
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j] != 0:
                    total += 1

        return total

    def available_fours_at(self, index):
        return [line for line in self.available_fours_all if index in line]

    def available_fours_at_index_for_player(self,player,index):
        l = []
        for line in self.available_fours_at(index):
                four_list = (self.arr[i][j] for i, j in line)
                s = list(set(four_list))
                s.sort()
                if s == [0,player]:
                    l.append((line))
        l2 = []
        for item in l:
            item = tuple(item)
            l2.append(item)
        return l2
            
    def check_four_alternate(self,player):
        '''checks the board for four in a row for the given player'''
        for entry in self.available_fours_all:
            four_list = [self.arr[i][j] for i, j in entry]
            s = set(four_list)
            if len(s) == 1 and s.pop() == player:
                    return True
        return False

    def check_open_three(self,player):
        '''a list of open threes for the given player. each element of the list is the list of four indices
        corresponding to the available three'''
        l = []
        for entry in self.available_fours_all:
            four_list = [self.arr[i][j] for i, j in entry]
            if four_list.count(player) == 3 and four_list.count(0) == 1:
                l.append(entry)
        return l


    def check_open_three_nonvertical(self,player):
        '''a list of open threes, not including verticals, since they're useless'''
        l = self.check_open_three(player)
        list_items_to_remove = []
        for item in l:
            if item[0][1] == item[1][1]:
                list_items_to_remove.append(item)
        if len(list_items_to_remove) > 0:
            for item in list_items_to_remove:
                l.remove(item)
        return l

    def threats(self,player):
        '''returns a list of indices of threat squares l is a list, each element is a single tuple
        and the tuple entry is column first, then row counting from top'''
        l1 = []
        l2 = self.check_open_three_nonvertical(player)
        for l in l2:
            for tup in l:
                if self.arr[tup[0]][tup[1]] == 0:
                    l1.append((tup[1],tup[0]))
        l = []
        for i in range(len(l1)-1):
            for j in range(i+1,len(l1)):
                if l1[i] == l1[j]:
                    l.append(l1[i])
        for tup in l:
            if tup in l1:
                l1.remove(tup)
        l1.sort()
        return l1


    def foursUtility(self, player1, player2):
        self.blackout(player1, player2)
        availableFoursMovingPlayer = self.check_total_possible_fours(player1)
        self.unblackout()
        return len(availableFoursMovingPlayer)

    def controlCol(self, col, player1, player2):
        '''if player1 controls the column with the lowest threat in the column, the column number gets returned. else, returns nothing'''
        threatsPlayer1 = self.threats(player1)
        threatsPlayer2 = self.threats(player2)
        threatColsPlayer1 = [tup[0] for tup in threatsPlayer1]
        threatColsPlayer2 = [tup[0] for tup in threatsPlayer2]

        if col in threatColsPlayer1:
            if col in threatColsPlayer2:
                threat1 = threatsPlayer1[threatColsPlayer1.index(col)][1]
                threat2 = threatsPlayer2[threatColsPlayer2.index(col)][1]
                if threat1 == max(threat1, threat2):
                    return col
            else:

                return col

    def numberColsControlled(self, player1, player2):
        '''returns number of cols controlled by player1'''
        total = 0
        for col in range(7):
            if self.controlCol(col, player1, player2):
                total += 1

        return total

    def blackout(self, player1, player2):
        '''blackout squares odd number above opponent's threats. TODO'''
        for threat in self.threats(player2):
            if threat[1] > 0:
                #print threat
                self.arr[threat[1] - 1][threat[0]] = 3

    def unblackout(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j] == 3:
                    self.arr[i][j] = 0

    def usefulThreats(self, player1, player2):
        self.blackout(player1, player2)
        threats = self.threats(player1)
        self.unblackout()

    def oddControllingThreats(self, player1, player2):
        oddThreats = []
        for threat in self.threats(player1):
            if self.controlCol(threat[0], player1, player2) and threat[1] % 2 == 1:
                oddThreats.append(threat[0])
        return list(set(oddThreats))

    def evenControllingThreats(self, player1, player2):
        evenThreats = []
        for threat in self.threats(player1):
            if self.controlCol(threat[0], player1, player2) and threat[1] % 2 == 0:
                evenThreats.append(threat[0])
        return list(set(evenThreats))

    def numberEvenControllingThreats(self, player1, player2):
        return len(self.evenControllingThreats(player1, player2))

    def numberOddControllingThreats(self, player1, player2):
        return len(self.oddControllingThreats(player1, player2))

    def numberTotalControllingThreats(self, player1, player2):
        return self.numberEvenControllingThreats(player1, player2) + self.numberOddControllingThreats(player1, player2)

    def controlEnd(self, player1, player2):
        '''for this function, the order matters. player1 has to be the player who moved first, unlike the other functions.
        returns 1 if player1 controls, -1 if player2 controls'''
        even = self.numberEvenControllingThreats(player2, player1)
        odd = self.numberOddControllingThreats(player1, player2)
        if odd >= even and odd > 0:
            return 1
        elif even > odd:
            return -1
        else:
            return 0

    def stacked_threats(self,player1,player2):
        '''gives a list of columns with stacked open threes'''
        l = self.threats(player1)
        l2 = self.threats(player2)
        stacks = []
        for i in range(len(l)-1):
            ## same column, zeroth index (remember they're reversed), row index one different
            if l[i][0] == l[i+1][0] and l[i][1]+1 == l[i+1][1]:
                not_a_valuable_stack = 0
                for j in range((l[i][1]+1),5):
                    if (l[i][0],j) in l2:
                        not_a_valuable_stack += 1
                if not_a_valuable_stack == 0:
                    stacks.append([l[i],l[i+1]])
        return stacks

    def check_total_possible_fours(self,player):
        '''this returns tuple with row index first, counting from top'''
        total = []
        for row in range(self.height):
            for col in range(self.width):
                if self.arr[row][col] == player:
                    total += self.available_fours_at_index_for_player(player,(row,col))
        l = list(set(total))
        #print l
        return l


    def opencols(self):
        open_cols = []
        for col in range(7):
            full_column = all([self.arr[row][col] for row in range(self.height)])
            if not full_column:
                open_cols.append(col)
        return open_cols

    def add_move(self,col,player,toPrint=False):
        '''adds a move to the board for the given player in the given column'''
        col = int(col)
        full_column = all([self.arr[row][col] for row in range(self.height)])
        if full_column:
            return False
        for j in range(5,-1,-1):
            if toPrint:
                print (j,col)
            if self.arr[j][col] == 0:
                self.arr[j][col] = player
                self.moves.append(col)
                self.moves_dict[col] += 1
                if j == 0:
                    self.open_cols.remove(col)
                return True

    def remove_move(self,col):
        '''takes the move off the board. will be called when the AI looks moves ahead'''
        found = 0
        for j in range(5,-1,-1):
            if self.arr[j][col] == 0:
                found += 1
                if j == 5:
                    raise 'ERROR: tried to remove move from empty column'
                else:
                    self.arr[j+1][col] = 0
                    self.moves_dict[col] -= 1
        if found == 0:
            self.arr[0][col] = 0
            self.open_cols.append(col)


    def gos(self,player1,player2):
        '''if a player has stacked open threes in a column, it should move in that column to force the game. this function
        returns a list of columns with stacked open threes'''
        l = [item[0][0] for item in self.stacked_threats(player1,player2)]
        l2 = list(set(l))
        return l2

    def checkmate(self, player1, player2, toPrint=False):
        '''check whether the board is in a checkmate state for player1, meaning that no move for player2 will not
        avoid defeat on the subsequent move'''
        newboard = copy.deepcopy(self)
        if toPrint:
            print 'new newboard in checkmate function '
            print newboard.arr
        l = newboard.open_cols[:]
        ans = 0
        for col1 in l:
            ## one move ahead for player 2
            newboard.add_move(col1,player2)
            if toPrint:
                print 'modified hypothetical board in checkmate function' 
                print newboard.arr
            ## make sure the other player doesn't win in the meantime
            if newboard.check_four_alternate(player2):
                return False
            else:
                if toPrint:
                    print 'passed the next step, player 2 did not win with this move'
                if newboard.accessible_open_threes(player1):
                    ans += 1
                    #print 'total = ', ans
            newboard.remove_move(col1)
                
        if ans == len(l):
            return True

        return False

    def centerScore(self, player1, player2):
        center_score = 0
        for j in range(self.height):
            if self.arr[j][3] == player1:
                center_score += 1
            elif self.arr[j][3] == player2:
                center_score -= 1
        return center_score
    
    
def play_game_manual(player1=1, player2=2, board=Board(1,2)):
    for i in range(21):
        pprint(board.arr)
        if not board.add_move(raw_input('player 1, your move, plz:  '),player1):
            print 'okay'
            board.add_move(raw_input('player 1, your move, plz:  '),player1)
        pprint(board.arr)
        if board.check_four_alternate(player1):
            return  
        if not board.add_move(raw_input('player 2, your move, plz:  '),player2):
            board.add_move(raw_input('player 2, your move, plz:  '),player2)
        pprint(board.arr)
        if board.check_four_alternate(player2):
            return 
    print 'it\'s a draw!'
        
if __name__ == '__main__':
    import connectfour as c
    from pprint import pprint
    b = c.Board(1,2)
    b.add_move(1,2)
    b.add_move(2,1)
    b.add_move(3,1)
    b.add_move(4,1)
    b.add_move(5,2)
    b.add_move(5,2)
    b.add_move(5,1)
    b.add_move(3,2)
    b.add_move(3,1)
    b.add_move(3,1)
    b.add_move(4,2)
    b.add_move(4,2)
    b.add_move(4,1)
    b.add_move(2,1)
    b.add_move(2,2)
    pprint(b.arr)
    #c.minimax_dict(b,3,1,2)
    b.add_move(0,1)
    # c.minimax(b,3,2,1)
    # c.alphabeta(b,3,-100,100,2)
    #c.minimax_dict(b,2,2,1)
    b.add_move(0,2)
    pprint(b.arr)
    # c.minimax(b,2,1,2)
    # c.alphabeta(b,2,-100,100,1)
    b.add_move(0,1)
    pprint(b.arr)
    # c.minimax(b,1,2,1)
    # c.alphabeta(b,1,-100,100,2)
    c.minimax(b,3,1,2)
    c.alphabeta(b,3,1)



    
    c.minimax(b,0,b.player1,b.player2,1)
    b = Board(1,0)
    d = Board(1,2)
    #alphabeta(b,2,-10000,10000,b.player1)
    alphabeta(d,2,-10000,10000,d.player1)
    play_game_manual()
        

