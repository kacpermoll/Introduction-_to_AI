import itertools
import random
from re import S


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
        if len(self.cells) == self.count != 0:
            return self.cells
        return None

    def known_safes(self):
        """ 
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):

        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        

    def mark_safe(self, cell):

        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
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
        #1
        self.moves_made.add(cell)

        #2
        self.mark_safe(cell)

        #3
        neighbours = self.neighbours(cell)
        unknown_neighbours, count_of_unknown_neighbours = self.clean_from_known_cells(neighbours, count)
        new_sentence = Sentence(unknown_neighbours, count_of_unknown_neighbours)
        self.knowledge.append(new_sentence)
        
        #4 & 5
        subset_checker = False
        for i in self.knowledge:
            if i.cells == new_sentence.cells:
                continue
            elif i.cells.issubset(new_sentence.cells):
                infer_cells = new_sentence.cells - i.cells
                infer_count = new_sentence.count - i.count
                subset_checker = True

            elif new_sentence.cells.issubset(i.cells):
                infer_cells = i.cells - new_sentence.cells
                infer_count = i.count - new_sentence.count  
                subset_checker = True

            if subset_checker:
                #Marking safes
                if infer_count == 0:
                    for cell in infer_cells:
                        self.mark_safe(cell)
                    self.knowledge.append(Sentence(infer_cells, infer_count))               
                #Marking mines
                if infer_count == len(infer_cells):
                    for cell in infer_cells:
                        self.mark_mine(cell)

                    self.knowledge.append(Sentence(infer_cells, infer_count))

            subset_checker = False
        
        #removing duplicates and sentences which are sure
        self.remove_duplicates()
        self.remove_sures()
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        #
        possible_moves = set()
        
        for row in range(self.height):
            for col in range(row):
                if (row,col) not in self.moves_made and (row, col) not in self.mines:
                    possible_moves.add((row,col))

        #no possible moves left
        if not len(possible_moves):
            return None
        
        #randomly chosen move
        move = random.choice(tuple(possible_moves))
        return move        

    
    def neighbours(self, cell):
        neighbours = []
        x_cell, y_cell = cell

        for i in range(x_cell - 1, x_cell + 2):
            for j in range(y_cell - 1, y_cell + 2):
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) != cell:
                    neighbours.append((i,j))

        return neighbours


    def clean_from_known_cells(self, neighbours, count):
        
        for cell in neighbours:
            if cell in self.mines:
                neighbours.remove(cell)
                count -= 1

            if cell in self.safes:
                neighbours.remove(cell)

        return set(neighbours), count

    #removes duplicate sentences
    def remove_duplicates(self):
        unique_knowledge = []

        for sentence in self.knowledge:
            if sentence not in unique_knowledge:
                unique_knowledge.append(sentence)
        self.knowledge = unique_knowledge
                

    #removes sentences that contain all cells that are mines or safe
    # while adding those cells to self.mark_mine or self.mark_safe
    def remove_sures(self):
        final_knowledge = []
        for sentence in self.knowledge:
            final_knowledge.append(sentence)
            #if all cells in this sentence are mines:
            if sentence.known_mines():
                for mine_cell in sentence.known_mines().copy():
                    self.mark_mine(mine_cell)
                final_knowledge.pop(-1)
            #if all cells in this sentence are safes:
            elif sentence.known_safes():
                for safe_cell in sentence.known_safes().copy():
                    self.mark_safe(safe_cell)
                final_knowledge.pop(-1)
        
        self.knowledge = final_knowledge