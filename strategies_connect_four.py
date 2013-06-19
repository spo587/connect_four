import random
import copy
import connectfour as cf

## TODO: fix bug that occurs when a row is filled and computer is forced to make a move, it makes human choose another move
## instead....very smart
##TODO: still a minor bug in surrounders function, it's 1 too high sometimes
## TODO: major bug in the naive strategy, not sure why
def minimum(comp,human,board):
    '''strategy that returns a move only to win the game or if in check'''
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
        
    return None

def better(comp,human,board):
    '''returns minimum move if there is one. otherwise, eliminates moves by first
    eliminating any move that will directly result in a win for opp, then by eliminating
    any moves that could lead to a checkmate for the opp. returns single move if only one satisfies 
    comditions, otherwise a list of potential column indices'''
    
    minmove = minimum(comp,human,board)
    if minmove != None:
        print 'move returned by minimum function ', minmove  
        return minmove
    else:      
        newboard = copy.deepcopy(board)
        l = newboard.open_cols[:]  
        print l
        list_moves_to_remove = []
        for col in l:

            newboard.add_move(col, comp)
            # print 'newboard in strategies function,' 
            # print newboard.arr
            if newboard.check_move_win(col, human):
                list_moves_to_remove.append(col)
            
                
            ## if not, test whether the next move by other player could be a checkmate. if so, remove it from l
            else:
                for next_move1 in newboard.open_cols:
                    newboard.add_move(next_move1,human)
                    length = len(newboard.open_cols)
                    ans = 0
                    for next_move2 in newboard.open_cols:
                        newboard.add_move(next_move2,comp)
                        if newboard.accessible_open_three(human):
                            ans += 1
                        if ans == l:
                            l.remove(col)
                        newboard.remove_move(next_move2)
                    newboard.remove_move(next_move1)
  
            newboard.remove_move(col) 
        if len(list_moves_to_remove) > 0:
            for col in list_moves_to_remove:
                l.remove(col)
                    
        if len(l) == 1:
            print 'move determined by better function ', l[0]
            return l[0]
        elif len(l) == 0:
            print '!#@$!@#%$@#^$@%&# checkmate checkmate checkmate !@#$%@#$%@$#%^'
            return random.choice(board.open_cols) 
        return l
          
    

                
def surrounders(comp,human,board):
    '''implements the better strategy above, and if the list returned is length 2 or more,
    checks each potential move in the list for the number of 'surrounders', defined in connectfour file''' 

    if len(board.moves) == 1 and board.moves[0] < 4:
        return board.moves[0] + 1
    elif len(board.moves) == 1 and board.moves >= 4:
        return board.moves[0] - 1
    elif len(board.moves) == 0:
        return 3
    else:
        potential_moves = better(comp,human,board)
    
        if type(potential_moves) == int:  ## only one potential move identified in better() above
            print 'move determined by previous function ',potential_moves
            return potential_moves
        else:
            newboard = copy.deepcopy(board)
            l = potential_moves
            dictionary_of_moves = {}
            for move in l:
                dictionary_of_moves[move] = 0   
            for col in dictionary_of_moves.keys():

                value = newboard.check_move_surrounders(col,comp)
                dictionary_of_moves[col] = value
        print dictionary_of_moves
        final_list = []
        ## find the dictionary value with the maximum score and put it in the list
        for col in dictionary_of_moves.keys():
            if dictionary_of_moves[col] == max(dictionary_of_moves.values()):
                final_list.append(col)
        print 'final potential moves list determined by surrounders function ', final_list
        ## randomly choose move from final list
        final_move = random.choice(final_list)
        print final_move
        return final_move    
    
    
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
            print 'computer wins!!!!!'
            return 
        elif board.accessible_open_three(team2):
            print '###### CHECK #######'
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team1):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team1)
        print board.arr
        if board.check_four(team1):
            print 'human wins!!!!!'
            return  
        elif board.accessible_open_three(team1):
            print '###### CHECK #######'
    print 'its a draw!!!!!'
        
     
def computer_play_computer(strat1=surrounders,strat2=surrounders,team1=1,team2=2,board=cf.Board(1,2)):
    for i in range(21):
        board.add_move(strat1(team2,team1,board),team2)
        print board.arr
        if board.check_four(team2):
            print 'team 2 wins!!!!!'
            return 
        board.add_move(strat2(team1,team2,board),team1)
        print board.arr
        if board.check_four(team1):
            print 'team 1 wins!!!!'
            return 
    print 'it\'s a draw!!!!'
 
    
 
if __name__ == '__main__': 
    play_game_1_player_comp_leads(surrounders)           
    
    #computer_play_computer()
    
    
    
    