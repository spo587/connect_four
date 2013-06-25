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

def build_stacked_open_threes(player1,player2,board):
    stacks1 = len(board.stacked_open_threes(player1))
    newboard = copy.deepcopy(board)
    l = newboard.open_cols[:]
    potential_moves = []
    for move in l:
        newboard.add_move(move,player1)
        if len(newboard.stacked_open_threes(player1)) > stacks1 and newboard.stacked_open_threes(player1)[-1][1] not in newboard.open_three_openings(player2):
            potential_moves.append(move)
        newboard.remove_move(move)
    return potential_moves

## wtf is going on with this ridiculous bug!!!!!!!!!!
#and newboard.stacked_open_threes(player2)[-1][1] not in newboard.open_three_openings(player1):

def avoid_stacked_open_threes_opp(player1,player2,board):
	stacks2 = len(board.stacked_open_threes(player2))
	newboard = copy.deepcopy(board)
	l = newboard.open_cols[:]
	potential_moves = board.open_cols[:]
	for move in l:
		newboard.add_move(move,player1)
		#print newboard.open_cols
		l2 = newboard.open_cols[:]
		for move2 in l2:
			#print move2
			newboard.add_move(move2,player2)
			#print newboard.arr
			if len(newboard.stacked_open_threes(player2)) > stacks2 and move in potential_moves and newboard.stacked_open_threes(player2)[-1][1] not in newboard.open_three_openings(player1):
				potential_moves.remove(move)
			#print 'potential moves list', potential_moves
			newboard.remove_move(move2)
		newboard.remove_move(move)
	return potential_moves



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

    if len(final_list) > 0:
        return final_list
    else:
        return l


def surrounders_stacker(player1,player2,board,l):
    '''bases move on the surrounders function, subject to the checkmate constraint, the stacker constraint, and the open row constraint'''
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

def utility_function(player1,player2,board,l,weight):
    '''look for the move that implements minimax on the utility board function, looking two moves ahead'''
    newboard = copy.deepcopy(board)
    final_list = []
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


def strat(player1,player2,board, show_decisions=False):
	first_cut = minimum(player1,player2,board)
	if len(first_cut) == 0:
		print 'minimum function fails to avoid defeat'
		return random.choice(board.open_cols)
	elif len(first_cut) == 1:
		print 'move determined by minimum function'
		return first_cut[0]
    if show_decision:
        print 'past first cut'
	second_cut = next_min(player1,player2,board)
	if len(second_cut) == 1:
		print 'move determined by next min function'
		return second_cut[0]
    if show_decision:
        print 'past second cut'
	third_cut = avoid_checkmate(player1,player2,board)
	if len(third_cut) == 0:
		print 'no move avoids checkmate'
		return random.choice(board.open_cols)
	if len(third_cut) == 1:
		print 'move determined by checkmate function'
		return third_cut[0]
    if show_decision:
        print 'past third  cut'
	fourth_cut = [item for item in third_cut if item in gos(player1,player2,board)]
	if len(fourth_cut) > 0:
		print 'move determined by gos function combined with avoid checkmate function'
		return random.choice(fourth_cut)
    if show_decision:
        print 'past fourth cut'
	fifth_cut = [item for item in third_cut if item in no_gos(player1,player2,board)]
	if len(fifth_cut) == 0:
		fifth_cut = third_cut
	elif len(fifth_cut) == 1:
		print 'move determined to avoid checkmate but not move in a no-go column'
		return fifth_cut[0]
	sixth_cut = [item for item in fifth_cut if item in build_stacked_open_threes(player1,player2,board)]
	if len(sixth_cut) > 0:
		print 'move determined to build a stack'
		return random.choice(sixth_cut)
	seventh_cut = [item for item in fifth_cut if item in avoid_stacked_open_threes_opp(player1,player2,board)]
	if len(seventh_cut) == 1:
		print 'move determined to avoid an opponents stack'
		return seventh_cut[0]
	elif len(seventh_cut) == 0:
		seventh_cut = fifth_cut
	eight_cut = [item for item in seventh_cut if item in avoid_three_in_open_row(player1,player2,board)]
	if len(eight_cut) == 0:
		eight_cut = seventh_cut
	elif len(eight_cut) == 1:
		print 'move determined to avoid an open row of three for opponent'
		return eight_cut[0]
	if show_decisions:
		print 'first cut ', first_cut
		print 'second_cut ', second_cut
		print 'third_cut ', third_cut
		print 'fourth_cut ', fourth_cut
		print 'fifth_cut ', fifth_cut
		print 'sixth_cut ', sixth_cut
		print 'seventh_cut ', seventh_cut
		print 'eight_cut ', eight_cut 

	return random.choice(eight_cut)

#def strat_utility


player1 = cf.Player(1)
player2 = cf.Player(2)

def play_game_1_player_comp_leads(strat=strat, team1=player1, team2=player2, board=cf.Board(player1,player2)):
    for i in range(21):
        board.add_move(strat(team2,team1,board,show_decisions=True),team2)
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

if __name__ == '__main__': 
    play_game_1_player_comp_leads()
    #play_game_1_player_human_leads()
    #comp_play_comp()
    #print multiple_games_computer(4,8,16)
    #print which_strat_simulation(1)           
    
    #computer_play_computer()