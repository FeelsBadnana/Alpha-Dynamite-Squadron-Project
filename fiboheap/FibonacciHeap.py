# Thanks to Daniel Borowski: https://github.com/danielborowski/fibonacci-heap-python
# Credit also to Introduction to Algorithms 3rd Edition by Thomas R. Cormen: https://edutechlearners.com/download/Introduction_to_algorithms-3rd%20Edition.pdf


class FibonacciHeap:
    class Node:
        def __init__(self, k, v):
            self.key = k
            self.value = v
            self.degree = 0
            self.parent = None
            self.child = None
            self.left = self.right = None
            self.mark = False

    def __init__(self):
        self.root = None
        self.min = None
        self.count = 0

    def insert(self, key, value):
        newNode = self.Node(key, value)
        newNode.left = newNode.right = newNode
        if self.min is None:
            self.root = newNode
            self.min = newNode
        else:
            self.addNodeToRoot(newNode)
            if newNode.key < self.min.key:
                self.min = newNode
        self.count += 1
        # self.addNodeToRoot(newNode)
        # if self.min is None or newNode.key < self.min.key:
        #     self.min = newNode
        # self.count += 1


    def findMin(self):
        return self.min
    
    def union(self, heap1, heap2):
        newHeap = FibonacciHeap()
        newHeap.min = heap1.min
        newHeap.root = heap1.root
        
        self.addRootsTogether(heap1, heap2)

        if (heap1.min is None) or (heap2.min is not None and heap2.min.key < heap1.min.key):
            newHeap.min = heap2.min
        newHeap.count = heap1.count + heap2.count
        return newHeap

    def extractMin(self):
        x = self.min
        if x is not None:
            if x.child is not None:
                children = [y for y in self.iterate(x.child)]
                for i in range(0, len(children)):
                    self.addNodeToRoot(children[i])
                    children[i].parent = None
            self.removeNodeFromRoot(x)

            if x == x.right:
                self.min = None
                self.root = None
            else:
                self.min = x.right
                self.consolidate()
            self.count -= 1
        return x

    def consolidate(self):
        a = [None] * self.count
        nodes = [w for w in self.iterate(self.root)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while a[d] != None:
                y = a[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heapLink(y, x)
                a[d] = None
                d += 1
            a[d] = x
        
        for i in range(0, len(a)):
            if a[i] is not None:
                if a[i].key < self.min.key:
                    self.min = a[i]

    def decreaseKey(self, x, k):
        if k > x.key:
            return None
        x.key = k
        temp = x.parent
        if temp is not None and x.key < temp.key:
            self.cut(x, temp)
            self.cascadingCut(temp)
        if x.key < self.min.key:
            self.min = x

    # if a child node becomes smaller than its parent node we
    # cut this child node off and bring it up to the root list
    def cut(self, x, y):
        self.removeNodeFromChildList(y, x)
        y.degree -= 1
        self.addNodeToRoot(x)
        x.parent = None
        x.mark = False

    # cascading cut of parent node to obtain good time bounds
    def cascadingCut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascadingCut(z)
    
    def heapLink(self, y, x):
        self.removeNodeFromRoot(y)
        y.left = y.right = y
        self.addNodeToChildList(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    def addNodeToRoot(self, node):
        if self.root is None:
            self.root = node
        else:
            node.right = self.root.right
            node.left = self.root
            self.root.right.left = node
            self.root.right = node

    def addRootsTogether(self, heap1, heap2):
        temp = heap2.root.left
        heap2.root.left = heap1.root.left
        heap1.root.left.right = heap2.root
        heap1.root.left = temp
        heap1.root.left.right = heap1.root

    def addNodeToChildList(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def removeNodeFromRoot(self, node):
        if node == self.root:
            self.root = node.right
        node.right.left = node.left
        node.left.right = node.right

    # remove a node from the doubly linked child list
    def removeNodeFromChildList(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.right.left = node.left
        node.left.right = node.right

    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right
          