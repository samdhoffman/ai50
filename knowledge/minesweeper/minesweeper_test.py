import pytest
import minesweeper as m

def test_known_mines():
    known_mines = [(0, 1), (1, 1), (2, 1)]
    known_mine_count = 3
    sentence = m.Sentence(cells=known_mines, count=known_mine_count)
    assert(sentence.known_mines()) == set(known_mines)

    mines = [(0, 1), (1, 1), (2, 1)]
    mine_count = 1
    sentence = m.Sentence(cells=mines, count=mine_count)
    assert(sentence.known_mines()) == set()


def test_known_safes():
    known_safes = [(0, 1), (1, 1), (2, 1)]
    known_mine_count = 0
    sentence = m.Sentence(cells=known_safes, count=known_mine_count)
    assert(sentence.known_safes()) == set(known_safes)

    mines = [(0, 1), (1, 1), (2, 1)]
    mine_count = 1
    sentence = m.Sentence(cells=mines, count=mine_count)
    assert(sentence.known_mines()) == set()


def test_mark_mine():
    known_mines = [(0, 1), (1, 1), (2, 1)]
    known_mine_count = 3
    sentence = m.Sentence(cells=known_mines, count=known_mine_count)
    sentence.mark_mine((0, 1))
    assert(sentence.cells) == set([(1, 1), (2, 1)])
    assert(sentence.count) == 2


def test_mark_safe():
    known_mines = [(0, 1), (1, 1), (2, 1)]
    known_mine_count = 2
    sentence = m.Sentence(cells=known_mines, count=known_mine_count)
    sentence.mark_safe((0, 1))
    assert(sentence.cells) == set([(1, 1), (2, 1)])
    assert(sentence.count) == 2

def test_add_knowledge():
    ai = m.MinesweeperAI(width=4, height=4)

    ai.mark_safe((1, 0))
    ai.add_knowledge((1, 2), 1)

    new_knowledge = m.Sentence(
        cells=[
            (0, 1), (0, 2), (0, 3),
            (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3),
        ],
        count=1
    )

    assert(all(cell in new_knowledge.cells for cell in ai.knowledge[0].cells))
    assert(ai.knowledge[0].count) == new_knowledge.count

def test_search_for_safes_and_mines():
    ai = m.MinesweeperAI(width=3, height=3)

    sentence_1 = m.Sentence(
        cells=[
            (0, 1), (0, 2),
        ],
        count=1
    )

    sentence_2 = m.Sentence(
        cells=[
            (0, 2), (0, 3)
        ],
        count=0
    )
    ai.knowledge.append(sentence_1)
    ai.knowledge.append(sentence_2)

    assert(ai.mines) == set()
    assert(ai.safes) == set()

    ai.add_knowledge((0, 2), 1)
    assert(ai.knowledge[0]) == m.Sentence(cells=[(0, 1)], count=1)
    assert(ai.safes) == {(0, 2), (0, 3)}
    assert(ai.mines) == {(0, 1)}

def test_make_safe_move():
    ai = m.MinesweeperAI(width=3, height=3)
    ai.moves_made.add((0, 0))
    ai.moves_made.add((0, 1))
    ai.safes.add((0, 1))
    ai.safes.add((0, 0))
    ai.safes.add((0, 2))
    assert(ai.make_safe_move()) == (0, 2)

    ai.moves_made.add((0, 2))
    assert(ai.make_safe_move()) == None

def test_make_random_move():
    ai = m.MinesweeperAI(width=3, height=3)
    ai.moves_made.add((0, 0))
    ai.moves_made.add((0, 1))
    ai.mines.add((0, 1))
    ai.mines.add((0, 0))
    mines_and_moves_made = ai.mines.union(ai.moves_made)

    assert(ai.make_random_move()) not in mines_and_moves_made



