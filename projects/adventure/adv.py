from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "projects/adventure/maps/test_line.txt"
# map_file = "projects/adventure/maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# ================================================================ #

def opposite_direction(direction):
    return {
        'n': 's',
        'e': 'w',
        's': "n",
        "w": "e"
    }[direction]

# maps room id to a set of paths not taken yet
unfinished = {}
visited = set()
# like traversal_path, but removes elements when walking back
current_path = deque()

unfinished[player.current_room.id] = player.current_room.get_exits()
visited.add(player.current_room.id)

while len(unfinished) > 0:
    # see if there are unfinished exits at any point
    if player.current_room.id in unfinished:
        exits = unfinished[player.current_room.id]
        choice = random.choice(exits)
        exits.remove(choice)
        
        # if this is our last exit in the room to take, remove it from the 'unfinished' set
        if len(exits) == 0:
            unfinished.pop(player.current_room.id)
        
        # travel to the room
        player.travel(choice)
        traversal_path.append(choice)
        current_path.append(choice)

        # TODO: optimization strategy:
        # if we entered a loop and don't need to go backwards for any missed rooms:
        # skip the whole backtracking completely

        room = player.current_room

        # we don't have to travel backwards, remove that direction from whatever this room is
        if room.id not in visited:
            next_exits = room.get_exits()
            next_exits.remove(opposite_direction(choice))
            if len(next_exits) > 0:
                unfinished[room.id] = next_exits
        elif room.id in unfinished:
            next_exits = unfinished[room.id]
            next_exits.remove(opposite_direction(choice))
            if len(next_exits) == 0:
                unfinished.pop(room.id)
        
        visited.add(room.id)
    else:
        backward = opposite_direction(current_path.pop())
        player.travel(backward)
        traversal_path.append(backward)

# ================================================================ #

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
