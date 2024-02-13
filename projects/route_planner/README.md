# Route Planner

## Introduction

This is a simple route planner that uses the A* algorithm to find the shortest path between two points on a grid. The grid is represented as a 2D array of 0s and 1s, where 0s represent open cells and 1s represent obstacles.

## Path Finder

This Python program implements a path finder that finds the shortest path between two nodes in a graph space. The graph space is represented by nodes and lines, where each node has an id, x and y coordinates, and each line connects two nodes.

## Classes

The program consists of several classes:

1. `GraphNode`: Represents a node in the graph. It has an id, x and y coordinates, and a list of nodes it is connected to.

2. `PriorityQueue`: A priority queue that stores nodes and their total distances. It allows adding or updating a node, and removing the node with the smallest total distance.

3. `GraphSpace`: Represents a graph space that contains nodes and lines. It allows finding linked nodes for a given node.

4. `PathFinder`: Finds the shortest path between two nodes in a graph space. It uses the A* search algorithm to find the shortest path.

## Methods

The main methods in the `PathFinder` class are:

1. `calculate_distance(from_xy, to_xy)`: Calculates the Euclidean distance between two points.

2. `initialize_goal(goal_id)` and `initialize_origin(origin_id)`: Initialize the goal and origin nodes respectively.

3. `add_to_frontier(from_node, to_node)`: Adds a node to the frontier, or updates its total distance if it is already in the frontier.

4. `get_route_ids()`: Returns the ids of the nodes in the shortest path.

5. `find_shortest_path(origin_id, goal_id)`: Finds the shortest path between two nodes.

## Usage

The main function `shortest_path(map_object, start, goal)` takes a map object and the ids of the start and goal nodes, and returns the shortest path between the start and goal nodes. The map object should have `intersections` and `roads` attributes, where `intersections` is a dictionary of node ids to (x, y) coordinates, and `roads` is a list of lists, where each sublist contains the ids of nodes that a node is connected to.

## Time and Space Complexity

The time complexity of the `find_shortest_path` method is O(n log n), where n is the number of nodes in the graph. This is because it uses a priority queue to keep track of the nodes to visit next, and each insertion operation in a priority queue takes log n time.

The space complexity is O(n), where n is the number of nodes in the graph. This is because it needs to store all nodes in the graph space, and in the worst case, all nodes could be added to the priority queue.
