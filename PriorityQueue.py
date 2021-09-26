# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any
from gridworld import Cell, Gridworld


class PrioritizedItem():
    def __init__(self, priority, cell):            
        self.priority = priority
        self.item = cell

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
  
    def isEmpty(self):
        return len(self.queue) == 0
  
    def insert(self, data):
        self.queue.append(data)
  
    def delete(self):
        max = 0
        for i in range(len(self.queue)):
            current_item = self.queue[i]
            max_item = self.queue[max]
            if current_item.priority > max_item.priority:
                max = i
        item = self.queue[max]
        del self.queue[max]
        return item