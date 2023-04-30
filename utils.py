import random
from typing import List, Tuple, Dict
from nltk.tree import *


# you can set up rules to analyze potential branches for permutation
search_rules = {
    'parent_may_be': ['NP'],
    'children_may_be': ['NP', 'JJ'],
}


class NodeObject:
    index: Tuple
    p_index: Tuple
    type: str
    value: str
    replace: str

    def __init__(self, index: Tuple, p_index: Tuple, type: str, value: str):
        self.index = index
        self.p_index = p_index
        self.type = type
        self.value = value


class SwappingGroup:
    p_index: Tuple
    p_type: str
    nodes_group: List[NodeObject]

    def __init__(self, p_index: Tuple, p_type: str):
        self.p_index = p_index
        self.p_type = p_type
        self.nodes_group = []


def make_tree_structure(input_tree: Tree) -> List[NodeObject]:
    """
    The function create List[NodeObject] from ParentedTree
    :param input_tree: Tree
    :return: List[NodeObject]
    """

    nodes_list: List[NodeObject] = []

    for index in input_tree.treepositions():
        tree_node = input_tree[index]
        value = tree_node

        if len(index) > 1:
            p_index = index[0:-1]
        else:
            p_index = ()

        if type(tree_node) == Tree:
            label = tree_node.label()
        else:
            label = ''

        # if label in can_be_changed:
        if label:
            n = NodeObject(index, p_index, label, value)
            nodes_list.append(n)

    return nodes_list


def get_children_by_parent_index(input_node_list: List[NodeObject], parent_index: Tuple) -> List[NodeObject]:
    children: List[NodeObject] = []
    for node in input_node_list:
        if node.p_index == parent_index:
            children.append(node)
    return children


def find_groups_of_nodes_for_swapping(input_tree: Tree) -> List[SwappingGroup]:
    """
    The function find the nodes, that can be swapping,
    contain it's into List[NodeObject],
    and return List[SwappingGroup]
    :param input_tree: Tree
    :return: List[SwappingGroup]
    """
    original_node_list: List[NodeObject] = make_tree_structure(input_tree)
    swapping_list: List[SwappingGroup] = []

    for node in original_node_list:
        if node.type in search_rules["parent_may_be"]:
            children = get_children_by_parent_index(original_node_list, node.index)
            if len(children) >= 2:
                swapping_group = SwappingGroup(node.index, node.type)
                for child in children:
                    if child.type in search_rules["children_may_be"]:
                        swapping_group.nodes_group.append(child)
                if len(swapping_group.nodes_group) >= 2:
                    swapping_list.append(swapping_group)

    return swapping_list


def all_choices_count(swapping_list: List[SwappingGroup]) -> int:
    """
    The function calculates all possible options of tree,
    using input swapping_list.
    (-1 option for original tree).
    :param swapping_list: List[SwappingGroup]
    :return: int
    """
    if swapping_list:
        choices_list: List[int] = []
        for sw_group in swapping_list:
            choices_in_group = 1
            for x in range(1, len(sw_group.nodes_group) + 1):
                choices_in_group = choices_in_group * x
            choices_list.append(choices_in_group)
        if choices_list:
            total = 1
            for n in choices_list:
                total = total * n
            return total - 1
        else:
            return 0
    else:
        return 0


def create_new_paraphrase(tree: str, swapping_list: List[SwappingGroup], limit: int) -> List[Dict[str, str]]:
    """
    The function creates and returns a new tree, using swapping_list to permutate branches,
    :param tree: str
    :param swapping_list: List[SwappingGroup]
    :param limit: int
    :return: List[str]
    """

    output_trees: List[Dict[str, str]] = []

    # create initial tree json example
    in_dict = {
        "tree": tree
    }

    if swapping_list:

        # in cycle (while < limit or if no variants)
        while len(output_trees) < limit:

            if len(output_trees) == all_choices_count(swapping_list):
                break

            # ============================================================
            values_mapping: Dict[str, str] = {}

            # fill source values in values_mapping (keys)
            for sg in swapping_list:
                for n in sg.nodes_group:
                    values_mapping[str(n.value)] = ""

            # create swapping list mixed copy and shuffle swapping groups
            swapping_list_mixed = swapping_list.copy()
            new_values_list: List[str] = []
            for sg in swapping_list_mixed:
                random.shuffle(sg.nodes_group)
                for n in sg.nodes_group:
                    new_values_list.append(str(n.value))

            # fill values_mapping mixed values
            counter: int = 0
            for key in values_mapping:
                values_mapping[key] = new_values_list[counter]
                counter += 1

            # create new paraphrase
            updated_string = tree
            for search_value, replace_value in values_mapping.items():
                marked_replace_value = replace_value.replace(replace_value[0], "(@@@ ", 1)
                updated_string = updated_string.replace(search_value, marked_replace_value)
            updated_string = updated_string.replace("@@@ ", "")

            # format new paraphrase
            # delete \n
            updated_string = updated_string.replace("\n", "")
            # delete spaces
            updated_string = updated_string.lstrip()

            # pack to dict
            out_dict = {
                "tree": updated_string
            }

            # if it is equal
            if out_dict == in_dict or out_dict in output_trees:
                continue
            else:
                # append new paraphrase to output_trees list
                output_trees.append(out_dict)

    return output_trees
