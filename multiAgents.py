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
from game import Directions, Agent
import random, util

from game import Agent
from numpy import empty
from pacman import GameState

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
        "Add more of your code here if you want to"
        # get all the legal moves
        legalMoves = gameState.getLegalActions()
        
        #find the scores using successor function for all the moves.
        scores = []
        for legalMove in legalMoves:
            scores.append(self.evaluationFunction(gameState, legalMove))
        
        #print("pacman current position:",gameState.getPacmanPosition())
        #print("food positions:", gameState.getFood().asList())
        #print("dists ",scores, legalMoves)
        
        #get the max score and the corresponding moves.
        maxScore = max(scores)
        possibleMoves = []
        for i in range(len(scores)):
            if scores[i] ==  maxScore:
                possibleMoves.append(i)
                
        #return any one move which results in max score.
        chosenMove = random.choice(possibleMoves) 
        return legalMoves[chosenMove]

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
        # Useful information you can extract from a GameState (pacman.py)
        if action is "Stop":
            return -99999
        #print(currentGameState.getPacmanPosition())
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        foodStates = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        ghostpos = []
        for newGhostState in newGhostStates:
            ghostpos.append(newGhostState.getPosition())
        #print(newFood)
        if(newPos in ghostpos):
            return -99999
        #print(newPos)
        #print(newFood.asList())
        #print("new pos is", newPos, type(newPos), " with action", action)
        #print("food positions",newFood.asList())
        min_dist = 99999
        dist = 0
        for foodlocation in foodStates.asList():
            dist = manhattanDistance(foodlocation,newPos)
            if(dist<min_dist):
                min_dist = dist

        return -min_dist

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore() - ghostscore

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
        
#         print("Total agents",gameState.getNumAgents())
#         print("depth",self.depth)
#         print("legal actions of pacman",gameState.getLegalActions(0))
                
#         for action in gameState.getLegalActions(0):
#             print("successors", gameState.generateSuccessor(0,action).getPacmanPosition())
            
        
        return gameState.getLegalActions(0)[self.returnEvaluations((0, 0), gameState, gameState.getNumAgents(), self.depth)]
        
        #util.raiseNotDefined()
    
    def returnEvaluations(self, agentid, gameState, totalAgents, depth):
        
        if (agentid[1] == depth) or gameState.isWin() or gameState.isLose() or gameState.getLegalActions(agentid[0])==0:
            return self.evaluationFunction(gameState)

        evals = []
        for action in gameState.getLegalActions(agentid[0]):
            successor = gameState.generateSuccessor(agentid[0],action)
            if agentid[0] == totalAgents-1:
                evals.append(self.returnEvaluations((0,agentid[1]+1), successor, totalAgents, depth))
            else:
                evals.append(self.returnEvaluations((agentid[0]+1,agentid[1]), successor, totalAgents, depth))
        
        if agentid[0] != 0:
            return min(evals)
        elif agentid[0] == 0 and agentid[1] != 0:
            return max(evals)
        else:
            return evals.index(max(evals))

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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

