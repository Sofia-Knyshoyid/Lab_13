"""
File: linkedbst.py
Author: Ken Lambert
"""


from math import log
from random import shuffle
from timeit import timeit
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_val = ""
            if node is not None:
                str_val += recurse(node.right, level + 1)
                str_val += "| " * level
                str_val += str(node.data) + "\n"
                str_val += recurse(node.left, level + 1)
            return str_val

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            lift_max_in_left_subtreetotop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            else:
                if top.left is None:
                    return 1 + height1(top.right)
                elif top.right is None:
                    return 1 + height1(top.left)
                else:
                    return 1 + max(height1(top.left), height1(top.right))

        top = self._root
        return height1(top)

    def node_num(self):
        'finds the number of nodes'
        total = 0
        for _ in self:
            total+=1
        return total


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        num = self.node_num()
        height = self.height()
        if height < 2 * log(num + 1, 2) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        val_ls = []
        for elem in self:
            if low <= elem <= high:
                val_ls.append(elem)
        return val_ls

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def rebuild(elements):
            if len(elements) == 0:
                return None
            mid_idx = len(elements) // 2
            new_node = BSTNode(elements[mid_idx])
            new_node.left = rebuild(elements[:mid_idx])
            new_node.right = rebuild(elements[mid_idx+1:])
            return new_node

        self._root = rebuild(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in self.inorder():
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        prev_val = None
        for elem in self.inorder():
            if elem < item:
                prev_val = elem
            else:
                return prev_val


    def read_words(self, path):
        """
        reads words from a file;
        returns a list
        """
        total_ls = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.strip()
                total_ls.append(word)
        return total_ls

    def choose_target_words(self, lst, num):
        """
        randomly defines num of
        target words from the list
        """
        shuffle(lst)
        target_words_ls = lst[:num]
        return target_words_ls

    def test_1(self, all_words:list, to_find:list):
        """finds num of words in
        the alphabetically sorted list"""
        idxs = []
        for word in to_find:
            idx = all_words.index(word)
            idxs.append(idx)
        return idxs

    def test_2_3_4(self, binary_tree, to_find:list):
        """finds num of words in the
        alphabetically sorted binary tree"""
        results = []
        for word in to_find:
            result = binary_tree.find(word)
            results.append(result)
        return results


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        words_ls = self.read_words(path)
        look_for = self.choose_target_words(words_ls, 10000)
        # case 1: regular list search
        time_1 = timeit('self.test_1(words_ls, look_for)',\
            globals={'self':LinkedBST(), 'words_ls':words_ls, 'look_for':look_for}, number=1)
        print()
        print('test 1: regular list search')
        print('time 1:', time_1)
        print()

        # case 2: binary tree from sorted list search
        tree_1 = LinkedBST(words_ls)
        time_2 = timeit('self.test_2_3_4(tree_1, look_for)',\
            globals={'self':LinkedBST(), 'tree_1':tree_1, 'look_for':look_for}, number=1)
        print('test 2: binary tree (from sorted list) search')
        print('time 2:', time_2)
        print()

        # case 3: binary tree from unsorted list search
        shuffle(words_ls)
        tree_2 = LinkedBST(words_ls)
        time_3 = timeit('self.test_2_3_4(tree_2, look_for)',\
            globals={'self':LinkedBST(), 'tree_2':tree_2, 'look_for':look_for}, number=1)
        print('test 3: binary tree (from unsorted list) search')
        print('time 3:', time_3)
        print()

        # case 4: balanced binary tree search
        tree_1.rebalance()
        time_4 = timeit('self.test_2_3_4(tree_1, look_for)',\
            globals={'self':LinkedBST(), 'tree_1':tree_1, 'look_for':look_for}, number=1)
        print('test 4: balanced binary tree search')
        print('time 4:', time_4)
        print()




test_tree = LinkedBST()
test_tree.demo_bst('words.txt')
