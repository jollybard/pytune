# coding: utf-8

# see https://en.xen.wiki/w/Mathematics_of_MOS
#
# We can tell whether a (gen,per) pair has a generator
# of size n by looking at whether it's within a Farey pair:
#               i/n <= gen/per <=  a/b
# (that is, bi - an = 1); that means they're neighbors
# in the scale tree.
#
# TODO: Make a scale object!

from collections import Counter
from math import log
from itertools import combinations

# basic functions
def mod(x,p):
    if x % p == 0:
        return p
    else:
        return x % p

def edo(n, m=None):
    if m is not None:
        return round(n * (1200/m),10)
    else:
        return [edo(i,n) for i in range(1,n+1)]

def fromJI(q):
    return round(1200 * log(q,2),3)

def fromJIscale(s):
    return [fromJI(x) for x in s]

def approxIn(s1, s2, offset = None):
    #approximate s1 in s2
    if offset is not None:
        if s1[-1] != s2[-1]:
            print("The two scales must have the same period.")
            return -1
        p = s1[-1]
        j = 0
        best = s2[0]
        out = []
        for note in sorted([mod(x + offset,p) for x in s1[:-1]]):
            for (k,x) in enumerate(s2[j+1:]):
                if abs(note - x) % p > abs(note - best) % p:
                    out.append(best)
                    j += k
                    break
                best = x
        out.append(p)
        return out
    else:
        return approxIn(s1,s2,0)

def rotate(s,i):
    p = s[-1]
    c = s[(i-1) % len(s)]
    scale = [round(mod(x - c, p),3) for x in s]
    scale.sort()
    return scale

# MOS scales

def generateScale(g,p,n,m):
    scale = [i*g for i in range(-m,-m+n)]
    scale = [mod(x,p) for x in scale]
    return sorted(list(set(scale)))

# TODO: edos, closest approximations
    
def fareyNeighbor(a,b):
    for i in range(1,b):
        k = a*i // b + 1
        if b*k - a*i == 1:
            return (k,i)
    return (0,1)
            
# 
def mosGenRanges(n,p):
    l = [[(i, n),fareyNeighbor(i,n)] for i in range(1,n)]
    return [[i * p / n, ii * p/ nn] for [(i,n),(ii,nn)] in l]

def generatorHasMOS(g,n,p):
    ranges = mosGenRanges(n,p)
    for [a,b] in ranges:
        if a <= g <= b:
            return True
        if a <= (p - g) <= b:
            return True
    return False

def intervalList(s, k):
    n = len(s)
    p = s[-1]
    return [round(mod(s[(i + k) % n] - s[i], p),3) for i in range(-1,n-1)]

def intervalTable(s):
    n = len(s)
    l = [intervalList(s,j) for j in range(n)]
    return l

def maxVariety(s):
    l = [set(x) for x in intervalTable(s)]
    l = [len(x) for x in l]
    return max(l)

def isNMOS(s,k):
    n = len(s)
    for i in range(n):
        steps = set(intervalList(s, i))
        if len(steps) > k:
            return False
    return True

def isMOS(s):
    return isNMOS(s,2)

# generate the MOS scales of a given (generator,period) pair
# TODO: make a scale object

def mosSizes(g,p):
    n = 1
    while True:
        if generatorHasMOS(g,n,p):
            yield n
        n += 1

# scales with two generators

def generateScale2(g1, g2, p, n1, n2, m1, m2):
    scale1 = generateScale(g1,n1+m1+1,m1,p)
    scale2 = generateScale(g2,n2+m2+1,m2,p)
    scale = sorted(list(set(scale1 + scale2)))

def temperScale(s, x1, x2):
    # returns the mean of x1 and x2
    steps = intervalList(s,1)
    n1 = steps.count(x1)
    n2 = steps.count(x2)
    n = n1 + n2
    x = (n1 * x1 + n2 * x2)/n
    steps = [x if i in [x1, x2] else i for i in steps]
    note = 0
    scale = []
    for i in range(len(s)):
        note += steps[i]
        scale.append(note)
    return scale

#def isPairwiseMOS(s):
#    steps = set(intervalList(s, 1))
#    for x1, x2 in combinations(steps,steps):

#def generateNMOS(g1, g2, p, n):
