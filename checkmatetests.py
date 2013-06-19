import connectfour as cf
import copy
import strategies_connect_four as scf

b = cf.Board(1,2)

#[[0 0 0 0 0 0 0]
 #[0 0 0 1 1 0 0]
 #[0 0 0 2 2 0 0]
 #[0 0 0 2 1 0 0]
 #[0 0 0 1 2 0 0]
 #[0 2 0 2 1 0 0]]

b.add_move(3,2)
b.add_move(3,1)
b.add_move(3,2)
b.add_move(3,2)
b.add_move(3,1)
b.add_move(4,1)
b.add_move(4,2)
b.add_move(4,1)
b.add_move(4,2)
b.add_move(4,1)
b.add_move(1,2)

print b.arr	


print scf.better(1,2,b)




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

