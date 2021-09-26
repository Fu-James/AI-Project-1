# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from gridworld import Cell, Gridworld
import math

class PrioritizedItem():
    def __init__(self, priority: int, cell: Cell) -> None:            
        self.priority = priority
        self.item = cell

class PriorityQueue():
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
  
    def is_empty(self):
        return len(self.queue) == 0
  
    def insert(self, item):
        self.queue.append(item)
  
    def delete(self):
        min = 0
        for i in range(len(self.queue)):
            current_item = self.queue[i]
            min_item = self.queue[min]
            if current_item.priority < min_item.priority:
                min = i
        item = self.queue[min]
        del self.queue[min]
        return item