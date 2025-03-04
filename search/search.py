# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    listStack = util.Stack()

    visited = []
    path = []
    actionCost = 0

    startPos = problem.getStartState()

    listStack.push((startPos, path, actionCost))

    while not listStack.isEmpty():

        currentNode = listStack.pop()
        path = currentNode[1]
        pos = currentNode[0]

        if pos not in visited:
            visited.append(pos)

        if problem.isGoalState(pos):
            return path

        successors = problem.getSuccessors(pos)

        for successor in successors:
            if successor[0] not in visited:

                newPos = successor[0]
                newPath = path + [successor[1]]
                listStack.push((newPos, newPath, successor[2]))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    listQueue = util.Queue()

    visited = []
    path = []
    actionCost = 0 

    startPos = problem.getStartState()

    listQueue.push((startPos, path, actionCost))

    while not listQueue.isEmpty():

        currentNode = listQueue.pop()
        path = currentNode[1]
        pos = currentNode[0]

        if pos not in visited:
            visited.append(pos)

        if problem.isGoalState(pos):
            return path

        successors = problem.getSuccessors(pos)

        for successor in successors:
            if successor[0] not in visited and successor[0] not in (node[0] for node in listQueue.list):

                newPos = successor[0]
                newPath = path + [successor[1]]
                listQueue.push((newPos, newPath, successor[2]))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    listPriorityQueue = util.PriorityQueue()

    visited = []
    path = []
    priority = 0

    startPos = problem.getStartState()

    listPriorityQueue.push((startPos, path), priority)

    while not listPriorityQueue.isEmpty():

        currentNode = listPriorityQueue.pop()
        path = currentNode[1]
        pos = currentNode[0]

        if pos not in visited:
            visited.append(pos)

        if problem.isGoalState(pos):
            return path

        successors = problem.getSuccessors(pos)

        def getPriorityOfNode(priority_queue, node):
            for item in priority_queue.heap:
                if item[2][0] == node:
                    return problem.getCostOfActions(item[2][1])

        for successor in successors:
            if successor[0] not in visited and (successor[0] not in (node[2][0] for node in listPriorityQueue.heap)):
                new_path = path + [successor[1]]
                new_priority = problem.getCostOfActions(new_path)
                listPriorityQueue.push((successor[0], new_path), new_priority)

            elif successor[0] not in visited and (successor[0] in (node[2][0] for node in listPriorityQueue.heap)):
                old_priority = getPriorityOfNode(listPriorityQueue, successor[0])
                new_priority = problem.getCostOfActions(new_path)

                if old_priority > new_priority:
                    new_path = path + [successor[1]]
                    listPriorityQueue.update((successor[0], new_path), new_priority)
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    pQueue = util.PriorityQueue()
    path = []
    visited = []
    startPos = problem.getStartState()
    pQueue.push((startPos, path), 0)

    while not pQueue.isEmpty():
        curNode = pQueue.pop()
        path = curNode[1]
        pos = curNode[0]

        if problem.isGoalState(pos):
            return path

        if pos not in visited:
            visited.append(pos)
            successors = problem.getSuccessors(pos)

            for successor in successors:
                if successor[0] not in visited:
                    newPath = path + [successor[1]]
                    newPos = successor[0]

                    f = problem.getCostOfActions(newPath) + heuristic(newPos, problem)
                    pQueue.push((newPos, newPath), f)
                
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
