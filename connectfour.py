import numpy as np
import itertools
import copy

indices_default = ()
for j in range(6):
    for i in range(7):
        indices_default += ((j,i),)
        

# class Team(object):
#     def __init__(self, num, strat, nummoves=0):

class Board(object):
    def __init__(self, team1, team2, open_cols=range(7), moves=None, indices=list(indices_default), arr=np.zeros((6,7),dtype=int), height=6, width=7):
        self.arr = arr
        self.team1 = team1
        self.team2 = team2
        self.height = height
        self.width = width
        self.indices = indices
        if moves is None:
            self.moves = []
        else:
            self.moves = moves
        self.open_cols = open_cols

    def surrounders(self, team, index):
        '''key method to the surrounders strategy. checks branches in all directions for potential 4's in a row for the given team
        and the given index'''
        a = 0
        i,j = index
        ## how many rows below, above, and columns below and above are there?
        spare_rows_down = self.height - i - 1
        spare_columns_right = self.width - j - 1
        spare_rows_up = i
        spare_columns_left = j
        ## for checking diagonals, can't go too far or will raise an index error in the array
        spare1 = min(spare_rows_down,spare_columns_right)
        spare2 = min(spare_rows_up,spare_columns_left)
        spare3 =  min(spare_rows_up,spare_columns_right)
        spare4 = min(spare_rows_down,spare_columns_left)
        ##check diagonals
        ## down, right  
        local = 0
        for s in range(1,spare1+1):
            
            if self.arr[i+s,j+s] in [0,team]:
                local += 1
            else:
                break

        downright = min(local,4)
        ## up, left
        local = 0
        for s in range(-1,-spare2-1,-1):
          
            if self.arr[i+s,j+s] in [0,team]:
                local += 1
            else:
                break
        upleft = min(local,4)
        ## d, on't count the square as its own surrounder
        ##upright
        local = 0
        for s in range(1,spare3+1):
            
            if self.arr[i-s,j+s] in [team,0]: 
                local += 1
            else:
  
                break
    
        upright = min(local,4)
  
        ## down, left
        local = 0
        for s in range(0,-spare4,-1):
            
            if self.arr[i-s,j+s] in [team,0]: 
                local += 1
            else:
                print local
                break
        
        downleft = min(local,4)
   
        ##up
        up = min(i,4)

        ## down

        local = 0
        for s in range(i+1,self.height):
            if self.arr[s,j] == team:
                local += 1
            else:
                break
        down = local

        ## left right
        ## right
        local = 0
        for s in range(1,spare_columns_right+1):
            
            if self.arr[i,j+s] == team or self.arr[i,j+s] == 0:
                local += 1
            else:

                break

        right = min(local,4)

        ## left
        local = 0
        for s in range(1,spare_columns_left+1):
            
            if self.arr[i,j-s] == team or self.arr[i,j-s] == 0:
                local += 1
            else:

                break

        left = min(local,4)
        total = 0
        if right +  left >= 3:
            total += right + left
        if upleft + downright  >= 3:
            total += upleft + downright
        if up + down >= 3:
            total += up + down
        if upright + downleft >= 3:
            total += upright + downleft
        return total
                
    def check_four(self,team):
        '''check for four in a row, rows, columns and diagonals'''
        a = np.array(4*[team],dtype=int)
   
        ## first, check rows
        for t in range(self.height):
            for r in range(self.width-3):
                if np.array_equal(self.arr[t,r:r+4],a):
 
                    return True
        ## columns         
        for r in range(self.width):
            for t in range(self.height-3):
                if np.array_equal(self.arr[t:t+4,r],a):

                    return True
        ## northwest diagonals
        for i in range(-2,4):
            length = len(self.arr.diagonal(i))
            for j in range(length-3):
                if np.array_equal(self.arr.diagonal(i)[j:j+4],a):

                    return True
        ## northeast diagonals
        b = np.fliplr(self.arr)
        for i in range(-2,4):
            length = len(b.diagonal(i))
            for j in range(length-3):
                if np.array_equal(b.diagonal(i)[j:j+4],a):
 
                    return True

        return False
    def check_move_win(self,col,team):
        '''will a move in the specified col for the team end the game?''' 
        for j in range(5,-1,-1):
            if self.arr[j,col] == 0:
                self.arr[j,col] = team
                
                value = self.check_four(team)
                self.arr[j,col] = 0
                return value
        return False
    def check_move_three(self,col,team):
        list_indices = []
        for j in range(5,-1,-1):
            if self.arr[j,col] == 0:
                self.arr[j,col] = team
                list_tuples = self.check_open_three(team)
                self.arr[j,col] = 0
                if list_tuples != False:
                    #list_indices.append(list_tuples)
                    for tup in list_tuples:
                        list_indices.append(tup)
        if len(list_indices) > 0:
            return list_indices
        return False
    def check_move_surrounders(self,col,team):
        list_indices = []
        for j in range(5,-1,-1):
            if self.arr[j,col] == 0:
                self.arr[j,col] = team
                value = self.surrounders(team,(j,col))
                self.arr[j,col] = 0
                return value
           
    def add_move(self,col,team):
        if self.arr[0:5,col].all() != 0:
            return False
        for j in range(5,-1,-1):
            if self.arr[j,col] == 0:
                self.arr[j,col] = team
                self.moves.append(col)
                self.indices.remove((j,col))
                if j == 0:
                    self.open_cols.remove(col)
                return True

    def remove_move(self,col):
        found = 0
        for j in range(5,-1,-1):
            if self.arr[j,col] == 0:
                found += 1
                if j == 5:
                    raise 'ERROR: tried to remove move from empty column'
                else:
                    self.arr[j+1,col] = 0
                    self.indices.append((j+1,col))
        if found == 0:
            self.arr[0,col] = 0
            self.open_cols.append(col)
            self.indices.append((0,col))    
    
    def accessible_open_three(self, team1):
        '''is there an open three that can be capitalized on in next move for team1? if there is, return the col of that move '''
        newboard = copy.deepcopy(self)
        list_cols = range(self.width)
        for col in list_cols:
            newboard.add_move(col,team1)
            value = newboard.check_four(team1)
            newboard.remove_move(col)
            if value:
                return True
        return False


    ### not using the methods below yet, but they could be useful. have tested them
    ### individually, and they seem to work well
    def checkmate(self, team1, team2):
        '''check whether the board is in a checkmate state for team1'''
        newboard = copy.deepcopy(self)
        print 'new newboard in checkmate function '
        print newboard.arr
        list_cols = range(self.width)
        ans = 0
        for col1 in list_cols:
            ## one move ahead for team 2
            newboard.add_move(col1,team2)
            print 'modified hypothetical board in checkmate function' 
            print newboard.arr
            ## make sure the other team doesn't win in the meantime
            if not self.check_four(team2):
                print 'passed the next step, team 2 did not win with this move'
                for col2 in list_cols:
                    newboard.add_move(col2,team1)
                    print 'next hypothetical board ' 
                    print newboard.arr
                    if newboard.check_four(team1):
                        ans += 1
                        newboard.remove_move(col2)
                        break
                    newboard.remove_move(col2)
            newboard.remove_move(col1)
                
        if ans == 7:
            return True
        return False
    def check_move_checkmate(self,col,team1,team2):
        '''check whether the given move puts the board in a checkmate state'''
        list_indices = []
        for j in range(5,-1,-1):
            if self.arr[j,col] == 0:
                self.arr[j,col] = team1
                value = self.checkmate(team1,team2)
                self.arr[j,col] = 0
                if value:
                    return True
        return False
  
    
    
def play_game_manual(team1=1, team2=2, board=Board(1,2)):
    for i in range(21):
        if not board.add_move(raw_input('team 1, your move, plz:  '),team1):
            board.add_move(raw_input('team 1, your move, plz:  '),team1)
        print board.arr
        if board.check_four(team1):
            return  
        if not board.add_move(raw_input('team 2, your move, plz:  '),team2):
            board.add_move(raw_input('team 2, your move, plz:  '),team2)
        print board.arr
        if board.check_four(team2):
            return 
    print 'it\'s a draw!'
        
        
if __name__ == '__main__':
    play_game_manual()
        

