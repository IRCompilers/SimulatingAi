from queue import PriorityQueue
import numpy as np
from copy import deepcopy

class MaskMatrix:
    def __init__(self, matrix, cost):
        self.matrix = matrix
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.cost == other.cost

    def __gt__(self, other):
        return self.cost > other.cost

def calculate_cost(mask_matrix, g_costs_matrix, h_costs_matrix):
    res = 0
    for i in range(len(mask_matrix)):
        for j in range(len(mask_matrix[0])):
            res += mask_matrix[i][j] * g_costs_matrix[i][j]
            res += mask_matrix[i][j] * h_costs_matrix[i][j]
    return res

def expand(mask_matrix, ind_reg):
    #expands by one column
    ans = []

    #find column with no 1s
    # keep count of rows that have a 1
    cols = []
    rows = []
    for i in range(len(mask_matrix)):
        if mask_matrix[i].count(1) == 0:
            rows.append(i)

    for j in range(len(mask_matrix[0])):
        if [mask_matrix[i][j] for i in range(len(mask_matrix))].count(1) == 0:
            cols.append(j)


    if len(rows) == 0:
        return []

    if len(cols) == 0:
        return []


    #get possible rows. the first that is below the ind_reg and the first above
    rows2 = []
    for i in rows:
        if i < ind_reg:
            rows2.append(i)
            break
    for i in rows:
        if i >= ind_reg:
            rows2.append(i)
            break


    perms = permute_column(mask_matrix, cols[0], rows2)
    ans += perms

    return ans

def permute_column(mask_matrix, column, rows):
    col = [mask_matrix[i][column] for i in range(len(mask_matrix))]

    perms = all_permutations(col, rows)
    res = []
    for perm in perms:

        new = deepcopy(mask_matrix)
        for i in range(len(perm)):
            new[i][column] = perm[i]

        res.append(new)
    return res

def all_permutations(array, rows):

    empty = [0 for i in range(len(array))]
    res = []
    for i in range(len(rows)):
        new = empty.copy()
        new[rows[i]] = 1
        res.append(new)
    return res

def valid_final(matrix):
    #count if the amount of 1s equals the min between patients and beds
    return sum([matrix[i].count(1) for i in range(len(matrix))]) == min(len(matrix), len(matrix[0]))


def astar(g_costs_matrix, h_costs_matrix,ind_reg):
    #initialize
    start = [[0 for i in range(len(g_costs_matrix[0]))] for j in range(len(g_costs_matrix))]
    start_cost = calculate_cost(start, g_costs_matrix, h_costs_matrix)
    start_node = MaskMatrix(start, start_cost)
    pq = PriorityQueue()
    pq.put(start_node)

    while not pq.empty():
        current = pq.get()

        if valid_final(current.matrix):
            return current.matrix
        for child in expand(current.matrix, ind_reg):
            cost = calculate_cost(child, g_costs_matrix, h_costs_matrix)
            node = MaskMatrix(child, cost)
            pq.put(node)

    return -1



def test():

    mat = [[0, 1,0], [0,0,0]]
    g_costs = [[1,2,3], [4,5,6]]
    h_costs = [[1,2,3], [4,5,6]]
    assert calculate_cost(mat, g_costs, h_costs) == 4
    ans = astar(g_costs, h_costs)
    print(ans)



    mat1 = [[1,0],[0,1],[0,0]]
    costs1 = [[1,2], [3,4], [5,6]]
    costs2 = [[1,2], [3,4], [5,6]]
    assert calculate_cost(mat1, costs1, costs2) == 10
    ans = astar(costs1, costs2)
    print(ans)

    mat2 = [[0,0,1], [0,1,0], [1,0,0]]
    costs1 = [[9,8,8], [4,5,6], [1,2,3]]
    costs2 = [[9,8,8], [4,5,6], [1,2,3]]
    ans = astar(costs1, costs2)
    print(ans)

    #test a 5x5
    costs1 = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,25]]
    costs2 = [[1,2,3,4,5], [6,7,8,9,10], [11,12,13,14,15], [16,17,18,19,20], [21,22,23,24,25]]
    ans = astar(costs1, costs2)
    print(ans)

    # test 10x10
    costs1 = [[1,2,3,4,5,6,7,8,9,10], [11,12,13,14,15,16,17,18,19,20], [21,22,23,24,25,26,27,28,29,30], [31,32,33,34,35,36,37,38,39,40], [41,42,43,44,45,46,47,48,49,50], [51,52,53,54,55,56,57,58,59,60], [61,62,63,64,65,66,67,68,69,70], [71,72,73,74,75,76,77,78,79,80], [81,82,83,84,85,86,87,88,89,90], [91,92,93,94,95,96,97,98,99,100]]
    costs2 = [[1,2,3,4,5,6,7,8,9,10], [11,12,13,14,15,16,17,18,19,20], [21,22,23,24,25,26,27,28,29,30], [31,32,33,34,35,36,37,38,39,40], [41,42,43,44,45,46,47,48,49,50], [51,52,53,54,55,56,57,58,59,60], [61,62,63,64,65,66,67,68,69,70], [71,72,73,74,75,76,77,78,79,80], [81,82,83,84,85,86,87,88,89,90], [91,92,93,94,95,96,97,98,99,100]]
    ans = astar(costs1, costs2)
    print(ans)


    assert not valid_final(mat)
    assert valid_final(mat1)
    assert valid_final(mat2)
    assert not valid_final([[1,0],[0,1],[1,0]])


def get_assignment(g_costs, h_costs, ind_reg):
    assignment = astar(g_costs, h_costs, ind_reg)
    row, col = [], []

    for i in range(len(assignment)):
        for j in range(len(assignment[0])):
            if assignment[i][j] == 1:
                row.append(i)
                col.append(j)

    return row, col

