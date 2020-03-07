from papers import PaperTree, csv
from typing import List

#DATA_FILE =

def test_all_papers_in() -> None:
    num_papers_csv = 0
    with open('cs1_papers.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for _ in reader:
            num_papers_csv += 1

    # Should subtree parameter be ignored
    tree = PaperTree('CS1', [], by_year=False, all_papers=True)
    assert count_papers(tree) == num_papers_csv

    tree = PaperTree('CS1', [], by_year=True, all_papers=True)
    assert count_papers(tree) == num_papers_csv


def count_papers(tree: PaperTree) -> int:
    if tree._subtrees == []:
        return 1
    else:
        count = 0
        for subtree in tree._subtrees:
            count += count_papers(subtree)
        return count


def test_correct_category() -> None:
    main_tree = PaperTree('CS1', [], by_year=False, all_papers=True)
    with open('cs1_papers.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for row in reader:
            categories = row[3].split(':')
            test_tree = main_tree
            for string in categories:
                cate = string.strip()
                cate_is_child = False
                for subtree in test_tree._subtrees:
                    if subtree._name == cate:
                        cate_is_child = True
                        test_tree = subtree
                        break
                assert cate_is_child
            paper_in_category = False
            for subtree in test_tree._subtrees:
                if row[0] == subtree._authors and row[1] == subtree._name and \
                        row[4] == subtree._doi and \
                        row[5] == str(subtree.data_size):
                    paper_in_category = True
            assert paper_in_category

    main_tree = PaperTree('CS1', [], by_year=True, all_papers=True)
    with open('cs1_papers.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        reader.__next__()
        for row in reader:
            year = row[2]
            year_in_first_sub = False
            for subtree in main_tree._subtrees:
                if subtree._name == year:
                    year_in_first_sub = True
                    test_tree = subtree
            assert year_in_first_sub

            categories = row[3].split(':')
            for string in categories:
                cate = string.strip()
                cate_is_child = False
                for subtree in test_tree._subtrees:
                    if subtree._name == cate:
                        cate_is_child = True
                        test_tree = subtree
                        break
                assert cate_is_child
            paper_in_category = False
            for subtree in test_tree._subtrees:
                if row[0] == subtree._authors and row[1] == subtree._name and \
                        row[4] == subtree._doi and \
                        row[5] == str(subtree.data_size):
                    paper_in_category = True
            assert paper_in_category


def test_category_reverse() -> None:
    main_tree = PaperTree('CS1', [], by_year=False, all_papers=True)
    papers = find_leaves(main_tree)
    for leaf in papers:
        with open('cs1_papers.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                one_line = False
                if leaf._name == row[1] and leaf._authors == row[0] and \
                    leaf._doi == row[4] and leaf.data_size == int(row[5]):
                    one_line = True
                    t = leaf._parent_tree
                    categories = t._name
                    while t._parent_tree._name != 'CS1':
                        t = t._parent_tree
                        categories = t._name + ': ' +  categories

                    assert categories == row[3]
                    break
            assert one_line

    main_tree = PaperTree('CS1', [], by_year=True, all_papers=True)
    papers = find_leaves(main_tree)
    for leaf in papers:
        with open('cs1_papers.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                one_line = False
                if leaf._name == row[1] and leaf._authors == row[0] and \
                        leaf._doi == row[4] and leaf.data_size == int(row[5]):
                    one_line = True
                    t = leaf._parent_tree
                    categories = t._name
                    while t._parent_tree._name != 'CS1':
                        t = t._parent_tree
                        categories = t._name + ': ' + categories
                    assert categories == row[2] + ': ' + row[3]
                    break
            assert one_line


def find_leaves(tree: PaperTree) -> List[PaperTree]:
    if tree._subtrees == []:
        return [tree]
    else:
        lst = []
        for subtree in tree._subtrees:
            lst.extend(find_leaves(subtree))
        return lst


if __name__ == '__main__':
    import pytest
    pytest.main(['task6_tests.py'])
