from typing import *
from tm_trees import TMTree, FileSystemTree
from treemap_visualiser import *


def get_trees() -> list:
    t13 = TMTree('t13', [], 50)
    t12 = TMTree('t12', [], 50)
    t11 = TMTree('t11', [t12, t13], 0)
    t10 = TMTree('t10', [], 150)
    t9 = TMTree('t9', [], 49)
    t8 = TMTree('t8', [t10, t11], 0)
    t7 = TMTree('t7', [], 75)
    t6 = TMTree('t6', [], 37)
    t5 = TMTree('t5', [], 139)
    t4 = TMTree('t4', [t7, t8], 0)
    t3 = TMTree('t3', [t6, t9], 0)
    t2 = TMTree('t2', [t4, t5], 0)
    t1 = TMTree('t1', [t2, t3], 0)
    return [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13]


# === Task 2 tests ===
def test_update_rectangles() -> Any:
    t8 = TMTree('t8', [], 249)
    t7 = TMTree('t7', [], 75)
    t6 = TMTree('t6', [], 37)
    t5 = TMTree('t5', [], 139)
    t4 = TMTree('t4', [t7, t8], 0)
    t3 = TMTree('t3', [t6], 0)
    t2 = TMTree('t2', [t4, t5], 0)
    t1 = TMTree('t1', [t2, t3], 0)
    t1.expand_all()

    assert t1.update_data_sizes() == 500

    t1.update_rectangles((0, 0, 800, 500))
    assert t1.rect == (0, 0, 800, 500)
    assert t2.rect == (0, 0, 740, 500)
    assert t3.rect == (740, 0, 60, 500)
    assert t4.rect == (0, 0, 517, 500)
    assert t5.rect == (517, 0, 223, 500)
    assert t6.rect == (740, 0, 60, 500)
    assert t7.rect == (0, 0, 119, 500)
    assert t8.rect == (119, 0, 398, 500)


def test_get_rectangles() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()

    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))
    rectangles = t1.get_rectangles()

    assert len(rectangles) == 7
    assert rectangles[0][0] == (0, 0, 472, 115)
    assert rectangles[1][0] == (0, 115, 283, 385)
    assert rectangles[2][0] == (283, 115, 189, 192)
    assert rectangles[3][0] == (283, 307, 189, 193)
    assert rectangles[4][0] == (472, 0, 202, 500)
    assert rectangles[5][0] == (674, 0, 126, 215)
    assert rectangles[6][0] == (674, 215, 126, 285)


def test_get_rectangles2() -> None:
    t3 = TMTree('t3', [], 0)
    t2 = TMTree('t2', [], 100)
    t1 = TMTree('t1', [t2, t3], 0)

    t1.expand_all()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 1
    assert a[0][0] == (0, 0, 800, 500)

    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t7.data_size = 0
    t9.data_size = 0
    t5.data_size = 0
    t12.data_size = 0
    t13.data_size = 0
    t1.update_data_sizes
    t1.expand_all()
    t1.update_rectangles((0, 0, 800, 500))

    a = t1.get_rectangles()
    assert len(a) == 2


def test_get_rectangles3() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()

    t1.expand_all()
    assert t1.data_size == 550
    t6.move(t4)
    t1.update_data_sizes
    t1.update_rectangles((0, 0, 800, 500))
    rectangles = t1.get_rectangles()
    len(rectangles) == 7
    assert t1.get_tree_at_position((800, 20)) == t9


# === Task 3 Test ===
def test_get_tree_at_position() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))
    # how the tree will look
    # [(0, 0, 472, 115), (0, 115, 283, 500), (283, 115, 472, 307),
    # (283, 307, 472, 500), (472, 0, 674, 500), (674, 0, 800, 215),
    # (674, 215, 800, 500)]

    p1 = (0, 192)
    p2 = (0, 500)
    p3 = (283, 125)
    p4 = (472, 307)
    p5 = (700, 60)
    p6 = (700, 215)

    assert t1.get_tree_at_position(p1) == t10
    assert t1.get_tree_at_position(p2) == t10
    assert t1.get_tree_at_position(p3) == t10
    assert t1.get_tree_at_position(p4) == t12
    assert t1.get_tree_at_position(p5) == t6
    assert t1.get_tree_at_position(p6) == t6


# === Task 4 Test === ????
def test_update_data_sizes() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t7.data_size = 100
    assert t1.update_data_sizes() == 575


def test_update_data_sizes2() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t10.data_size = 0
    t9.data_size = 0
    assert t1.update_data_sizes() == 351


def test_update_sizes3() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t7.data_size = 0
    t6.data_size = 0
    assert t1.update_data_sizes() == 438


def test_move() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    # move file to a folder
    t7.move(t3)
    assert t7 in t3._subtrees
    assert t7._parent_tree == t3
    t1.update_data_sizes()
    assert t4.data_size == 250
    t7.move(t4)

    # move a folder to a file
    t4.move(t9)
    assert t4 in t2._subtrees
    assert t4._parent_tree == t2

    # move a file to a file
    t13.move(t6)
    assert t13 in t11._subtrees
    assert t13._parent_tree == t11

    # move a folder to folder
    t2.move(t3)
    assert t2 in t1._subtrees
    assert t2._parent_tree == t1


def test_move2() -> None:
    t6 = TMTree('t6', [], 50)
    t5 = TMTree('t5', [], 200)
    t4 = TMTree('t4', [], 100)
    t3 = TMTree('t3', [t6], 0)
    t2 = TMTree('t2', [t4, t5], 0)
    t1 = TMTree('t1', [t2, t3], 0)
    t1.expand_all()
    assert t1.data_size == 350
    t1.update_rectangles((0, 0, 800, 500))
    t6.move(t2)
    assert t6._parent_tree == t2
    t1.update_data_sizes()
    assert t3.data_size == 0


def test_change_data_size1() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    # change the size for a file
    t12.change_size(0)
    assert t12.data_size == 50
    t1.update_data_sizes()
    assert t1.data_size == 550


# test the seize change of a file
def test_change_data_size2() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    # change the size for a file
    t12.change_size(1390)
    assert t12.data_size == 69550
    t1.update_data_sizes()
    assert t1.data_size == 70050


def test_change_data_size3() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    t10.change_size(3.9)
    assert t10.data_size == 735
    t1.update_data_sizes()
    assert t1.data_size == 1135


def test_change_data_size4() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    t5.change_size(-0.89)
    assert t5.data_size == 15
    t1.update_data_sizes()
    assert t1.data_size == 426


def test_change_data_size5() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    t5.change_size(-1)
    t1.update_data_sizes()
    assert t5.data_size == 1
    t1.update_data_sizes()
    assert t1.data_size == 412


def test_change_data_size6() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    t9.change_size(5)
    t6.change_size(5)
    t1.update_data_sizes()
    assert t3.data_size == 516
    assert t1.data_size == 980
    t1.update_rectangles((0, 0, 800, 500))
    assert t1.get_tree_at_position((800, 250)) == t9


# change the size for a folder
def test_change_data_size7() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    assert t1.data_size == 550
    t1.update_rectangles((0, 0, 800, 500))

    t4.change_size(-0.89)
    assert t4.data_size == 325
    t1.update_data_sizes()
    assert t1.data_size == 550

    t3.change_size(1.96)
    assert t3.data_size == 86
    t1.update_data_sizes()
    assert t1.data_size == 550


# ==== Tests for task 5 ====

def test_expand1() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 2


def test_expand2() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand()
    t2.expand()
    t4.expand()
    t8.expand()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 5


def test_expand3() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand()
    # expanding a folder whose parent is not expanded
    t8.expand()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 2


def test_expand4() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand()
    # expanding a leaf
    t5.expand()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 2


def test_expand_all1() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 7


def test_expand_all2() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand()
    t2.expand_all()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 6


def test_expand_all3() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand()
    t3.expand_all()
    t7.expand_all()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 3


# look at these again

def test_collapse1() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t4.collapse()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 3


def test_collapse2() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t4.collapse()
    t3.collapse()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 1


def test_collapse3() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t1.collapse()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 7


def test_collapse4() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t11.collapse()
    t9.collapse()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 4


def test_collapse_all1() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.collapse_all()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 1


def test_collapse_all2() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t4.collapse_all()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 1


def test_collapse_all3() -> None:
    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13 = get_trees()
    t1.expand_all()
    t5.collapse_all()
    t1.update_rectangles((0, 0, 800, 500))
    a = t1.get_rectangles()
    assert len(a) == 1


if __name__ == '__main__':
    import pytest
    pytest.main(['tests.py'])
    print("Hey Sexy")

