class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.info)


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def create(self, val):
        if self.root == None:
            self.root = Node(val)
        else:
            current = self.root

            while True:
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break


'''
class Node:
      def __init__(self,info): 
          self.info = info  
          self.left = None  
          self.right = None 


       // this is a node of the tree , which contains info as data, left , right
'''
hist_a = []
hist_b = []
flag = False


def lca(root, v1, v2):
    global hist_a
    global hist_b
    global flag
    hist_a = parents(root, v1, hist_a)
    flag = False
    hist_b = parents(root, v1, hist_b)
    for hist in hist_a:
        if hist in hist_b:
            ancestor = hist
        else:
            return ancestor
    return hist_a[len(hist_a) - 1]


def parents(root, v, histry):
    global flag
    if root.left and not flag:
        histry.append(root)
        if root.left.info == v:
            flag = True
            return histry
        histry = parents(root.left, v, histry)
    if root.right and not flag:
        histry.append(root)
        if root.right.info == v:
            flag = True
            return histry
        histry = parents(root.right, v, histry)
    try:
        histry.pop()
    except:
        histry.append(root)
        return histry
    return histry


tree = BinarySearchTree()
t = int(input())

arr = list(map(int, input().split()))

for i in range(t):
    tree.create(arr[i])

v = list(map(int, input().split()))

ans = lca(tree.root, v[0], v[1])
print(ans.info)
