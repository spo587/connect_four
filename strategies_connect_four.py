import random
import copy
import connectfour as cf

## TODO: fix bug that occurs when a row is filled and computer is forced to make a move, it makes human choose another move
## instead....very smart
def minimum(comp,human,board):
    l = range(board.width)
    forces = []
    for col in l:
        if board.check_move_win(col,comp):
            print col
            return col
    for col in l:
        if board.check_move_win(col,human):
            forces.append(col)
    if len(forces) == 1:
        print forces[0]
        return forces[0]
    elif len(forces) > 1:
        print 'checkmate'
        assert 'forfeit'
    return None

def better(comp,human,board):
    l = range(board.width)
    minmove = minimum(comp,human,board)
    if minmove != None:
        print 'move returned by minimum function'  
        return minmove
    else:      
        newboard = copy.deepcopy(board)
        for col in l:
            ## if the column is full, remove it as an option
            if board.arr[0:5,col].all() != 0:
                l.remove(col)
            ## otherwise, test a move in each column, and whether it leads to a win for human player
            else:
                newboard.add_move(col, comp)
                if newboard.check_move_win(col, human) is True:
                    l.remove(col)
        if len(l) == 1:
            print 'move determined by better function'
            return l[0]
        else: 
            return l
        
def better_strategy(comp,human,board):
    potential_moves = better(comp,human,board)
    if type(potential_moves) == int:  ## only one potential move identified in better() above
        print 'move determined by previous function'
        return potential_moves
    else:
        choice = random.choice(potential_moves)
        print choice
        return choice
    
    
def naive(comp,human,board):
    print board.arr
    potential_moves = better(comp,human,board)
    print board.arr
    if type(potential_moves) == int:  ## only one potential move identified in better() above
        print 'move determined by previous function'
        return potential_moves
    else:
        
        print 'potential moves list', potential_moves
        newboard = copy.deepcopy(board)
        print 'hypothetical board \n', newboard.arr
        print 'old board, should be same \n', board.arr
        l = potential_moves
        for col in l:
            ## if the column is full, remove it as an option
            if board.arr[0:5,col].all() != 0:
                l.remove(col)
            ## otherwise, test a move in each potential column, and whether it leads to a three in a row
            else:
                openspots = newboard.check_move_three(col,comp)
                print openspots
                if openspots:
                    for move in openspots:
                        if move not in board.indices:
                            openspots.remove(move)
                        print openspots
                        finalmove = random.choice(openspots)

                        board.indices.remove(finalmove)
                        print 'move determined to make 3'
                        return finalmove[1]
        print 'move determined randomly' 
        return random.choice(l)
                
def surrounders(comp,human,board):
    if len(board.moves) == 1 and board.moves[0] < 4:
        return board.moves[0] + 1
    elif len(board.moves) == 1 and board.moves >= 4:
        return board.moves[0] - 1
    elif len(board.moves) == 0:
        return 3
    else:
        
         
    
        potential_moves = better(comp,human,board)
    
        if type(potential_moves) == int:  ## only one potential move identified in better() above
            print 'move determined by previous function'
            return potential_moves
        else:
            print 'potential moves list', potential_moves
            newboard = copy.deepcopy(board)
            print 'hypothetical board \n', newboard.arr
            print 'old board, should be same \n', board.arr
            l = potential_moves
            dictionary_of_moves = {}
            for move in l:
                dictionary_of_moves[move] = 0   
            for col in dictionary_of_moves.keys():
                ## if the column is full, remove it as an option
                if board.arr[0:5,col].all() != 0:
                    dictionary_of_moves[col] = 0
                ## otherwise, test a move in each potential column, and what its surrounders score is
                else:
                    value = newboard.check_move_surrounders(col,comp)
                    dictionary_of_moves[col] = value
        for col in dictionary_of_moves.keys():
            if dictionary_of_moves[col] == max(dictionary_of_moves.values()):
                return col    
    
    
def play_game_1_player_human_leads(strat=surrounders, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team1):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team1)
        print board.arr
        if board.check_four(team1):
            return  
        
        board.add_move(strat(team2,team1,board),team2)
        print board.arr
        if board.check_four(team2):
            return 
    print 'it\'s a draw!!!!!' 
 
def play_game_1_player_comp_leads(strat=surrounders, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        board.add_move(strat(team2,team1,board),team2)
        print board.arr
        if board.check_four(team2):
            return 
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team1):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team1)
        print board.arr
        if board.check_four(team1):
            return  
        
     
 
 
    
 
if __name__ == '__main__':            
    play_game_1_player_comp_leads()
    
    
    
    