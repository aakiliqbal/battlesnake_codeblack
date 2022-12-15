# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
#import collideitself


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    def avoid_walls(my_head, board_width, board_height, is_move_safe):
      if my_head["x"] == 0 and my_head["y"]==0:
        is_move_safe["down"] = False
        is_move_safe["left"] = False
      elif my_head["x"] == board_width and my_head["y"]==0:
        is_move_safe["down"] = False
        is_move_safe["right"] = False
      elif my_head["x"] ==0  and my_head["y"]== board_height:
        is_move_safe["left"] = False
        is_move_safe["up"] = False
      elif my_head["x"] ==board_width  and my_head["y"]== board_height:
        is_move_safe["right"] = False
        is_move_safe["up"] = False
      elif my_head["x"]==0:
        is_move_safe["left"] = False
      elif my_head["y"]==0:
        is_move_safe["down"] = False
      elif my_head["x"]==board_width:
        is_move_safe["right"] = False
      elif my_head["y"]==board_height:
        is_move_safe["up"] = False
      return is_move_safe

    def avoid_snakes(opponents, is_move_safe):
      for opponent in opponents:
        for b in opponent['body']:
          if(my_head["x"] == b["x"]-1 and my_head["y"] == b["y"]):
            is_move_safe["right"] = False
          if(my_head["x"] == b["x"]+1 and my_head["y"] == b["y"]):
            is_move_safe["left"] = False
          if(my_head["y"] == b["y"]-1 and my_head["x"] == b["x"]):
            is_move_safe["up"] = False
          if(my_head["y"] == b["y"]+1 and my_head["x"] == b["x"]):
            is_move_safe["down"] = False
      return is_move_safe

    def avoid_body(my_body, is_move_safe):
      for b in my_body:
        if(my_head["x"] == b["x"]-1 and my_head["y"] == b["y"]):
          is_move_safe["right"] = False
        if(my_head["x"] == b["x"]+1 and my_head["y"] == b["y"]):
          is_move_safe["left"] = False
        if(my_head["y"] == b["y"]-1 and my_head["x"] == b["x"]):
          is_move_safe["up"] = False
        if(my_head["y"] == b["y"]+1 and my_head["x"] == b["x"]):
          is_move_safe["down"] = False
      return is_move_safe
    
    def get_distance(my_future_head, f):
      x2 = f["x"]
      y2 = f["y"]
      x1 = my_future_head["x"]
      y1 = my_future_head["y"]
      difference1 = x2 - x1
      difference2 = y2 - y1
      absolute_difference = abs(difference1) + abs(difference2)
      return absolute_difference

    def get_close_food(foods, my_head):
      if len(foods) == 0:
        return None
      closest_food_distance = 9999
      closest_food = foods[0]
      for food in foods:
        if get_distance(my_head, food) < closest_food_distance:
          closest_food_distance = get_distance(my_head, food)
          closest_food = food
      return closest_food
    
    def get_future_head(my_head, my_move):
      my_future_head = my_head.copy()
      if my_move == "right":
        my_future_head["x"] = my_head["x"]+1
        return my_future_head
      if my_move == "left":
        my_future_head["x"] = my_head["x"]-1
        return my_future_head
      if my_move == "up":
        my_future_head["y"] = my_head["y"]+1
        return my_future_head
      if my_move == "down":
        my_future_head["y"]= my_head["y"]-1
        return my_future_head

    def move_target(safe_moves, my_head, target):
      distance_x = abs(my_head["x"] - target["x"])
      distance_y = abs(my_head["y"] - target["y"])
      
      for direction in safe_moves():
        location = get_future_head(my_head, direction)
        new_distance_x = abs(location["x"] - target["x"])
        new_distance_y = abs(location["y"] - target["y"])
        if new_distance_x < distance_x or new_distance_y < distance_y:
          return direction
      return safe_moves[0]
        
      
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']-1
    board_height = game_state['board']['height']-1

    is_move_safe = avoid_walls(my_head, board_width, board_height, is_move_safe)
    

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    is_move_safe = avoid_body(my_body, is_move_safe)


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    is_move_safe = avoid_snakes(opponents, is_move_safe)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    foods = game_state['board']['food']
    target = get_close_food(foods, my_head)


    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
      if isSafe:
        safe_moves.append(move)

    if len(safe_moves)> 0:
      if target is not None:
          print(target)
          print(safe_moves)
          next_move = move_target(safe_moves, my_head, target)
      else:
        # Choose a random move from the safe ones
        next_move = random.choice(safe_moves)
    else:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
    
      


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
