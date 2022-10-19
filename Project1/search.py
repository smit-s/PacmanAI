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
def backTrack(currentState,pred,problem):
    #to store final directions to reach goal state
    direction_list=[]
    #backtrack the predecessor map to find the final path from goal to start state                   
    while(currentState[0]!=problem.getStartState()):
        direction_list.append(currentState[1])
        currentState=pred[currentState[0]]
    #reverese the direction list because we want path from start to end.
    direction_list.reverse()
    return direction_list
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    #keeps track of nodes visited
    visited=[]
    #fringe list
    stk=util.Stack()
    #Pushing start position
    stk.push((problem.getStartState(),'start',0))
    #To store the parent
    pred={}
    while(not stk.isEmpty()):
        currentState=stk.pop()
        #Exit loop if goal state reached
        if(problem.isGoalState(currentState[0])):
            break
        #mark current state visited as we will add all successors to fringe list.
        visited.append(currentState[0])
        succ=problem.getSuccessors(currentState[0])
        for each in succ:
            #If successor not already visited only then push in stack
            if each[0] not in visited:
                stk.push(each)
                #this is to keep track of the parent node. We can obtain path to goal from this predecessor map.
                pred[each[0]]=currentState
    #backtrack the predecessor map to find the final path from goal to start state    
    return backTrack(currentState,pred,problem)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    #keeps track of nodes visited
    visited=[]
    #fringe list
    q=util.Queue()
    #Pushing start position
    q.push((problem.getStartState(),'start',0))

    #To store the parent
    pred={}
    while(not q.isEmpty()):
        currentState=q.pop()
        #Exit loop if goal state reached
        if(problem.isGoalState(currentState[0])):
            break
        #mark current state visited as we will add all successors to fringe list.
        visited.append(currentState[0])
        #get successors of current state
        succ=problem.getSuccessors(currentState[0])
        for each in succ:
            #If successor not already visited only then push in queue
            if each[0] not in visited:
                #Because we are doing bfs we dont want to add nodes to fringe which are 
                # already there in the fringe to avoid extra operations, so we mark nodes in fringe, visited.
                visited.append(each[0])
                q.push(each)
                #this is to keep track of the parent node. We can obtain path to goal from this predecessor map.
                pred[each[0]]=currentState
    #backtrack the predecessor map to find the final path from goal to start state    
    return backTrack(currentState,pred,problem)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #keeps track of nodes visited
    visited=[]
    #fringe list
    q=util.PriorityQueue()
    #Pushing start position
    q.push((problem.getStartState(),'start',0),0)

    #To store the parent
    pred={}
    #To keep track of smallest weighted path
    weights={}
    while(not q.isEmpty()):
        currentState=q.pop()
        #Exit loop if goal state reached
        if(problem.isGoalState(currentState[0])):
            break
        if(currentState[0] not in visited):
            #mark current state visited as we will add all successors to fringe list.
            visited.append(currentState[0])
            #get successors of current state
            succ=problem.getSuccessors(currentState[0])
            for each in succ:
                #If successor not already visited only then push in priority queue
                if each[0] not in visited:
                    #Converting to list ot modify tuple
                    aux=list(each)
                    #Adding weight from previous state.
                    aux[2]+=currentState[2]
                    #If key already present in weights means it has been seen once.
                    #So, update the cost if it is less than previous cost.However current cost is larger then ignore the node.
                    if(aux[0] in weights.keys()):
                        if(aux[2]<weights[aux[0]]):
                            q.push(tuple(aux),aux[2])
                            weights[aux[0]]=aux[2]
                            #this is to keep track of the parent node. We can obtain path to goal from this predecessor map.
                            pred[each[0]]=currentState
                    else:
                        #If key not already present in weights then add it.
                        q.push(tuple(aux),aux[2])
                        weights[aux[0]]=aux[2]
                        #this is to keep track of the parent node. We can obtain path to goal from this predecessor map.
                        pred[each[0]]=currentState
    #backtrack the predecessor map to find the final path from goal to start state    
    return backTrack(currentState,pred,problem)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #keeps track of nodes visited
    visited=[]
    #fringe list
    q=util.PriorityQueue()
    #Pushing start position
    q.push((problem.getStartState(),'start',0),0)

    #To store the parent
    pred={}
    #To keep track of smallest weighted path
    weights={problem.getStartState():0}
    while(not q.isEmpty()):
        currentState=q.pop()
        #Exit loop if goal state reached
        if(problem.isGoalState(currentState[0])):
            break
        if(currentState[0] not in visited):
            #mark current state visited as we will add all successors to fringe list.
            visited.append(currentState[0])
            #get successors of current state
            succ=problem.getSuccessors(currentState[0])
            for each in succ:
                #If successor not already visited only then push in priority queue
                if each[0] not in visited:
                    #Converting to list ot modify tuple
                    aux=list(each)
                    #Adding weight from previous state.
                    aux[2]+=currentState[2]
                    #If key already present in weights means it has been seen once.
                    #So, update the cost with heuristics if it is less than previous cost.However current cost is larger then ignore the node.
                    if(aux[0] in weights.keys()):
                        if(aux[2]<weights[aux[0]]):
                            q.push(tuple(aux),aux[2]+heuristic(aux[0],problem))
                            #this is to keep track of the parent node. We can obtain path to goal from this predecessor map.
                            pred[each[0]]=currentState
                    else:
                        #If key not already present in weights then add it.
                        q.push(tuple(aux),aux[2]+heuristic(aux[0],problem))
                        weights[aux[0]]=aux[2]
                        #this is to keep track of the parent node. We can obtain path to goal from this predecessor map.
                        pred[each[0]]=currentState
    #backtrack the predecessor map to find the final path from goal to start state    
    return backTrack(currentState,pred,problem)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
