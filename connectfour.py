import itertools
import copy
        
'''this file contains the board class, whose methods will be called in the strategies file cf_strats_redone. you can also
play a two-player, human vs. human game in this file.'''




class Board(object):
    def __init__(self, player1, player2, height=6, width=7):
        self.arr = [[0 for i in range(7)] for j in range(6)]
        self.open_cols = range(7)
        self.moves = []
        self.player1 = player1
        self.player2 = player2
        self.height = height
        self.width = width
        self.available_fours = self.build_available_four_strings()

    def opposite_player(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def surrounders(self, player, index):
        '''key method to the surrounders strategy. checks branches in all directions for potential 4's in a row for the given player
        and the given index'''

        opponent = self.opposite_player(player)
        adjacent_fours = self.available_fours_at(index)

        unoccupied_fours = adjacent_fours[:]
        for line in adjacent_fours:
            for i, j in line:
                if self.arr[i][j] == opponent:
                    unoccupied_fours.remove(line)
        # no_opponent_fours = [line for line in adjacent_fours if not any([self.arr[i][j] == opponent for i,j in line])]

        def add(x, y):
            return x + y

        squares = reduce(add, unoccupied_fours)
        unique_squares = set(squares)
        return len(unique_squares) - 1

    def available_fours_at(self, index):
        return [line for line in self.available_fours if index in line]

    def build_available_four_strings(self):
        '''a list. each entry is a list of four indices making a possible connect four'''
        fours = []
        ## rows
        for row in range(self.height):
            for col in range(self.width - 3):
                fours.append([(row, col+i) for i in range(4)])
        ## columns
        for row in range(self.height - 3):
            for col in range(self.width):
                fours.append([(row+i, col) for i in range(4)])
        ## nw diagonals
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                fours.append([(row+i, col+i) for i in range(4)])
        ## ne diagonals
        for row in range(self.height - 3, self.height):
            for col in range(self.width - 3):
                fours.append([(row-i, col+i) for i in range(4)])
        assert len(fours) == 69
        return fours


    def check_four_alternate(self,player):
        '''checks the board for four in a row for the given player'''
        for entry in self.available_fours:
            temp_list = []
            for tup in entry:
                temp_list.append(self.arr[tup[0]][tup[1]])
            if temp_list == [player,player,player,player]:
                return True
        return False


    def check_open_three(self,player):
        '''a list of open threes for the given player. each element of the list is the list of four indices
        corresponding to the available three'''
        l = []
        for entry in self.available_fours:
            temp_list = []
            for tup in entry:
                temp_list.append(self.arr[tup[0]][tup[1]])
            total = 0
            for num in temp_list:
                if num != player and num != 0:
                    total = 0
                    break
                elif num == player:
                    total += 1
            if total == 3:
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

    def open_three_openings(self,player):
        '''returns a list of indices of only the OPEN entries in the open threes. l is a list, each element is a single tuple'''
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

    def stacked_open_threes(self,player):
        '''gives a list of columns with stacked open threes'''
        l = self.open_three_openings(player)
        stacks = []
        for i in range(len(l)-1):
            if l[i][0] == l[i+1][0] and l[i][1]+1 == l[i+1][1]:
                stacks.append([l[i],l[i+1]])
        return stacks
    def three_in_open_row(self,player):
        result = 0
        for tup in self.open_three_openings(player2):
            if (tup[0] + 4, tup[1]) in self.open_three_openings(player2):
                result += 1
        return result

    def check_move_win(self,col,player):
        '''will a move in the specified col for the player end the game?''' 
        for j in range(5,-1,-1):
            if self.arr[j][col] == 0:
                self.arr[j][col] = player
                
                value = self.check_four_alternate(player)
                self.arr[j][col] = 0
                return value
        return False

    def check_move_surrounders(self,col,player):
        '''what is the surrounders value of a move to the specified column?'''
        list_indices = []
        for j in range(5,-1,-1):
            if self.arr[j][col] == 0:
                self.arr[j][col] = player
                value = self.surrounders(player,(j,col))
                self.arr[j][col] = 0
                return value
     
    def check_total_surrounders(self,player):
        total = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.arr[row][col] == player:
                    total += self.surrounders(player,index)
        return total

    def add_move(self,col,player,toPrint=False):
        '''adds a move to the board for the given player in the given column'''
        full_column = all([self.arr[row][col] for row in range(self.height)])
        if full_column:
            return False
        for j in range(5,-1,-1):
            if toPrint:
                print (j,col)
            if self.arr[j][col] == 0:
                self.arr[j][col] = player
                self.moves.append(col)
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

        if found == 0:
            self.arr[0][col] = 0
            self.open_cols.append(col)
    
    def accessible_open_threes(self, player1):
        '''is there an open three that can be capitalized on in next move for player1? if there is, return the columns of those moves 
        in a list '''
        l = []
        newboard = copy.deepcopy(self)
        list_cols = newboard.open_cols[:]
        for col in list_cols:
            newboard.add_move(col,player1)
            value = newboard.check_four_alternate(player1)
            newboard.remove_move(col)
            if value:
                l.append(col)
        return len(l)   ## will map to False if len(l) == 0


    ### not using the methods below yet, but they could be useful. have tested them
    ### individually, and they seem to work well
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

    def check_move_for_checkmate(self,col,player1,player2):
        '''check whether the given move puts the board in a checkmate state for player1'''
        newboard = copy.deepcopy(self)
        newboard.add_move(col, player1)
        ans = newboard.checkmate(player1,player2)
        newboard.remove_move(col)
        if ans:
            return True
        return False

    def checkmate_moves(self,player1,player2):
        '''check all moves for a checkmate move for player1'''
        if self.accessible_open_threes(player1) > 0:
            return False
        newboard = copy.deepcopy(self)
        for move in newboard.open_cols:
            ans = newboard.check_move_for_checkmate(move,player1,player2)

            if ans:
                return move
        return False

    def utility_estimator(self,player1,player2,weight1, weight2):
        '''the estimator of the utility of the board state for player1'''
        u1 = self.open_three_openings(player1)[:]
        u2 = self.open_three_openings(player2)[:]

        for tup1 in self.open_three_openings(player1):
            for tup2 in self.open_three_openings(player2):
                if tup2[0] == tup1[0] and tup2[1] == tup1[1] + 1:
                    u1.remove(tup1)
                elif tup2[0] == tup1[0] and tup2[1] + 1 == tup1[1]:
                    u2.remove(tup2)
        open_rows_1 = 0
        open_rows_2 = 0
        for tup1 in u1:
            if (tup1[0] + 4, tup1[1]) in u1:
                open_rows_1 += 1
        for tup2 in u2:
            if (tup2[0]+4,tup2[1]) in u2:
                open_rows_2 += 1

        stacks1 = len(self.stacked_open_threes(player1))
        stacks2 = len(self.stacked_open_threes(player2))
        ## weight the stacks higher than other open threes
        return len(u1) + weight1*stacks1+weight2*open_rows_1 - (len(u2) + weight1*stacks2+weight2*open_rows_1)
    
    
def play_game_manual(player1=1, player2=2, board=Board(1,2)):
    for i in range(21):
        if not board.add_move(raw_input('player 1, your move, plz:  '),player1):
            board.add_move(raw_input('player 1, your move, plz:  '),player1)
        print board.arr
        if board.check_four(player1):
            return  
        if not board.add_move(raw_input('player 2, your move, plz:  '),player2):
            board.add_move(raw_input('player 2, your move, plz:  '),player2)
        print board.arr
        if board.check_four(player2):
            return 
    print 'it\'s a draw!'
        
        
if __name__ == '__main__':
    play_game_manual()
        

