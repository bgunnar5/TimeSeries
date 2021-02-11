"""
This module implements a transformation tree allows data scientists to build and evaluate multiple pipelines,
as specified in the project 1 specifications.
Authors: Brian Gunnarson, Sam Peters
Groupname: The Classy Coders
Most recent modification: 2/9/2021
"""

import pickle
from copy import deepcopy
from queue import Queue
import preprocessing

class CompatibilityError(Exception):
    """ 
    Error raised when a pair of parent-child nodes have
    incompatible operator types 
    """
    pass

class Node:
    """ Node class used inside TransformationTree class """
    def __init__(self, operator, args, parent=None, tag="", save_result=False):
        """
        Initializes a Node object containing operator, tag, args, parent, children, and save_result attributes

        Args:
            operator (function): function to be executed when self.apply_operator method is called
            args (list): list of positional arguments to be included when calling self.operator function
            parent (Node, optional): Parent of the initialized Node in the tree. Defaults to None.
            tag (str, optional): Tag used to identify and find the initialized Node in the tree. Defaults to "".
            save_result (bool, optional): Dictates whether the result of calling self.apply_method should be saved during tree execution. Defaults to False.
        """
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
        # Whether or not the result of executing the stored operator is added to the tree.results list in the TransformationTree object
        # The results attribute in the TransformationTree object is a non branch-specific list used to access the results of executing specific operators after the entire
        # tree has finished executing
        self.save_result = save_result
    
    def apply_operator(self, dynamic_data: list):
        """
        Calls self.operator, passing in the values contained in dynamic_data and self.args as positional arguments

        Args:
            dynamic_data (list): [description]

        Returns:
            Any: The result of calling self.operator
        """
        return self.operator(*dynamic_data, *self.args)

    def __str__(self):
        """
        Returns string representing Node object

        Returns:
            str: String containing operator name, or the operator name and tag string
        """
        op_string = str(self.operator).split()[1]
        if self.tag:
            return f"{op_string}:{self.tag}"
        else:
            return f"{op_string}"

    def __repr__(self):
        """
        Returns string representation of Node object

        Returns:
            str: Takes the form of "Node(operator_name)" or "Node(operator_name):tag" depending on if the node's tag == ""
        """
        op_string = str(self.operator).split()[1]
        if self.tag:
            return f"Node({op_string}):{self.tag}"
        else:
            return f"Node({op_string})"

class TransformationTree:
    def __init__(self, input_keys, output_keys):
        """
        Creates a TransformationTree object, initializing results, root, input_keys, and output_keys attributes in the object.

        Args:
            input_keys (dict): Describes which key value pairs should be pulled from a branch specific dictionary and used as input during an operator's
            execution. Keys in this dict are operator functions, and values are lists of strings (used as keys in the branch dictionary to get input values).
            output_keys (dict): Describes how an operator's output should be stored in a branch specific dictionary after execution. Keys in this dict are operator functions,
            and values are lists of strings (used as keys in the branch dictionary to store output values).
        """
        self.results = []
        self.root = Node(preprocessing.TimeSeries,[], tag="root")
        self.root.children = []
        self.input_keys = input_keys
        self.output_keys = output_keys

    def _execute(self, path=None):
        """
        Generic tree execution method called by self.execute_tree and self.execute_path.
        Modifies self.results.

        Args:
            path (list, optional): List of nodes in a path to execute. If None whole tree will be executed. Defaults to None.
        """
        self.results = []
        q = Queue()
        q.put((self.root, {}))
        while not q.empty():
            node, branch_dict = q.get()
            dynamic_values = []
            # Getting dynamic values from branch dict
            for key in self.input_keys[node.operator]:
                if key in branch_dict:
                    dynamic_values.append(branch_dict[key])
            # Checking if all the required input data was created by previous operators
            if len(self.input_keys[node.operator]) == len(dynamic_values):
                result = node.apply_operator(dynamic_values)
                # Optionally saving the returned result to a list that can be viewed after tree execution
                if node.save_result:
                    self.results.append((result, node))
                # Making result iterable
                if result is None:
                    result = []
                elif type(result) != list and type(result) != tuple:
                    result = [result]
                # If the correct amount of data was returned, update the branch_dict and add node's children to queue
                if len(result) == len(self.output_keys[node.operator]):
                    for key, value in zip(self.output_keys[node.operator], result):
                        branch_dict[key] = value
                    for child in node.children:
                        if path is None or child in path:
                            q.put((child, deepcopy(branch_dict)))


    def execute_tree(self):
        """
        Executes entire tree by calling self._execute() without a path argument.
        Modifies self.results
        """
        self._execute(path=None)

    def execute_path(self, end_node):
        """
        Executes a single path in the tree by calling self._execute(path=end_node).
        Modifies self.results

        Args:
            end_node (Node): Last node in the path to be executed.
        """
        self.results = []
        # Finding the path
        path = [end_node]
        current_node = end_node.parent
        while current_node != self.root.parent:
            path.append(current_node)
            current_node = current_node.parent
        self._execute(path=path)

    def get_nodes_by_tag(self, tag):
        """
        Finds all the nodes in the tree with a tag equal to the input tag.
        Calls self._get_nodes()

        Args:
            tag (str): Tag to find

        Returns:
            [Node]: List of Nodes with a tag equal to the input tag.
        """
        return self._get_nodes(tag, mode="tag")

    def get_nodes_by_operator(self, operator):
        """
        Finds all nodes in the tree containing the input operator function (operator).

        Args:
            operator (function): function to find

        Returns:
            [Node]: List of Nodes containing the same operator function as the input operator function.
        """
        return self._get_nodes(operator, mode="operator")

    def _get_nodes(self, value, mode: str):
        """ 
        Generic tree search method that finds Nodes in the tree with a given value.
        Used by self.get_nodes_by_tag and self.get_nodes_by_operator.

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

    def add_operator(self, operator, args, parent_node, tag="", save_result=False):
        """
        Adds a Node containing a new operator to the tree.

        Args:
            operator (function): Operator function to be called during tree execution
            args ([Any]): Positional arguments using during operator function call
            parent_node (Node): Parent of the new Node, must be an existing Node object in the tree.
            tag (str, optional): String used by users to identify specific important Nodes later on. Defaults to "".
            save_result (bool, optional): Specifies whether the rseult of executing the operator function should be saved to self.results,
            for additional processing after the tree is finished executing. Defaults to False.

        Raises:
            CompatibilityError: Signifies that two successive operator functions are incompatible with each other.

        Returns:
            Node: Newly created Node in the tree.
        """
        new_node = Node(operator, args, parent=parent_node, tag=tag, save_result=save_result)
        
        if not self._check_compatibility(parent_node, new_node):
            raise CompatibilityError()
        
        parent_node.children.append(new_node)
        return new_node

    def replace_operator(self, operator,args, node, tag="", save_result=False):
        """
        Updates the attributes of an existing node with new operator, args, tag, and save_result values.

        Args:
            operator (function): New operator function
            args ([Any]): New list of positional args to be passed to the operator function during execution
            node (Node): Node to be updated
            tag (str, optional): New tag value. Defaults to "".
            save_result (bool, optional): New save_result value. Defaults to False.

        Returns:
            Node: Newly updated node
        """
        new_node = self.add_operator(operator, args, node.parent, tag=tag, save_result=save_result)
        # At this point the new_node and the old node (node) are both children of node.parent
        # We need to remove one of them later in the function depending on if the children are compatible with new_node
        compatible_with_children = True
        for child in node.children:
            if not self._check_compatibility(child, new_node):
                compatible_with_children = False
                break
        if compatible_with_children:
            # Transferring children to new_node
            for child in node.children:
                child.parent = new_node
                new_node.children.append(child)
            node.parent.children.remove(node)
        else:
            node.parent.children.remove(new_node)
        return new_node
    

    def replicate_subtree(self, subtree: Node, tag_modifier="_copy"):
        '''
        This method creates a copy of a subtree starting at a specified Node.

        ARGS:
            subtree: the Node to start replicating the subtree at
            tag_modifier: a string to clarify that the new subtree is a copy

        CALLS:
            self._modify_tags(): modifies the tags of Nodes in the replicated subtree using tag_modifier

        RETURNS:
            replicated: a copy of the subtree starting at "subtree"
        '''
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

        Return reference to first node in replica tree path
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
        """
        Creates an exact copy of a given Node, except for the Node's children and parent attributes, which it sets to empty.
        Used internally.

        Args:
            node (Node): Node to be copied.

        Returns:
            Node: Returns reference to Node copy
        """
        return Node(node.operator, node.args, tag=node.tag, save_result=node.save_result)
        

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

    def _check_compatibility(self, new_node, parent_node):
        """ 
        Checks if the required input for the new node's operator matches the 
        expected data types that will be passed to the new operator by the previous nodes
        in the tree branch.

        ARGS:
            new_node: the node we're trying to add to the tree branch
            parent_node: the previous node in the tree branch

        RETURNS:
            True if the required input matches the expected data types. False otherwise.
        """ 
        required_input_keys = self.input_keys[new_node.operator]
        branch_key_set = set()
        current_node = parent_node
        while current_node != self.root.parent:
            operator_output_keys = self.output_keys[current_node.operator]
            for key in operator_output_keys:
                branch_key_set.add(key)
            current_node = current_node.parent
        for key in required_input_keys:
            if key not in branch_key_set:
                return False
        return True

    def get_path_str(self, end_node):
        '''
        Returns string representing path from the root node of the tree to a given node (end_node)

        ARGS:
            end_node: The last node in the path we want to turn into a string

        RETURNS:
             A string representation of a path
        '''
        node_strs = []
        current_node = end_node
        while current_node != self.root.parent:
            node_strs.append(str(current_node))
            try:
                current_node = current_node.parent
            except:
                print(current_node, current_node.parent)
        node_strs.reverse()
        return " -> ".join(node_strs)

    def export_pipeline(self, end_node: Node):
        '''
        Exports a Pipeline object

        ARGS:
            end_node: The last node in a path of the tree

        CALLS:
            Pipeline(): to create a pipeline object

        RETURNS:
             pip: a Pipeline object
        '''
        pip = Pipeline(self, end_node)
        return pip


# Save works for both trees and pipelines so we use the argument name 'object'
def save(object, filename):
    '''
    Saves a TimeSeries or Pipeline object to a file.

    RETURNS:
        status: a boolean value to determine if the save worked properly
    '''
    try:
        pickle.dump(object, open(filename, 'wb'))
        status = True
    except:
        status = False
    return status

# Load works for both trees and pipelines so we use the variable name 'loaded_object'
def load(filename):
    '''
    Loads a TimeSeries or Pipeline object to a file.

    RETURNS:
        status: a boolean value to determine if the save worked properly
    '''
    try:
        loaded_object = pickle.load(open(filename, 'rb'))
        return loaded_object
    except:
        return False


class Pipeline:
    """
    Static pipeline of operator functions that process data. Can be executed but not edited.
    """
    def __init__(self, tree: TransformationTree, pipeline_end_node: Node):
        self.tree = tree
        self.end_node = pipeline_end_node
        self.results = None

    def run_path(self):
        '''
        Executes a Pipeline path and modifies self.results.

        CALLS:
            TransformationTree.execute_path: calls this method to run a path of the tree
        '''
        self.tree.execute_path(self.end_node)
        self.results = self.tree.results
        
