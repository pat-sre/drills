# Trie (Prefix Tree)
#
# Implement a Trie data structure that supports:
#
#   insert(word)        -> None
#       Insert a word into the trie.
#
#   search(word)        -> bool
#       Return True if the exact word exists in the trie, False otherwise.
#
#   starts_with(prefix) -> bool
#       Return True if any word in the trie starts with the given prefix.
#
# The trie is case-sensitive ("Hello" and "hello" are different words).
#
# Implementation hint:
#   Each node stores a dict of children keyed by character, and an
#   is_end flag marking whether a complete word ends at that node.
#
# Example:
#   t = Trie()
#   t.insert("apple")
#   t.search("apple")       # True
#   t.search("app")         # False  — "app" was not inserted
#   t.starts_with("app")    # True   — "apple" starts with "app"
#   t.insert("app")
#   t.search("app")         # True


class TrieNode:
    def __init__(self):
        self.is_end = False
        self.children = {}


class Trie:
    def __init__(self):
        pass


solve = Trie
