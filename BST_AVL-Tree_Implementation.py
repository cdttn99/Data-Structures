import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):

    def __init__(self, value: object) -> None:
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):

    def __init__(self, start_tree=None) -> None:
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Add a value to the AVL tree and rebalance the tree if the value exists do nothing

        Value (Object): value to add to tree
        """
        # Checks if value exists
        if self.contains(value):
            return
        # If the tree is empty add the value as rood
        if not self._root:
            self._root = AVLNode(value)
        else:
            self._root = self._add(self._root, value)

    def _add(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper method to add a value to the avl tree and rebalance it

        node (AVLNode): root of subtree
        value (Object): value to add to the avl tree

        Returns the new root of the subtree
        """
        # Checks if the node is none
        if not node:
            return AVLNode(value)
        # Recursively adds the value to the left or right tree
        if value < node.value:
            node.left = self._add(node.left, value)
            if node.left:
                node.left.parent = node
        else:
            node.right = self._add(node.right, value)
            if node.right:
                node.right.parent = node
        # Update height and rebalance
        self._update_height(node)
        return self._rebalance(node)

    def remove(self, value: object) -> bool:
        """
        Remove a value from the AVL tree and rebalance it

        value (Object): Value to remove from the tree

        Return true if removed and false if value was not found
        """
        if self.contains(value):
            self._root = self._remove(self._root, value)
            return True
        return False

    def _remove(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper metho to remove a value from the tree

        node (AVLNode): root of subtree
        value (Object): value to remove to the avl tree

        Returns new root of the subtree
        """
        # Check if the node is none
        if not node:
            return node
        # Recursively remove the value from the left or right subtree
        if value < node.value:
            node.left = self._remove(node.left, value)
        elif value > node.value:
            node.right = self._remove(node.right, value)
        else:
            # If the node has no left child replace it with its right child
            if not node.left:
                temp = node.right
                if temp:
                    temp.parent = node.parent
                node = None
                return temp
            # If the node has no right child replace it with its left child
            elif not node.right:
                temp = node.left
                if temp:
                    temp.parent = node.parent
                node = None
                return temp
            # If node has two children replace it with its successor
            temp = self._find_min(node.right)
            node.value = temp.value
            node.right = self._remove(node.right, temp.value)

        self._update_height(node)
        return self._rebalance(node)

    def _find_min(self, node: AVLNode) -> AVLNode:
        """
        Finds the node with the min value in the subtree

        node (AVLNode): root of subtree
        
        Returns node with the min value
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculate the balance factor of the node

        node (AVLNode): node to calculate factor for

        Returns the balance factor
        """
        # Get the height of the left child else set to -1
        left_height = node.left.height if node.left else -1
        # Get the height of the right child else set to -1
        right_height = node.right.height if node.right else -1
        return left_height - right_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Get the height of the node

        node (AVLNode): node thats height is needed

        Returns the height of the node
        """
        # Checks for valid node
        if not node:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Does a left rotation on a node

        node (AVLNode): node that needs rotation done on

        Returns the new subtree after rotation
        """
        # Set new_root to the right child of the current node
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node
        # Set the current node to be the left child of new_root
        new_root.left = node
        new_root.parent = node.parent
        node.parent = new_root
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Does a right rotation on a node

        node (AVLNode): node that needs rotation done on

        Returns the new subtree after rotation
        """
        # Set new_root to the left child of the current node
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node
         # Set the current node to be the right child of new_root
        new_root.right = node
        new_root.parent = node.parent
        node.parent = new_root
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _update_height(self, node: AVLNode) -> None:
        """
        Update the height of the node.

        node (AVLNode): node that needs updated height
        """
        if node:
            # Get the height of the left and right children
            left_height = self._get_height(node.left)
            right_height = self._get_height(node.right)
            node.height = 1 + max(left_height, right_height)

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        Rebalance the node if it is unbalanced.

        node (AVLNode): node to rebalance.

        Returns the new root of the subtree after rebalancing.
        """
        if not node:
            return node
        #Update the height of the node
        self._update_height(node)
        balance = self._balance_factor(node)
        # Checks for left heavy
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            node = self._rotate_right(node)
        # Checks for right heavy
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            node = self._rotate_left(node)

        return node