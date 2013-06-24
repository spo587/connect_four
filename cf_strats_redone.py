import random
import copy
import connectfour as cf
from collections import defaultdict

## TODO: fix bug that occurs when a row is filled and computer is forced to make a move, it makes human choose another move
## instead....very smart
##TODO: still a minor bug in surrounders function, it's 1 too high sometimes
## TODO: major bug in the naive strategy, not sure why
def minimum(comp,human,board):
    '''strategy that returns a move only to win the game or if comp is in check. returns a list that will be passed
     to other functions'''
    if len(board.moves) == 1 and board.moves[0] != 3 or len(board.moves) == 0:
        return [3]
    elif len(board.moves) == 1 and board.moves[0] == 3:
        return [2]
    else:
        l = board.open_cols[:]
        forces = []
        for col in l:
            if board.check_move_win(col,comp):
                print col
                return [col]
        for col in l:
            if board.check_move_win(col,human):
                forces.append(col)
        if len(forces) == 1:
            print forces[0]
            return [forces[0]]
        elif len(forces) > 1:
            print 'minimum function fails to find a move to avoid defeat. must be checkmate'       
        
        return l
    

def next_min(player1,player2,board):
    '''will return a list of moves that will not immediately lose the game, or the list of all open columns if the board
    is in checkmate'''
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
    '''builds on the min strategies to return a list of moves that will not immediately result in checkmate. if a checkmate
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


def test_strategy(player1,player2,board):
    l = avoid_checkmate(player1,player2,board)
    print l
    return l

def build_stacked_open_threes(player1,player2,board):
    stacks1 = len(board.stacked_open_threes(player1))
    l = avoid_checkmate(player1,player2,board)
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
    l = avoid_checkmate(player1,player2,board)
    newboard = copy.deepcopy(board)
    potential_moves = l[:]
    for move in l:
        newboard.add_move(move,player1)
        for move2 in newboard.open_cols:
            newboard.add_move(move2,player2)
            if newboard.stacked_open_threes(player2) > stacks2 and move in potential_moves:
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
        return test_strategy(player1,player2,board)

def surrounders_stacker(player1,player2,board):
    l = test_strategy2(player1,player2,board)
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

def utility_function(player1,player2,board):
    '''look for the move that implements minimax on the utility board function, looking two moves ahead'''
    newboard = copy.deepcopy(board)
    final_list = []
    l = avoid_checkmate(player1,player2,board)[:]
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
                u = newboard.utility_estimator(player1,player2)
                list_of_utilities.append(u)
                newboard.remove_move(col2)
            utility_dict[col1] = min(list_of_utilities)
            newboard.remove_move(col1)
    for col in utility_dict.keys():
        if utility_dict[col] == max(utility_dict.values()):
            final_list.append(col)
    print 'final list of moves choosing from based on utility function ', final_list 
    return final_list

def real_strat(player1,player2,board,number):
    if len(board.moves) < number:
        move = random.choice(surrounders_stacker(player1,player2,board))
        print move
        return move
    else:
        moves = utility_function(player1,player2,board)
        print 'moves from utility function ', moves
        if len(moves) == 1:
            return moves[0]
        if len(moves) > 1:
            fewer_moves = surrounders_builder(player1,player2,board,moves)
            move = random.choice(fewer_moves)
            print 'moves determined by surrounders function from utility function  ', fewer_moves
            print move
            return move











def play_game_1_player_comp_leads(strat=real_strat, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        board.add_move(strat(team2,team1,board,10),team2)
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
    #play_game_1_player_comp_leads()
    #play_game_1_player_human_leads()
    #comp_play_comp()
    #print multiple_games_computer(4,8,16)
    print which_strat_simulation(1)           
    
    #computer_play_computer()

## results: -1 when player1 plays with num = 12 and player2 plays with num = 6
## - 4 when both play with num = 6
## -2 when player1 num = 16 and player2 num = 6
## 0 when player1 num=20 and player2 num=6
## 0 when player1 num=20 and player num = 12
## -4 when both at 20
## 1 when team1 = 8 and team2 = 24
## -4 when team1 = 8 and team2 = 16
        





