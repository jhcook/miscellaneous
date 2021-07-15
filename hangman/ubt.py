#!/usr/bin/env python3

from sys import stdin

class BinaryTree:

    def __init__(self, val:int=None):
        self.l_node = None
        self.r_node = None
        self.val = val

    def insert(self, val):
        #print("Inserting {0}".format(val))
        if self.val is None:
            self.val = val
        else:
            if self.val > val:
                if self.l_node is None:
                    self.l_node = BinaryTree(val)
                else:
                    self.l_node.insert(val)
            else:
                if self.r_node is None:
                    self.r_node = BinaryTree(val)
                else:
                    self.r_node.insert(val)


    def depth(self):
        l_depth = self.l_node.depth() if self.l_node else -1
        r_depth = self.r_node.depth() if self.r_node else -1
        return max(l_depth, r_depth) + 1

    def display(self):
        """Display the binary tree in ASCII format.

        Totally ripped off: 
        https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python
        """
        lines, _, _, _ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.r_node is None and self.l_node is None:
            line = '%s' % self.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.r_node is None:
            lines, n, p, x = self.l_node._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.l_node is None:
            lines, n, p, x = self.r_node._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.l_node._display_aux()
        right, m, q, y = self.r_node._display_aux()
        s = '%s' % self.val
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2



line = stdin.readline()
line = line.split()

tree = BinaryTree()
for i in line:
    tree.insert(int(i))

tree.display()

print(tree.depth())