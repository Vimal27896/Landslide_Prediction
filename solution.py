class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.active_child = None
        self.switch_count = 0

def main():
    import sys
    input = sys.stdin.readline

    N = int(input().strip())
    graph = dict()
    parent_map = dict()  # child -> parent

    for _ in range(N):
        parts = input().strip().split()
        parent = parts[0]
        if parent not in graph:
            graph[parent] = Node(parent)
        for child in parts[1:]:
            graph[parent].children.append(child)
            parent_map[child] = parent
            if child not in graph:
                graph[child] = Node(child)

    products = input().strip().split()
    K = int(input().strip())

    # Ensure workstations exist
    for ws in products:
        if ws not in graph:
            graph[ws] = Node(ws)

    # Find packing center: node never appears as child
    children_set = set(parent_map.keys())
    packing_center = None
    for node in graph:
        if node not in children_set:
            packing_center = node
            break

    total_time = 0
    for product in products:
        path = []
        current = product
        while True:
            path.append(current)
            if current == packing_center:
                break
            current = parent_map[current]  # follow reverse map
        path.reverse()  # workstation -> packing center
        total_time += simulate_path(path, graph, K)

    print(total_time)

def simulate_path(path, graph, K):
    wait_time, cool_time, reset_time = 0, 0, 0
    waiting, cooling, reset = 1, 2, 3

    for i in range(len(path) - 1):
        curr = path[i]
        next_node = path[i + 1]
        node = graph[curr]

        wait_time += waiting

        if node.active_child != next_node:
            if node.switch_count < K:
                node.active_child = next_node
                node.switch_count += 1
                cool_time += cooling
            else:
                reset_time += reset
                node.switch_count = 1  # Reset counter and count this switch
                node.active_child = next_node

    # Waiting time for packing center
    wait_time += waiting
    return wait_time + cool_time + reset_time

if __name__ == "__main__":
    main()
