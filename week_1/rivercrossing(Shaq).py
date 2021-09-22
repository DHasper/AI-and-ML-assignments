chars = ['w','g','c','f']
nodes = []
class Node:
    parentNode = None
    def __init__(self, char):
        self.char = char
    def setParent(self, parentNode):
        self.parentNode = parentNode

def Debug(arrayID, node):
    # print('Array {} char "{}"'.format(arrayID, node.char))
    nodes[arrayID].append(node.char)
    if(node.parentNode is not None):
        Debug(arrayID, node.parentNode)

def IsGameOver(char, parentNode):
    if(char == parentNode.char):
        return True
    if(((char == chars[0]) & (parentNode.char == chars[1])) | ((char == chars[1]) & (parentNode.char == chars[0]))):
        return True
    if(((char == chars[1]) & (parentNode.char == chars[2])) | ((char == chars[2]) & (parentNode.char == chars[1]))):
        return True
    return False

def CreateChildNodes(parentNode):
    childNodes = []
    for i in range(4):
        if(IsGameOver(chars[i], parentNode)):
            nodes.append([])
            Debug(len(nodes) - 1, parentNode)
            return childNodes
        node = Node(chars[i])
        node.setParent(parentNode)
        childNodes.append(node)
        CreateChildNodes(node)
    return childNodes

for i in range(4):
    node = Node(chars[i])
    CreateChildNodes(node)

for i in nodes:
    print(i)


#5 trees, within each breath check all 5 options
#gameover state

