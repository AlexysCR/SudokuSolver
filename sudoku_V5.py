"""
Author: Alexys Martín Coate Reyes

Description: Sudoku based on own algorythm

The following rules are followed:

------ QUADRANTS ------
They are ordered as the following:
  0  |  1  |  2
----------------
  3  |  4  |  5
----------------
  6  |  7  |  8

------ ROWS & COLUMNS ------
     1 2 3     4 5 6     7 8 9
-------------------------------
1 :  0 0 0  |  0 0 0  |  0 0 0
2 :  0 0 0  |  0 0 0  |  0 0 0
3 :  0 0 0  |  0 0 0  |  0 0 0
-------------------------------
4 :  0 0 0  |  0 0 0  |  0 0 0
5 :  0 0 0  |  0 0 0  |  0 0 0
6 :  0 0 0  |  0 0 0  |  0 0 0
-------------------------------
7 :  0 0 0  |  0 0 0  |  0 0 0
8 :  0 0 0  |  0 0 0  |  0 0 0
9 :  0 0 0  |  0 0 0  |  0 0 0

Classes:
- Sudoku
- Cell
"""
import grids


class Cell:
    def __init__(self,num,coordinates):
        self.num = int(num)
        self.coordinates = (coordinates[0],coordinates[1])
        self.possibleNumbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}

class Sudoku:
    def __init__(self):
        self.grid = [[Cell(0,[x,y]) for x in range(9)] for y in range(9)]
        self.universe = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.emptySlots = 81
        self.probabilityGrid = dict()
        self.possibleNumsInRow = [{1,2,3,4,5,6,7,8,9} for rows in range(9)]
        self.possibleNumsInCol = [{1,2,3,4,5,6,7,8,9} for cols in range(9)]
        self.possibleNumsInQuad = [{1,2,3,4,5,6,7,8,9} for quad in range(9)]


    def printSudoku(self):
        print()
        for row in range(9):
            # Print Horizontal Square lines
            if row % 3 == 0 and row != 0:
                for x in range(9 * 2 + 7):
                    print("-", end="")
                print()
            # Print vertical Square lines
            for col in range(9):
                if col % 3 == 0:
                    print("|", self.grid[row][col].num, end=" ")
                else:
                    print(self.grid[row][col].num, end=" ")
            print("|")
        print()

    def printStatus(self):
        self.printSudoku()
        print("POSSIBLE NUMS (ROW):", self.possibleNumsInRow)
        print("POSSIBLE NUMS (COL):", self.possibleNumsInCol)
        print("POSSIBLE NUMS (QUAD):", self.possibleNumsInQuad)
        print("Empty Slots: ", self.emptySlots)
        print()

    def updateProbabilityGrid(self):
        probabilityGridDict = dict()
        probabilityGridList = list()
        probabilityGridList2 = list()
        for row in range(9):
            for col in range(9):
                cell = self.grid[row][col]
                probabilityGridDict.update({(row,col) : cell.possibleNumbers})
                self.probabilityGrid.update({(row, col): cell.possibleNumbers})
                probabilityGridList.append(cell.possibleNumbers)
            #probabilityGridList2.append(probabilityGridList2)
        probabilityGrid = [prob for prob in probabilityGridList if prob != set()]
        print(probabilityGrid)
        #print(probabilityGridDict)
        print(probabilityGridDict)

    def detectQuadrant(self, numRow, numCol):
        resRow = numRow // 3
        resCol = numCol // 3
        if resRow == 0:
            if resCol == 0:
                return 0
            elif resCol == 1:
                return 1
            elif resCol == 2:
                return 2
        elif resRow == 1:
            if resCol == 0:
                return 3
            elif resCol == 1:
                return 4
            elif resCol == 2:
                return 5
        elif resRow == 2:
            if resCol == 0:
                return 6
            elif resCol == 1:
                return 7
            elif resCol == 2:
                return 8
        print("WRONG MAPPING")

    def returnQuadRange(self,quadrant):
        rowRange, colRange = list(), list()
        if quadrant == 0:
            rowRange = range(0,3)
            colRange = range(0,3)
        elif quadrant == 1:
            rowRange = range(0,3)
            colRange = range(3,6)
        elif quadrant == 2:
            rowRange = range(0,3)
            colRange = range(6,9)
        elif quadrant == 3:
            rowRange = range(3,6)
            colRange = range(0,3)
        elif quadrant == 4:
            rowRange = range(3,6)
            colRange = range(3,6)
        elif quadrant == 5:
            rowRange = range(3,6)
            colRange = range(6,9)
        elif quadrant == 6:
            rowRange = range(6,9)
            colRange = range(0,3)
        elif quadrant == 7:
            rowRange = range(6,9)
            colRange = range(3,6)
        elif quadrant == 8:
            rowRange = range(6,9)
            colRange = range(6,9)
        return rowRange,colRange

    # Updates the variables when a new number inside the sudoku is written
    def writeNumInSudoku(self,num,rowAndCol,printBool):

        row, col = rowAndCol[0], rowAndCol[1]
        quadrant = self.detectQuadrant(row,col)
        targetCell = self.grid[row][col]
        # Writes given number in the grid
        targetCell.num = num
        # Sets the possibleNumbers to None
        targetCell.possibleNumbers = set()


        # Eliminate the possible number from every ROW cell
        for cell in self.grid[row]:
            cell.possibleNumbers.discard(num)
        # Eliminate the possible number from every COLUMN cell
        for sudokuRow in self.grid:
            cell = sudokuRow[col]
            cell.possibleNumbers.discard(num)
        # Eliminate the possible number from every QUADRANT cell
        rowRange, colRange = list(),list()
        if quadrant == 0:
            rowRange = range(0,3)
            colRange = range(0,3)
        elif quadrant == 1:
            rowRange = range(0,3)
            colRange = range(3,6)
        elif quadrant == 2:
            rowRange = range(0,3)
            colRange = range(6,9)
        elif quadrant == 3:
            rowRange = range(3,6)
            colRange = range(0,3)
        elif quadrant == 4:
            rowRange = range(3,6)
            colRange = range(3,6)
        elif quadrant == 5:
            rowRange = range(3,6)
            colRange = range(6,9)
        elif quadrant == 6:
            rowRange = range(6,9)
            colRange = range(0,3)
        elif quadrant == 7:
            rowRange = range(6,9)
            colRange = range(3,6)
        elif quadrant == 8:
            rowRange = range(6,9)
            colRange = range(6,9)

        for ROW in rowRange:
            for COL in colRange:
                cell = self.grid[ROW][COL]
                cell.possibleNumbers.discard(num)


        # Eliminate the possible number from the rowSet
        self.possibleNumsInRow[row].discard(num)
        # Eliminate the possible number from the columnSet
        self.possibleNumsInCol[col].discard(num)
        # Eliminate the possible number from the quadrantSet
        self.possibleNumsInQuad[quadrant].discard(num)

        # Update the emptySlots
        self.emptySlots -= 1

        #Print
        if printBool == True:
            x,y = col,row
            print("CELL ({}, {}): Num {} written".format(row,col,num))
            #self.printSudoku()


    # Given a sudoku, copies all the values into a sudoku class
    def transcrpitSudoku(self,sudoku):
        for row in range(9):
            for col in range(9):
                num = sudoku[row][col]
                if num != 0:
                    self.writeNumInSudoku(num,[row,col],False)

    # Updates the possible numbers of the actual cell
    def updateCellPosNums(self,cellCoordinates):
        row,col = cellCoordinates[0], cellCoordinates[1]
        quadrant = self.detectQuadrant(row,col)
        # Calculate the possible number in a cell
        # Intersection between PossibleNums in: Col & Row & Quad
        cellPosNums = {1,2,3,4,5,6,7,8,9}.intersection(self.possibleNumsInRow[row]).intersection(self.possibleNumsInCol[col]).intersection(self.possibleNumsInQuad[quadrant])

        # If only one number is possible, write it down. Else update cell possible numbers
        if len(cellPosNums) == 1:
            num = cellPosNums.pop()
            print("CELL ({}, {}): Num {} written \t METHOD: CALCULATE PROBABILITY".format(row, col, num))
            self.writeNumInSudoku(num,[row,col],False)
        elif len(cellPosNums) > 1:
            self.grid[row][col].possibleNumbers = cellPosNums
            #print("CELL ({}, {}): Many numbers are possible".format(row, col))
        elif cellPosNums == set():
            print("CELL ({}, {}): None numbers are possible ANOMALY!!!".format(row,col))
            exit()
        else:
            print("UNKNOWN ANOMALY!!!")
            exit()



    # Update the probablity of all the cells in the sudoku and writes a new number if there is only one possible number
    def updateSudoku(self):
        for row in range(9):
            for col in range(9):
                # If there is no number in cell, update possible numbers (If only one noumber is possible, it is written)
                num = self.grid[row][col].num
                #print("Analizing NUM: {}      Row & Col: {}, {}".format(num,row,col))
                if num == 0:
                    self.updateCellPosNums([row,col])

    def probCompare(self,cellCoordinates,columnOrRow):
        row,col = cellCoordinates[0], cellCoordinates[1]
        cell = self.grid[row][col]
        probDiff = cell.possibleNumbers
        probList = list()
        if columnOrRow == "row":
            probList = [self.grid[row][COL].possibleNumbers for COL in range(9)
                        if self.grid[row][COL].possibleNumbers != set()]
        elif columnOrRow == "col":
            probList = [self.grid[ROW][col].possibleNumbers for ROW in range(9)
                        if self.grid[ROW][col].possibleNumbers != set()]
        #print("Probability List BEFORE: ", probList)
        #print("Probability List AFTAER: ", probList)

        probList.remove(cell.possibleNumbers)
        #print("Probability List AFTAER: ", probList)
        probDiffUnion = set()
        for numSet in probList:
            probDiffUnion = probDiffUnion.union(numSet)
        probDiff = probDiff.difference(probDiffUnion)

        #print("probDiffUnion: ", probDiffUnion)
        #print("Cell Possible Numbers: ", cell.possibleNumbers)
        #print("ProbDiff: ",probDiff)
        if len(probDiff) == 1:
            #print("Probability List BEFORE: ", probList)
            #print("Probability List AFTER: ", probList)
            #print("Cell Possible Numbers: ", cell.possibleNumbers)
            #print("ProbDiff: ", probDiff)
            num = probDiff.pop()
            if columnOrRow == "col":
                #print("!!!!!!!!!!!!!COMPARE COLUMN PROBABILITY!!!!!!!!!!!!!")
                print("CELL ({}, {}): Num {} written \t METHOD: COMPARE COLUMN PROBABILITY".format(row, col, num))
            elif columnOrRow == "row":
                #print("!!!!!!!!!!!!!ROW METHOD USED!!!!!!!!!!!!!!!!")
                print("CELL ({}, {}): Num {} written \t METHOD: COMPARE ROW PROBABILITY".format(row, col, num))
            self.writeNumInSudoku(num, [row,col], False)
            return 1
        else:
            #print("CELL ({}, {}): There are more or none numbers in set = {}".format(row,col,probDiff))
            pass

    def probRowColAlgorythm(self):
        for row in range(9):
            for col in range(9):
                cell = self.grid[row][col]
                if self.grid[row][col].num == 0:
                    #print("CELL {} \t NUM: {}".format(cell.coordinates,cell.num))
                    self.probCompare([row,col],"row")
                if self.grid[row][col].num == 0:
                    #print("CELL {} \t NUM: {}".format(cell.coordinates,cell.num))
                    self.probCompare([row, col], "col")

    def checkRowsColsQuads(self):
        # Check ROWS (Falta revisar)
        for row in range(9):
            if len(self.possibleNumsInRow[row]) == 1:
                num = self.possibleNumsInRow[row].pop()
                for col in range(9):
                    cell = self.grid[row][col]
                    if cell.num == 0:
                        print("CELL ({}, {}): Num {} written \t METHOD: CHECK ROW METHOD".format(row, col, num))
                        self.writeNumInSudoku(num, [row, col], False)
        #Check columns
        for col in range(9):
            if len(self.possibleNumsInCol[col]) == 1:
                num = self.possibleNumsInCol[col].pop()
                for row in range(9):
                    cell = self.grid[row][col]
                    if cell.num == 0:
                        print("CELL ({}, {}): Num {} written \t METHOD: CHECK COLUMN METHOD".format(row, col, num))
                        self.writeNumInSudoku(num,[row,col],False)

        #Check Quadrants
        for quadrant in range(9):
            if len(self.possibleNumsInQuad[quadrant]) == 1:
                num = self.possibleNumsInQuad[quadrant].pop()

                rowRange, colRange = self.returnQuadRange(quadrant)
                for ROW in rowRange:
                    for COL in colRange:
                        cell = self.grid[ROW][COL]
                        if cell.num == 0:
                            print("CELL ({}, {}): Num {} written \t METHOD: CHECK QUADRANT METHOD".format(row, col, num))
                            self.writeNumInSudoku(num, [ROW,COL], False)


def solveSudoku(sudokuGrid):
    # Initialization of an empty sudoku
    sudoku = Sudoku()
    # Copy the values of a given sudoku into the empty grid
    sudoku.transcrpitSudoku(sudokuGrid)

    sudoku.printStatus()

    sudoku.updateProbabilityGrid()
    print("1. SUDOKU TRANSCIPTION FINISHED!!!")
    print("----------------------------------------------------------")

    """
    for x in range(5):
        sudoku.updateSudoku()
        sudoku.printStatus()

    print("COLUMN AND ROW ALGORYTHM---------------")

    #sudoku.probCompare([3, 3], "row")
    for x in range(2):
        sudoku.probRowColAlgorythm()
        sudoku.printStatus()
    for x in range(1):
        sudoku.updateSudoku()
        sudoku.printStatus()

    sudoku.checkRowsColsQuads()
    sudoku.printStatus()
    """
    counter = 0
    limit = 30
    while(sudoku.emptySlots > 0):
        prevEmptySlots = sudoku.emptySlots
        sudoku.updateSudoku()
        #sudoku.printStatus()
        sudoku.probRowColAlgorythm()
        #sudoku.printStatus()
        #sudoku.checkRowsColsQuads()
        sudoku.printStatus()
        counter += 1
        if prevEmptySlots == sudoku.emptySlots:
            sudoku.updateProbabilityGrid()
            print(sudoku.probabilityGrid.get((7,2)))
            print(sudoku.probabilityGrid.get((8,2)))
            print(sudoku.probabilityGrid.get((7,7)))
            print(sudoku.probabilityGrid.get((8,7)))
            print("SUDOKU NOT SOLVED! :( --- Empty Slots not changing --- Iterations: {}".format(counter))
            exit()
        if counter >= limit:
            print("SUDOKU NOT SOLVED! :( -------- Iterations exceded: {}".format(counter))
            exit()
    print("-------- SUDOKU  SOLVED in {} iterations! :D -------- ".format(counter))
    sudoku.updateProbabilityGrid()

    #print(sudoku.grid[3][3].num,"\t",sudoku.grid[3][3].possibleNumbers)
    #print(sudoku.grid[3][2].num, "\t", sudoku.grid[3][2].possibleNumbers)
    #print(sudoku.grid[3][5].num, "\t", sudoku.grid[3][5].possibleNumbers)

"""
    # Update the Possible nu
    cicleCounter = 0
    while(sudoku.emptySlots != 0):

        # Updating Sudoku probability
        sudoku.updateSudoku()
        sudoku.printStatus()
"""

#solveSudoku(grids.grid_medio_1)        #SOLVED
#solveSudoku(grids.grid_dificil_1)      #SOLVED
#solveSudoku(grids.grid_expert_1)       #SOLVED
#solveSudoku(grids.grid_expert_2)
#solveSudoku(grids.grid_expert_3)       #SOLVED
#solveSudoku(grids.grid_expert_4)       #
#solveSudoku(grids.grid_expert_5)       #
#solveSudoku(grids.grid_expert_6)       #
#solveSudoku(grids.grid_carlos)         #
#solveSudoku(grids.grid_master_1)        #SOLVED
solveSudoku(grids.grid_master_2)        #SOLVED
