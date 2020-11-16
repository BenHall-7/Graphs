from collections import deque

def earliest_ancestor(ancestors, starting_node):
    ancestry = {}
    for parent, child in ancestors:
        if child not in ancestry:
            ancestry[child] = [parent]
        else:
            ancestry[child].append(parent)
    if starting_node not in ancestry:
        return -1
    
    visited = set(ancestry[starting_node])
    q = deque(map(lambda x: (x, 1), ancestry[starting_node]))
    max_anc, max_lvl = -1, -1
    while len(q) > 0:
        anc, lvl = q.popleft()
        if anc not in ancestry:
            if lvl > max_lvl:
                max_anc, max_lvl = anc, lvl
            elif lvl == max_lvl:
                max_anc = min(anc, max_anc)
        else:
            for parent in ancestry[anc]:
                if parent not in visited:
                    q.append((parent, lvl + 1))
                    visited.add(parent)
    
    return max_anc
