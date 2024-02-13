import math


class GraphNode:
    """A node in a graph. It has an id, x and y coordinates, and a list of
    nodes it is connected to.
    """

    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x = x
        self.y = y
        self.reset()

    def reset(self):
        """Reset the node to its initial state."""
        self.via = None
        self.visited = False
        self.distance_to_goal = float("inf")
        self.distance_to_origin = float("inf")

    @property
    def total_distance_to_goal(self):
        """The total distance to the goal. It is the sum of the distance to
        the origin and the distance to the goal."""
        return self.distance_to_origin + self.distance_to_goal


class PriorityQueue:
    """A priority queue that stores nodes and their total distances. It
    allows adding or updating a node, and removing the node with the
    smallest total distance.
    """

    def __init__(self):
        self.nodes = {}

    def add_or_update(self, node_id, total_distance):
        """Add a node to the queue, or update its total distance if it is
        already in the queue.

        Args:
            node_id: The id of the node.
            total_distance: The total distance to the node.
        """
        self.nodes[node_id] = total_distance

    def remove(self):
        """Remove the node with the smallest total distance from the queue.

        Returns:
            The id of the node with the smallest total distance, or None if
            the queue is empty.
        """
        if not self.nodes:
            return None

        node_id = min(self.nodes, key=self.nodes.get)
        del self.nodes[node_id]
        return node_id


class GraphSpace:
    """A graph space that contains nodes and lines. It allows finding
    linked nodes for a given node.
    """

    def __init__(self, nodes, lines):
        self.nodes = {
            node_id: GraphNode(node_id, pos[0], pos[1])
            for node_id, pos in nodes.items()
        }
        self.lines = {line_id: nodes for line_id, nodes in enumerate(lines)}

    def find_linked_nodes(self, node_id):
        """Find the ids of nodes that are linked to the given node.

        Args:
            node_id: The id of the node.

        Returns:
            A list of ids of nodes that are linked to the given node.
        """
        return self.lines.get(node_id, [])


class PathFinder:
    """A path finder that finds the shortest path between two nodes in a
    graph space.
    """

    def __init__(self, space):
        self.space = space
        self.frontier = PriorityQueue()
        self.goal = None
        self.origin = None

    def calculate_distance(self, from_xy, to_xy):
        """Calculate the distance between two points.

        Args:
            from_xy: The x and y coordinates of the first point.
            to_xy: The x and y coordinates of the second point.

        Returns:
            The distance between the two points.
        """
        diff_x = math.fabs(from_xy[0] - to_xy[0])
        diff_y = math.fabs(from_xy[1] - to_xy[1])
        return math.sqrt(diff_x**2 + diff_y**2)

    def initialize_goal(self, goal_id):
        """Initialize the goal node.

        Args:
            goal_id: The id of the goal node.
        """
        self.goal = self.space.nodes[goal_id]
        self.goal.distance_to_goal = 0

    def initialize_origin(self, origin_id):
        """Initialize the origin node.

        Args:
            origin_id: The id of the origin node.
        """
        self.origin = self.space.nodes[origin_id]
        self.origin.distance_to_origin = 0

    def add_to_frontier(self, from_node, to_node):
        """Add a node to the frontier, or update its total distance if it is
        already in the frontier.

        Args:
            from_node: The node from which the edge to the node is.
            to_node: The node to add to the frontier.
        """
        if to_node.visited:
            return

        distance_to_node = (
            0
            if from_node is None
            else (
                self.calculate_distance(
                    (from_node.x, from_node.y), (to_node.x, to_node.y)
                )
                + from_node.distance_to_origin
            )
        )

        if distance_to_node < to_node.distance_to_origin:
            to_node.distance_to_origin = distance_to_node
            to_node.via = from_node

        if math.isinf(to_node.distance_to_goal):
            to_node.distance_to_goal = (
                self.calculate_distance(
                    (to_node.x, to_node.y), (self.goal.x, self.goal.y)
                )
                * 0.9
            )

        self.frontier.add_or_update(to_node.id, to_node.total_distance_to_goal)

    def get_route_ids(self):
        """Get the ids of the nodes in the shortest path.

        Returns:
            A list of the ids of the nodes in the shortest path.
        """
        route = []
        node = self.goal
        while node is not None:
            route.append(node.id)
            node = node.via
        return list(reversed(route))

    def find_shortest_path(self, origin_id, goal_id):
        """Find the shortest path between two nodes.

        Args:
            origin_id: The id of the origin node.
            goal_id: The id of the goal node.

        Returns:
            A list of the ids of the nodes in the shortest path, or None if
            no path is found.
        """
        if origin_id not in self.space.nodes or goal_id not in self.space.nodes:
            return None

        if origin_id == goal_id:
            return [origin_id]

        self.initialize_origin(origin_id)
        self.initialize_goal(goal_id)
        self.add_to_frontier(None, self.origin)

        return self._find_shortest_path()

    def _find_shortest_path(self):
        """Find the shortest path between two nodes.

        Returns:
            A list of the ids of the nodes in the shortest path, or None if
            no path is found.
        """
        active_node_id = self.frontier.remove()

        if active_node_id is None:
            return None
        if active_node_id == self.goal.id:
            return self.get_route_ids()

        active_node = self.space.nodes[active_node_id]
        active_node.visited = True

        for linked_id in self.space.find_linked_nodes(active_node_id):
            linked_node = self.space.nodes.get(linked_id)
            if linked_node is not None:
                self.add_to_frontier(active_node, linked_node)

        return self._find_shortest_path()


def shortest_path(map_object, start, goal):
    space = GraphSpace(map_object.intersections, map_object.roads)
    finder = PathFinder(space)
    return finder.find_shortest_path(start, goal)
