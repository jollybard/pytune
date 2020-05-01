# coding: utf-8
def mod(x,p):
    if x % p == 0:
        return p
    else:
        return x % p

def edo(n,m):
    return n * (1200/m)

def generateScale(x,n,m,p):
    scale = [i*x for i in range(-m,-m+n)]
    scale = [mod(x,p) for x in scale]
    scale.sort()
    return scale
    
def fareyNeighbor(a,b):
    for i in range(1,b):
        k = a*i // b + 1
        if b*k - a*i == 1:
            return (k,i)
    return (0,1)
            
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

def intervalTable(l):
    n = len(l)
    l = [[mod(l[(i+j) % n] - l[j], l[-1]) for i in range(n)] for j in range(n)]
    return l

# generate the MOS scales of a given (generator,period) pair
# TODO: make a scale object

def mosSizes(g,p):
    n = 1
    while True:
        if generatorHasMOS(g,n,p):
            yield n
        n += 1
