# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        #No need to stop
        if(action=='Stop'):
          return 0
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        mn=1000000
        crd=[]
        #print(newFood.asList())
        curFood=currentGameState.getFood()
        #Find the closest food
        for i in newFood.asList():
          ttl=(abs(i[0]-newPos[0])+abs(i[1]-newPos[1]))
          #Save coordinates and manhattan distance of closest food.
          if(ttl<mn):
            mn=ttl
            crd=i
        
        mndist=10000000
        #get the distance of closest ghost in state.
        for i in range(len(newGhostStates)):
          pos=newGhostStates[i].getPosition()
          manhattan=abs(newPos[0]-pos[0])+abs(newPos[1]-pos[1])
          if(mndist>manhattan):
            mndist=manhattan
        #If the distance becomes 0, the ghost will eat pacman so never choose this state.
        if(mndist==0):
          return 0
        #If the food gets eaten in this state then, always take this state.
        elif(len(curFood.asList())>len(newFood.asList())):
          return 1000000000000
        #if none of above case then, the weight of state where food is closes has to be highest so, taking inverse of distance from food. 
        else:
          return 10000000000/mn

        "*** YOUR CODE HERE ***"

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    #for counting nodes
    nodes=0
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def cmpare(val,newVal,bestAction,legalAction,isMin):
          #If ghost
          if isMin:
            if newVal <= val:
              return newVal, legalAction
          #If pacman
          elif not isMin:
            if newVal >= val:
              return newVal, legalAction
          return val,bestAction
                        
        def MiniMax(gameState, aIndex, depth):
            answerAction = None
            #Get list of all actions.
            next_actions_list = gameState.getLegalActions(aIndex)
            #If win or lose or depth of tree reached then, return response of evaluation function.
            if ( gameState.isWin() or gameState.isLose() or depth == self.depth):
                return [self.evaluationFunction(gameState),0]
            #if all ghost have been visited once and currently we are at last ghost then, reset index and increase depth
            elif aIndex ==  gameState.getNumAgents() - 1:
                depth += 1
                next_index = self.index
            #increase index if all all ghost not yet visited.
            else:
                next_index = aIndex + 1
            #Initializing min and max
            mn = 1000000000
            mx = -1000000000
            #If it is a ghost
            if aIndex != 0:
                for next_action in next_actions_list:
                    self.nodes+=1
                    newVal = MiniMax(gameState.generateSuccessor(aIndex, next_action), next_index, depth)[0]
                    #Find the min among new value and current minimum.
                    mn, answerAction=cmpare(mn,newVal,answerAction,next_action,True)
                return mn, answerAction
            #If it is pacman
            elif aIndex == 0:
                for next_action in next_actions_list:
                    self.nodes+=1
                    newVal = MiniMax(gameState.generateSuccessor(aIndex, next_action), next_index, depth)[0]
                    #Find the maximum among new value and current maximum.
                    mx, answerAction=cmpare(mx,newVal,answerAction,next_action,False)
                return mx, answerAction
        #print(self.nodes)
        return  MiniMax(gameState, self.index,0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    #for counting nodes
    node=0
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def alphaBetaPruning(gameState,aIndex,depth,alpha,beta): 
            answerAction = None
            #Get list of all actions.
            next_actions_list = gameState.getLegalActions(aIndex)
            #If win or lose or depth of tree reached then, return response of evaluation function.
            if ( gameState.isWin() or gameState.isLose() or depth == self.depth):
                return [self.evaluationFunction(gameState),0]
            #if all ghost have been visited once and currently we are at last ghost then, reset index and increase depth
            elif aIndex ==  gameState.getNumAgents() - 1:
                depth += 1
                next_index = self.index
            #increase index if all all ghost not yet visited.
            else:
                next_index = aIndex + 1
            #Initializing alpha, beta, action and value with starting move.
            self.node+=1
            next_value = alphaBetaPruning(gameState.generateSuccessor(aIndex,next_actions_list[0]),next_index,depth,alpha,beta)[0]
            if aIndex == self.index:
                alpha = max(next_value,alpha)
            else:
                beta = min(next_value,beta)
            minmaxVal,answerAction=next_value,next_actions_list[0]
            #Find value for each possible action excpet 0 because we have initialized using 0th action.
            for i in range(1,len(next_actions_list)):
                    #if minmaxVal is greater than beta in case of pacman we ignore exploring others. Similarly when alpha is greater than minmaxVal in case of ghost we stop exploring further.
                    if (minmaxVal > beta and aIndex == self.index) or (minmaxVal < alpha and aIndex != self.index):
                        return minmaxVal,answerAction
                    #Obtain new value by recursing over child states till depth of self.depth
                    self.node+=1
                    next_value = alphaBetaPruning(gameState.generateSuccessor(aIndex,next_actions_list[i]),next_index,depth,alpha,beta)[0]
                    #If it is pacman and value obtained is greater than minmax value then, reassign alpha if applicable and store the action.
                    if aIndex == self.index and next_value > minmaxVal:
                            alpha = max(next_value,alpha)
                            minmaxVal,answerAction = next_value,next_actions_list[i]
                    #If it is ghost and value obtained is smaller than minmax value then, reassign beta if applicable and store the action.
                    elif aIndex != self.index and next_value < minmaxVal:
                            beta = min(next_value,beta)
                            minmaxVal,answerAction = next_value,next_actions_list[i]
            return minmaxVal,answerAction
        #Passing alpha and beta extreme values.
        #print(self.node)
        return alphaBetaPruning(gameState,self.index,0,-100000000,10000000)[1]



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    #for counting nodes
    node=0
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expMax(gameState,aIndex,depth):
            answerAction = None
            #Get list of all actions.
            next_actions_list = gameState.getLegalActions(aIndex)
            #If win or lose or depth of tree reached then, return response of evaluation function.
            if ( gameState.isWin() or gameState.isLose() or depth == self.depth):
                return [self.evaluationFunction(gameState),0]
            #if all ghost have been visited once and currently we are at last ghost then, reset index and increase depth
            elif aIndex ==  gameState.getNumAgents() - 1:
                depth += 1
                next_index = self.index
            #increase index if all all ghost not yet visited.
            else:
                next_index = aIndex + 1
            minmaxVal=0
            for i in range(len( next_actions_list)):
              #Obtain new value by recursing over child states till depth of self.depth
              self.node+=1
              next_value = expMax(gameState.generateSuccessor(aIndex,next_actions_list[i]),next_index,depth)[0]
              #If it is pacman and value obtained is greater than minmax value then, store the action and corresponding value.
              if aIndex == self.index:
                  if next_value > minmaxVal:
                      minmaxVal,answerAction = next_value,next_actions_list[i]
              #If it is ghost node then we take it as chance node and value obtained is smaller than minmax value then, reassign minmaxValue as addition of current value and average of successor states and store the action.
              else:
                  minmaxVal,answerAction = minmaxVal+ (next_value / len(next_actions_list)) ,next_actions_list[i]
            return minmaxVal,answerAction  
        # print(self.node)
        return expMax(gameState,self.index,0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

