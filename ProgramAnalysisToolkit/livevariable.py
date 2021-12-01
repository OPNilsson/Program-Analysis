class LiveVariable():

    def __init__(self, wl):
        self.wl = wl

    def solve(self, node):
        self.list = dict()
        self.i = 0

        if node.value in "A" or "R" or "while":
            for i in range(len(node.value)):
                self.list["kill"] = node.parent
                self.list["gen"] = node.value
                self.i += i

        elif node.value in 10:
            for i in range(10):
                self.list["kill"] = node.parent
                self.list["gen"] = node.value
                self.i += i
        else:
            self.list["kill"] = node.parent.value
            self.list["gen"] = node.value
