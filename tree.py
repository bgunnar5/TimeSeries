"""
Transformation tree allows data scientists to build and evaluate multiple pipelines

Parts:
OP_TYPE_TABLE: Stores the type of operator for each func/method
Node: Stores individual operator along with positional and keyword args necessary to execute operator (except for data),
along with references to parent and children nodes. Includes method to execute operator function stored in Node.
Tree: Non-binary tree made up of Nodes. Includes methods to manipulate the tree by adding/removing/changing individual nodes, enforce
compatibility between nodes, execute pipelines in the tree, and write/read trees to/from files.
"""
from copy import deepcopy
from queue import Queue
import preporcessing

test_func(DummyClass.seta, DummyClass.geta)


class OP_TYPE:
    INPUT_DATA = 0
    OUTPUT_DATA = 1
    PREPROCESSING = 2
    MODELING = 3
    FORECASTING = 4
    VISUALIZATION = 5
    ERROR_MEASUREMENT = 6

class CompatibilityError(Exception):
    """ 
    Error raised when a pair of parent-child nodes have
    incompatible operator types 
    """
    pass

class Node:
    def __init__(self, operator, parent=None: Node, tag="": str, args=[]: list, save_result=False: bool, pass_result=True, children=[]: list):
        # Operator function applied to input data
        self.operator = operator
        # Tag used to identify node
        self.tag = tag
        # Positional args fed into operator function
        self.args = args
        # Parent node of this node
        self.parent = parent
        # list of children nodes
        self.children = children
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

class TransformationTree:
    def __init__(self, children=[]):
        self.results = []
        self.root = Node(lambda: None, tag="root")
        self.root.children = children

    def execute_tree(self):
    """ Executes full tree """
        q = Queue()
        q.put(self.root, None)
        while q.not_empty():
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
        q.put(self.root, None)
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
        while q.not_empty:
            node = q.get()
            if mode == "tag":
                if node.tag == value:
                    result.append(node)
            elif mode == "operator":
                if node.operator == value:
                    result.append(node)
            for child in children:
                q.put(child)
        return result

    def add_operator(self, operator, parent_node, tag="": str, args=[]: list, save_result=False: bool):
        """ Add operator to tree """
        new_node = Node(operator, parent=parent_node, tag=tag, args=args, save_result=save_result)
        """
        if not self._check_compatibility(parent_node, new_node):
            raise CompatibilityError()
        """
        parent_node.children.append(new_node)
        return new_node
    
    def replace_operator(self, new_operator, node, args=None, tag=None, save_result=None):
        parent_node = node.parent
        if parent_node is None:
            raise Exception('Cannot replace operator in root node of tree')
        if self._check_compatibility(parent_node.operator, new_operator):
            node.operator = new_operator
            if args is not None:
                node.args = args
            if tag is not None:
                node.tag = tag
            if save_result is not None:
                node.save_result = save_result
        return node

    def replicate_subtree(self, start_node, tag_modifier="_copy"):
        parent_node = = start_node.parent
        start_node.parent = None
        replicated = deepcopy(start_node)
        self._modify_tags(replicated, tag_modifier)
        start_node.parent = parent_node
        replicated.parent = parent_node
        parent_node.children.append(replicated)
        return replicated

    def replicate_path(end_node: Node, start_node: Node):
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

    def _copy_node(node, incl_parent=False, incl_children=False):
        operator = node.operator
        tag = node.tag + "_copy"
        args = node.args.copy()
        save_result = node.save_result
        parent = node.parent
        children = node.children
        if incl_parent and incl_parent:
            return Node(operator, parent=parent, children=children, tag=tag, args=args, save_result=save_result)
        elif incl_parent:
            return Node(operator, parent=parent, tag=tag, args=args, save_result=save_result)
        elif incl_children:
            return Node(operator, children=children, tag=tag, args=args, save_result=save_result)
        else:
            return Node(operator, tag=tag, args=args, save_result=save_result)

    def _modify_tags(self, node, modifier):
        q = Queue()
        q.put(node)
        while q.not_empty():
            node = q.get()
            if node.tag:
                node.tag += modifier
            for child in node.children:
                q.put(child)
    """
    def _check_compatibility(parent, child):
        if type(parent) == Node and type(child) == Node:
            return self.compatibility_table.check_node_compatibility(parent, child)
        elif callable(parent) and callable(child):
            return self.compatibility_table.check_operator_compatibility(parent, child)
        else:
            raise Exception('Attempted compatibility check when parent and child types are different')
    """


"""
class CompatibilityTable:
    def __init__(self):
        # Stores the OP_TYPE of each operator
        self.op_type_table = {
            preporcessing.TimeSeries.read_from_file: INPUT_DATA,
            preporcessing.TimeSeries.write_to_file: OUTPUT_DATA,
            preporcessing.TimeSeries.assign_time: PREPROCESSING,
            preporcessing.TimeSeries.clip: PREPROCESSING,
            preporcessing.TimeSeries.denoise: PREPROCESSING,
            preporcessing.TimeSeries.impute_missing: PREPROCESSING,
            preporcessing.TimeSeries.difference: PREPROCESSING,
        }
        self.stage_table = {
            # Keys are operators of child nodes, values are comptabile parent operator types
            INPUT_DATA: [OUTPUT_DATA, PREPROCESSING, MODELING, FORECASTING, VISUALIZATION, ERROR_MEASUREMENT],
            OUTPUT_DATA: [OUTPUT_DATA, PREPROCESSING, MODELING, FORECASTING, VISUALIZATION, ERROR_MEASUREMENT],
            PREPROCESSING: [OUTPUT_DATA, PREPROCESSING, MODELING, FORECASTING, VISUALIZATION, ERROR_MEASUREMENT],
            MODELING: [OUTPUT_DATA, PREPROCESSING, MODELING, FORECASTING, VISUALIZATION, ERROR_MEASUREMENT],
            FORECASTING: [OUTPUT_DATA, PREPROCESSING, MODELING, FORECASTING, VISUALIZATION, ERROR_MEASUREMENT],
            VISUALIZATION: [OUTPUT_DATA, PREPROCESSING, MODELING, FORECASTING, VISUALIZATION, ERROR_MEASUREMENT],
            ERROR_MEASUREMENT: [OUTPUT_DATA, PREPROCESSING, MODELING, FORECASTING, VISUALIZATION, ERROR_MEASUREMENT],
            None: []
        }
    
    def check_node_compatibility(parent_node: Node, child_node: Node):
        parent_type = self.op_type_table.get(parent_node.operator)
        child_type = self.op_type_table.get(child_node.operator)
        return parent_type in self.stage_table[child_type]

    def check_operator_compatibility(parent_operator, child_operator):
        parent_type = self.op_type_table.get(parent_operator)
        child_type = self.op_type_table.get(child_operator)
        return parent_type in self.stage_table[child_type]

    def add_operator(self, operator, operator_type: OP_TYPE):
        if type(operator_type) is not OP_TYPE:
            raise TypeError("Variable operator_type must be an OP_TYPE")
        self.op_type_table[operator] = operator_type
"""