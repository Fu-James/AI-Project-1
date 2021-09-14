from func_Astar import *

testmaze = np.zeros([5,5])
testmaze[1,2]=1
testmaze[2,2]=1
testmaze[2,3]=1
testmaze[3,2]=1
testmaze[3,3]=1
testmaze[4,3]=1
print(testmaze)

dim=5
start = Cell(0,0,0,dim,None)
result = func_Astar(start, [dim-1,dim-1] , testmaze, dim = dim )

##track back the path
print('----------path (backwards)--------')
print(result.getIndex())
while result.parent is not None:
  result = result.parent
  print(result.getIndex())