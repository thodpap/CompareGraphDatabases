import random

# max connections: ((n-1)*(n-2)/2) = 9*8/2 = 36

f = open("node_10.txt", 'w')
f.write("\n\n")
myset = set()

NUM_OF_CONNECTIONS = 30

for k in range(NUM_OF_CONNECTIONS):

    i = None
    j = None
    while True:
        i = random.randint(1, 10)
        j = random.randint(1, 10)
        
        if i == j:
            continue

        if ((i, j) in myset) or ((j, i) in myset):
            continue

        myset.add((i, j))
        myset.add((j, i))
        f.write(f"{i} {j}\n")
        break
   