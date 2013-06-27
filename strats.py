import random
import copy
import connectfour as cf
from collections import defaultdict
from pprint import pprint

## count, map, dir, reduce

'''this file contains the computer's strategies that will be implemented. the functions are stacked on top of each other, starting
with a minimum function. each function returns a list, and the more complex functions call the previous functions in building their own
lists of potential moves. this file also contains the basic playgame functions, either to play human (with manual input) vs computer,
or a simulation of the computer vs itself with different strategies'''
def minimum(player1,player2,board):
    '''strategy that returns a move only to win the game or if comp is in check. returns a list that will be passed
     to other functions'''
    # if len(board.moves) == 1 and board.moves[0] != 3 or len(board.moves) == 0:
    #     return [3]
    # elif len(board.moves) == 1 and board.moves[0] == 3:
    #     return [2]
    # elif len(board.moves) == 2 and board.moves[1] == 3:
    #     return [2]
    # else:
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

def look_for_two_move_checkmate(player1,player2,board):
    

def gos(player1,player2,board):
    '''if a player has stacked open threes in a column, it should move in that column to force the game. this function
    returns a list of columns with stacked open threes'''
    l = [item[0][0] for item in board.stacked_open_threes(player1,player2)]
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
    stacks1 = len(board.stacked_open_threes(player1,player2))
    newboard = copy.deepcopy(board)
    l = newboard.open_cols[:]
    potential_moves = []
    for move in l:
        newboard.add_move(move,player1)
        if len(newboard.stacked_open_threes(player1,player2)) > stacks1 and newboard.stacked_open_threes(player1,player2)[-1][1] not in newboard.open_three_openings(player2):
            potential_moves.append(move)
        newboard.remove_move(move)
    return potential_moves



def avoid_stacked_open_threes_opp(player1,player2,board):
    stacks2 = len(board.stacked_open_threes(player2,player1))
    newboard = copy.deepcopy(board)
    l = newboard.open_cols[:]
    potential_moves = board.open_cols[:]
    for move in l:
        newboard.add_move(move,player1)
        #pprint(newboard.arr)
        l2 = newboard.open_cols[:]
        for move2 in l2:
            #print move2
            newboard.add_move(move2,player2)
            #pprint(newboard.arr)
            if len(newboard.stacked_open_threes(player2,player1)) > stacks2 and move in potential_moves and newboard.stacked_open_threes(player2,player1)[-1][1] not in newboard.open_three_openings(player1):
                potential_moves.remove(move)
                #print 'this move removed ', move
                #print 'list of potential moves remaining ', potential_moves
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


def surrounders(player1,player2,board,l):
    '''bases move on the surrounders function, taking a list of potential moves as an input, so that it can be implemented
    at any cutoff level'''
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

def utility_function(player1,player2,board,l,weight_center, weight_stacks,weight_open_rows):
    '''look for the move that implements minimax on the utility board function, looking two moves ahead'''
    newboard = copy.deepcopy(board)
    final_list = []
    print 'columns available for moves based on eight cut function above ', l
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
                u = newboard.utility_estimator(player1,player2,weight_center, weight_stacks,weight_open_rows)
                list_of_utilities.append(u)
                newboard.remove_move(col2)
            utility_dict[col1] = min(list_of_utilities)
            newboard.remove_move(col1)
    return utility_dict
    # for col in utility_dict.keys():
    #     if utility_dict[col] == max(utility_dict.values()):
    #         final_list.append(col)
    # print 'final list of moves choosing from based on utility function ', final_list
    # return final_list

def utility_function_simpler(player1,player2,board,l,weights):
    newboard = copy.deepcopy(board)
    final_list = []
    print 'columns available for moves based on eight cut function above ', l
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
                if player1 == 1:
                    u = newboard.utility_estimator_simpler_p1(player1,player2,weights)
                elif player1 == 2:
                    u = newboard.utility_estimator_simpler_p2(player1,player2,weights)
                list_of_utilities.append(u)
                newboard.remove_move(col2)
            utility_dict[col1] = min(list_of_utilities)
            newboard.remove_move(col1)
    return utility_dict



def strat_basic(player1,player2,board, cutoff, show_decision=False):
    first_cut = minimum(player1,player2,board)
    if len(first_cut) == 0:

        print 'minimum function fails to avoid defeat'
        return random.choice(board.open_cols)
    elif len(first_cut) == 1:
        print 'move determined by minimum function'
        return first_cut
    if show_decision:
        print 'past first cut ', first_cut
    second_cut = next_min(player1,player2,board)
    if len(second_cut) == 1:
        print 'move determined by next min function'
        return second_cut
    if show_decision:
        print 'past second cut ', second_cut
    if cutoff == 2:
        return second_cut
    third_cut = avoid_checkmate(player1,player2,board)
    if len(third_cut) == 0:
        print 'no move avoids checkmate'
        return random.choice(board.open_cols)
    if len(third_cut) == 1:
        print 'move determined by checkmate function'
        return third_cut
    if show_decision:
        print 'past third  cut ', third_cut
    if cutoff == 3:
        return third_cut
    fourth_cut = [item for item in third_cut if item in gos(player1,player2,board)]
    if len(fourth_cut) > 0:
        print 'move determined by gos function combined with avoid checkmate function'
        return fourth_cut
    if show_decision:
        print 'past fourth cut ', fourth_cut
    if player1 == 1:
        fifth_cut = [item for item in third_cut if item not in board.no_gos_first_player(player1,player2)]
    else:
        fifth_cut = [item for item in third_cut if item not in board.no_gos_second_player(player1,player2)]
    if len(fifth_cut) == 0:
        fifth_cut = third_cut
    elif len(fifth_cut) == 1:
        print 'move determined to avoid checkmate but not move in a no-go column'
        return fifth_cut
    if show_decision:
        print 'past fifth cut ', fifth_cut
    if cutoff == 5:
        return fifth_cut
    sixth_cut = [item for item in fifth_cut if item in build_stacked_open_threes(player1,player2,board)]
    if len(sixth_cut) > 0:
        print 'move determined to build a stack'
        return sixth_cut
    if show_decision:
        print 'past 6th cut ', sixth_cut

    seventh_cut = [item for item in fifth_cut if item in avoid_stacked_open_threes_opp(player1,player2,board)]
    if len(seventh_cut) == 1:
        print 'move determined to avoid an opponents stack'
        return seventh_cut
    elif len(seventh_cut) == 0:
        seventh_cut = fifth_cut
    if show_decision:
        print 'past 7th cut ', seventh_cut
    if cutoff == 7:
        return seventh_cut
    eight_cut = [item for item in seventh_cut if item in avoid_three_in_open_row(player1,player2,board)]
    if len(eight_cut) == 0:
        eight_cut = seventh_cut
    elif len(eight_cut) == 1:
        print 'move determined to avoid an open row of three for opponent'
        return eight_cut
    if show_decision:

        print 'eight_cut ', eight_cut

    return eighth_cut

def strat_utility(player1,player2,board,weights,show_decision=False):
    u1,u2,u3 = weights
    available_moves = strat_basic(player1,player2,board,show_decision=True)
    list_of_maximum_utility_moves = []
    if len(available_moves) == 1:
        print 'utility function not called'
        return available_moves[0]
    dictionary_of_moves = utility_function(player1,player2,board,available_moves,u1,u2,u3)
    print 'this is the utility function dictionary ', dictionary_of_moves
    for col in dictionary_of_moves.keys():
        if dictionary_of_moves[col] == max(dictionary_of_moves.values()):
            list_of_maximum_utility_moves.append(col)
    print 'final list of moves choosing from based on utility function ', list_of_maximum_utility_moves
    return random.choice(list_of_maximum_utility_moves)

def strat_utility_simpler(player1,player2,board,weights,cutoff,show_decision=False):
    available_moves = strat_basic(player1,player2,board,cutoff,show_decision=True)
    list_of_maximum_utility_moves = []
    if len(available_moves) == 1:
        print 'utility function not called'
        return available_moves[0]
    dictionary_of_moves = utility_function_simpler(player1,player2,board,available_moves,weights)
    print 'this is the utility function dictionary ', dictionary_of_moves
    for col in dictionary_of_moves.keys():
        if dictionary_of_moves[col] == max(dictionary_of_moves.values()):
            list_of_maximum_utility_moves.append(col)
    print 'final list of moves choosing from based on utility function ', list_of_maximum_utility_moves
    return random.choice(list_of_maximum_utility_moves)


## change
#def strat_utility

def comp_play_comp(weights_team_1,weights_team_2,strat1=strat_utility_simpler,strat2=strat_utility_simpler,team1=1,team2=2):
    board = cf.Board(team1,team2)
    for i in range(21):
        print 'utility function for player 1', board.utility_estimator_simpler_p1(1,2,weights_team_1,toPrint=True)
        board.add_move(strat1(team1,team2,board,weights_team_1,7),team1)
        print 'number of moves so far: ', len(board.moves)
        pprint(board.arr)
        if board.check_four_alternate(team1):
            print 'team 1 wins!!!!!'
            return 1
        print 'utility function for player 2', board.utility_estimator_simpler_p2(2,1,weights_team_2,toPrint=True)
        board.add_move(strat2(team2,team1,board,weights_team_2,7),team2)
        print 'number of moves so far: ', len(board.moves)
        pprint(board.arr)
        if board.check_four_alternate(team2):
            print 'team 2 wins!!!!'
            return -1
    print 'it\'s a draw!!!!'
    return 0


def play_game_1_player_comp_leads(weights, strat=strat_utility_simpler, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        print 'utility estimator for comp '
        print board.utility_estimator_simpler_p1(team1,team2,weights,toPrint=True)
        board.add_move(strat(team1,team2,board,weights,7),team1)
        pprint(board.arr)
        if board.check_four_alternate(team1):
            print 'computer wins!!!!!'
            return
        elif board.accessible_open_threes(team1):
            print '###### CHECK #######'
        print 'utility estimator for human '
        print board.utility_estimator_simpler_p2(team2,team1,weights,toPrint=True)
        print 'utility estimator for comp, should be - of above'
        print board.utility_estimator_simpler_p1(team1,team2,weights,toPrint=True)
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team2):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team2)
        pprint(board.arr)
        if board.check_four_alternate(team2):
            print 'human wins!!!!!'
            return
        elif board.accessible_open_threes(team2):
            print '###### CHECK #######'
    print 'its a draw!!!!!'

def play_game_1_player_human_leads(weights,strat=strat_utility_simpler,team1=1,team2=2):
    board=cf.Board(1,2)
    for i in range(21):
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team1):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team1)
        pprint(board.arr)
        if board.check_four_alternate(team1):
            print 'human wins!!!!!'
            return
        elif board.accessible_open_threes(team1):
            print '###### CHECK #######'
        print 'utility estimator for human '
        print board.utility_estimator_simpler_p1(team1,team2,weights,toPrint=True)
        board.add_move(strat(team2,team1,board,weights,7),team2)
        pprint(board.arr)
        if board.check_four_alternate(team2):
            print 'computer wins!!!!!'
            return
        elif board.accessible_open_threes(team2):
            print '###### CHECK #######'
        print 'utility estimator for comp '
        print board.utility_estimator_simpler_p2(team2,team1,weights,toPrint=True)

        
    print 'its a draw!!!!!'


def multiple_games_computer(num,strat1=strat_utility, strat2=strat_utility):
    result = 0
    for i in range(num):
        result += comp_play_comp(strat1, strat2)
    return result

#### changed!!!!
if __name__ == '__main__':
    #play_game_1_player_comp_leads((1,20,0))
    play_game_1_player_human_leads((1,20,0))
    #comp_play_comp((1,20,0),(1,20,0))
    #print multiple_games_computer(4,8,16)
    #print which_strat_simulation(1)

    #computer_play_computer()
