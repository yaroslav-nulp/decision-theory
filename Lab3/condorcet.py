#!/usr/bin/python

import re

def condorcet(data, benefits):
    votes = {}

    for benefit in benefits:
        for line in data:
            electorate = line[0]
            for candidate in line[1]:
                if candidate == benefit: continue
                if line[1].index(candidate) > line[1].index(benefit): continue

                key = candidate + '>' + benefit
                votes[key] = int(electorate) if key not in votes else votes[key] + int(electorate)

    print("Comparison of votes:", votes)

    final_eloctorates = {}
    benefits_first_place = {}
    for benefit in benefits:
        benefits_first_place[benefit] = 0

    for result in votes:
        candidates = re.split('>', result)
        largest_candidate = candidates if votes[result] > votes[candidates[1] + '>' + candidates[0]] else [candidates[1], candidates[0]]
        key = largest_candidate[0] + '>' + largest_candidate[1]
        final_eloctorates[key] = votes[key]
    print("The following decisions remain:", final_eloctorates)

    for e in final_eloctorates.keys():
        candidates = re.split('>', e)
        if candidates[0] not in benefits_first_place: continue

        benefits_first_place[candidates[0]] += 1

    places = []
    for count in sorted (benefits_first_place, key = benefits_first_place.get, reverse=True):
        places.append(count)

    return { 'places': places, 'final_eloctorates': final_eloctorates }

