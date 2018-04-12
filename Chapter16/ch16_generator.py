#!/usr/bin/env python3
"""Functional Python Programming

Chapter 16, Sample Data Generator
"""
import csv
import random
from itertools import cycle, islice
from typing import List, Tuple, Optional

seed = [
    ('1', 'A', 15),
    ('2', 'A', 26),
    ('3', 'A', 33),
    ('1', 'B', 21),
    ('2', 'B', 31),
    ('3', 'B', 17),
    ('1', 'C', 45),
    ('2', 'C', 34),
    ('3', 'C', 49),
    ('1', 'D', 13),
    ('2', 'D', 5),
    ('3', 'D', 20),
]

def create_data(seed: List[Tuple[str, str, int]]) -> None:
    Data = Tuple[str, Optional[str]]

    raw_defects: List[Data] = [
        (shift, defect)
        for shift, defect, count in seed for x in range(count)
    ]

    # Should be `set(shift for shift, defect, count in seed)`
    # Also 1000-309 is based on 1000-sum(count for shift, defect, count in seed)
    shifts = ['1', '2', '3']
    non_defects: List[Data] = [
        (shift, None)
        for shift in islice(cycle(shifts), 1000-309)
    ]

    data = raw_defects + non_defects

    random.shuffle(data)

    with open("qa_data.csv", 'w', newline='') as output:
        wtr = csv.writer(output)
        wtr.writerow(["shift", "defect_type", "serial_number"])
        wtr.writerows(
            (s_d[0], s_d[1], serial)
            for serial, s_d in enumerate(data, start=12345)
        )

def verify_data(seed: List[Tuple[str, str, int]]) -> None:
    from collections import Counter
    with open("qa_data.csv", newline="") as input_file:
        rdr = csv.DictReader(input_file)
        defects = (
            (row['shift'], row['defect_type'])
            for row in rdr if row['defect_type']
        )
        tally = Counter(defects)
    print(tally)
    expected = Counter({(s, d): c for s, d, c in seed})
    assert tally == expected

if __name__ == "__main__":
    #create_data(seed)
    verify_data(seed)
