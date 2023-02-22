

f = open("100_nodes.txt", 'r')
lines = f.readlines()[2:]
myset = set(list(range(1, 101)))

NUM_OF_CONNECTIONS = 600 # (12% * 50000 (CLIQUE))

for i, line in enumerate(lines):

    line = line.replace("\n","")
    vertex_1, vertex_2 = line.split(" ")
    vertex_1 = int(vertex_1)
    vertex_2 = int(vertex_2) 
    if vertex_1 in myset:
        myset.remove(vertex_1)
    if vertex_2 in myset:
        myset.remove(vertex_2)
    if len(myset) == 0:
        print("Integrity passed!")
        exit()

print("Integrity failed..")
print(myset)