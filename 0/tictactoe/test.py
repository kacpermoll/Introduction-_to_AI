# from tictactoe import actions, player
import numpy as np

# arr = [[None for i in range(3)] for j in range(3)]

# arr = np.array(arr)
# print(np.count_nonzero(arr == None))

arr = [[1, 2, 1],
       [1, 1, 3],
       [1, 2, 2]]

sactionArray = arr
print(sactionArray)
actionArray = [row[:] for row in arr]
print(actionArray)

# actionArray[x][y] = player(board)