#!/usr/bin/python

import sys
import re
import string

def open_file():
    try:
        return [open("lab2_variant_5.txt"), 5]
    except FileNotFoundError:
        print("Oops! File not exist...")
        exit()


[file, years] = open_file()
lines = []
benefits = []

for line in file:
    if (not (line and not line.isspace()) or len(lines) >= 3): continue

    lines.append(re.split(';', re.sub('\n', '', line)))

if len(lines) != 3: 
    print("Must be 3 lines!")
    exit()

if len(lines[0]) != 5 or len(lines[1]) != 5 or len(lines[2]) != 4:
    print("Wrong data...")
    exit()

A = { 'M1': float(lines[0][0]), 'D1': float(lines[0][1]), 'P1': float(lines[0][2]), 'D2': float(lines[0][3]), 'P2': float(lines[0][4]) }
B = { 'M2': float(lines[1][0]), 'D1': float(lines[1][1]), 'P1': float(lines[1][2]), 'D2': float(lines[1][3]), 'P2': float(lines[1][4]) }
C = { 'P3': float(lines[2][0]), 'P4': float(lines[2][1]), 'P1': float(lines[2][2]), 'P2': float(lines[2][3]) }

print("A:", A)
print("B:", B)
print("C:", C)

print("\nCalculation of the expected value of node A:")
EVM_A = A['P1'] * A['D1'] * years + A['P2'] * A['D2'] * years - A['M1'];
print("EVM(A) =", A['P1'], '*', A['D1'], '*', years, '+', A['P2'], '*', A['D2'], '*', years, '-', A['M1'], '=', EVM_A)

print("\nCalculation of the expected value of node B:")
EVM_B = B['P1'] * B['D1'] * years + B['P2'] * B['D2'] * years - B['M2'];
print("EVM(B) =", B['P1'], '*', B['D1'], '*', years, '+', B['P2'], '*', B['D2'], '*', years, '-', B['M2'], '=', EVM_B)

print("\nCalculation of the expected value of node C:")
EVM_A1 = C['P1'] * A['D1'] * (years - 1) + C['P2'] * A['D2'] * (years - 1) - A['M1']
EVM_B1 = C['P1'] * B['D1'] * (years - 1) + C['P2'] * B['D2'] * (years - 1) - B['M2']
print("EVM(A1) =", C['P1'], '*', A['D1'], '*', years - 1, '+', C['P2'], '*', A['D2'], '*', years - 1, '-', A['M1'], '=', EVM_A1)
print("EVM(B1) =", C['P1'], '*', B['D1'], '*', years - 1, '+', C['P2'], '*', B['D2'], '*', years - 1, '-', B['M2'], '=', EVM_B1)

EVM_MAX = max([EVM_A1, EVM_B1])
print("Best value is", EVM_MAX)

EVM_C = (EVM_A1 + EVM_B1) * C['P3']
print("So, EVM(C) =","(",EVM_A1, '+', EVM_B1,")", '*', C['P3'], '=', EVM_C)

letters = ['A', 'B', 'C']
bestSolution = max([EVM_A, EVM_B, EVM_C])

print("\nThe best solution of { A:", EVM_A, ',', "B:", EVM_B, ',', "C:", EVM_C, "} is", letters[[EVM_A, EVM_B, EVM_C].index(bestSolution)], '{', bestSolution, '}')

