import pytest
from unittest.mock import Mock

from flexi_nlp_tools.flexi_dict.flexi_trie.flexi_trie_traverser import FlexiTrieTraverser
from flexi_nlp_tools.flexi_dict import FlexiDict


@pytest.fixture
def search_engine():
    return Mock()


@pytest.fixture
def trie_traverser():
    return FlexiTrieTraverser()


def test_apply_string(search_engine, trie_traverser):
    d = FlexiDict(search_engine)
    d['abcd'] = 1

    path_nodes = trie_traverser.apply_string(d.trie.root, 'a')
    assert len(path_nodes) == 1

    path_nodes = trie_traverser.apply_string(d.trie.root, 'abcd')
    assert len(path_nodes) == 4

    path_nodes = trie_traverser.apply_string(d.trie.root, 'ax')
    assert len(path_nodes) == 1

    d = FlexiDict(search_engine)
    d['ab'] = 1
    d['abc'] = 2
    d['abcd'] = 3

    path_nodes = trie_traverser.apply_string(d.trie.root, 'abcd')
    assert len(path_nodes) == 4


def test_get_node_leaves(trie_traverser, search_engine):
    d = FlexiDict(search_engine)
    d['abcd'] = 1
    d['ade'] = 2
    d['ae'] = 3
    assert trie_traverser.get_node_leaves(d.trie.root) == [(3, ['a', 'e']), (2, ['a', 'd', 'e']), (1, ['a', 'b', 'c', 'd'])]

    d = FlexiDict(search_engine)
    d['abcd'] = 3
    d['ade'] = 2
    d['ae'] = 1
    assert trie_traverser.get_node_leaves(d.trie.root) == [(1, ['a', 'e']), (2, ['a', 'd', 'e']), (3, ['a', 'b', 'c', 'd'])]

    d = FlexiDict(search_engine)
    d['abcd'] = 1
    d['abc'] = 2
    d['ab'] = 3
    assert trie_traverser.get_node_leaves(d.trie.root) == [(3, ['a', 'b']), (2, ['a', 'b', 'c']), (1, ['a', 'b', 'c', 'd'])]


def test_get_n_node_leaves(trie_traverser, search_engine):
    d = FlexiDict(search_engine)
    d['abcd'] = 1
    d['ade'] = 2
    d['ae'] = 3
    assert trie_traverser.get_node_leaves(d.trie.root) == [(3, ['a', 'e']), (2, ['a', 'd', 'e']), (1, ['a', 'b', 'c', 'd'])]
    assert trie_traverser.get_node_leaves(d.trie.root, 2) == [(3, ['a', 'e']), (2, ['a', 'd', 'e'])]
    assert trie_traverser.get_node_leaves(d.trie.root, 1) == [(3, ['a', 'e']), ]
