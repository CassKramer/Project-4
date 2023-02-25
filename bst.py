# Name: Cassandra Kramer
# OSU Email: kramecas@oregonstate.edu
# Course: CS261 - Data Structures/ Section 405
# Assignment: 4 BST/AVL Tree Implementation
# Due Date: 2/27/2023
# Description: Implement a BST class


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree, if duplicate value add to right of the subtree of that node
        """

        curr = self._root
        new_node = BSTNode(value)

        if self._root is None:
            self._root = new_node
        else:
            while curr.left != new_node and curr.right != new_node:
                if curr.value > new_node.value:
                    if curr.left is None:
                        curr.left = new_node

                    else:
                        curr = curr.left

                if curr.value <= new_node.value:
                    if curr.right is None:
                        curr.right = new_node

                    else:
                        curr = curr.right

    def remove(self, value: object) -> bool:
        """
        Removes a given value from the tree, if the value is removed returns true, if not returns false
        """
        parent = self._root
        pos = self._root

        if pos is None:
            return False

        if pos.value == value:
            if pos.right is None and pos.left is None:
                self._remove_no_subtrees(parent, pos)
                return True

            elif pos.right is None or pos.left is None:
                self._remove_one_subtree(parent, pos)
                return True

            elif pos.right is not None and pos.left is not None:
                self._remove_two_subtrees(parent, pos)
                return True

        while pos.value != value:
            if pos.value < value:
                if pos.right is not None:
                    parent = pos
                    pos = pos.right
                else:
                    return False
            elif pos.value > value:
                if pos.left is not None:
                    parent = pos
                    pos = pos.left
                else:
                    return False

        if pos.right is None and pos.left is None:
            self._remove_no_subtrees(parent, pos)
            return True

        if pos.right is None or pos.left is None:
            self._remove_one_subtree(parent, pos)
            return True

        if pos.right is not None and pos.left is not None:
            self._remove_two_subtrees(parent, pos)
            return True

        return False



    # Consider implementing methods that handle different removal scenarios; #
    # you may find that you're able to use some of them in the AVL.          #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change these methods in any way you'd like.                            #

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove a node that has no subtrees
        """

        if remove_parent == remove_node:
            self._root = None
        if remove_parent.left == remove_node:
            remove_parent.left = None
        else:
            remove_parent.right = remove_node
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove a node that has only one subtree
        """
        if remove_parent == remove_node:
            if remove_node.left is None:
                self._root = remove_node.right
            else:
                self._root = remove_node.left

        if remove_parent.left == remove_node:
            if remove_node.left is None:
                remove_parent.left = remove_node.right
            else:
                remove_parent.left = remove_node.left

        elif remove_parent.right == remove_node:
            if remove_node.left is None:
                remove_parent.right = remove_node.right
            else:
                remove_parent.right = remove_node.left

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Removes a node that has two subtrees
        """
        successor = None
        pos = remove_node.right
        parent_successor = remove_node.right


        while successor != pos:
            if pos.left is not None:
                parent_successor = pos
                pos = pos.left
            else:
                successor = pos

        successor.left = remove_node.left

        if remove_node.right != successor:
            parent_successor.left = successor.right
            successor.right = remove_node.right

        if remove_parent == remove_node:
            self._root = successor

        elif remove_parent.right == remove_node:
            remove_parent.right = successor
        else:
            remove_parent.left = successor



    def contains(self, value: object) -> bool:
        """
        Returns True if value is in the tree, otherwise returns False
        """
        if self._root is None:
            return False

        pos = self._root

        if pos.value == value:
            return True

        while pos.value != value:
            if pos.value < value:
                if pos.right is not None:
                    pos = pos.right
                else:
                    return False
            elif pos.value > value:
                if pos.left is not None:
                    pos = pos.left
                else:
                    return False
        return True
    def inorder_traversal(self) -> Queue:
        """
        Performs an inorder transversal, and returns a queue object that contains the values of the visited nodes
        """
      #  new_queue = Queue()

       # pos = self._root.left
       # parent = self._root

       # while pos.left is not None:
         #   parent = pos
#            pos = pos.left

      #  new_queue.enqueue(pos)

       # while pos.value:
         #   pos = parent




    def find_min(self) -> object:
        """
        Returns the lowest value in the tree
        """
        pos = self._root

        if self._root is None:
            return None

        while pos.left is not None:
            pos = pos.left

        return pos.value

    def find_max(self) -> object:
        """
        Returns the highest value in the tree
        """
        pos = self._root

        if self._root is None:
            return None

        while pos.right is not None:
            pos = pos.right

        return pos.value

    def is_empty(self) -> bool:
        """
        Returns True if Tree is empty or False otherwise
        """
        if self._root is None:
            return True

        return False

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
        """
        pass


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
