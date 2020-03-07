"""Assignment 2: Modelling CS Education research paper data

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/

Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.

TODO: (Task 6) Complete the steps below
Recommended steps:
1. Start by reviewing the provided dataset in cs1_papers.csv. You can assume
   that any data used to generate this tree has this format,
   i.e., a csv file with the same columns (same column names, same order).
   The categories are all in one column, separated by colons (':').
   However, you should not make assumptions about what the categories are, how
   many categories there are, the maximum number of categories a paper can have,
   or the number of lines in the file.

2. Read through all the docstrings in this file once. There is a lot to take in,
   so don't feel like you need to understand it all the first time.
   Draw some pictures!
   We have provided the headers of the initializer as well as of some helper
   functions we suggest you implement. Note that we will not test any
   private top-level functions, so you can choose not to implement these
   functions, and you can add others if you want to for your solution.
   For this task, we will be testing that you are building the correct tree,
   not that you are doing it in a particular way. We will access your class
   in the same way as in the client code in the visualizer.

3. Plan out what you'll need to do to implement the PaperTree initializer.
   In particular, think about how to use the boolean parameters to do different
   things in setting up the tree. You may also find it helpful to review the
   Python documentation about the csv module, which you are permitted and
   encouraged to use. You should have a good plan, including what your subtasks
   are, before you begin writing any code.

4. Write the code for the PaperTree initializer and any helper functions you
   want to use in your design. You should not make any changes to the public
   interface of this module, or of the PaperTree class, but you can add private
   attributes and helpers as needed.

5. Tidy and test your code, and try it with the visualizer client code. Make
   sure you have documented any new private attributes, and that PyTA passes
   on your code.
"""
import csv
from typing import List, Dict
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    _authors:
        authors of the paper, does not keep any information for categories.
    _doi:
        link of the paper, '' for the categories
    _by_year:
        stores in formation if sorting is doing by year or not.
    These should store information about this paper's <authors> and <doi>.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """

    _authors: str
    _doi: str
    _by_year: bool

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        if subtrees == []:
            TMTree.__init__(self, name, subtrees, citations) # i.e our file is a
            self._doi = doi
            self._authors = authors
            # self._citation = citations ### Data_size
            self._by_year = by_year
        if not all_papers and subtrees != []:
            TMTree.__init__(self, name, subtrees, citations)
            self._doi = doi
            self._authors = authors
            self._by_year = by_year
        if all_papers:
            x = _get_paper_list(by_year)
            subtrees = _build_tree_from_dict(x)
            TMTree.__init__(self, name, subtrees, citations)
            self._doi = doi
            self._authors = authors
            self._by_year = by_year

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return ": "

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return '(paper)'
        else:
            return '(category)'


def _build_tree_from_dict(nested_dict: Dict) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    lst = []
    for items in nested_dict:
        if nested_dict[items] == {}:
            temp_tree = PaperTree(items[1], [],
                                  items[0], items[2],
                                  items[3],
                                  False, False)
            # put here data for authors, size ect
            lst.append(temp_tree)
        else:
            temp_tree = PaperTree(items,
                                  _build_tree_from_dict(nested_dict[items]),
                                  by_year=False, all_papers=False)
            temp_tree.update_data_sizes()
            lst.append(temp_tree)

    return lst


def _get_paper_list(by_year: bool) -> dict:
    """
    'hey'
    """
    dic = {}
    with open(DATA_FILE, newline='') as csv_file:
        csv_file.readline()
        reader = csv.reader(csv_file)
        for line in reader:
            author, title, year, categories, url, size = line
            size = int(size)
            # year = int(year)
            categories = categories.split(":")
            for i in range(len(categories)):
                categories[i] = categories[i].strip()
            tup1 = (author, title, url, size)
            categories.append(tup1)
            if by_year:
                categories.insert(0, year)
            new = categories
            dic = _convert_dict(new, dic)
            # print(dic)
    csv_file.close()
    return dic


def _convert_dict(lst: List, dics: Dict) -> Dict:
    if len(lst) == 0:
        pass
    elif len(lst) == 1:
        if lst[0] in dics:
            pass
        else:
            d = {lst[0]: {}}
            dics.update(d)
    else:
        if lst[0] in dics:
            dics[lst[0]] = _convert_dict(lst[1:], dics[lst[0]])
        else:
            dics[lst[0]] = _convert_dict(lst[1:], {})
    return dics


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict', '_get_paper_list'],
        'max-args': 8
    })
    # x = _get_paper_list()
    # y = _build_tree_from_dict(x)
    # print(y)
