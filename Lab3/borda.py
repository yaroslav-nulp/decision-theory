#!/usr/bin/python

import re

def borda(data, benefits):
    result = { "sum": {}, "note": {} }
    for benefit in benefits:
        result["sum"][benefit] = 0
        result["note"][benefit] = ""

    for benefit in benefits:
        for line in data:
            votes = line[0]
            position = line[1].index(benefit)
            line_length = len(line[1])
            result["note"][benefit] += votes + "*" + str(line_length - position) + "+"
            result["sum"][benefit] += (line_length - position) * int(votes)
        result["note"][benefit] = result["note"][benefit][:-1]

    places = []
    for count in sorted (result["sum"], key = result["sum"].get, reverse=True):
        places.append(count)

    return { 'places': places, 'sum': result['sum'], 'note': result['note'] }
    
