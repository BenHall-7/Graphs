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
# map_file = "projects/adventure/maps/test_loop.txt"
# map_file = "projects/adventure/maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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

# find any/all loops by doing a full depth-first traversal

def get_loops(start_room):
    # each loop is a list of directions (forward, backward) to take to traverse the loop
    loops = []
    # stores which loop ID each room corresponds to (if any, only one for this problem)
    # and also what position that room is in inside the corresponding loop structure
    corr = {}

    unfinished = {}
    current_path = deque()
    visited = set()

    unfinished[start_room.id] = start_room.get_exits()
    current_path.append((start_room, None))
    visited.add(start_room.id)
    while len(unfinished) > 0:
        # last room in path is the one we're on
        current = current_path[len(current_path) - 1][0]
        if current.id in unfinished:
            dirs_left = unfinished[current.id]
            # take an arbitrary direction out of the unfinished list
            next_direction = dirs_left.pop()
            # when all paths from the room are finished, we take the room out of our map
            if len(dirs_left) == 0:
                unfinished.pop(current.id)
            next_room = current.get_room_in_direction(next_direction)
            if next_room.id not in visited:
                visited.add(next_room.id)
                # the path also contains what direction we need to go backward
                current_path.append((next_room, opposite_direction(next_direction)))
                subsequent_rooms = next_room.get_exits()
                # remove 'backwards' from next room
                subsequent_rooms.remove(opposite_direction(next_direction))
                if len(subsequent_rooms) > 0:
                    unfinished[next_room.id] = subsequent_rooms
            else:
                # we've reached a loop point
                loop_id = len(loops)
                loop = []
                # 'next_room' will be index 0
                # 'next_room' would go backward to end up in 'current'
                first_dir = opposite_direction(next_direction)
                loop.append(first_dir)
                first_dir_left = unfinished[next_room.id]
                first_dir_left.remove(first_dir)
                if len(first_dir_left) == 0:
                    unfinished.pop(next_room.id)
                corr[next_room.id] = (loop_id, 0)
                for i, v in enumerate(reversed(current_path), 1):
                    back_room = v[0]
                    back_dir = v[1]
                    if back_room.id == next_room.id:
                        break
                    loop.append(back_dir)
                    corr[back_room.id] = (loop_id, i)
                        
                loops.append(loop)
        else:
            current_path.pop()
    return loops, corr

loops, corr = get_loops(player.current_room)

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
        not_in_loop = [e for e in exits if player.current_room.get_room_in_direction(e).id not in corr]
        if len(not_in_loop) > 0:
            choice = random.choice(not_in_loop)
        else:
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
        else:
            print(room.id)
            if room.id in unfinished:
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
