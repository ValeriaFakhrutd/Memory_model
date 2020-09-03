from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # if len(self._subtrees) > 0:
        #     self._expanded = True
        # else:
        #     self._expanded = False

        # self._expanded = True
        # for subtree in self._subtrees:
        #     subtree._expanded = False
        self._expanded = False

        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.
        if self._subtrees == []:
            self.data_size = data_size
        else:
            self.data_size = 0
            for tree in self._subtrees:
                self.data_size += tree.data_size
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        for tree in self._subtrees:
            tree._parent_tree = self

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        if self._name is None or self.data_size == 0:
            pass
        # self.rect = rect
        elif self._subtrees == []:
            self.rect = rect
        else:
            self.rect = rect
            x, y, width, height = rect
            x1 = x
            y1 = y
            if width > height:
                for i in range(len(self._subtrees) - 1):
                    tree = self._subtrees[i]
                    size_coef = tree.data_size / self.data_size
                    temp_width = math.floor(size_coef * width)
                    tree.update_rectangles((x1, y, temp_width, height))
                    x1 = x1 + temp_width
                last_rect = (x1, y, x - x1 + width, height)
                self._subtrees[-1].update_rectangles(last_rect)
            else:
                for i in range(len(self._subtrees) - 1):
                    tree = self._subtrees[i]
                    size_coef = tree.data_size / self.data_size
                    temp_height = math.floor(size_coef * height)
                    tree.update_rectangles((x, y1, width, temp_height))
                    y1 = y1 + temp_height
                last_rect = (x, y1, width, y - y1 + height)
                self._subtrees[-1].update_rectangles(last_rect)

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self._name is None or self.data_size == 0:
            return []
        if self._subtrees == []:
            return [(self.rect, self._colour)]
        else:
            new_list = []
            if self._expanded:
                for tree in self._subtrees:
                    new_list.extend(tree.get_rectangles())
                return new_list
            return [(self.rect, self._colour)]

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        x, y = pos
        if self.is_empty():
            return None
        x1, y1, width, height = self.rect
        # base case:
        if self._subtrees == []: #### and self._expanded
            if x1 <= x <= x1 + width and y1 <= y <= y1 + height:
                return self
            else:
                return None
        elif self._expanded:
            for tree in self._subtrees:
                x2, y2, width2, height2 = tree.rect
                if x2 <= x <= x2 + width2 and y2 <= y <= y2 + height2:
                    return tree.get_tree_at_position(pos)
            return None
        else:
            if x1 <= x <= x1 + width and y1 <= y <= y1 + height:
                return self
            return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        # empty?
        if self._subtrees == [] or self.is_empty():
            return self.data_size
        else:
            temp = 0
            for subtree in self._subtrees:
                temp += subtree.update_data_sizes()
            self.data_size = temp
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if (self._subtrees == [] and destination._subtrees != []):
            # new_subtree = TMTree(self._name, [], self.data_size)
            new_subtree = self
            temp = self._parent_tree
            self._parent_tree._subtrees.remove(self)
            if self._parent_tree._subtrees == []:
                self._parent_tree.data_size = 0
            temp.update_data_sizes()  #####
            # new_subtree = TMTree(self._name, [], self.data_size)
            destination._subtrees.append(new_subtree)
            new_subtree._parent_tree = destination # ?
            destination.update_data_sizes()

        # I changed this part!!!

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if factor >= 0:
            temp = self.data_size
            if self._subtrees == []:
                self.data_size += math.ceil(factor * temp)
            # self.update_data_sizes()
        else:
            factor = abs(factor)
            temp = self.data_size
            if self._subtrees == []:
                self.data_size -= math.ceil(factor * temp)
            # self.update_data_sizes()
        if self.data_size < 1:
            self.data_size = 1
            self.update_data_sizes()


    def expand(self) -> None:
        """
        expanding one rectangle
        """
        if self.is_empty() or self._subtrees == []:
            pass
        else:
            self._expanded = True

    def expand_all(self) -> None:
        """
        expanding rectangle and its subtree, and their subtrees and so on...
        """
        if self.is_empty() or self._subtrees == []:
            pass
        else:
            self.expand()
            for tree in self._subtrees:
                tree.expand_all()

    def collapse(self) -> None:
        """
        collapsing this rectangle, i.e only its parentree is visible rn.
        """
        if self._parent_tree is None:
            pass
        else:
            for subtree in self._parent_tree._subtrees:
                subtree._expanded = False
            self._parent_tree._expanded = False

    def collapse_all(self) -> None:
        """
        collapsing everything so only the main root is visible
        """
        if self._parent_tree is None:
            pass
        else:
            self.collapse()
            self._parent_tree.collapse_all()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        name = os.path.basename(path)
        size = os.path.getsize(path)
        # Base case
        if not os.path.isdir(path):
            # the path to a file
            TMTree.__init__(self, name, [], size)
        # elif os.listdir(path) == []:
        #     #the path to an empty directory
        #     TMTree.__init__(self, name, [], size)

        # Recursive case
        else:
            subtrees_names = os.listdir(path)
            our_list = []
            for tree in subtrees_names:
                sub_path = os.path.join(path, tree)
                temp = FileSystemTree(sub_path)
                our_list.append(temp)
            TMTree.__init__(self, name, our_list, size)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
