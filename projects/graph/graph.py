"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
        self.visited_cache = set()

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v2 not in self.vertices:
            raise Exception(f"node '{v2}' not found in graph")
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        visited = set()
        q.enqueue(starting_vertex)
        visited.add(starting_vertex)
        while q.size() > 0:
            name = q.dequeue()
            print(name)
            for neighbor in self.get_neighbors(name):
                if neighbor not in visited:
                    q.enqueue(neighbor)
                    visited.add(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        visited = set()
        s.push(starting_vertex)
        visited.add(starting_vertex)
        while s.size() > 0:
            name = s.pop()
            print(name)
            for neighbor in self.get_neighbors(name):
                if neighbor not in visited:
                    s.push(neighbor)
                    visited.add(neighbor)


    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        print(starting_vertex)
        if len(self.visited_cache) == 0:
            self.visited_cache.add(starting_vertex)
            for neighbor in self.get_neighbors(starting_vertex):
                if neighbor not in self.visited_cache:
                    self.dft_recursive(neighbor)
            # clear cache since this case must have been the initial case
            # our cache needs to be clear for future calls
            self.visited_cache.clear()
        else:
            self.visited_cache.add(starting_vertex)
            for neighbor in self.get_neighbors(starting_vertex):
                if neighbor not in self.visited_cache:
                    self.dft_recursive(neighbor)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        # map of node names to their parent
        # also used to keep track of visited nodes
        visited = {}

        q.enqueue(starting_vertex)
        visited[starting_vertex] = None
        while q.size() > 0:
            name = q.dequeue()

            # check for match
            if name == destination_vertex:
                path = []
                cur = name
                while cur:
                    path.append(cur)
                    cur = visited[cur]

                return list(reversed(path))

            for neighbor in self.get_neighbors(name):
                if neighbor not in visited:
                    q.enqueue(neighbor)
                    visited[neighbor] = name

        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        visited = {}

        s.push(starting_vertex)
        visited[starting_vertex] = None
        while s.size() > 0:
            name = s.pop()
            
            if name == destination_vertex:
                path = []
                cur = name
                while cur:
                    path.append(cur)
                    cur = visited[cur]

                return list(reversed(path))

            for neighbor in self.get_neighbors(name):
                if neighbor not in visited:
                    s.push(neighbor)
                    visited[neighbor] = name

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if starting_vertex == destination_vertex:
            return [starting_vertex]
        
        for neighbor in self.get_neighbors(starting_vertex):
            if neighbor not in self.visited_cache:
                self.visited_cache.add(neighbor)
                found = self.dfs_recursive(neighbor, destination_vertex)
                if found:
                    self.visited_cache.clear()
                    found.insert(0, starting_vertex)
                    return found

        self.visited_cache.clear()
        return None

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))
