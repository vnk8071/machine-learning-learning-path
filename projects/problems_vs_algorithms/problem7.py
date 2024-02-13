# A RouteTrie will store our routes and their associated handlers
class RouteTrie:
    def __init__(self, root_handler, invalid_handler):
        # Initialize the trie with an root node and a handler, this is the root
        # path or home page node
        self.root = RouteTrieNode(root_handler)
        self.invalid_handler = invalid_handler

    def insert(self, path, handler):
        # Similar to our previous example you will want to recursively add nodes
        # Make sure you assign the handler to only the leaf (deepest) node of
        # this path
        current_node = self.root
        for part in path:
            if part not in current_node.children:
                current_node.children[part] = RouteTrieNode()
            current_node = current_node.children[part]
        current_node.handler = handler

    def find(self, path):
        # Starting at the root, navigate the Trie to find a match for this path
        # Return the handler for a match, or None for no match
        path_parts = self._split_path(path)
        current_node = self.root
        for part in path_parts:
            if part not in current_node.children:
                return self.invalid_handler
            current_node = current_node.children[part]
        return current_node.handler

    def _split_path(self, path):
        # you need to split the path into parts for
        # both the add_handler and loopup functions,
        # so it should be placed in a function here
        path = path.strip("/")
        return path.split("/") if path else []


# A RouteTrieNode will be similar to our autocomplete TrieNode... with one
# additional element, a handler.
class RouteTrieNode:
    def __init__(self, handler=None):
        # Initialize the node with children as before, plus a handler
        self.children = {}
        self.handler = handler


# The Router class will wrap the Trie and handle
class Router:
    def __init__(self, root_handler, invalid_handler):
        # Create a new RouteTrie for holding our routes
        # You could also add a handler for 404 page not found responses as
        # well!
        self.root = RouteTrie(root_handler, invalid_handler)

    def add_handler(self, path, handler):
        # Add a handler for a path
        # You will need to split the path and pass the pass parts
        # as a list to the RouteTrie
        self.root.insert(self.split_path(path), handler)

    def lookup(self, path):
        # lookup path (by parts) and return the associated handler
        # you can return None if it's not found or
        # return the "not found" handler if you added one
        # bonus points if a path works with and without a trailing slash
        # e.g. /about and /about/ both return the /about handler
        return self.root.find(path)

    def split_path(self, path):
        # you need to split the path into parts for
        # both the add_handler and loopup functions,
        # so it should be placed in a function here
        return self.root._split_path(path)


# create the router and add a route
router = Router(
    root_handler="root handler", invalid_handler="not found handler"
)  # remove the 'not found handler' if you did not implement this
router.add_handler(path="/home/about", handler="about handler")  # add a route

# Test Cases 1
print(router.lookup("/"))  # should print 'root handler'

# Test Cases 2
print(
    router.lookup("/home")
)  # should print 'not found handler' or None if you did not implement one

# Test Cases 3
print(router.lookup("/home/about"))  # should print 'about handler'

# Edge Cases 1
# should print 'about handler' or None if you did not handle trailing slashes
print(router.lookup("/home/about/"))

# Edge Cases 2
print(
    router.lookup("/home/about/me")
)  # should print 'not found handler' or None if you did not implement one

print("All test cases passed!")
