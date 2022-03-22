"""This file is the provided AVLTree class from prof. Yuan Tian. In this file
I will only comment altered or added code which appear in the following
WebPageIndex -> def __init__(self, file):
             -> getCount(self, s):
             -> put(self, key, value=None):
             -> print_tree(self, root, space):
"""


class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.height = None


class WebPageIndex:
    def __init__(self, file):
        """
        Initializes AVL tree that is an index representation of a given webpage
        :param file: Webpage that has it's contents put in AVL tree
        """
        self.root = None
        self.contents = open(file, "r").read().lower()
        # Only keep alphanumeric characters
        self.contents = self.contents.replace(";", "")
        self.contents = self.contents.replace(")", " ")
        self.contents = self.contents.replace(",", "")
        self.contents = self.contents.replace(".", "")
        self.contents = self.contents.replace("(", " ")
        self.contents = self.contents.replace("/", " ")
        self.contents = self.contents.replace(":", "")
        self.contents = self.contents.replace("?", "")

        self.contents = self.contents.split()
        self.path = file

        # Adding every word into AVL tree
        for position, word in enumerate(self.contents):
            self.put(word, position)

    def search(self, data, cur_node):
        if cur_node is None:
            return False

        elif data == cur_node.key:
            return cur_node

        if data < cur_node.key:
            return self.search(data, cur_node.left)
        else:
            return self.search(data, cur_node.right)

    def get(self, data):

        node = self.search(data, self.root)

        if node is not None:
            return node.value

        return None

    def getCount(self, s):
        """
        Gets number of times a word appears in a web page... AKA priority
        :param s: determine number of occurrences of this string
        :return: number of times a word appears
        """
        possible_node = self.search(s, self.root)
        if possible_node is False:
            return False
        else:
            return len(possible_node.value)

    def put(self, key, value=None):
        """
        Puts node in AVL tree
        :param key: word in web page
        :param value: position of the key
        """
        possible_node = self.search(key, self.root)

        # If key is not in AVL tree
        if not possible_node:
            key = Node(key, [])
            key.value.append(value)
            y = None
            x = self.root

            while x is not None:
                y = x
                if key.key < x.key:
                    x = x.left
                elif key.key > x.key:
                    x = x.right

            key.parent = y

            if y is None:
                self.root = key

            elif key.key < y.key:
                y.left = key
            else:
                y.right = key

            self.set_height(key, key.key)
        # If key is in AVL tree, append value to value of node
        else:
            possible_node.value.append(value)

    def set_height(self, node, new_insert=None):
        new_insert = new_insert
        node.height = self.set_height2(node)

        if new_insert is not None:
            self.unbalance_detector(node, new_insert)

        if node.parent is not None:
            self.set_height(node.parent, new_insert)

    def set_height2(self, node):

        if node is None:
            return 0
        left = self.set_height2(node.left)
        right = self.set_height2(node.right)
        return max(left, right) + 1

    def set_height3(self, node):

        if node is not None:
            node.height = self.set_height2(node)
            self.set_height3(node.left)
            self.set_height3(node.right)

    def unbalance_detector(self, node, new_insert):

        root = node
        if root.left is not None:
            left_height = root.left.height

        else:
            left_height = 0

        if root.right is not None:
            right_height = root.right.height
        else:
            right_height = 0

        b_height = left_height - right_height

        if b_height < -1 or b_height > 1:
            self.direction_detector(node, b_height, new_insert)

    def direction_detector(self, node, balance_factor, new_insert):

        if balance_factor > 1 and new_insert < node.left.key:
            self.left_rotation(node)

        elif balance_factor < -1 and new_insert > node.right.key:
            self.right_rotation(node)

        elif balance_factor > 1 and new_insert > node.left.key:
            self.right_rotation(node.left)
            self.left_rotation(node)

        elif balance_factor < -1 and new_insert < node.right.key:
            self.left_rotation(node.right)
            self.right_rotation(node)

    def left_rotation(self, node):

        root = node
        pivot = node.left  # find the pivot in left side

        root.left = pivot.right  # move the right child of pivot to root
        # FIX2: add parent reset
        if pivot.right is not None:
            pivot.right.parent = root
        pivot.right = root  # then pivot has right child root

        # reset their parent
        pivot.parent = root.parent
        root.parent = pivot

        # if the pivot has parent
        if pivot.parent is not None:

            # depends if pivot is in his parent left or right
            # according to the position, insert pivot as child to his parent
            # FIX1: need to check if pivot.parent.left exists or not
            if pivot.parent.left is not None:
                if pivot.parent.left.key == root.key:
                    pivot.parent.left = pivot
                else:
                    pivot.parent.right = pivot
            else:
                pivot.parent.right = pivot

            # reset the height for parent above
            self.set_height(pivot.parent)
        else:
            self.root = pivot

        # reset the height for pivot
        self.set_height3(pivot)

    def right_rotation(self, node):

        root = node
        pivot = node.right

        root.right = pivot.left
        # FIX2: add parent reset
        if pivot.left is not None:
            pivot.left.parent = root
        pivot.left = root

        pivot.parent = root.parent
        root.parent = pivot

        if pivot.parent is not None:
            # FIXED: need to check if pivot.parent.left exists or not
            if pivot.parent.left is not None:
                if pivot.parent.left.key == root.key:
                    pivot.parent.left = pivot
                else:
                    pivot.parent.right = pivot
            else:
                pivot.parent.right = pivot

            self.set_height(pivot.parent)
        else:
            self.root = pivot
        self.set_height3(pivot)

    def print_tree(self, root, space):
        """
        Prints BST in tree structure; horizontally where root is most left
        :param root: Root of BST
        :param space: Space between nodes
        """
        if root is None:
            return

        space += 15

        self.print_tree(root.right, space)
        print("")

        for i in range(10, space):
            print(' ', end='')

        print(str(root.key) + ":" + str(len(root.value)),
              end='')  # Prints nodes from right to left
        print("")

        self.print_tree(root.left, space)


def main():
    page = WebPageIndex("data/doc1-arraylist.txt")
    print(page.getCount("and"))


# Testing
if __name__ == '__main__':
    main()
