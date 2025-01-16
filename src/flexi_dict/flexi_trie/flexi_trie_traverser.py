from typing import List, Tuple
from collections import deque

from .flexi_trie import FlexiTrieNode
from ..config import DEFAULT_TOPN_LEAVES


class FlexiTrieTraverser:
    """
    A class responsible for traversing the prefix tree and applying a string to the tree.

    Methods:
        apply_string(node, s, position): Applies a string to the prefix tree and traverses from the given node.
    """

    @staticmethod
    def apply_string(node: FlexiTrieNode, s: str) -> List[FlexiTrieNode]:

        path_nodes: List[FlexiTrieNode] = []

        for char in s:
            current_node = node.get(char)
            if not current_node:
                return path_nodes

            path_nodes.append(current_node)
            node = current_node

        return path_nodes
    #
    # @staticmethod
    # def get_node_leaves(node: FlexiTrieNode, topn: int = DEFAULT_TOPN_LEAVES) -> List[int]:
    #
    #     queue = deque(list(node.children.values()))
    #     leaves = []
    #
    #     while queue and len(leaves) < topn:
    #         current_node = queue.popleft()
    #
    #         if current_node.values:
    #             leaves.extend(current_node.values)
    #             if len(leaves) >= topn:
    #                 return leaves[:topn]
    #
    #         queue.extend(current_node.children.values())
    #
    #     return leaves[:topn]


    @staticmethod
    def get_node_leaves(node: FlexiTrieNode, topn: int = DEFAULT_TOPN_LEAVES) -> List[Tuple[int, List[str]]]:
        """
        Collects leaf node values and their paths from the given node.

        Args:
            node (FlexiTrieNode): The starting node of the tree or subtree.
            topn (int): The maximum number of leaf nodes to return.

        Returns:
            List[Tuple[int, List[str]]]: A list of tuples where each tuple contains:
                                          - the leaf node value
                                          - the path of symbols leading to that leaf.
        """
        queue = deque([(child, [key,]) for key, child in node.children.items()])  # Queue holds pairs of (current_node, current_path)
        leaves = []

        while queue and len(leaves) < topn:
            current_node, current_path = queue.popleft()

            # If the current node is a leaf (it has values), we add its values and paths
            if current_node.values:
                for value in current_node.values:
                    leaves.append((value, current_path))

                # If we've gathered enough leaves, return them
                if len(leaves) >= topn:
                    return leaves[:topn]

            # Add the children to the queue with the updated path
            for symbol, child_node in current_node.children.items():
                queue.append((child_node, current_path + [symbol]))

        return leaves[:topn]
