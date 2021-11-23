#!/usr/bin/python

import sys
import re

def open_file():
    try:
        return open("lab1_variant_5.txt")
    except FileNotFoundError:
        print("Oops! File not exist...")
        exit()


def walds_maximin_model(matrix):
    minOfRows = []
    for row in matrix:
        minOfRows.append(min(row))

    maxValue = max(minOfRows)
    print("Smallest elements for each rows:", minOfRows)
    print("The largest of the smallest elements:", maxValue)
    return minOfRows.index(maxValue)


def laplace_criterion(matrix):
    sumOfRows = []
    for row in matrix:
        sumOfRows.append(sum(row)/len(row))

    maxValue = max(sumOfRows)
    print("Summing divided values for each row:", sumOfRows)
    print("The largest element is:", maxValue)
    return sumOfRows.index(maxValue)


def hurwitz_criterion(matrix, coefficient):
    minOfRows = []
    maxOfRows = []

    for row in matrix:
        minOfRows.append(min(row))
        maxOfRows.append(max(row))

    result = []
    for i in range(len(minOfRows)):
        result.append(coefficient * minOfRows[i] + (1 - coefficient) * maxOfRows[i])

    print("Coefficient:", coefficient)
    print("The smallest elements for each rows:", minOfRows)
    print("The largest elements for each rows:", maxOfRows)
    print("The calculated values:", result)
    return result.index(max(result))


def bayes_laplace_criterion(matrix, coefficients):
    result = [0 for x in range(len(matrix))] 
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            result[i] += coefficients[j] * matrix[i][j];

    print("Coefficients:", coefficients)
    print("The calculated values:", result)
    return result.index(max(result))


file = open_file()
lines = []

for line in file:
    if (not (line and not line.isspace())): continue
    
    row = re.split(',\s?', re.sub('\n', '', line))
    
    lines.append([int(element) for element in row])

print("Matrix:", lines)

print("\nWalds maximin criterion:")
indexByWald = walds_maximin_model(lines)
print("The best solution:", lines[indexByWald])

print("\nLaplace criterion:")
indexByLaplace = laplace_criterion(lines)
print("The best solution:", lines[indexByLaplace])

print("\nHurwitz criterion:")
indexByHurwitz = hurwitz_criterion(lines, 0.9)
print("The best solution:", lines[indexByHurwitz])

print("\nHurwitz criterion:")
indexByHurwitz = hurwitz_criterion(lines, 0.3)
print("The best solution:", lines[indexByHurwitz])

print("\nBayes-Laplace criterion:")
indexByBayesLaplace = bayes_laplace_criterion(lines, [0.55, 0.3, 0.15])
print("The best solution:", lines[indexByBayesLaplace])
