# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Action, PlaceAction, Coord, board
import heapq
import math
import time

from referee.game.coord import Direction
from referee.game.board import Board, CellState
import random


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Tetress game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        self.board = Board()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        # Below we have hardcoded two actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.
        #print(self.board._state[Coord(0,0)].player == None)
        '''
        match self._color:
            case PlayerColor.RED:
                print("Testing: RED is playing a PLACE action")
                return PlaceAction(
                    Coord(3, 3), 
                    Coord(3, 4), 
                    Coord(4, 3), 
                    Coord(4, 4)
                )
            case PlayerColor.BLUE:
                print("Testing: BLUE is playing a PLACE action")
                return PlaceAction(
                    Coord(2, 3), 
                    Coord(2, 4), 
                    Coord(2, 5), 
                    Coord(2, 6)
                )
        '''
        
        possible_actions = []
        possible_expansions = get_all_expansion(self.board._state, self._color)
        for e in possible_expansions:
            possible_actions.append(e.get_placeAction())

        #print(Coord(0,0) in self.board)

        if not possible_actions:
            if checkEmpty(self.board._state):
                action = PlaceAction(
                    Coord(2, 3), 
                    Coord(2, 4), 
                    Coord(2, 5), 
                    Coord(2, 6)
                )
                #self.board.apply_action(action)
                return action
            else:
                first_actions = []
                possible_first = get_all_expansion(self.board._state, self._color.opponent)
                action = random.choice(possible_first).get_placeAction()
                #self.board.apply_action(action)
                return action
        
        action = random.choice(possible_actions)
        #self.board.apply_action(action)
        return action
        
        
        

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after an agent has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        # There is only one action type, PlaceAction
        place_action: PlaceAction = action
        c1, c2, c3, c4 = place_action.coords

        # Here we are just printing out the PlaceAction coordinates for
        # demonstration purposes. You should replace this with your own logic
        # to update your agent's internal game state representation.
        print(f"Testing: {color} played PLACE action: {c1}, {c2}, {c3}, {c4}")
        #self.board.apply_action(action)
        self.board.apply_action(action)
        
        

        

def get_all_expansion(board: dict[Coord, CellState], color):
    if color == PlayerColor.BLUE:
        color_list = get_all_blue(board)
    elif color == PlayerColor.RED:
        color_list = get_all_red(board)
    spaces = get_all_space(board, color_list)   #array of Coord
    expansions = [] 
    temp = []
    for space in spaces :   # use space to create a new expansion to recurse
        expension = Expansion(space)
        expand(board,expansions,expension)
    return expansions

def expand(board,expansions,expansion):
    if expansion.length == 4:
        if expansion not in expansions:
            expansions.append(expansion)
        return

    # not sure if no return for this part is ok
    for c in expansion.Coords:
        for d in Direction:
            new_coord = c + d  
            if board[new_coord].player == None and new_coord not in expansion.Coords:
                new_expansion = Expansion()
                new_expansion.Coords = expansion.Coords.copy()
                new_expansion.length = expansion.length
                new_expansion.add_coord(new_coord)
                expand(board, expansions, new_expansion)

def get_all_red(board: dict[Coord, CellState]):
    red = []
    for key in board:
        if board[key].player == PlayerColor.RED:
            red.append(key)
    return red

def get_all_blue(board: dict[Coord, CellState]):
    blue = []
    for key in board:
        if board[key].player == PlayerColor.BLUE:
            blue.append(key)
    return blue

def get_all_space(board,red):
    spaces = []
    for r in red:
        for d in Direction:
            if board[r+d].player == None and r + d not in spaces:
                spaces.append(r+d)
    return spaces

def checkEmpty(board):
    for key in board:
        if board[key].player != None:
            return False
    
    return True

class Expansion:

    def __init__(self,initial_Coord=None):
        self.Coords = []  # Initialize Coords as an empty list
        self.length = 0
        if initial_Coord:
            self.add_coord(initial_Coord)

    def add_coord (self,c: Coord):
        self.Coords.append(c)
        self.length += 1

    # inherit function to show difference. for if not in purpose
    def __eq__(self,other) -> bool:
        for c in other.Coords:
            if c not in self.Coords:
                return False
        return True
    
    # convert expansion into place action
    def get_placeAction(self) -> PlaceAction:
        if self.length == 4:
            return PlaceAction(self.Coords[0],self.Coords[1],self.Coords[2],self.Coords[3])
        
    