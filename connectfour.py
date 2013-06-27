import itertools
import copy
from collections import defaultdict
from pprint import pprint
        
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

    def surrounders(self, player, index):
        '''key method to the surrounders strategy. checks branches in all directions for potential 4's in a row for the given player
        and the given index'''

        opponent = self.opposite_player(player)
        adjacent_fours = self.available_fours_at(index)

        list_fours_to_remove = []
        for line in adjacent_fours:
            for i, j in line:
                if self.arr[i][j] == opponent:
                    list_fours_to_remove.append(tuple(line))
        list_fours_to_remove_set = list(set(list_fours_to_remove))
        for item in list_fours_to_remove_set:
            item = list(item)
            adjacent_fours.remove(item)

        unoccupied_fours = adjacent_fours   
        # no_opponent_fours = [line for line in adjacent_fours if not any([self.arr[i][j] == opponent for i,j in line])]

        def add(x, y):
            return x + y
        if len(unoccupied_fours) == 0:
            return 0
        squares = reduce(add, unoccupied_fours)
        unique_squares = set(squares)
        return len(unique_squares) - 1

    def available_fours_at(self, index):
        return [line for line in self.available_fours_no_columns if index in line]

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
                
    def num_of_lowest_open_threes(self,player1,player2):

        openings_reverted_1 = [(j,i) for (i,j) in self.open_three_openings(player1)]
        
        openings_reverted_2 = [(j,i) for (i,j) in self.open_three_openings(player2)]
        
        total = 0
        col = 0
        while col < 7:
            row = 5
            while row > -1:
                if (row,col) in openings_reverted_1 and (row,col) not in openings_reverted_2:
                    total += 1
                    
                    break
                elif (row,col) in openings_reverted_2 and (row,col) not in openings_reverted_1:
                    total -= 1
                    
                    break
                row -= 1
            col += 1
        return total

    def free_moves_remaining(self,player1,player2):
        newboard = copy.deepcopy(board)
        l1 = newboard.open_cols[:]
        for col1 in l1:
            newboard.add_move(col1,player1)
            for col2 in newboard.open_cols:
                newboard.add_move(col2,player2)



    def control_end(self,player1,player2):
        '''modifies lowest open threes function for even odd row indexing.
        note that this function must be called in the right order, 
        player1 is the player who starts the game. returns 1 if player1 controls the end game, returns 
        -1 if player 2 controls the end game, returns 0 otherwise.'''
        openings_reverted_1 = [(j,i) for (i,j) in self.open_three_openings(player1)]
        
        openings_reverted_2 = [(j,i) for (i,j) in self.open_three_openings(player2)]
        total_1 = 0
        total_2_even = 0
        total_2_odd = 0
        col = 0
        while col < 7:
            row = 4
            while row > -1:
                if row%2 == 1:
                    if (row,col) in openings_reverted_2 and (row,col) not in openings_reverted_1 and self.arr[row+1][col] == 0:
                        #print 'incrementing total 2 odd'
                        total_2_odd += 1
                        break
                    elif (row,col) in openings_reverted_1 and (row,col) in openings_reverted_2 and self.arr[row+1][col] == 0:
                        #print 'incrementing total 1 and total 2 odd'
                        total_1 += 1
                        total_2_odd += 1
                        break
                    elif (row,col) in openings_reverted_1 and self.arr[row+1][col] == 0:
                        #print 'incrementing total 1'
                        total_1 += 1
                        break
                elif row%2 == 0 and (row,col) in openings_reverted_2 and self.arr[row+1][col] == 0:
                    #print 'incrementing total 2 even'
                    total_2_even += 1
                    break
                row -= 1
            col += 1
        if total_2_odd % 2 == 0 and total_2_odd > 0:
            total = -1
        elif total_1 > 0:
            total = total_1
        elif total_2_even > 0:
            total = -total_2_even
        else:
            total = 0 
        return total

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
    def check_total_possible_fours(self,player):
        total = []
        for row in range(self.height):
            for col in range(self.width):
                if self.arr[row][col] == player:
                    total += self.available_fours_at_index_for_player(player,(row,col))
        l = list(set(total))
        #print l
        return l
    def prune_total_possible_fours(self,player1,player2):
        openings_reverted_2 = [(j,i) for (i,j) in self.open_three_openings(player2)]
        l1 = self.check_total_possible_fours(player1)[:]
        for list_of_tuples in self.check_total_possible_fours(player1):
            for tup in list_of_tuples:
                for row in range(tup[0]+1,self.height+1,2):
                    if (row,tup[1]) in openings_reverted_2 and list_of_tuples in l1:
                        l1.remove(list_of_tuples)
        openings_reverted_1 = [(j,i) for (i,j) in self.open_three_openings(player1)]
        l2 = self.check_total_possible_fours(player1)[:]
        for list_of_tuples in self.check_total_possible_fours(player1):
            for tup in list_of_tuples:
                for row in range(tup[0]+2,self.height+1,2):
                    if (row,tup[1]) in openings_reverted_1 and list_of_tuples in l2:
                        l2.remove(list_of_tuples)

        l = [item for item in l1 if item in l2]
        return l



     
    def check_total_surrounders(self,player):
        total = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.arr[row][col] == player:
                    total += self.surrounders(player,(row,col))
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

    def gos(self,player):
        '''if a player has stacked open threes in a column, it should move in that column to force the game. this function
        returns a list of columns with stacked open threes'''
        l = [item[0][0] for item in self.stacked_open_threes(player)]
        l2 = list(set(l))
        return l2



    def no_gos_first_player(self,player1,player2):
        '''if a move by player2 in a column results in a win for player1, then player1 should not go in that column, unless it
        has open three indices stacked on top of each other. this function
        returns those columns in a list
        ALERT: must be called in right order! player1 is the first player to move int eh game'''
        newboard = copy.deepcopy(self)
        l = newboard.open_cols[:]
        list_of_no_gos = []
        for move in l:
            newboard.add_move(move,player2)
            if newboard.check_move_win(move,player1) is not False and move not in self.gos(player1) and newboard.moves_dict[move]%2==0:
                list_of_no_gos.append(move)
            newboard.remove_move(move)
        l2 = list(set(list_of_no_gos))
        return l2

    def no_gos_second_player(self,player2,player1):
        '''same as above, but for the second player to move'''
        newboard = copy.deepcopy(self)
        l = newboard.open_cols[:]
        list_of_no_gos = []
        for move in l:
            newboard.add_move(move,player1)
            if newboard.check_move_win(move,player2) is not False and move not in self.gos(player2) and newboard.moves_dict[move]%2==1:
                list_of_no_gos.append(move)
            newboard.remove_move(move)
        l2 = list(set(list_of_no_gos))
        return l2



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


    def utility_estimator(self,player1,player2,weight_center, weight_stacks,weight_open_rows,toPrint=False,weight_no_gos=5,change_factor=1/float(42)):
        '''the estimator of the utility of the board state for player1'''
        center_score = 0
        for j in range(self.height):
            if self.arr[j][3] == player1:
                center_score += weight_center
            elif self.arr[j][3] == player2:
                center_score -= weight_center
        s1 = self.check_total_surrounders(player1)
        s2 = self.check_total_surrounders(player2)
        surrounders_factor = (s1 - s2)*change_factor*(42 - len(self.moves))
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

        stacks1 = len(self.gos(player1))
        stacks2 = len(self.gos(player2))
        no_gos_1 = len(self.no_gos(player1,player2))
        no_gos_2 = len(self.no_gos(player2,player1))
        ## weight the stacks higher than other open threes

        threes_factor = len(u1) + weight_stacks*stacks1+weight_open_rows*open_rows_1 + weight_no_gos*no_gos_1 - (len(u2) + weight_stacks*stacks2+weight_center*open_rows_1 + weight_no_gos*no_gos_2)
        if toPrint:
            print 'surrounders factor ', surrounders_factor
            print 'center score ', center_score
            print 'threes factor ', threes_factor
        utility = surrounders_factor + threes_factor + center_score
        return utility

    def utility_estimator_simpler_p1(self,player1,player2,weights,toPrint=False):
        '''must be called in the right order, player1 being the player who goes first'''
        potential_fours_utility = weights[0]*(len(self.prune_total_possible_fours(player1,player2)) - len(self.prune_total_possible_fours(player2,player1)))
        end_utility = weights[1]*(self.control_end(player1,player2))
        center_score = 0
        for j in range(self.height):
            if self.arr[j][3] == player1:
                center_score += weights[2]
            elif self.arr[j][3] == player2:
                center_score -= weights[2]
        if toPrint:
            print 'end utility estimate ', end_utility
            print 'potential fours utility ', potential_fours_utility
        return potential_fours_utility + end_utility + center_score

    def utility_estimator_simpler_p2(self,player2,player1,weights,toPrint=False):
        return -self.utility_estimator_simpler_p1(player1,player2,weights,toPrint=False)
  

    
    
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
        

