from pyparsing import *


class Node():

    def __init__(self, parent, child_left, child_right, value):
        self.parent = parent
        self.child_left = child_left
        self.child_right = child_right
        self.value = value

    def getParent(self):
        return  self.parent

    def  getLChild(self):
        return self.child_left

    def getRChild(self):
        return  self.child_right

class ProgramGraph():

    def __init__(self, ast):
        self.pg = list()

        self.makePG(ast)

    def makePG(self, ast):
        index = len(ast)

        print(index)

    def makePG(self, ast):

        for i in range(len(ast)):
            index = 0

            for x in ast[i]:
                if type(x) == ParseResults:
                    x.as_list()
                    if (len(x) > 1):
                        self.makePG(x)
                        break

                else:
                    if type(ast[i][index]) == ParseResults:
                        value = (ast[i][index][0]) + " " + x
                        node = Node(parent=0, child_left=0, child_right=0, value=value)
                        self.pg.append(node)



            index += 1

    def getPG(self):
        return self.pg