#!/usr/bin/python

import sys
import re
import string
from copy import deepcopy 
from colorama import Fore, Style, Back
from prettytable import PrettyTable
from simplex import Simplex

def open_file():
    try:
        return open("lab5_variant_5.txt")
    except FileNotFoundError:
        print("Oops! File not exist...")
        exit()


def get_matrix_table(matrix):
    if len(matrix) < 1: return ''

    x = PrettyTable()
    fields = ['']
    for i in range(len(matrix[0])):
        fields.append("B" + str(i + 1))

    x.field_names = fields
    for i in range(len(matrix)):
        x.add_row(['A' + str(i + 1)] + matrix[i])
    return x


def check_saddle_point(minA, maxB):
    maxFromMatrixA = minA[max(minA, key = minA.get)]
    minFromMatrixB = maxB[min(maxB, key = maxB.get)]
    return [maxFromMatrixA, minFromMatrixB]


def check_rows(firstRow, secondRow):
    equalElements = 0
    for i in range(len(firstRow)):
        if firstRow[i] < secondRow[i]: return 0
        if firstRow[i] == secondRow[i]: equalElements += equalElements

    return 0 if equalElements == len(firstRow) else 1


def check_dominant_rows(matrix):
    matrixAfterExcludingRows = []
    deletedRows = []

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j: continue
            result = check_rows(matrix[i], matrix[j])
            if result != 0 and j not in deletedRows:
                deletedRows.append(j)
                print("Стретегія А" + str(i + 1), "домінуюча над стратегією А" + str(j + 1), "тому забираємо рядок", j + 1)

    for i in range(len(matrix)):
        if i in deletedRows: continue
        matrixAfterExcludingRows.append(matrix[i])

    return matrixAfterExcludingRows


def check_dominant_columns(matrix):
    matrixAfterExcludingColumns = []
    deletedColumns = []
    transposedMatrix = [list(x) for x in zip(*matrix)]

    for i in range(len(transposedMatrix)):
        for j in range(len(transposedMatrix)):
            if i == j: continue
            result = check_rows(transposedMatrix[j], transposedMatrix[i])
            if result != 0 and j not in deletedColumns:
                deletedColumns.append(j)
                print("Стретегія В" + str(i + 1), "домінуюча над стратегією В" + str(j + 1), "тому забираємо стовпчик", j + 1)
    
    for i in range(len(matrix)):
        matrixAfterExcludingColumns.append([])
        for j in range(len(matrix[i])):
            if j in deletedColumns: continue
            matrixAfterExcludingColumns[i].append(matrix[i][j])

    return matrixAfterExcludingColumns


file = open_file()

matrix = []
for line in file:
    matrix.append([int(d) for d in re.split(';', re.sub('\n', '', line))])

if len(matrix) < 2: exit()
print(Fore.WHITE + "Вхідні дані", Style.RESET_ALL)
print(get_matrix_table(matrix))

print(Fore.WHITE + "Перевірка матриці на наявність сідлової точки", Style.RESET_ALL)
x = PrettyTable()
fields = ['']
for i in range(len(matrix)):
    fields.append("B" + str(i + 1))

fields.append('a = min(Ai)')
x.field_names = fields

minA = {}
maxB = {}

for i in range(len(matrix)):
    minA[i] = min(matrix[i])
    x.add_row(['A' + str(i + 1)] + matrix[i] + [Fore.WHITE + str(minA[i]) + Style.RESET_ALL])
    for j in range(len(matrix[i])):
        if j not in maxB or maxB[j] < matrix[i][j]:
            maxB[j] = matrix[i][j]

x.add_row(['b = max(Bi)' + Fore.WHITE] + [maxB[element] for element in maxB] + ['' + Style.RESET_ALL])
print(x)

[maxFromMatrixA, minFromMatrixB] = check_saddle_point(minA, maxB)
if maxFromMatrixA == minFromMatrixB:
    print("Сідлова точка присутня!")
else:
    print("a = max(min(Ai)) =", maxFromMatrixA)
    print("b = min(max(Bi)) =", minFromMatrixB)
    print("Сідлова точка відсутня, так як a != b")
    print("Ціна гри знаходиться в межах:", Fore.RED, maxFromMatrixA, "<= y <=", minFromMatrixB, Style.RESET_ALL) 


print(Fore.WHITE, "\nПеревірка матриці на домінуючі рядки і домінуючі стовпці:", Style.RESET_ALL)
print(Fore.WHITE + "З позиції виграшу гравця А", Style.RESET_ALL)
matrixAfterExcludingRows = check_dominant_rows(matrix)
print(Fore.RED + "Після перевірки домінуючих рядків наша матриця набула наступного вигляду: ", Style.RESET_ALL)
print(get_matrix_table(matrixAfterExcludingRows))


print(Fore.WHITE + "З позиції програшу гравця В", Style.RESET_ALL)
matrixAfterExcludingColumns = check_dominant_columns(matrixAfterExcludingRows)
print(Fore.RED + "Після перевірки домінуючих стовпчиків наша матриця набула наступного вигляду: ", Style.RESET_ALL)
print(get_matrix_table(matrixAfterExcludingColumns))

transposedMatrix = [list(x) for x in zip(*matrixAfterExcludingColumns)]
print(Fore.WHITE + "\nЗнаходимо рішення гри в змішаних стратегіях", Style.RESET_ALL)
print(Fore.RED + "Знайти мінімум функції F(x) при обмеженнях (для гравця ||)", Style.RESET_ALL)

secondPlayersConditions = []
for i in range(len(transposedMatrix)):
    secondPlayersConditions.append('')
    for j in range(len(transposedMatrix[i])):
        secondPlayersConditions[i] += str(transposedMatrix[i][j]) + 'x_' + str(j + 1) + ' + '

for i in range(len(secondPlayersConditions)):
    print(secondPlayersConditions[i][:-2] + '>= 1')

mainCondition = 'F(x) = '
for i in range(len(matrixAfterExcludingColumns)):
    mainCondition += 'x_' + str(i + 1) + ' + '

print(mainCondition[:-2] + '--> min')

print(Fore.RED + "Знайти мінімум функції Z(y) при обмеженнях (для гравця |)", Style.RESET_ALL)
firstPlayersConditions = []

vars_count = 0
for i in range(len(matrixAfterExcludingColumns)):
    firstPlayersConditions.append('')
    columns = len(matrixAfterExcludingColumns[i])
    for j in range(columns):
        firstPlayersConditions[i] += str(matrixAfterExcludingColumns[i][j]) + 'y_' + str(j + 1) + ' + '
        if columns > vars_count:
            vars_count = columns

conditions = ''
for i in range(len(firstPlayersConditions)):
    firstPlayersConditions[i] = firstPlayersConditions[i][:-2] + '<= 1'

mainCondition = ''
for i in range(len(transposedMatrix)):
    mainCondition += '1y_' + str(i + 1) + ' + '

mainCondition = mainCondition[:-2]

for line in firstPlayersConditions:print(line)
print('Z(y) = ' + mainCondition + '--> max')

print(Fore.WHITE + "\nВирішимо пряму задачу лінійного програмування симплексним методом", Style.RESET_ALL)
print(Fore.WHITE + "Визначимо максимальне значення цільової функції", Fore.RED, mainCondition + '--> max', Fore.WHITE + "при настуних умовах-обмеженнях:", Style.RESET_ALL)
print(conditions)
print(Fore.WHITE + "Після переведення в канонічну форму переходимо до основно алгоритму симплекс-методом", Style.RESET_ALL)

simplexResult = Simplex(num_vars=vars_count, constraints=firstPlayersConditions, objective_function=mainCondition)
print(Fore.WHITE + "\nОтримуємо наступні результати:", Style.RESET_ALL)

x_result = {}
y_result = {}
for key in simplexResult.solution:
    if 'y_' in key:
        y_result[key] = simplexResult.solution[key]
    elif 'x_' in key:
        x_result[key] = simplexResult.solution[key]

yResultCond = 'F(y) = '
yResult = 0
for i in range(vars_count):
    print('y' + str(i + 1) + ' =', y_result['y_' + str(i + 1)], end=' ')
    yResult += 1 * y_result['y_' + str(i + 1)]
    yResultCond += "1 * " + str(y_result['y_' + str(i + 1)]) + ' + '


print("\n" + Fore.RED + yResultCond[:-2] + '= ' + str(yResult), Style.RESET_ALL, '\n')

xResultCond = 'F(x) = '
xResult = 0
for i in range(vars_count):
    print('x' + str(i + 1) + ' =', x_result['x_' + str(i + 1)], end=' ')
    xResult += 1 * x_result['x_' + str(i + 1)]
    xResultCond += "1 * " + str(x_result['x_' + str(i + 1)]) + ' + '


print("\n" + Fore.RED + xResultCond[:-2] + '= ' + str(xResult), Style.RESET_ALL)

print("\nЦіна гри буде рівна g = 1/F(x)")
print(Fore.WHITE + "g = 1/(" + str(xResult), ") =", str(1/xResult), Style.RESET_ALL)
