import connectfour as cf
import copy
import strategies_connect_four as scf
import random

b = cf.Board(1,2)
print b.arr
print b.arr[0,0]
#assert False

def createrandomboard(nummoves):
	board = cf.Board(1,2)
	while board.check_four_alternate(1) == True or board.check_four_alternate(2) == True or len(board.moves) < 2*nummoves:
		board = cf.Board(1,2)
		l = board.open_cols
		for i in range(nummoves):
			board.add_move(random.choice(board.open_cols),1)
			board.add_move(random.choice(board.open_cols),2)



	return board	


def test_betters(numtrials):
	i = 0
	while i <  numtrials:

		c = createrandomboard(8)
		
		#print better2(1,2,c) == better(1,2,c)
		a = scf.better1(1,2,c)
		b = scf.better2(1,2,c)
		e = scf.better1(2,1,c)
		f = scf.better2(2,1,c)
		print c.arr
		print a == b
		print e == f
		if a!=b:
			print c.arr
			print 'team 1 ', a
			print 'team1 ', b
		if e != f:
			print c.arr
			print 'team2 ', e
			print 'team2  ', f
		i += 1
		

test_betters(15)

[[0 0 0 0 0 0 0]
 [0 0 0 0 0 2 0]
 [0 0 2 0 0 1 0]
 [0 0 2 0 0 2 0]
 [0 0 1 2 0 1 1]
 [2 1 2 1 1 2 1]]
team 1  [3, 4] --  better1
team1  [0, 1, 2, 3, 4, 5, 6]   --better2

[[0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0]
 [0 0 0 0 0 2 0]
 [1 1 0 0 0 1 0]
 [2 1 2 0 2 1 0]
 [1 2 1 2 2 2 1]]
team2  [0, 1, 2, 4, 5, 6]  -- better1
team2   [0, 1, 2, 3, 4, 5, 6] --better2

[[0 2 0 0 0 0 0]
 [0 1 0 0 0 0 0]
 [0 1 0 0 0 0 0]
 [2 2 0 0 1 0 0]
 [1 1 0 0 2 0 0]
 [2 1 2 2 1 2 1]]
team2  [2, 3] --better1
team2   [0, 2, 3, 4, 5, 6] --better2


#[[0 0 0 0 0 0 0]
 #[0 0 0 1 1 0 0]
 #[0 0 0 2 2 0 0]
 #[0 0 0 2 1 0 0]
 #[0 0 0 1 2 0 0]
 #[0 2 0 2 1 0 0]]

 
##check strategy functions on this board!!!
 # [[0 0 0 1 0 0 0]
 # [0 0 0 2 0 0 0]
 # [0 0 1 1 1 0 0]
 # [0 0 2 2 1 0 0]
 # [0 0 2 1 2 0 0]
 # [0 2 1 2 1 2 0]]

b.add_move(1,2)
b.add_move(2,1)
b.add_move(2,2)
b.add_move(2,2)
b.add_move(2,2)
b.add_move(3,2)
b.add_move(3,1)
b.add_move(3,2)
b.add_move(3,1)
b.add_move(3,2)
b.add_move(3,1)
b.add_move(4,1)

b.add_move(4,1)
b.add_move(4,2)
b.add_move(4,2)
b.add_move(5,2)

print b.arr
print b.open_three_openings(2)
print b.check_four_alternate(2)	
# print scf.better(2,1,b)
# print scf.better2(2,1,b,toPrint=True)


## testing new check_available_three and ccheck_four_alternate functions
# b.add_move(3,2)
# b.add_move(3,1)
# b.add_move(3,2)
# b.add_move(3,2)
# b.add_move(3,1)
# b.add_move(4,1)
# b.add_move(4,2)
# b.add_move(4,1)
# b.add_move(4,2)
# b.add_move(4,1)
# b.add_move(1,2)
# b.add_move(2,1)
# b.add_move(2,2)
# b.add_move(1,2)
# for i in range(3):
# 	b.add_move(1,1)

# b.add_move(2,2)
# b.add_move(2,1)
# b.add_move(2,1)


# print b.arr	

# print b.check_open_three(1)
# print b.check_four_alternate(1)




# b.add_move(3,2)
# b.add_move(2,1)
# b.add_move(4,1)
# # for i in range(2):
# #     b.add_move(2,2)
# #     
# # for i in range(2):
# b.add_move(4,1)
# b.add_move(3,1)
# b.add_move(2,1)


    

# for i in range(3):
# 	b.add_move(2,2)
# 	b.add_move(3,2)
# 	b.add_move(4,2)

# b.add_move(2,1)
# b.add_move(3,1)
# b.add_move(4,1)

# print b.arr

# print scf.better(2,1,b)

# # print b.open_cols

# # l = []

# # for col in b.open_cols:
	
# # 	print col
# # 	b.add_move(col,2)
# # 	print b.arr
# # 	print b.check_move_win(col,1)
# # 	if b.check_move_win(col,1):
# # 		l.append(col)
		
# # 	b.remove_move(col)
# # print l
# # for col in l:
# # 	b.open_cols.remove(col)
# # print b.open_cols

# # b.add_move(5,2)
# # print b.arr
# # print b.check_move_win(5,1)

