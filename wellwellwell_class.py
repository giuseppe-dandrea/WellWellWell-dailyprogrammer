import networkx as nx


class Well:
    def __init__(self):
        self.WIDTH = 0
        self.HEIGHT = 0

        self.time = 0
        self.target = 0

        self.matrix = []
        self.g = nx.Graph()

        self.heights = []

    def readfile(self, filename):
        file = open(filename, 'r')
        self.WIDTH, self.HEIGHT = [int(i) for i in file.readline().split()]
        for i in range(self.HEIGHT):
            for line in file:
                self.matrix.append([int(i) for i in line.split()])
        self.target = self.matrix.pop()[0]
        file.close()
        # Initialization of the heights matrix
        for x in range(0, self.WIDTH * self.HEIGHT + 1):
            self.heights.append(x)

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

    def getnodeheight(self, node):
        return self.heights[node]

    def removefromtofill(self, start, tofill):
        queue = [start]
        if start in tofill:
            tofill.remove(start)
        while queue != []:
            current = queue.pop()
            for neigh in self.g.neighbors(current):
                if self.heights[neigh] == self.heights[current] and neigh in tofill:
                    queue.append(neigh)
                    tofill.remove(neigh)
        return tofill

    def fillbfs(self, start):
        nodeMarked = [start]
        returnVal = False
        lessequal = [start]
        tofill = [start]
        while lessequal != []:
            current = lessequal.pop()
            for neigh in self.g.neighbors(current):
                if self.heights[neigh] < self.heights[current] and neigh not in nodeMarked:
                    # Remove from tofill all the elements with height equal to current that are neighbors of current!
                    tofill = self.removefromtofill(current, tofill)

                    tofill.append(neigh)
                    nodeMarked.append(neigh)
                    lessequal.append(neigh)
                elif self.heights[neigh] == self.heights[current] and neigh not in nodeMarked:
                    tofill.append(neigh)
                    nodeMarked.append(neigh)
                    lessequal.append(neigh)

        for elem in tofill:
            self.heights[elem] += 1
            if elem == self.target and self.heights[self.target] == self.target + 1:
                returnVal = True

        return returnVal

    def getTime(self):
        for i, heigth in enumerate(self.heights):
            self.time += self.heights[i] - i

        return self.time


well = Well()
well.readfile('input2.txt')
well.generategraph()
while not well.fillbfs(1):
    pass
time = well.getTime()
print(time)
