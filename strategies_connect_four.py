import random
import copy
import connectfour as cf

## TODO: fix bug that occurs when a row is filled and computer is forced to make a move, it makes human choose another move
## instead....very smart
##TODO: still a minor bug in surrounders function, it's 1 too high sometimes
## TODO: major bug in the naive strategy, not sure why
def minimum(comp,human,board):
    '''strategy that returns a move only to win the game or if comp is in check'''
    if len(board.moves) == 1 and board.moves[0] != 3 or len(board.moves) == 0:
        return 3
    elif len(board.moves) == 1 and board.moves[0] == 3:
        return 2
    else:
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

def better_min(player1,player2,board,toPrint=False):
    '''returns list of moves that won't immediately result in losing the game'''
    minmove = minimum(player1,player2,board)
    if minmove != None:
        return [minmove]
    else:      
        newboard = copy.deepcopy(board)
        l = newboard.open_cols[:]  
        #print l
        list_moves = []
        hypotheticals = [0,0,0]
        for col in l:
            hypotheticals[0] = col
            newboard.add_move(col, player1)
            if toPrint:
                print 'where are we in the tree?  ', hypotheticals
                print 'hypothetical board, 1 move ahead'
                print newboard.arr
            if newboard.check_move_win(col, player2) is False:
                list_moves.append(col)
        if len(list_moves) > 0:
            return list_moves
        else:
            print 'no moves will not immediately result in a defeat'
            return l



def better1(comp,human,board, toPrint=False):
    '''returns minimum move if there is one. otherwise, eliminates moves by first
    eliminating any move that will directly result in a win for opp, then by eliminating
    any moves that could lead to a checkmate for the opp. returns single move if only one satisfies 
    comditions, otherwise a list of potential column indices'''
    
    minmove = minimum(comp,human,board)
    if minmove != None:
        #print 'move returned by minimum function ', minmove  
        return minmove
    else:      
        newboard = copy.deepcopy(board)
        l = better_min(comp,human,board)[:]  
        #print l
        list_moves_to_remove = []
        hypotheticals = [0,0,0]
        for col in l:
            hypotheticals[0] = col
            newboard.add_move(col, comp)
            if toPrint:
                print 'where are we in the tree?  ', hypotheticals
                print 'hypothetical board, 1 move ahead'
                print newboard.arr
            ## does the new move make  
            if newboard.accessible_open_threes(comp) > 1 and newboard.check_move_win(col) is False:
                    return col
            elif newboard.check_move_win(col, human):
                list_moves_to_remove.append(col)    
            ## if not, test whether the next move by other player could be a checkmate. if so, add it to list of moves to be removed
            else:
                l1 = newboard.open_cols[:]
                for next_move1 in l1:
                    newboard.add_move(next_move1,human)
                    hypotheticals[1] = next_move1
                    if toPrint:
                        'where are we in the tree?', hypotheticals
                        print 'new hypothetical board, 2 moves ahead'
                        print newboard.arr
                    # print 'new hypothetical board, 2 moves ahead: %s', hypotheticals
                    # print newboard.arr
                    length = len(newboard.open_cols)
                    if toPrint:
                        print 'number of open columns left in the new hypothetical board', length
                    ans = 0
                    l2 = newboard.open_cols[:]
                    for next_move2 in l2:
                        hypotheticals[2] = next_move2
                        newboard.add_move(next_move2,comp)
                        if toPrint:
                            print 'where are we in the tree?  ', hypotheticals
                            print 'hypothetical board, 3 moves ahead'
                            print newboard.arr
                        if newboard.accessible_open_threes(human):
                            ans += 1
                            if toPrint:
                                print 'wins for the other player on this branch:  ', ans
                        if ans == length and col not in list_moves_to_remove:
                            list_moves_to_remove.append(col)
                        newboard.remove_move(next_move2)
                    newboard.remove_move(next_move1)
  
            newboard.remove_move(col)
        if toPrint:
            print 'list of moves to remove  ', list_moves_to_remove
            print 'original list of potential moves  ', l

        if len(list_moves_to_remove) > 0:
            for col in list_moves_to_remove:
                l.remove(col)
                    
        if len(l) == 1:
            #print 'move determined by better function ', l[0]
            return l[0]
        elif len(l) == 0:
            #print '!#@$!@#%$@#^$@%&# checkmate checkmate checkmate for team %s', human
            #print 'randomly choosing the move because there are no possible moves left to avoid defeat'
            return random.choice(board.open_cols) 
        return l
          
def better3(player1,player2,board,toPrint=False):
    '''returns minmove if there is one. returns a checkmate move is there is one. otherwise returns a list of moves that will not immediately
    result in checkmate for the other player'''
    minmove = minimum(player1,player2,board)
    if minmove != None:
        #print 'move returned by minimum function ', minmove  
        return minmove
    else:
        move = board.checkmate_moves(player1,player2)
        if move is not False:
            return move
        else:
            list_moves_to_remove = []
            newboard = copy.deepcopy(board)
            l = better_min(player1,player2,board)[:]
            for col in l:
                newboard.add_move(col,player1)
                if newboard.checkmate_moves(player2,player1) is not False:
                    list_moves_to_remove.append(col)
                newboard.remove_move(col)
            for item in list_moves_to_remove:
                l.remove(item)
            if len(l) > 0:
                return l
            else:
                print 'game must be lost, returning whole list'



def better2(comp,human,board, toPrint=False):
    '''returns minimum move if there is one. otherwise, eliminates moves by first
    eliminating any move that will directly result in a win for opp, then by eliminating
    any moves that could lead to a checkmate for the opp. returns single move if only one satisfies 
    comditions, otherwise a list of potential column indices'''
    
    minmove = minimum(comp,human,board)
    if minmove != None:
        #print 'move returned by minimum function ', minmove  
        return minmove
    else:      
        newboard = copy.deepcopy(board)
        l = newboard.open_cols[:]  
        #print l
        list_moves_to_remove = []
        hypotheticals = [0,0,0]
        for col in l:
            hypotheticals[0] = col
            newboard.add_move(col, comp)
            if toPrint:
                print 'where are we in the tree?  ', hypotheticals
                print 'hypothetical board, 1 move ahead'
                print newboard.arr
            if newboard.check_move_win(col, human):
                list_moves_to_remove.append(col)
            else:
                l2 = newboard.open_cols[:]
                #print 'here are the columns where we should be testing player 1\'s moves ', newboard.open_cols
                for next_move1 in l2:
                    newboard.add_move(next_move1,human)
                    hypotheticals[1] = next_move1
                    if toPrint:
                        print 'where are we in the tree?', hypotheticals
                        print 'new hypothetical board, 2 moves ahead'
                        print newboard.arr
                    # print 'new hypothetical board, 2 moves ahead: %s', hypotheticals
                    # print newboard.arr
                    #print 'accessible open threes on this board', newboard.accessible_open_threes(human)
                    if newboard.accessible_open_threes(human) > 1 and col not in list_moves_to_remove:
                        #print 'success. this move should be added to the list'
                        list_moves_to_remove.append(col)
                    newboard.remove_move(next_move1)
            newboard.remove_move(col)
        if toPrint:
            print 'list of moves to remove  ', list_moves_to_remove
            print 'original list of potential moves  ', l

        if len(list_moves_to_remove) > 0:
            for col in list_moves_to_remove:
                l.remove(col)
                    
        if len(l) == 1:
            #print 'move determined by better function ', l[0]
            return l[0]
        elif len(l) == 0:
            #print '!#@$!@#%$@#^$@%&# checkmate checkmate checkmate for team %s', human
            #print 'randomly choosing the move because there are no possible moves left to avoid defeat'
            return random.choice(board.open_cols) 
        return l


# def better1_better2_combined:

def surrounders_builder(player1,player2,board):
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
    return final_list
                
def surrounders_initial_better3(comp,human,board):
    '''implements the better strategy above, and if the list returned is length 2 or more,
    checks each potential move in the list for the number of 'surrounders', defined in connectfour file''' 
    potential_moves = better3(comp,human,board)

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
    return final_list

def surrounders_initial_better1(comp,human,board):
    '''implements the better strategy above, and if the list returned is length 2 or more,
    checks each potential move in the list for the number of 'surrounders', defined in connectfour file''' 
    potential_moves = better1(comp,human,board)

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
    return final_list

def surrounders_random_1(comp,human,board):
    unique_surrounders_move = surrounders_initial_better1(comp,human,board)
    if type(unique_surrounders_move) == int:
        return unique_surrounders_move
    else:
        ## randomly choose move from final list
        final_move = random.choice(unique_surrounders_move)
        print final_move
        return final_move  

def surrounders_random_3(comp,human,board):
    unique_surrounders_move = surrounders_initial_better3(comp,human,board)
    if type(unique_surrounders_move) == int:
        return unique_surrounders_move
    else:
        ## randomly choose move from final list
        final_move = random.choice(unique_surrounders_move)
        print final_move
        return final_move  


# def combined_strategy_1(player1,player2,board,nummoves):
#     '''a combined strategy that implements the surrounders strategy for the first nummoves moves, '''

#     if len(board.moves) <= 14:
#         return random.choice(surrounders_builder(player1,player2,board))
#     else:
#         l = []
#         for i in range(7):
#             if i in better(player1,player2,board) and i in better2(player1,player2,board):
#                 l.append(i)
#         for i in l =



def surrounders_outer(comp,human,board):
    '''if surrounders returns a list, chooses the outermost column for move''' 
    unique_surrounders_move = surrounders_initial(comp,human,board)
    if type(unique_surrounders_move) == int:
        return unique_surrounders_move
    else:
        final_list_dict = {}
        final_list = []
        for move in unique_surrounders_move:
            final_list_dict[move] = abs(3 - move)
        for move in final_list_dict.keys():
            if final_list_dict[move] == max(final_list_dict.values()):
                final_list.append(move)
        return random.choice(final_list)


def surrounders_inner(comp,human,board):
    '''if surrounders returns a list, chooses closer to the center''' 
    unique_surrounders_move = surrounders_initial(comp,human,board)
    if type(unique_surrounders_move) == int:
        return unique_surrounders_move
    else:
        final_list_dict = {}
        final_list = []
        for move in unique_surrounders_move:
            final_list_dict[move] = abs(3 - move)
        for move in final_list_dict.keys():
            if final_list_dict[move] == min(final_list_dict.values()):
                final_list.append(move)
        return random.choice(final_list)





     
    
    
def play_game_1_player_human_leads(strat=surrounders_random_1, team1=1, team2=2, board=cf.Board(1,2)):
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
 
def play_game_1_player_comp_leads(strat=surrounders_random_3, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        board.add_move(strat(team2,team1,board),team2)
        print board.arr
        if board.check_four_alternate(team2):
            print 'computer wins!!!!!'
            return 
        elif board.accessible_open_threes(team2):
            print '###### CHECK #######'
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team1):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team1)
        print board.arr
        if board.check_four_alternate(team1):
            print 'human wins!!!!!'
            return  
        elif board.accessible_open_threes(team1):
            print '###### CHECK #######'
    print 'its a draw!!!!!'
        
     
def comp_play_comp(strat1=surrounders_random_3,strat2=surrounders_random_1,team1=1,team2=2):
    board = cf.Board(team1,team2)
    for i in range(21):
        board.add_move(strat1(team1,team2,board),team1)
        print board.arr
        if board.check_four_alternate(team1):
            print 'team 1 wins!!!!!'
            return 1
        board.add_move(strat2(team2,team1,board),team2)
        print board.arr
        if board.check_four_alternate(team2):
            print 'team 2 wins!!!!'
            return -1
    print 'it\'s a draw!!!!'

def multiple_games_computer(num, strat1=surrounders_random_3, strat2=surrounders_random_3):
    result = 0
    for i in range(num):
        result += comp_play_comp(strat1, strat2)
    return result


 
    
 
if __name__ == '__main__': 
    play_game_1_player_comp_leads()
    # comp_play_comp()
    # print multiple_games_computer(2)           
    
    #computer_play_computer()
    
    
    
    