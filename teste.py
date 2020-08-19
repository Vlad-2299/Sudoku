import numpy as np
import queue as q

sudoku = '000005000020004010030080020000008400800600000090010705006000000950003060003000001'

begin_state = q.Queue()

for s in sudoku:
    begin_state.put(int(s))


a = dict([(chr(64+i) + str(j), begin_state.get()) for i in np.arange(1, 10, 1) for j in np.arange(1, 10, 1)])

# for m in a:
#     if m.find('2') == 1:
#         print(m)

i = 1
const = list()

var = list()
for key in a:
    var.append(key)


while i < 10:
    row = list(rowVal for rowVal in a if not rowVal.find(chr(64+i)))
    const.append(row)
    i += 1

j = 1
while j < 10:
    col = list(rowVal for rowVal in a if rowVal.find(str(j)) == 1)
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

units = dict((v, [u for u in const if v in u]) for v in var)
peers = dict((v, set(sum(units[v],[])) - set([v])) for v in var)
constraints = {(v, p) for v in var for p in peers[v]}

b = list(np.arange(1, 10, 1))

print(b[1])

