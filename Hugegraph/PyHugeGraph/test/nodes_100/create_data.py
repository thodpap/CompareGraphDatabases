import random

# max connections: ((n)*(n-1)/2) =~ 5000 

f = open("100_nodes.txt", 'w')
f.write("\n\n")
myset = set()

NUM_OF_CONNECTIONS = 600 # (12% * 5000 (CLIQUE))

for k in range(NUM_OF_CONNECTIONS):

    i = None
    j = None
    while True:
        # print("WHAT")
        i = random.randint(1, 100)
        j = random.randint(1, 100)
        
        if i == j:
            print("here")
            continue

        if ((i, j) in myset) or ((j, i) in myset):
            print("here___________")
            continue


        myset.add((i, j))
        myset.add((j, i))
        f.write(f"{i} {j}\n")
        
        break
    print(k)
   