import itertools
import random


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
        if (self.cells == self.count) and (self.count!= 0):
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
        if cell in self.cells:
            self.cells.remove(cell)
        count -= 1

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
        self.moves_made.add(cell)
        self.mark_safe(cell)
        new_sentance = set()
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1,cell[1]+2):
                #print(i,j)
                if (i,j) == cell:
                    continue
                if (i,j) in self.safes:
                    continue
                if (i, j) in self.mines:
                    count -= 1
                    continue
                if (0<=i<self.height) and (0<=j<self.width):
                    new_sentance.add((i,j))
        self.knowledge.append(Sentence(new_sentance,count))

        safes = set()
        mines = set()
        for curr in self.knowledge:
            safes = safes.union(curr.known_safes())
            mines = mines.union(curr.known_mines())
        if safes:
            for i in safes:
                self.mark_safe(i)
        if mines:
            for i in mines:
                self.mark_mine(i)
        empty = Sentence(set(), 0)
        for i in self.knowledge:
            if (i == empty):
                self.knowledge.remove(i)
        adders = []
        for sent1 in self.knowledge:
            for sent2 in self.knowledge:
                if (sent1.cells == set()) and (sent1.count != 0):
                    return "Error!!"
                    #print(str(sent1.cells) + "Sent 1 Cells ")
                    #print(str(sent2.cells) + " SEnt 2 Cells ")
                    #print(str(sent1) + " Sent1 ")
                    #print(str(sent2) + " Sent 2")
                    #print(sent1.cells.issubset(sent2.cells))
                    #print(len(self.knowledge))
                if sent1.cells == sent2.cells:
                    continue
                if sent1.cells.issubset(sent2.cells):
                    newcells = sent2.cells - sent1.cells
                        #print("Ran")
                    newcount = sent2.count - sent1.count
                        #print(str(newcount) + " New Count ")
                    new_sentence = Sentence(newcells, newcount)
                    if new_sentence not in self.knowledge:
                            #print(str(new_sentence) + " New Sent ")
                        adders.append(new_sentence)
                        
                    #print(self.knowledge)
        for i in adders:
                #print(i.cells, i.count)
                #print(len(self.knowledge))
            self.knowledge.append(i)
    #Tried to recheck every time new information was added, but found it to be unnecsary (and it didnt work)
    '''
        recheck = True
        while recheck == True:
            recheck = False
            
            safes = set()
            mines = set()
            for curr in self.knowledge:
                print(curr)
                print(len(self.knowledge))
                safes = safes.union(curr.known_safes())
                mines = mines.union(curr.known_mines())
            if safes:
                for i in safes:
                    self.mark_safe(i)
                    recheck = True
            if mines:
                for i in mines:
                    self.mark_mine(i)
                    recheck = True
        #More generally, any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset of set2, then we can construct the new sentence set2 - set1 = count2 - count1. Consider the example above to ensure you understand why that’s true.
            empty = Sentence(set(), 0)
            for i in self.knowledge:
                if (i == empty):
                    self.knowledge.remove(i)
            adders = []
            for sent1 in self.knowledge:
                for sent2 in self.knowledge:
                    if (sent1.cells == set()) and (sent1.count != 0):
                        raise ValueError
                    #print(str(sent1.cells) + "Sent 1 Cells ")
                    #print(str(sent2.cells) + " SEnt 2 Cells ")
                    #print(str(sent1) + " Sent1 ")
                    #print(str(sent2) + " Sent 2")
                    #print(sent1.cells.issubset(sent2.cells))
                    #print(len(self.knowledge))
                    if sent1.cells == sent2.cells:
                        continue
                    if sent1.cells.issubset(sent2.cells):
                        newcells = sent2.cells - sent1.cells
                        #print("Ran")
                        newcount = sent2.count - sent1.count
                        #print(str(newcount) + " New Count ")
                        new_sentence = Sentence(newcells, newcount)
                        if new_sentence not in self.knowledge:
                            #print(str(new_sentence) + " New Sent ")
                            adders.append(new_sentence)
                            recheck = True
                    #print(self.knowledge)
            for i in adders:
                #print(i.cells, i.count)
                #print(len(self.knowledge))
                self.knowledge.append(i)
    '''
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        move = None
        safes = self.safes

        possible_moves = safes - self.moves_made

        if possible_moves:
            #print(list(possible_moves)[0])
            return random.choice(list(possible_moves))
        return None
        

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                possible_moves.add((i,j))
        possible_moves = possible_moves - self.mines
        possible_moves = possible_moves - self.moves_made
        #print(list(possible_moves))
        return random.choice(list(possible_moves))
            
        raise NotImplementedError
