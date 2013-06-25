import random
import copy
import connectfour as cf
from collections import defaultdict

'''this file contains the computer's strategies that will be implemented. the functions are stacked on top of each other, starting
with a minimum function. each function returns a list, and the more complex functions call the previous functions in building their own
lists of potential moves. this file also contains the basic playgame functions, either to play human (with manual input) vs computer,
or a simulation of the computer vs itself with different strategies'''
def minimum(player1,player2,board):
    '''strategy that returns a move only to win the game or if comp is in check. returns a list that will be passed
     to other functions'''
    if len(board.moves) == 1 and board.moves[0] != 3 or len(board.moves) == 0:
        return [3]
    elif len(board.moves) == 1 and board.moves[0] == 3:
        return [2]
    elif len(board.moves) == 2 and board.moves[1] == 3:
        return [2]
    else:
        l = board.open_cols[:]
        forces = []
        for col in l:
            if board.check_move_win(col,player1):
                print col
                return [col]
        for col in l:
            if board.check_move_win(col,player2):
                forces.append(col)
        if len(forces) == 1:
            print forces[0]
            return [forces[0]]
        elif len(forces) > 1:
            print 'minimum function fails to find a move to avoid defeat. must be checkmate'       
        
        return l
    

def next_min(player1,player2,board):
    '''will return a list of moves that will not immediately lose the game, or the list of all open columns if the board
    is in checkmate for player2'''
    newboard = copy.deepcopy(board)
    l = minimum(player1,player2,newboard)
    if len(l) == 1:
        return l
    else:
        list_moves = []
        for col in l:
            newboard.add_move(col,player1)
            if newboard.check_move_win(col,player2) is False:
                list_moves.append(col)
            newboard.remove_move(col)
        if len(list_moves) == 1:
            print 'move determined by next_min function to avoid defeat on the next play'
            return list_moves
        
        elif len(list_moves) == 0:
            print 'all moves result in defeat in the next-min function on the next move'
            return board.open_cols
        else:
            return list_moves


def avoid_checkmate(player1,player2,board):
    '''builds on the min strategies to return a list of moves that will not then immediately result in checkmate. if a checkmate
    move is available, returns it in a list of length 1'''
    l = next_min(player1,player2,board)
    if len(l) == 1:
        return l
    else:
        move = board.checkmate_moves(player1,player2)
        if move is not False:
            return [move]
        else:
            potential_moves = l[:]
            list_moves_to_remove = []
            newboard = copy.deepcopy(board)
            for col in l:
                newboard.add_move(col,player1)
                if newboard.checkmate_moves(player2,player1) is not False:
                    list_moves_to_remove.append(col)
                newboard.remove_move(col)
            if len(list_moves_to_remove) > 0:
                for move in list_moves_to_remove:
                    potential_moves.remove(move)
            if len(potential_moves) > 0:
                return potential_moves
            else:
                print 'no move avoids checkmate, but the game can perhaps be extended by putting in check'

                return l

def avoid_three_in_open_row(player1,player2,board):
    '''returns all moves that will avoid the opponent building three in an open row with 0's on either side'''
    if len(board.moves) < 4:
        return range(board.width)
    newboard = copy.deepcopy(board)
    l = newboard.open_cols[:]
    final_list = []
    for col in l:
        newboard.add_move(col,player2)
        for tup in newboard.open_three_openings(player2):
            if (tup[0] + 4, tup[1]) in newboard.open_three_openings(player2):
                final_list.append(col)
        newboard.remove_move(col)
    other_list = avoid_checkmate(player1,player2,board)
    if len(final_list) > 0:
        for item in final_list:
            if item not in other_list:
                final_list.remove(item)
        return final_list
    else:
        return l

def gos(player1,player2,board):
    '''if a player has stacked open threes in a column, it should move in that column to force the game. this function
    returns a list of columns with stacked open threes'''
    l = [item[0][0] for item in board.stacked_open_threes(player1)]
    l2 = list(set(l))
    return l2



def no_gos(player1,player2,board):
    '''if a move by player2 in a column results in a win for player1, then player1 should not go in that column, unless it
    has open three indices stacked on top of each other. this function
    eliminates those columns and returns list of available moves without them included'''
    newboard = copy.deepcopy(board)
    l = newboard.open_cols[:]
    list_of_no_gos = []
    for move in l:
        newboard.add_move(move,player2)
        if newboard.check_move_win(move,player1) is not False and move not in gos(player1,player2,board):
            list_of_no_gos.append(move)
        newboard.remove_move(move)
    for item in list_of_no_gos:
        l.remove(item)
    return l

def gos_avoid_checkmate_combined(player1,player2,board):
    list_of_gos = gos(player1,player2,board)
    if len(list_of_gos) > 0:
        l = [elem for elem in list_of_gos if elem in avoid_checkmate(player1,player2,board)]
        if len(l) > 0:
            return l
    else:
        return avoid_checkmate(player1,player2,board)

def build_stacked_open_threes(player1,player2,board):
    stacks1 = len(board.stacked_open_threes(player1))
    l = gos_avoid_checkmate_combined(player1,player2,board)
    newboard = copy.deepcopy(board)
    potential_moves = []
    for move in l:
        newboard.add_move(move,player1)
        if len(newboard.stacked_open_threes(player1)) > stacks1 and newboard.stacked_open_threes(player1)[-1][1] not in newboard.open_three_openings(player2):
            potential_moves.append(move)
        newboard.remove_move(move)
    return potential_moves

def avoid_stacked_open_threes_opp(player1,player2,board):
    stacks2 = board.stacked_open_threes(player2)
    l = gos_avoid_checkmate_combined(player1,player2,board)
    newboard = copy.deepcopy(board)
    potential_moves = l[:]
    for move in l:
        newboard.add_move(move,player1)
        for move2 in newboard.open_cols:
            newboard.add_move(move2,player2)
            if newboard.stacked_open_threes(player2) > stacks2 and move in potential_moves and newboard.stacked_open_threes(player2)[-1][1] not in newboard.open_three_openings(player1):
                potential_moves.remove(move)
            newboard.remove_move(move2)
        newboard.remove_move(move)
    return potential_moves

def test_strategy2(player1,player2,board):
    l1 = build_stacked_open_threes(player1,player2,board)
    l2 = avoid_stacked_open_threes_opp(player1,player2,board)
    if len(l1) > 0:
        print 'building a stack'
        return l1
    elif len(l2) > 0:
        print l2
        return l2
    else:
        print 'no move avoids stack for opponent?'
        return gos_avoid_checkmate_combined(player1,player2,board)

def surrounders_stacker(player1,player2,board):
    '''bases move on the surrounders function, subject to the checkmate constraint, the stacker constraint, and the open row constraint'''
    l = test_strategy2(player1,player2,board) 
    print 'modified list comprehension dealy ', l
    newboard = copy.deepcopy(board)
    dictionary_of_moves = {}
    for move in l:
        dictionary_of_moves[move] = 0   
    for col in dictionary_of_moves.keys():

        value = newboard.check_move_surrounders(col,player1)
        dictionary_of_moves[col] = value
    print dictionary_of_moves
    final_list = []
    ## find the dictionary value with the maximum score and put it in the list
    for col in dictionary_of_moves.keys():
        if dictionary_of_moves[col] == max(dictionary_of_moves.values()):
            final_list.append(col)
    print 'final potential moves list determined by surrounders function ', final_list
    return final_list


def surrounders_builder(player1,player2,board,l):
    '''takes a list of potential moves as an argument and returns the move with the most surrounders'''
    newboard = copy.deepcopy(board)
    dictionary_of_moves = {}
    for move in l:
        dictionary_of_moves[move] = 0   
    for col in dictionary_of_moves.keys():

        value = newboard.check_move_surrounders(col,player1)
        dictionary_of_moves[col] = value
    print dictionary_of_moves
    final_list = []
    ## find the dictionary value with the maximum score and put it in the list
    for col in dictionary_of_moves.keys():
        if dictionary_of_moves[col] == max(dictionary_of_moves.values()):
            final_list.append(col)
    print 'final potential moves list determined by surrounders function ', final_list
    return final_list




def utility_function(player1,player2,board,weight):
    '''look for the move that implements minimax on the utility board function, looking two moves ahead'''
    newboard = copy.deepcopy(board)
    final_list = []
    l = gos_avoid_checkmate_combined(player1,player2,board)[:]
    print 'columns available for moves based on test avoid checkmate function above ', l
    utility_dict = {}
    for col1 in l:
        newboard.add_move(col1,player1)
        l2 = newboard.open_cols[:]
        if len(l2) == 0:
            return l
        else:
            # print 'open columns in new hypothetical board ', l2
            list_of_utilities = []
            for col2 in l2:
                newboard.add_move(col2,player2)
                u = newboard.utility_estimator(player1,player2,weight)
                list_of_utilities.append(u)
                newboard.remove_move(col2)
            utility_dict[col1] = min(list_of_utilities)
            newboard.remove_move(col1)
    for col in utility_dict.keys():
        if utility_dict[col] == max(utility_dict.values()):
            final_list.append(col)
    print 'final list of moves choosing from based on utility function ', final_list 
    return final_list

## incorporate in this order: 1. min functions. 2. avoid checkmate 3. force game in go columns 4. build stacked open threes. 
## 5. avoid stacked open threes for opponent. 6. minimax (ish) on board utility, two moves ahead. if early in game,
## prioritize surrounders function. if later, prioritize utility function

def real_strat(player1,player2,board,number):
    if len(board.moves) < number:
        l = [elem for elem in surrounders_stacker(player1,player2,board) if elem in no_gos(player1,player2,board)]
        print 'this is the list in the real_strat function ', l
        if len(l) == 0:
            move = random.choice(surrounders_stacker(player1,player2,board))
            print move
            return move
        else:
            move = random.choice(l)
            print move
            return move
    else:
        ## set the utility stack weight to 3 or else to whatever you please
        print 'this is the utility function list ', utility_function(player1,player2,board,3)
        print 'this is the no-gos list ', no_gos(player1,player2,board)

        moves = [elem for elem in utility_function(player1,player2,board,3) if elem in no_gos(player1,player2,board)]
        print 'moves from utility function ', moves
        if len(moves) == 0:
            moves = utility_function(player1,player2,board,3)
            if len(moves) == 1:
                return moves[0]
            elif len(moves) > 1:
                fewer_moves = surrounders_builder(player1,player2,board,moves)
                move = random.choice(fewer_moves)
                print 'moves determined by surrounders function from utility function  ', fewer_moves
                print move
                return move
        elif len(moves) == 1:
            print moves[0]
            return moves[0]
        elif len(moves) > 0:
            fewer_moves = surrounders_builder(player1,player2,board,moves)
            move = random.choice(fewer_moves)
            print 'moves determined by surrounders function from utility function  ', fewer_moves
            print move
            return move













def play_game_1_player_comp_leads(strat=real_strat, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        board.add_move(strat(team2,team1,board,10),team2,toPrint=True)
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

def play_game_1_player_human_leads(strat=real_strat, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team1):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team1)
        print board.arr
        if board.check_four_alternate(team1):
            print 'human wins!!!!!'
            return  
        
        board.add_move(strat(team2,team1,board,10),team2)
        print board.arr
        if board.check_four_alternate(team2):
            print 'computer wins!!!!!!!'
            return 
    print 'it\'s a draw!!!!!'
    return 


def comp_play_comp(cutoff1,cutoff2,strat1=real_strat,strat2=real_strat,team1=1,team2=2):
    board = cf.Board(team1,team2)
    for i in range(21):
        board.add_move(strat1(team1,team2,board,cutoff1),team1,toPrint=True)
        print 'number of moves so far: ', len(board.moves)
        print board.arr
        if board.check_four_alternate(team1):
            print 'team 1 wins!!!!!'
            return 1
        board.add_move(strat2(team2,team1,board,cutoff2),team2,toPrint=True)
        print 'number of moves so far: ', len(board.moves)
        print board.arr
        if board.check_four_alternate(team2):
            print 'team 2 wins!!!!'
            return -1
    print 'it\'s a draw!!!!'
    return 0



def multiple_games_computer(num, cutoff1,cutoff2,strat1=real_strat, strat2=real_strat):
    result = 0
    for i in range(num):
        result += comp_play_comp(strat1, strat2)
    return result

def which_strat_simulation(numgames_per):
    results_dict = defaultdict(int)
    cut_off1 = 0
    
    while cut_off1 < 21:
        cut_off2 = 0
        while cut_off2 < 21:
            results_dict[(cut_off1,cut_off2)] = multiple_games_computer(numgames_per,cut_off1,cut_off2)
            cut_off2 += 2
            print 'cut off point for player 2 is now ', cut_off2
            print 'results dict so far  ', results_dict
        cut_off1 += 2
        print 'cut off point for player 1 is now ', cut_off1
        print 'results dict so far  ', results_dict
    return results_dict

if __name__ == '__main__': 
    play_game_1_player_comp_leads()
    #play_game_1_player_human_leads()
    #comp_play_comp()
    #print multiple_games_computer(4,8,16)
    #print which_strat_simulation(1)           
    
    #computer_play_computer()

## results: -1 when player1 plays with num = 12 and player2 plays with num = 6
## - 4 when both play with num = 6
## -2 when player1 num = 16 and player2 num = 6
## 0 when player1 num=20 and player2 num=6
## 0 when player1 num=20 and player num = 12
## -4 when both at 20
## 1 when team1 = 8 and team2 = 24
## -4 when team1 = 8 and team2 = 16
        





