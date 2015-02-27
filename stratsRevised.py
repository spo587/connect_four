import random
import copy
import cf_revised as cf
from collections import defaultdict
from pprint import pprint

## TODO: add CHECK feature
## try different variations of strategy

def minimax(Board, depth, movingPlayer, otherPlayer): 
    if Board.check_four_alternate(Board.player1):
        return 100
    elif Board.check_four_alternate(Board.player2):
        return -100
    elif depth == 0:  
        return 0
    if movingPlayer == Board.player1: 
        bestVal = -100
        moves = Board.opencols()[:]
        for i in range(len(moves)):
            move = moves[i]
            Board.add_move(move, movingPlayer)
            val = minimax(Board, depth - 1, Board.player2, Board.player1)
            Board.remove_move(move)
            bestVal = max(val, bestVal)
        return bestVal
    else:
        movingPlayer = Board.player2
        bestVal = 100
        moves = Board.opencols()[:]
        for i in range(len(moves)):
            move = moves[i]
            Board.add_move(move, movingPlayer)
            #print 'new moves sequence ', newMoves
            val = minimax(Board, depth - 1, Board.player1, Board.player2) #, maxDepth)
            #val, newMoves = minimax(Board, depth + 1, Board.player1, Board.player2, maxDepth, newMoves)
            Board.remove_move(move)
            bestVal = min(val, bestVal)
        return bestVal
       
def alphabeta_dict(board, depth, movingPlayer, otherPlayer):
    scores = defaultdict(int)
    moves = board.opencols()[:]
    for i in range(len(moves)):
        move = moves[i]
        board.add_move(move, movingPlayer)
        scores[move] = alphabeta(board, depth, otherPlayer, movingPlayer)
        board.remove_move(move)
    ## correct for looking too far in the future!! if alphabeta depth 4 all return defeats,
    ## then choose move based on alphabeta depth 2 to at least delay
    ## if all scores are the same, must all result in win or defeat. take the move that speeds things up
    if sameValues(scores) and depth > 1:
        #print 're-evaluting alphabeta_dict'
        return alphabeta_dict(board, depth - 2, movingPlayer, otherPlayer)
    return scores

def sameValues(dictionary):
    if len(set(dictionary.values())) == 1:
        return True
    return False


def make_alphabeta_move(board, depth, movingPlayer, otherPlayer):
    if movingPlayer == board.player1:
        return maxDict(alphabeta_dict(board, depth, movingPlayer, otherPlayer))
    else:
        return minDict(alphabeta_dict(board, depth, movingPlayer, otherPlayer))

def maxDict(dictionary):
    l = []
    for k in dictionary:
        if dictionary[k] == max(dictionary.values()):
            l.append(k)
    print l
    return random.choice(l)

def minDict(dictionary):
    l = []
    for k in dictionary:
        if dictionary[k] == min(dictionary.values()):
            l.append(k)
    print l
    return random.choice(l)


def alphabeta(Board, depth, movingPlayer, otherPlayer, alpha=-1000, beta=1000):
    if Board.check_four_alternate(Board.player1): 
        return 1000
    elif Board.check_four_alternate(Board.player2):
        return -1000
    elif depth == 0:
        #return 0
        return utilityEstimator(Board, otherPlayer, movingPlayer)
    if movingPlayer == Board.player1:
        val = -1000
        moves = Board.opencols()[:]
        #print 'available moves at depth ', moves, depth
        for i in range(len(moves)):
            move = moves[i]
            Board.add_move(move, Board.player1)
            #print 'move just made by player 1 ', move
            #pprint(Board.arr)
            val = max(val, alphabeta(Board, depth - 1, Board.player2, Board.player1, alpha, beta))
            Board.remove_move(move)
            alpha = max(alpha, val)
            if beta < alpha:
                #print 'breaking '
                break

        return val
    else:
        #movingPlayer = Board.player2
        val = 1000
        moves = Board.opencols()[:]
        #print 'available moves at depth ', moves, depth
        for i in range(len(moves)):
            move = moves[i]
            Board.add_move(move, Board.player2)
            #print 'move just made by player 2 ', move
            #pprint(Board.arr)
            val = min(val,alphabeta(Board, depth - 1, Board.player1, Board.player2, alpha, beta))
            Board.remove_move(move)
            beta = min(beta, val)
            if beta < alpha:
                #print 'breaking '
                break

        return val

def utilityEstimator(board, movingPlayer, otherPlayer):
    ## count number of moves on board
    numMovesMade = board.numMoves()

    ## stacks
    stacksMovingPlayer = board.gos(movingPlayer, otherPlayer)
    stacksOtherPlayer = board.gos(otherPlayer, movingPlayer)
    stacksScore = len(stacksMovingPlayer) - len(stacksOtherPlayer)
    if stacksScore != 0:
        ## might have to change this, not all stacks are great
        #print 'returning from stacks'
        return stacksScore * 100
    ## total threats
    # totalThreatsMovingPlayer = board.countThreats(movingPlayer)
    # totalThreatsOtherPlayer = board.countThreats(otherPlayer)
    ## column control: count up threats that are lowest whatever column they're in, not counting lowest square
    controllingThreatsMovingPlayer = board.numberTotalControllingThreats(movingPlayer,otherPlayer)
    controllingThreatsOtherPlayer = board.numberTotalControllingThreats(otherPlayer,movingPlayer)
    threatsScore = (controllingThreatsMovingPlayer - controllingThreatsOtherPlayer)
    #print 'threatsScore ', threatsScore

    ## end threats, controlling odd threats for player1, controlling even threats for player2
    if movingPlayer == board.player1:
        endUtility = board.controlEnd(movingPlayer, otherPlayer)
    else:
        endUtility = - board.controlEnd(otherPlayer, movingPlayer)
    #print 'endUtility ', endUtility

    centerUtility = board.centerScore(movingPlayer, otherPlayer)
    # #print 'center utility ', centerUtility

    # ## blackout squares just above an opponent's threats
    foursUtilityMoving = board.foursUtility(movingPlayer, otherPlayer)
    foursUtilityOther = board.foursUtility(otherPlayer, movingPlayer)
    foursUtility = foursUtilityMoving - foursUtilityOther

    if movingPlayer == board.player1:
        ## surrounders
        
        #print stacks
        #print 'final ', movingPlayer, (endUtility + foursUtility + centerUtility + threatsScore)
        return (endUtility + centerUtility + threatsScore + foursUtility)

    else:
        #print 'final ', movingPlayer, - (endUtility + centerUtility + foursUtility + threatsScore)
        return  -(endUtility + centerUtility + threatsScore + foursUtility)

def strat1(board, player1, player2):
    '''uses alphabeta with depth 3 for the first 10 moves, then depth four, and uses the utility estimator for leaves
    of the alphabeta tree'''
    if board.numMoves() == 0:
        return 3
    if board.numMoves() < 10:
        return make_alphabeta_move(board,3,player1,player2)
    else:
        return make_alphabeta_move(board, 4, player1, player2)

def comp_play_comp(strat1, strat2,team1=1,team2=2):
    board = cf.Board(team1,team2)
    for i in range(21):
        move1 = strat1(board, team1, team2)
        board.add_move(move1,team1)
        print 'last move ', move1
        pprint(board.arr)
        if board.check_four_alternate(team1):
            print 'team 1 wins!!!!!'
            return 1
        move2 = strat1(board, team2, team1)
        board.add_move(move2, team2)
        print 'last move ', move2
        pprint(board.arr)
        if board.check_four_alternate(team2):
            print 'team 2 wins!!!!'
            return -1
    print 'it\'s a draw!!!!'
    return 0

def play_game_1_player_comp_leads(weights, strat=strat1, team1=1, team2=2, board=cf.Board(1,2)):
    for i in range(21):
        #print 'utility estimator for comp '
        #print board.utility_estimator_simpler_p1(team1,team2,weights,toPrint=True)
        move = strat(board, team1, team2)
        board.add_move(move, team1)
        print 'computers move ', move
        pprint(board.arr)
        if board.check_four_alternate(team1):
            print 'computer wins!!!!!'
            return
        #elif board.accessible_open_threes(team1):
        #    print '###### CHECK #######'
        #print 'utility estimator for human '
        #print board.utility_estimator_simpler_p2(team2,team1,weights,toPrint=True)
        #print 'utility estimator for comp, should be - of above'
        #print board.utility_estimator_simpler_p1(team1,team2,weights,toPrint=True)
        if not board.add_move(int(raw_input('team 1, your move, plz:  ')),team2):
            board.add_move(int(raw_input('team 1, your move, plz:  ')),team2)
        pprint(board.arr)
        if board.check_four_alternate(team2):
            print 'human wins!!!!!'
            return
        #elif board.accessible_open_threes(team2):
        #    print '###### CHECK #######'
    print 'its a draw!!!!!'


if __name__ == '__main__':
    #play_game_1_player_comp_leads((1,20,0))
    #play_game_1_player_human_leads((1,20,0))
    comp_play_comp(strat1, strat1)
    #print multiple_games_computer(4,8,16)
    #print which_strat_simulation(1)

    #computer_play_computer()
