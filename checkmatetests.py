import connectfour as cf
import copy

b = cf.Board(1,2)

b.add_move(3,1)
b.add_move(1,1)
b.add_move(1,1)
# for i in range(2):
#     b.add_move(2,2)
#     
# for i in range(2):
b.add_move(4,2)
b.add_move(4,1)
b.add_move(2,1)
    
# b.add_move(4,2)
# 
# b.add_move(2,1)
# #b.add_move(2,1)
# b.add_move(3,1)
# b.add_move(4,1)

for i in range(4):
    b.add_move(1,2)

print b.arr

b.remove_move(1)
b.remove_move(2)
print b.arr
# print b.check_open_three(1)
# print b.accessible_open_three(1)
# print b.open_cols

# ## checkmate function tests: fail
# print b.arr
# newboard = copy.deepcopy(b)
# l = [1,2,3,4,5,6]                
# for next_move in range(7):
#     print newboard.check_move_checkmate(next_move,2,1)
#         


#print b.check_move_checkmate(2,1,2)
# 
# print b.arr
# 
# print len(b.indices)

