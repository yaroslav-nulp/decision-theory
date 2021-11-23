#!/usr/bin/python

import sys
import re
import string
from copy import deepcopy 
from colorama import Fore, Style, Back


def open_file():
    try:
        return open("lab4_variant_5.txt")
    except FileNotFoundError:
        print("Oops! File not exist...")
        exit()


def set_max_object_length(parameters, objects, maxWidths):
    for parameter in parameters:
        for obj in objects:
            objParamLength = len(str(parameters[parameter][obj]))
            if obj not in maxWidths:
                maxWidths[obj] = len(obj)
            if objParamLength > maxWidths[obj]:
                maxWidths[obj] = objParamLength
    

def draw_header(objects, maxWidths, getStartLength = False):
    return_str = ''
    numberPart = '|' + ('%' + str(maxWidths['NUMBER']) + 's') % "№|"
    parameterPart = ('%' + str(maxWidths['PARAMETER']) + 's') % "Parameter"
    coefficientPart = ('%' + str(maxWidths['COEFFICIENT']) + 's') % "Coefficient"
    objectsPart = ''

    if getStartLength == True: return len(numberPart + parameterPart + '|' + coefficientPart + '|')

    for obj in objects:
        objectsPart += ('%' + str(maxWidths[obj]) + 's') % str(obj)
        objectsPart += '|'

    return numberPart + parameterPart + '|' + coefficientPart + '|' + Fore.BLUE + objectsPart + Style.RESET_ALL
   


def draw_parameters(parameters, objects, maxWidths):
    return_str = ''
    count = 1

    for parameter in parameters:
        numberPart = '|' + ('%' + str(maxWidths['NUMBER']) + 's') % (str(count) + "|")
        parameterPart = Fore.BLUE  + ('%' + str(maxWidths['PARAMETER']) + 's') % parameter + Style.RESET_ALL
        coefficientPart = Fore.LIGHTRED_EX + ('%' + str(maxWidths['COEFFICIENT']) + 's') % parameters[parameter]['COEFFICIENT'] + Style.RESET_ALL
        objectsPart = ''

        for obj in objects:
            objectsPart += ('%' + str(maxWidths[obj]) + 's') % str(parameters[parameter][obj])
            objectsPart += '|'

        return_str += numberPart + parameterPart + '|' + coefficientPart + '|' + Fore.WHITE + objectsPart + Style.RESET_ALL + '\n' 
        count += 1

    return return_str

def print_result (header, parameters):
    header_line = ''

    for i in range(len(header) - len(Style.RESET_ALL) - len(Fore.BLUE )): header_line += '-'

    print(header_line)
    print(header)
    print(header_line)
    print(parameters)
    print(header_line)


def print_total (header, objects, parameters, maxWidths):
    header_line = ''
    for i in range(len(header) - len(Style.RESET_ALL) - len(Fore.BLUE )): header_line += '-'

    total = draw_header(objects, maxWidths, True)
    totalPart = '|' + ('%' + str(total - 1) + 's') % ('Sum:' + "|")
    objTotal = {}
    for obj in objects:
        objSum = 0
        for param in parameters:
            objSum += parameters[param][obj]

        objTotal[obj] = objSum
  
    maxValue = max(objTotal, key=objTotal.get)
    for obj in objTotal:
        if maxValue == obj:
            totalPart += Fore.RED  + Back.LIGHTWHITE_EX
            totalPart += ('%' + str(maxWidths[obj]) + 's') % str(round(objTotal[obj], 2))
            totalPart += '|' + Style.RESET_ALL
            continue
        totalPart += ('%' + str(maxWidths[obj]) + 's') % str(round(objTotal[obj], 2))
        totalPart += '|'
    print(totalPart)
    print(header_line)
    print('Best object has ' + Fore.RED  + Back.LIGHTWHITE_EX + '(' + maxValue + ')' + Style.RESET_ALL)

file = open_file()

parameters = {}
objects = re.split(';', re.sub('\n', '', file.readline()))
maxWidths = { 'PARAMETER': len("Parameter\t|"), 'COEFFICIENT': len('Coefficient|'), 'NUMBER': 2 }

if (len(objects) < 2):
    print("Please enter more than two objects")
    exit()

for line in file:
    [parameter, values_str] = re.split(':', re.sub('\n', '', line))
    values = re.split(';', values_str)
    if (len(values) - 1 < len(objects)):
        print("Discrepancy between objects and parameters")
        exit()

    parameters[parameter] = {}
    parameters[parameter]['COEFFICIENT'] = float(values[0])

    if (len(parameter) > maxWidths['PARAMETER']): maxWidths['PARAMETER'] = len(parameter)
    if (len(values[0]) > maxWidths['COEFFICIENT']): maxWidths['COEFFICIENT'] = len(values[0])

    for i in range(0, len(objects)):
        parameters[parameter][objects[i]] = float(values[i + 1])

maxWidths['NUMBER'] = len(str(len(parameters))) + 1

print('\nStart data from file "' + "lab4_variant_5.txt" + '"')
set_max_object_length(parameters, objects, maxWidths)
header = draw_header(objects, maxWidths)
parameter_str = str(draw_parameters(parameters, objects, maxWidths))[:-1]
print_result(header, parameter_str)

print('\nMaking calculations...')
parameters_equations = deepcopy(parameters)

for param in parameters_equations:
    for obj in objects:
        parameters_equations[param][obj] = str(parameters_equations[param]['COEFFICIENT']) + '*' + str(parameters_equations[param][obj])

set_max_object_length(parameters_equations, objects, maxWidths)

header = draw_header(objects, maxWidths)
parameter_str = str(draw_parameters(parameters_equations, objects, maxWidths)[:-1])
print_result(header, parameter_str)


print('\nThe result of calculations:')
for param in parameters:
    for obj in objects:
        parameters[param][obj] = float(parameters[param]['COEFFICIENT']) * float(parameters[param][obj])

set_max_object_length(parameters, objects, maxWidths)

header = draw_header(objects, maxWidths)
parameter_str = str(draw_parameters(parameters, objects, maxWidths)[:-1])
print_result(header, parameter_str)
print_total(header, objects,parameters, maxWidths)
