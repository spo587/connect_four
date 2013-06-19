def better(comp,human,board):
    l = range(board.width)
    minmove = minimum(comp,human,board)
    if minmove != None:
        print 'move returned by minimum function ', minmove  
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
            print 'move determined by better function ', l[0]
            return l[0]
        else: 
            return l
        