#!/usr/bin/env python3
import itertools

def get_ranges(i):
    def difference(pair):
        x, y = pair
        return y - x
    for a, b in itertools.groupby(enumerate(i), difference):
        b = list(b)
        yield b[0][1], b[-1][1]

def parse(s):
    parts = s.split("..")
    if len(parts) == 1:
        return (int(parts[0], 16), 1)
    low = int(parts[0], 16)
    high = int(parts[1], 16)
    return (low, high - low + 1)

def output(label, variable, values):
    print("// " + label)
    nums = []
    for v in values:
        start, count = parse(v)
        for i in range(count):
            nums.append(start + i)
    for r in get_ranges(nums):
        start = r[0]
        count = r[1] - r[0] + 1
        print("        [%s addCharactersInRange:NSMakeRange(%s, %d)];" % (variable, hex(start), count))
    print("")

def output_ignorables():
    """Output emoji that have a default emoji presentation."""
    # Section labeled '# Derived Property: Default_Ignorable_Code_Point'
    # http://www.unicode.org/Public/UNIDATA/DerivedCoreProperties.txt
    f = open("DerivedCoreProperties.txt", "r")
    ranges = []
    for line in f:
        try:
            i = line.index("#")
            line = line[0:i]
        except:
            pass
        parts = line.split(";")
        if len(parts) < 2:
            continue
        flavor = parts[1].strip()
        if flavor != "Default_Ignorable_Code_Point":
            continue
        ranges.append(parts[0])
    output("Ignorable", "ignorable", ranges)

# wget 'http://www.unicode.org/Public/UNIDATA/DerivedCoreProperties.txt'
output_ignorables()
