# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part B: Game Playing Agent  python -m referee agenth.program agentr.program
#python -m referee agentr.program agenth.program
#python -m referee agenth.program agentm.program
#python -m referee agentr.program agentm.program
#691

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
        print(referee["time_remaining"])
        possible_actions = []
        possible_expansions = get_all_expansion(self.board._state, self._color, 4)
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
                possible_first = get_all_expansion(self.board._state, self._color.opponent, 4)
                #action = random.choice(possible_first).get_placeAction()
                #self.board.apply_action(action)
                for p in possible_first:
                    first_actions.append(p.get_placeAction())
                return choose_action(self.board, self._color, first_actions, referee["time_remaining"])
        
        #action = random.choice(possible_actions)
        #self.board.apply_action(action)
        return choose_action(self.board, self._color, possible_actions, referee["time_remaining"])
        
        
        

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
        #print(referee["time_remaining"])
        #self.board.apply_action(action)
        self.board.apply_action(action)
        
        

        

def get_all_expansion(board: dict[Coord, CellState], color, depth):
    if color == PlayerColor.BLUE:
        color_list = get_all_blue(board)
    elif color == PlayerColor.RED:
        color_list = get_all_red(board)
    spaces = get_all_space(board, color_list)   #array of Coord
    expansions = [] 
    temp = []
    for space in spaces :   # use space to create a new expansion to recurse
        expension = Expansion(space)
        expand(board,expansions,expension, depth)
    return expansions

def expand(board,expansions,expansion, depth):
    if expansion.length == depth:
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
                expand(board, expansions, new_expansion, depth)

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

def get_color_blocks(board: dict[Coord, CellState], color):
    if color == PlayerColor.RED:
        return get_all_red(board)
    else:
        return get_all_blue(board)

def get_all_space(board,color_list):
    spaces = []
    for r in color_list:
        for d in Direction:
            if board[r+d].player == None and r + d not in spaces:
                spaces.append(r+d)
    return spaces


def heuristic(board: Board, color: PlayerColor, depth):

    if depth == -1:
        print(" h changed ")
        my_color = 0
        opp_color = 0
        for key in board._state:
            if board._state[key] == color:
                my_color += 1
            elif board._state[key] == color.opponent:
                opp_color += 1
        
        if board.turn_color == color:
            if my_color == 0:
                return -1000
            #if opp_color == 0:
                #return 1000
        if board.turn_color == color.opponent:
            if opp_color == 0:
                return 1000
            #if my_color == 0:
                #return -1000
        
        return my_color - (121 - my_color)



    #board.apply_action(action)
    my_expension = get_all_expansion(board._state, color, depth)
    opp_expension = get_all_expansion(board._state, color.opponent, depth)
    if board.turn_count == color:
        #board.undo_action()
        if len(my_expension) == 0:
            return -1000
        #if len(opp_expension) == 0:
            #return 1000
    if board.turn_count == color.opponent:
        if len(opp_expension) == 0:
            return 1000
        #if len(my_expension) == 0:
            #return -1000
    h = len(my_expension) - len(opp_expension)
    #board.undo_action()
    #nprint(h)
    #print("h = ", h)
    return h

def checkEmpty(board):
    for key in board:
        if board[key].player != None:
            return False
    
    return True


'''
minmax(3 blur 1)
expand(blue)
get maximum h
apply(a blue)
    minmax(2 red 0)
    expand(red)
    get minimum h
    apply(a, red)
        minmax(1 blue 1)
        expand(blue)
        get maximum h
        apply(a blue)
            minmax(0 red 0)
            return h(blue)
'''

def minMax(board: Board, depth, ismax, color: PlayerColor, alpha, beta, h_depth, start_time):
    #print(board.render(True, True))
    #print("curr depth = ", depth, color)

    if depth == 0:
        #board.undo_action
        #print(board.render(True, True))

        if ismax == 0:
            h = heuristic(board, color.opponent, h_depth)
        else:
            h = heuristic(board, color, h_depth)

        board.undo_action()
        #print(board.render(True, True))
        #print("h = ", h)
        return h
    
    #board.apply_action(action)
    my_expension = get_all_expansion(board._state, color, 4)
    my_actions = []
    for e in my_expension:
        my_actions.append(e.get_placeAction())
    
    depth_decrement_factor = 1
    if len(my_expension) <= 25 and h_depth != -1:
        #print("current depth = " , h_depth)
        h_depth = 4
    elif 25 < len(my_expension) <= 50 and h_depth != -1:
        #print("current depth = " , h_depth)
        h_depth = 3
    else:
        h_depth = 3
        print("current depth = " , depth,   "depth_decrement_factor = 2")
        depth_decrement_factor = 2

    if time.time() - start_time >= 35:
        h_depth = 2
        print("too slow lol")
        depth_decrement_factor = 2

    opp_expension = get_all_expansion(board._state, color.opponent, 4)

    if(len(opp_expension) == 0):
        board.undo_action()
        if(ismax == 0):
            return float('inf')
        else:
            return float('-inf')
    elif(len(my_expension) == 0):
        board.undo_action()
        if(ismax == 0):
            return float('-inf')
        else:
            return float('inf')
    
    if ismax == 1:
        currMax = float('-inf')
        for a in my_actions:
            #print("action = ", a, "color = ", color)
            board.apply_action(a)
            new_depth = depth - depth_decrement_factor
            if new_depth < 0:
                new_depth = 0
            evaluation = minMax(board, new_depth, ismax - 1, color.opponent, alpha, beta, h_depth, start_time)
            if evaluation > currMax:
                currMax = evaluation

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                #print("prunning   maxmaxmax")
                break  # Beta cutoff

        board.undo_action()
        return currMax

    else:
        currMin = float('inf')
        for a in my_actions:
            #print("action = ", a, "color = ", color)
            board.apply_action(a)
            #print("action = ", a)
            new_depth = depth - depth_decrement_factor
            if new_depth < 0:
                new_depth = 0
            evaluation = minMax(board, new_depth, ismax + 1, color.opponent, alpha, beta, h_depth, start_time)
            if evaluation < currMin:
                currMin = evaluation

            beta = min(beta, evaluation)
            if beta <= alpha:
                #print("prunning  minminmin")
                break  # Alpha cutoff

        board.undo_action()
        return currMin

def choose_action(board: Board, color: PlayerColor, my_actions, time_remaining):
    start_time = time.time()

    h_depth = 3

    curr_best_move = my_actions[0]
    curr_best_value = float('-inf')

    alpha = float('-inf')
    beta = float('inf')

    depth = 0
    if len(my_actions) <= 10:
        depth = 3
    elif 10 < len(my_actions) <= 40:
        depth = 2
    elif 40 < len(my_actions) <= 120:
        depth = 1
    else:
        depth = 0

    if time_remaining <= 30:
        depth = 0

    if len(my_actions) <= 30:
        h_depth = 4
    elif 30 < len(my_actions) <= 100:
        h_depth = 3
    elif 100 < len(my_actions):
        h_depth = 2

    if time_remaining <= 35:
        depth = 0
        #h_depth = 3
    elif time_remaining <= 20:
        depth = 0
        h_depth = 2
    elif time_remaining <= 2:
        return random.choice(my_actions)
    
    print("depth = ", depth)


    if board.turn_count >= 110:
        cellFilled = 0
        for key in board._state:
            if board._state[key] != PlayerColor.BLUE:
                cellFilled += 1
        if cellFilled <= 70:
            h_depth = -1
 
    for a in my_actions:
        #print("111")
        board.apply_action(a)
        curr_value = minMax(board, depth, 0, color.opponent, alpha, beta, h_depth, start_time)
        if curr_value > curr_best_value:
            curr_best_value = curr_value
            curr_best_move = a
        alpha = max(alpha, curr_value)
        if beta <= alpha:
            #print("prunning aaa")
            break  # Beta cutoff
    #board.undo_action()

    return curr_best_move

#python -m referee agentr.program agentm.program
#python -m referee agenth.program agentm.program
#python -m referee agentr.program agent -t 180
    




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
        
    