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
    def __init__(self, team1, team2, moves=None, indices=list(indices_default), arr=np.zeros((6,7),dtype=int), height=6, width=7):
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

    def surrounders(self, team, index):
        a = 0
        i,j = index
        ## diagonals
        spare_rows_down = self.height - i - 1
        spare_columns_right = self.width - j - 1
        spare_rows_up = i
        spare_columns_left = j
        spare1 = min(spare_rows_down,spare_columns_right)
        spare2 = min(spare_rows_up,spare_columns_left)
        spare3 =  min(spare_rows_up,spare_columns_right)
        spare4 = min(spare_rows_down,spare_columns_left)
        ## downright  
        local = 0
        for s in range(1,spare1+1):
            
            if self.arr[i+s,j+s] in [0,team]:
                local += 1
            else:
                print local
                break
        print local
        a += min(local,4)
        print 'a = previous a + local printed above ', a
        ## upleft
        local = 0
        for s in range(-1,-spare2-1,-1):
          
            if self.arr[i+s,j+s] in [0,team]:
                local += 1
            else:
                print local
                break
        print local
        a += min(local,4)
        print 'a = previous a + local printed above ', a
        ## don't count the square as its own surrounder
        ##upright
        local = 0
        for s in range(1,spare3+1):
            
            if self.arr[i-s,j+s] in [team,0]: 
                local += 1
            else:
                print local
                break
        print local
        a += min(local,4)
        print 'a = previous a + local printed above ', a
        ## downleft
        local = 0
        for s in range(0,-spare4,-1):
            
            if self.arr[i-s,j+s] in [team,0]: 
                local += 1
            else:
                print local
                break
        print local
        a += min(local,4)
        print 'a = previous a + local printed above ', a
        ##up
        a += min(i,4)
        print i
        print 'a = previous a + spare rows above ', a
        
        ## left right
        ## right
        local = 0
        for s in range(1,spare_columns_right+1):
            
            if self.arr[i,j+s] == team or self.arr[i,j+s] == 0:
                local += 1
            else:
                print 'break'
                break
        print local
        a += min(local,4)
        print 'a = previous a + local printed above ', a
        ## left
        local = 0
        for s in range(1,spare_columns_left+1):
            
            if self.arr[i,j-s] == team or self.arr[i,j-s] == 0:
                local += 1
            else:
                print 'break completed'
                break
        print local
        a += min(local,4)
        print 'a = previous a + local printed above ', a
        return a
        
        
        
                    
        
    def check_open_three(self, team):
        '''check for three in a row'''
        list_indices = []
        a = np.array(3*[team],dtype=int)
        ## first, check rows
        for r in range(self.height):
            for c in range(self.width-2):
                if np.array_equal(self.arr[r,c:c+4],a):
                    if c == 0:
                        ## check to the right
                        if self.arr[r,c+5] == 0:
                            
                            list_indices.append((r,c+5))
                            
                    elif c == 4:
                        ## check to the left
                        if self.arr[r,c-1] == 0:
                            
                            list_indices.append((r,c-1))
                            
                    else:
                        ## check either side
                        if self.arr[r,c-1] == 0:
                            
                            list_indices.append((r,c-1))
                             
                        if self.arr[r,c+5] == 0:
                            
                            list_indices.append((r,c+5))
                            
                        
        ## columns         
        for c in range(self.width):
            for r in range(self.height-2):
                if np.array_equal(self.arr[r:r+4,c],a):
                    if r != 0: 
                        
                        list_indices.append((r-1,c))
                        
        ## nw diagonals, top left open only
        for i in range(-2,4):

            length = len(self.arr.diagonal(i))

            for j in range(length-3):

                if np.array_equal(self.arr.diagonal(i)[j+1:j+4],a):
                    
                    if i >= 0:
                        if self.arr[j,j+i] == 0:
                            
                            list_indices.append((j,j+1)) 
                    elif i < 0:
                        if self.arr[-i,-i+j] == 0:
                            
                            list_indices.append((-i,-i+j))
         
        ## ne diagonals, top right open only
        b = np.fliplr(self.arr)
        for i in range(-2,4):
            length = len(b.diagonal(i))
            for j in range(length-3):
                if np.array_equal(b.diagonal(i)[j+1:j+4],a):
                    if i >= 0:
                        if b[j,j+i] == 0:
                            
                            list_indices.append((j,j+1))
                    elif i < 0:
                        if b[-i,-i+j] == 0 :
                            
                            list_indices.append((-i,7-(-i+j)))
        if len(list_indices) > 0:
            return list_indices
        return False
            
        
    def check_four(self,team):
        '''check for four in a row, rows, columns and diagonals'''
        a = np.array(4*[team],dtype=int)
   
        ## first, check rows
        for t in range(self.height):
            for r in range(self.width-3):
                if np.array_equal(self.arr[t,r:r+4],a):
                    print 'team ' + str(team) + ' wins!'
                    return True
        ## columns         
        for r in range(self.width):
            for t in range(self.height-3):
                if np.array_equal(self.arr[t:t+4,r],a):
                    print 'team ' + str(team) + ' wins!'
                    return True
        ## northwest diagonals
        for i in range(-2,4):
            length = len(self.arr.diagonal(i))
            for j in range(length-3):
                if np.array_equal(self.arr.diagonal(i)[j:j+4],a):
                    print 'team ' + str(team) + ' wins!'
                    return True
        ## northeast diagonals
        b = np.fliplr(self.arr)
        for i in range(-2,4):
            length = len(b.diagonal(i))
            for j in range(length-3):
                if np.array_equal(b.diagonal(i)[j:j+4],a):
                    print 'team ' + str(team) + ' wins!'
                    return True

        return False
    def check_move_win(self,col,team):
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
            print 'illegal move! try again'
            return False
        for j in range(5,-1,-1):
            if self.arr[j,col] == 0:
                self.arr[j,col] = team
                self.moves.append(col)
                return True
    def checkmate(self, team1, team2):
        '''check whether the board is in a checkmate state for team1'''
        newboard = copy.deepcopy(self)
        list_cols = range(self.width)
        ans = 0
        for col1 in list_cols:
            ## one move ahead for team 2
            newboard.add_move(col1,team2)
            ## make sure the other team doesn't win in the meantime
            if not self.check_four(team2):
                for col2 in list_cols:
                    newboard.add_move(col2,team1)
                    if newboard.check_four(team1):
                        ans += 1
        if ans == 7:
            return True
        return False
    ## below might be useless. it's either len 0 (returns None), len 1 (doesn't help) or len >1 (checkmate)
    # def accessible_open_threes(self, team1, team2):
    #     newboard = copy.deepcopy(self)
    #     list_cols = range(self.width)
    #     l = self.check_open_three(team1)
    #     accessible_threes = []
    #     for tup in l:
    #         newboard.add_move(tup[1],team1)
    #         if newboard.check_four(team1):
    #             accessible_threes += tup
    #             return accessible_threes
    #     
    # def check_move_tree(self,col,team):
    #     list_indices = []
    #     for j in range(5,-1,-1):
    #         if self.arr[j,col] == 0:
    #             self.arr[j,col] = team
    #             if self.check_four(team):
    #                 return col
    #             if self.checkmate(team,self.team2):
    #                 return col
    #             
                
        


        
 
# class HyBoard(Board):
#     def __init__(self,arr):
#         self.arr = 
    
## bug: board.indices is team independent, shouldn't be    
    
    
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
        

# def check_four(board,team1,team2):
#     '''check for four in a row, rows, columns and diagonals'''
#     a = array(4*[team1],dtype=int)
#     c = array(4*[team2],dtype=int)
#     ## first, check rows
#     for t in range(6):
#             for r in range(4):
#                 if array_equal(board.arr[t,r:r+4],a) or array_equal(board.arr[t,r:r+4],c):
#                     print 'team ' + str(board.arr[t,r]) + ' wins!'
#                     return True
#     ## columns         
#     for r in range(7):
#         for t in range(3):
#             if array_equal(board.arr[t:t+4,r],a) or array_equal(board.arr[t:t+4,r],c):
#                 print 'team ' + str(board.arr[t,r]) + ' wins!'
#                 return True
#     ## northwest diagonals
#     for t in range(3):
#         for r in range(4):
#             d = array([board.arr[t,r],board.arr[t+1,r+1],board.arr[t+2,r+2],board.arr[t+3,r+3]],dtype=int)
#             if array_equal(d,a) or array_equal(d,c):
#                 print 'team ' + str(board.arr[t,r]) + ' wins!'
#                 return True
#     ## northeast diagonals
#     for t in range(3):
#         for r in range(6,2,-1):
#             d = array([board.arr[t,r],board.arr[t+1,r-1],board.arr[t+2,r-2],board.arr[t+3,r-3]],dtype=int)
#             if array_equal(d,a) or array_equal(d,c):
#                 print 'team ' + str(board.arr[t,r]) + ' wins!'
#                 return True
