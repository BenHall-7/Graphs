import random
from collections import deque
from math import sqrt, ceil

class User:
    def __init__(self, name):
        self.name = name

def fisher_yates_shuffle(l):
    for i in range(0, len(l)):
        random_index = random.randint(i, len(l) - 1)
        l[random_index], l[i] = l[i], l[random_index]

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for name in range(num_users):
            self.add_user(name)

        # Create friendships (refer to diagram for this algorithm)

        # All possible friendship ID's in a group of 5:
        #     5  4  3  2
        #   +-----------
        # 1 | 1  2  4  7
        # 2 | 3  5  8 
        # 3 | 6  9
        # 4 | 10
        #
        # use a random selection from 1 - 10
        # use math to figure out the corresponding coordinates

        # Duplications are prevented by only choosing friends with lower IDs
        num_friendships = num_users * avg_friendships // 2
        # there are a 'triangle' number of possible friendships, we can ID them all
        num_possible = (num_users - 1) * num_users // 2
        # pick a random sample
        for friendship_id in random.sample(range(1, num_possible + 1), num_friendships):
            reverse_triangle = (sqrt(8 * friendship_id + 1) - 1) / 2
            rounded = ceil(reverse_triangle)
            # get the first triangle number greater or equal to friendship_id
            next_highest_triangle = (rounded + 1) * rounded // 2
            # the difference tells us what two friends the id corresponds to
            difference = next_highest_triangle - friendship_id
            first_friend = rounded - difference
            second_friend = num_users - difference
            self.add_friendship(first_friend, second_friend)

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        # Stores the next neighbors to add, and also the node one level closer
        # in order to concatenate a path 
        q = deque()
        q.append((user_id, None))
        while len(q) > 0:
            user, prev = q.popleft()
            # write the path for the current user
            visited[user] = visited[prev] + [user] if prev is not None else [user]
            for neighbor in self.friendships[user]:
                if neighbor not in visited:
                    q.append((neighbor, user))

        return visited

if __name__ == '__main__':
    # sg = SocialGraph()
    # sg.populate_graph(10, 2)
    # print(sg.friendships)
    # connections = sg.get_all_social_paths(1)
    # print(connections)

    # question 1 and 2:
    q1_results = []
    q2_results = []
    for _ in range(1000):
        sg = SocialGraph()
        sg.populate_graph(1000, 5)
        network = sg.get_all_social_paths(1)
        network_count = len(network) - 1 # exclude self
        if network_count == 0:
            # slim chance this can happen
            continue
        
        degree_of_separation = 0
        for person in network.items():
            if person[0] != 1: # exclude self
                degree_of_separation += len(person[1]) - 1
        degree_of_separation /= network_count
        
        q1_results.append(network_count / 999)
        q2_results.append(degree_of_separation)

    print("Q1: percent of users in extended network")
    print(sum(q1_results) / len(q1_results))
    print("Q2: average degree of separation")
    print(sum(q2_results) / len(q2_results))

