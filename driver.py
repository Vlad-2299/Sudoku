import queue as q
import numpy as np
from copy import deepcopy

class csp():

    def __init__(self, sudoku):
        self.variables = self.setVariables(sudoku)
        self.values = self.setDomain(sudoku)
        self.domain = self.setDomain(sudoku)
        self.unitSet = self.setUnitSet(sudoku)
        self.units = dict((v, [u for u in self.unitSet if v in u]) for v in self.variables)
        self.peers = dict((v, set(sum(self.units[v],[])) - set([v])) for v in self.variables)
        self.constraints = {(v, p) for v in self.variables for p in self.peers[v]}

    def setVariables(self, sudoku):
        var = list()
        for key in sudoku:
            var.append(key)
        return var

    def setDomain(self, sudoku):
        dom = sudoku.copy()
        for key in dom:
            if dom[key] == 0:
                dom[key] = list(np.arange(1, 10, 1))
            else:
                se = list()
                se.append(dom[key])
                dom[key] = se
        return dom


    def setUnitSet(self, sudoku):
        i = 1
        const = list()

        while i < 10:
            row = list(rowVal for rowVal in sudoku if not rowVal.find(chr(64 + i)))
            const.append(row)
            i += 1

        j = 1
        while j < 10:
            col = list(rowVal for rowVal in sudoku if rowVal.find(str(j)) == 1)
            const.append(col)
            j += 1

        const.append(['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'])
        const.append(['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'])
        const.append(['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'])
        const.append(['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'])
        const.append(['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'])
        const.append(['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'])
        const.append(['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'])
        const.append(['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'])
        const.append(['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9'])

        return const


def AC3(csp):
    queue = q.Queue()

    for arc in csp.constraints:
        queue.put(arc)

    while not queue.empty():
        (Xi, Xj) = queue.get()
        if revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 0:
                return False

            for Xk in (csp.peers[Xi] - set(Xj)):
                queue.put((Xk, Xi))
    return True


def revise(csp, Xi, Xj):
    revised = False
    domainXi = csp.domain[Xi]
    for x in domainXi:
        if not isConsistent(csp, x, Xi, Xj):
            csp.domain[Xi].remove(x)
            revised = True
    return revised

def isConsistent(csp, x, Xi, Xj):
    domainXj = csp.domain[Xj]
    for y in domainXj:
        if Xj in csp.peers[Xi] and y != x:
            return True
    return False
        

def backtrackingSearch(csp):
    return backtrack({}, csp)

def backtrack(assignment, csp):
    if isComplete(assignment, csp):
        return assignment
    var = selectUnassignedVariable(csp, assignment)
    domain = deepcopy(csp.values)

    for value in csp.values[var]:
        if isConsistentBT(var, value, assignment, csp):
            assignment[var] = value
            inferences = {}
            inferences = forwardChecking(assignment, inferences, csp, var, value)
            if inferences != 'failure':
                result = backtrack(assignment, csp)
                if result != 'failure':
                    return result

            del assignment[var]
            csp.values.update(domain)

    return 'failure'



def forwardChecking(assignment, inferences, csp, var, value):
    inferences[var] = value

    for neighbor in csp.peers[var]:
        if neighbor not in assignment and value in csp.values[neighbor]:
            if len(csp.values[neighbor]) == 1:
                return 'failure'

            csp.values[neighbor].remove(value)
            remaining = csp.values[neighbor]

            if len(remaining) == 1:
                flag = forwardChecking(assignment, inferences, csp, neighbor, remaining)
                if flag == 'failure':
                    return 'failure'


def isConsistentBT(var, value, assignment, csp):
    for neighbor in csp.peers[var]:
        if neighbor in assignment.keys() and assignment[neighbor] == value:
            return False
    return True


def selectUnassignedVariable(csp, assignment):
    unassigned_variables = dict((s, len(csp.values[s])) for s in csp.values if s not in assignment.keys())
    mrv = min(unassigned_variables, key=unassigned_variables.get)
    return mrv


def isComplete(assignment, csp):
    return set(assignment.keys()) == set(csp.variables)

def solved(csp):
    for var in csp.variables:
        if len(csp.domain[var]) > 1:
            return False
    return True

def getSolvedBoard(csp):
    sti = str()
    for val in csp.domain:
        sti += str(''.join(map(str, csp.domain[val])))
    return sti

def getSolvedBoardBTS(csp, assignment):
    sti = str()
    for var in csp.variables:
        sti += str(assignment[var])
    return sti


def main():
    # sudokuInput = input().lower()
    # sudokuInput = sys.argv[1].lower()

    sudokuInput = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    sudokuQueue = q.Queue()


    for s in sudokuInput:
        sudokuQueue.put(int(s))

    sudoku = dict([(chr(64 + i) + str(j), sudokuQueue.get()) for i in np.arange(1, 10, 1) for j in np.arange(1, 10, 1)])


    outputFile = open('output.txt', 'w')

    cspSudoku = csp(sudoku)
    AC3(cspSudoku)
    if solved(cspSudoku):
        outputFile.write(getSolvedBoard(cspSudoku) + ' AC3\n')
        # print(getSolvedBoard(cspSudoku) + ' AC3\n')
    else:
        cspSudoku = csp(sudoku)
        backtrackingSearch(cspSudoku)
        cspSudoku = csp(sudoku)
        assignment = backtrackingSearch(cspSudoku)
        outputFile.write(getSolvedBoardBTS(cspSudoku, assignment) + ' BTS\n')
        # print(getSolvedBoardBTS(cspSudoku, assignment) + ' BTS\n')
        # print(assignment['B1'])



if __name__ == '__main__':
    main()