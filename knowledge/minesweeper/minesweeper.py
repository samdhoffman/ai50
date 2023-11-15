import itertools
import random
from collections import deque


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count > 0 and len(self.cells) == self.count:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells and self.count > 0:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)
        
        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        self.create_knowledge(cell, count)

        # 4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        self.search_for_safes_and_mines()

        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge

    def create_knowledge(self, cell, count):
        """
        for each cell left, right, up, down, and diagnonal
        check if it is not in the known safes or known mines.
        if it is not, add it to the sentence cells set
        """
        cells = []

        cell_row = cell[0]
        cell_col = cell[1]

        # N, S, E, W, NE, NW, SE, SW
        neighbors = [
            (cell_row - 1, cell_col),
            (cell_row + 1, cell_col),
            (cell_row, cell_col + 1),
            (cell_row, cell_col - 1),
            (cell_row - 1, cell_col + 1),
            (cell_row - 1, cell_col - 1),
            (cell_row + 1, cell_col + 1),
            (cell_row + 1, cell_col - 1),
        ]

        for r in range(self.height):
            for c in range(self.width):
                cur_cell = (r, c)

                if cur_cell not in self.safes and cur_cell not in self.mines and cur_cell in neighbors:
                    cells.append(cur_cell)

        sentence = Sentence(cells, count)
        self.knowledge.append(sentence)
        next_move = self.make_safe_move()

        if next_move:
            return next_move
        else:
            return self.make_random_move()

    def search_for_safes_and_mines(self):
        for k in self.knowledge:
            self.mines.update(k.known_mines())
            self.safes.update(k.known_safes())

    def generate_knowledge(self):
        q = deque([(i, self.knowledge[i]) for i in range(len(self.knowledge))])

        while q:
            cur = q.popleft()
            cur_knowledge, idx = cur[1], cur[0]

            for i in range(len(self.knowledge)):
                if i == idx:
                    continue

                other_knowledge = self.knowledge[i]
                if len(cur_knowledge) >= len(other_knowledge):
                    self.create_subset_knowledge(cur_knowledge, other_knowledge, q)
                else:
                    self.create_subset_knowledge(other_knowledge, cur_knowledge, q)

    def create_subset_knowledge(self, a, b, q):
        if a.cells.issubset(b.cells):
            new_cells = b.cells - a.cells
            new_count = b.count - a.count
            new_sentence = Sentence(cells=new_cells, count=new_count)
            self.knowledge.append(new_sentence)
            q.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        return next((move for move in self.safes if move not in self.moves_made), None)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_move = None

        for r in range(self.height):
            for c in range(self.width):
                cur_cell = (r, c)
                if cur_cell not in self.moves_made and cur_cell not in self.mines:
                    random_move = cur_cell
                    break

        return random_move
