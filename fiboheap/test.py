import FibonacciHeap as fh

f = fh.FibonacciHeap()

f.insert(10, 10)
f.insert(2, 2)
f.insert(15, 15)
f.insert(6, 6)

m = f.findMin()
print(m.key) # 2

q = f.extractMin()
print(q.key) # 2

q = f.extractMin()
print(q.key) # 6

f2 = fh.FibonacciHeap()
f2.insert(100, 100)
f2.insert(56, 56)

f3 = f.union(f2, f)

x = f3.root.right # pointer to random node
f3.decreaseKey(x, 1)

# print the root list using the iterate class method
print([x.key for x in f3.iterate(f3.root)]) # [10, 1, 56]

q = f3.extractMin()
print(q.key) # 1