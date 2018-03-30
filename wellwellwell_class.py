import networkx as nx


class Well:
    def __init__(self):
        self.WIDTH = 0
        self.HEIGHT = 0

        self.time = 0
        self.target = 0

        self.matrix = []
        self.nodeMarked = []
        self.nodeUsed = []
        self.nodeFilled = []
        self.g = nx.Graph()

    def readfile(self, filename):
        file = open(filename, 'r')
        self.WIDTH, self.HEIGHT = [int(i) for i in file.readline().split()]
        for i in range(self.HEIGHT):
            for line in file:
                self.matrix.append([int(i) for i in line.split()])
        self.target = self.matrix.pop()[0]
        file.close()

    def generategraph(self):
        self.g.add_nodes_from(range(1, self.WIDTH * self.HEIGHT + 1))
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if x - 1 >= 0:
                    self.g.add_edge(self.matrix[y][x], self.matrix[y][x - 1],
                                    weight=self.matrix[y][x - 1] - self.matrix[y][x])
                if x + 1 < self.WIDTH:
                    self.g.add_edge(self.matrix[y][x], self.matrix[y][x + 1],
                                    weight=self.matrix[y][x + 1] - self.matrix[y][x])
                if y - 1 >= 0:
                    self.g.add_edge(self.matrix[y][x], self.matrix[y - 1][x],
                                    weight=self.matrix[y - 1][x] - self.matrix[y][x])
                if y + 1 < self.HEIGHT:
                    self.g.add_edge(self.matrix[y][x], self.matrix[y + 1][x],
                                    weight=self.matrix[y + 1][x] - self.matrix[y][x])

    def fill(self, start):
        neighbors = [start]
        localmarked = [start]
        #if start == 1:
        #    localmarked.append(start)
        self.nodeMarked.append(start)
        while len(neighbors) != 0:
            startsearch = neighbors.pop()
            for neigh in self.g.neighbors(startsearch):
                if neigh <= self.target and neigh not in self.nodeMarked:
                    self.nodeMarked.append(neigh)
                    neighbors.append(neigh)
                    localmarked.append(neigh)
        if self.target in localmarked:
            if start != 1:
                localmarked.pop(0)
            for x in localmarked:
                self.time += (self.target + 1) - x
            return self.target
        else:
            for node in self.nodeMarked:
                for neigh in self.g.neighbors(node):
                    if neigh not in self.nodeMarked:
                        neighbors.append(neigh)
            next = min(neighbors)
            maxheight = self.fill(next)
            suplimit = max(next, maxheight)
            for x in localmarked:
                self.time += suplimit - x
            return suplimit


well = Well()
well.readfile('input4.txt')
well.generategraph()
well.fill(1)
print(well.time)
