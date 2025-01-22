import logging
import bisect
from typing import List, Dict, Optional
from dataclasses import dataclass

from ..config import DEFAULT_TOPN_LEAVES, MAX_CORRECTION_RATE

from ..flexi_trie import FlexiTrie, FlexiTrieNode, FlexiTrieTraverser
from .fuzzy_search_result import FuzzySearchResult
from .correction_detail import CorrectionDetail
from .correction import Correction, SymbolInsertion, SymbolsDeletion, SymbolSubstitution, SymbolsTransposition
from ..config import MAX_QUEUE_SIZE

logger = logging.getLogger(__name__)


@dataclass
class SearchState:
    position: int
    path: str
    node: FlexiTrieNode
    corrections: List[CorrectionDetail]


class SearchEngine:
    """
    Search engine for performing fuzzy searches within an FlexiTrie.

    Attributes:
        _trie_traverser (FlexiTrieTraverser): Helper class to traverse the trie.
        _corrections (List[Correction]): List of correction strategies to apply during the search.
    """

    def __init__(self, corrections: Optional[List[Correction]] = None, symbol_insertion: Optional[Correction] = None):
        """
        Initializes the SearchEngine with a list of corrections.

        Args:
            corrections (List[Correction]): List of correction strategies.
        """
        self._trie_traverser = FlexiTrieTraverser()
        self._corrections = corrections or [SymbolInsertion(), SymbolsDeletion(), SymbolSubstitution(), SymbolsTransposition()]
        self._symbol_insertion = symbol_insertion or SymbolInsertion()

    def search(
            self, trie: FlexiTrie, query: str,
            topn_leaves: int = DEFAULT_TOPN_LEAVES,
            max_correction_rate: Optional[float] = None,
            max_correction_rate_for_leaves: Optional[float] = None
    ) -> List[FuzzySearchResult]:
        """
        Perform a fuzzy search in the trie based on the query.

        Args:
            trie (FlexiTrie): Trie structure to search.
            query (str): Query string.
            topn_leaves (int): Number of leaves to consider in results.
            max_correction_rate (float): Maximum allowed correction rate.

        Returns:
            List[FuzzySearchResult]: List of search results.
        """
        logger.info(f"Starting search for query: '{query}'")

        if max_correction_rate is None:
            max_correction_rate = MAX_CORRECTION_RATE
        if max_correction_rate_for_leaves is None:
            max_correction_rate_for_leaves = max_correction_rate

        search_result: List[FuzzySearchResult] = []
        visited_status: Dict[int, int] = {}
        added = set()

        path_nodes = self._trie_traverser.apply_string(node=trie.root, s=query)

        if len(path_nodes) == len(query):
            logger.info("Exact match found.")
            search_result = self._generate_search_result_from_node(
                node=path_nodes[-1],
                path=query,
                key=query,
                topn_leaves=topn_leaves,
                corrections=[],
                max_correction_rate_for_leaves=max_correction_rate_for_leaves
            )
            visited_status[path_nodes[-1].idx] = 1
            added = {x.value for x in search_result}

            if trie.find(query):
                return search_result
        queue = [SearchState(position + 1, query[:position + 1], node, []) for position, node in enumerate(path_nodes)]
        queue.append(SearchState(0, "", trie.root, []))

        iteration = 0

        while queue:
            iteration += 1
            logger.info(f"Iteration {iteration}: {len(queue)} states in the queue.")
            updated_queue = []

            for step in queue:
                logger.debug(f"Processing node ID {step.node.idx} at position {step.position}, path='{step.path}', corrections={[c.correction_name for c in step.corrections]}")

                if step.position == len(query):
                    node_result = self._generate_search_result_from_node(
                        node=step.node, key=query[:step.position], path=step.path,
                        topn_leaves=topn_leaves, corrections=step.corrections,
                        max_correction_rate_for_leaves=max_correction_rate_for_leaves)
                    for item in node_result:
                        if item.value not in added:
                            pos = bisect.bisect_left(
                                search_result, item.total_corrections_price,
                                lo=0, hi=len(search_result),
                                key=lambda x: x.total_corrections_price)
                            search_result.insert(pos, item)

                            added.add(item.value)
                            logger.info(f"Added result: path='{item.path}', value='{item.value}'")
                    continue

                if visited_status.get(step.node.idx) == 1:
                    logger.debug(f"Node ID {step.node.idx} already visited.")
                    continue

                visited_status[step.node.idx] = 1

                nodes_ids_path = self._trie_traverser.apply_string(step.node, query[step.position:])
                for i, node in enumerate(nodes_ids_path):
                    updated_queue.append(SearchState(
                        position=step.position + i + 1,
                        path=step.path + query[step.position: step.position + i + 1],
                        node=node,
                        corrections=step.corrections))
                    if len(updated_queue) > MAX_QUEUE_SIZE:
                        break
                if len(updated_queue) >= MAX_QUEUE_SIZE:
                    queue = updated_queue[:MAX_QUEUE_SIZE]
                    continue

                current_correction_rate = (len(step.corrections) + 1) / len(query)
                if current_correction_rate <= max_correction_rate:
                    for correction in self._corrections:
                        corrections_states = correction.apply(query=query, search_state=step)
                        for correction_state in corrections_states:
                            if correction_state.node.idx == step.node.idx:
                                visited_status[step.node.idx] = 0
                                logger.debug(f"Correction loopback detected for node ID {step.node.idx}. Marked for revisit.")
                        updated_queue.extend(corrections_states)
                        if len(updated_queue) > MAX_QUEUE_SIZE:
                            break
            if len(updated_queue) >= MAX_QUEUE_SIZE:
                queue = updated_queue[:MAX_QUEUE_SIZE]
                continue

            if not updated_queue:
                logger.info("No items left in queue. Search completed.")
                break

            queue = updated_queue

        logger.info(
            f"Search completed. Found {len(search_result)} results:\n" +
            "\n".join([
                f'{i+1}) "{x.path}" corr_rate: {len(x.corrections) / len(query):4.2f}, corr_price: {x.total_corrections_price:4.2f}, corrs: {x.corrections}'
                for i, x in enumerate(search_result)]))

        return search_result

    def _generate_search_result_from_node(
            self,
            node: FlexiTrieNode,
            key: str,
            path: str,
            topn_leaves: int,
            corrections: List[CorrectionDetail],
            max_correction_rate_for_leaves: float
    ) -> List[FuzzySearchResult]:
        """
        Generate search results from a trie node and its leaves.

        Args:
            node (FlexiTrieNode): Current node in the trie.
            key (str): Key string associated with the result.
            path (str): Path taken to reach this node.
            topn_leaves (int): Number of leaves to consider.
            corrections (List[CorrectionDetail]): List of corrections applied.

        Returns:
            List[FuzzySearchResult]: List of fuzzy search results.
        """
        logger.debug(f"Generating search result for node #{node.idx} with path: '{path}' and corrections: {corrections}")
        result = [
            FuzzySearchResult(value=value, key=key, path=path, corrections=corrections)
            for value in node.values
        ]
        leaves = self._trie_traverser.get_node_leaves(node, topn=topn_leaves)
        logger.debug(f'Generating search result for node #{node.idx}: found leaves: {leaves}')

        for value, leaf_path in leaves:
            leaf_path = ''.join(leaf_path)

            corrections = corrections + [
                    CorrectionDetail(
                        correction_name=self._symbol_insertion.name,
                        position=len(path) + c_pos,
                        parameters=[c, ],
                        price=self._symbol_insertion.price
                    )
                    for c_pos, c in enumerate(leaf_path)]
            correction_rate = min(1., len(corrections) / (len(path) + len(leaf_path)))
            logger.debug(
                f'Generating search result for node #{node.idx}: leaf "{"".join(leaf_path)}":\n'
                f'\t corrections number: {len(corrections)}\n'
                f'\t        path length: {len(path) + len(leaf_path)} ("{path + leaf_path}")\n'
                f'\t    correction rate: {correction_rate:4.2f}\n'
                f'\t        corrections: {[c.correction_name for c in corrections]}\n'
                f'\t    added to result: {correction_rate <= max_correction_rate_for_leaves}')

            if correction_rate > max_correction_rate_for_leaves:
                continue

            fuzzy_search_result = FuzzySearchResult(
                value=value,
                key=key,
                path=path + leaf_path,
                corrections=corrections
            )

            pos = bisect.bisect_left(
                                result, fuzzy_search_result.total_corrections_price,
                                lo=0, hi=len(result),
                                key=lambda x: x.total_corrections_price)
            result.insert(pos, fuzzy_search_result)

        logger.debug(f"Generated {len(result)} results for node #{node.idx}.")
        return result
