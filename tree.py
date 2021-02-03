"""
Transformation tree allows data scientists to build and evaluate multiple pipelines

Parts:
OP_TYPE_TABLE: Stores the type of operator for each func/method
Node: Stores individual operator along with positional and keyword args necessary to execute operator (except for data),
along with references to parent and children nodes. Includes method to execute operator function stored in Node.
Tree: Non-binary tree made up of Nodes. Includes methods to manipulate the tree by adding/removing/changing individual nodes, enforce
compatibility between nodes, execute pipelines in the tree, and write/read trees to/from files.
"""
import pickle
from copy import deepcopy
from queue import Queue
import preporcessing as preprocessing

class CompatibilityError(Exception):
    """ 
    Error raised when a pair of parent-child nodes have
    incompatible operator types 
    """
    pass

class Node:
    def __init__(self, operator, parent=None, tag="", args=[], save_result=False, pass_result=True):
        # Operator function applied to input data
        self.operator = operator
        # Tag used to identify node
        self.tag = tag
        # Positional args fed into operator function
        self.args = args
        # Parent node of this node
        self.parent = parent
        # list of children nodes
        self.children = []
        # Whether or not the result of executing the stored operater is added to the self.results list in the TransformationTree object
        self.save_result = save_result
        """ 
        self.pass_result dictates whether this node's children apply their operators to the result of executing this node's operator (pass_result = True), or
        to the same data this node was given (pass_result = False)
        """
        self.pass_result = pass_result
    
    def apply_operator(self, data=None):
        """ Applies stored operator and args to given data, returning the result """
        if data is not None:
            return self.operator(data, *self.args)
        else:
            return self.operator(*self.args)

    def __str__(self):
        op_string = str(self.operator).split()[1]
        if self.tag:
            return f"{op_string}:{self.tag}"
        else:
            return f"{op_string}"

    def __repr__(self):
        op_string = str(self.operator).split()[1]
        if self.tag:
            return f"Node({op_string}):{self.tag}"
        else:
            return f"Node({op_string})"

class TransformationTree:
    def __init__(self, branches=[]):
        self.results = []
        self.root = Node(root_func, tag="root")
        self.root.children = branches

    def execute_tree(self):
        """ Executes full tree """
        self.results = []
        q = Queue()
        q.put((self.root, None))
        while not q.empty():
            node, data = q.get()
            if data is not None:
                result = node.apply_operator(data=data)
            else:
                result = node.apply_operator()
            if node.save_result:
                self.results.append((result, node))
            if node.pass_result:
                data = result
            for child in node.children:
                q.put((child, deepcopy(data)))

    def execute_path(self, end_node):
        """ Executes a path in the tree. End node denotes the last node in the path """
        self.results = []
        # Finding the path
        path = [end_node]
        current_node = end_node.parent
        while current_node != self.root:
            path.append(current_node)
            current_node = current_node.parent
        path.reverse()

        # Executing the path
        q = Queue()
        q.put((self.root, None))
        data = None
        for node in path:
            if data is not None:
                result = node.apply_operator(data=data)
            else:
                result = node.apply_operator()
            if node.save_result:
                self.results.append((result, node))
            if result is not None:
                data = result

    def get_nodes_by_tag(self, tag):
        """ Find all nodes in the tree with the given operator and return a list. """
        return self._get_nodes(tag, mode="tag")

    def get_nodes_by_operator(self, operator):
        """ Find all nodes in the tree with the given operator and return a list. """
        return self._get_nodes(operator, mode="operator")

    def _get_nodes(self, value, mode: str):
        """ 
        Generic tree search method that finds Nodes in the tree with a given value.
        Used by self.get_nodes_by_tag and self.get_nodes_by_operater.

        Positional arguments:
        value -- the value the function checks for
        mode -- specifies what attribute is checked, either "tag" or "operator"

        Return list of Node objects
        """
        result = []
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            if mode == "tag":
                if node.tag == value:
                    result.append(node)
            elif mode == "operator":
                if node.operator == value:
                    result.append(node)
            for child in node.children:
                q.put(child)
        return result

    def add_operator(self, operator, parent_node, tag="", args=[], save_result=False, pass_result=True, enforce_comptability=True):
        """ Add operator to tree """
        new_node = Node(operator, parent=parent_node, tag=tag, args=args, save_result=save_result, pass_result=True)
        if enforce_comptability and not self._check_compatibility(parent_node, new_node):
            raise CompatibilityError()
        parent_node.children.append(new_node)
        return new_node
    

    def replicate_subtree(self, subtree: Node, tag_modifier="_copy"):
        parent_node = subtree.parent
        # Temporarily remove the parent of the original node, so we can deepcopy it without replicating the nodes above it
        subtree.parent = None
        # Replicated subtree
        replicated = deepcopy(subtree)
        self._modify_tags(replicated, tag_modifier)
        subtree.parent = parent_node
        replicated.parent = parent_node
        parent_node.children.append(replicated)
        # Return reference to replica subtree
        return replicated

    def replicate_path(self, start_node: Node, end_node: Node):
        """ 
        Add a copy of a path of nodes to the tree. Path goes from 
        start_node to end_node. New path is added as a child of start_node.parent

        Positional arguments:
        start_node -- First node in the copied path
        end_node -- Last node in the copied path

        Return list of Node objects

        """
        replica = self._copy_node(end_node)
        current_node = end_node.parent
        while current_node != start_node.parent:
            if current_node.parent is None:
                raise Exception('Root node reached without finding start node, replicate_path() aborted')
            new_node = self._copy_node(current_node)
            replica.parent = new_node
            new_node.children.append(replica)
            replica = new_node
            current_node = current_node.parent
        start_node.parent.children.append(replica)
        replica.parent = start_node.parent
        return replica

    def _copy_node(self, node):
        node_parent = node.parent
        node_children = node.children
        node.parent = None
        node.children = []
        node_copy = deepcopy(node)
        node.parent = node_parent
        node.children = node_children
        return node_copy

    def _modify_tags(self, subtree_root, modifier):
        """
        Modifies all the nodes with tags in a given subtree by appending the modifier string to the their current tags

        Args:
            subtree_root (Node): Node at the root of the subtree
            modifier (str): String to be appended to modified tags
        """
        q = Queue()
        q.put(subtree_root)
        while not q.empty():
            node = q.get()
            if node.tag:
                node.tag += modifier
            for child in node.children:
                q.put(child)

    def _get_inherited_data_type(self, node):
        """
        Starting with a given Node (node), go up the tree looking for the first node with node.pass_result == True,
        and then look up the return type(s) of the function in the given.

        Args:
            node (Node): First node we check

        Raises:
            Exception: If the output_type_table has insufficient information

        Returns:
            [type]: [description]
        """
        inherited_data_type = (None)
        current_node = node
        # Looking for the first node with pass_result arg == True
        while current_node != self.root:
            if current_node.pass_result == True:
                inherited_data_type = self.output_type_table.get(current_node.operator)
                if inherited_data_type is None:
                    raise Exception('Operator: {current_node.operator} is not listed in the output type table')
                break
            else:
                current_node = current_node.parent
        return inherited_data_type

    def _check_compatibility(self, new_operator, parent_node):
        """ 
        Checks if the required input for the new operator matches the 
        expected data types that will be passed to the new operator by the previous nodes
        in the tree branch
        """ 
        expected_input_types = self.input_type_table.get(new_operator)
        if expected_input_types is None:
            raise Exception('Operator: {new_operator} is not listed in the input type table')
        expected_inherited_types = self._get_inherited_data_type(parent_node)
        return expected_inherited_types == expected_input_types

    def get_path_str(self, end_node):
        node_strs = []
        current_node = end_node
        while current_node != self.root:
            node_strs.append(str(current_node))
            current_node = current_node.parent
        node_strs.reverse()
        return " -> ".join(node_strs)

        
def save_tree(tree, filename):
    try:
        pickle.dump(tree, open(filename, 'wb'))
        status = True
    except:
        status = False
    return status


def load_tree(filename):
    try:
        loaded_tree = pickle.load(open(filename, 'rb'))
        return loaded_tree
    except:
        return False

def root_func():
    """ Filler function stored in root node """
    return None

def test()
    """ Function used to test functionality, will remove in final version """
    def f1():
        return 5
    def f2(a, multiplier):
        return a*multiplier
    def f3(c):
        return 3*c


    filename = 'finalized_tree.sav'
    # Building first tree with dummy functions
    tree = TransformationTree()
    # Adding f1 function as first operator
    first = tree.add_operator(f1,tree.root,tag="first", enforce_comptability=False)
    # Adding f2 and f3 as children of f1
    # Save_result == True means the result of executing the operator is stored in tree.results
    tree.add_operator(f2, first, args=[2], save_result=True, tag="second", enforce_comptability=False)
    tree.add_operator(f3, first, save_result=True, tag="third", enforce_comptability=False)
    print("Printing paths to f2 and f3 in original tree")
    second = tree.get_nodes_by_tag("second")[0]
    third = tree.get_nodes_by_tag("third")[0]
    print(tree.get_path_str(second))
    print(tree.get_path_str(third))
    print("Executing original tree and printing the results")
    tree.execute_tree()
    print(tree.results)

    # Dumping tree to pickle file
    pickle.dump(tree, open(filename, 'wb'))
    # Loading tree from pickle file
    loaded_tree = pickle.load(open(filename, 'rb'))
    second = loaded_tree.get_nodes_by_tag("second")[0]
    third = loaded_tree.get_nodes_by_tag("third")[0]
    print("Printing paths to f2 and f3 operators in loaded tree")
    print(loaded_tree.get_path_str(second))
    print(loaded_tree.get_path_str(third))
    print("Executing loaded tree and printing results")
    loaded_tree.execute_path(third)
    print(loaded_tree.results)

test()