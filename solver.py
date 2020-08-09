import time


class Cube:

    solvedPos = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]

    pos = [[j for j in i] for i in solvedPos]

    def U(self):
        firstPos = self.pos[0]
        self.pos[0] = self.pos[3]
        self.pos[3] = self.pos[2]
        self.pos[2] = self.pos[1]
        self.pos[1] = firstPos

    def Ui(self):
        for i in range(3):
            self.U()

    def U2(self):
        for i in range(2):
            self.U()

    def R(self):
        firstPos = self.pos[1]
        self.pos[1] = self.pos[2]
        self.pos[2] = self.pos[5]
        self.pos[5] = self.pos[6]
        self.pos[6] = firstPos

        self.pos[1][1] = (self.pos[1][1] + 1) % 3
        self.pos[2][1] = (self.pos[2][1] - 1) % 3
        self.pos[5][1] = (self.pos[5][1] + 1) % 3
        self.pos[6][1] = (self.pos[6][1] - 1) % 3

    def Ri(self):
        for i in range(3):
            self.R()

    def R2(self):
        for i in range(2):
            self.R()

    def F(self):
        firstPos = self.pos[2]
        self.pos[2] = self.pos[3]
        self.pos[3] = self.pos[4]
        self.pos[4] = self.pos[5]
        self.pos[5] = firstPos

        self.pos[2][1] = (self.pos[2][1] + 1) % 3
        self.pos[3][1] = (self.pos[3][1] - 1) % 3
        self.pos[4][1] = (self.pos[4][1] + 1) % 3
        self.pos[5][1] = (self.pos[5][1] - 1) % 3

    def Fi(self):
        for i in range(3):
            self.F()

    def F2(self):
        for i in range(2):
            self.F()

    def Inverse(self, alg):
        inverse = []
        for move in reversed(alg):
            if len(move) == 1:
                inverse.append(move + "'")
            elif move[1] == "'":
                inverse.append(move[0])
            else:
                inverse.append(move)
        return inverse

    def Scramble(self, scramble):
        movesKey = {"U": self.U, "U'": self.Ui, "U2": self.U2, "R": self.R, "R'": self.Ri, "R2": self.R2, "F": self.F,
                    "F'": self.Fi, "F2": self.F2}

        for move in scramble:
            movesKey[move]()

    def FastSolve(self):
        moves = ["U", "U'", "U2", "R", "R'", "R2", "F", "F'", "F2"]

        scrambledPos = [[j for j in i] for i in self.pos]

        algs = [[[]]]

        scrambledPosDict = {}
        solvedPosDict = {tuple([tuple(i) for i in self.solvedPos]): []}

        poses = (scrambledPos, self.solvedPos)
        posDicts = (scrambledPosDict, solvedPosDict)

        for i in range(6):

            resetPos = poses[i % 2]
            addingPosDict = posDicts[i % 2]
            checkingPosDict = posDicts[(i + 1) % 2]

            algs.append([])

            for alg in algs[i]:
                self.pos = [[j for j in i] for i in resetPos]
                self.Scramble(alg)

                posTuple = tuple([tuple(i) for i in self.pos])
                if posTuple in checkingPosDict:
                    solution = alg + self.Inverse(checkingPosDict[posTuple])
                    if i % 2 == 1:
                        solution = self.Inverse(solution)
                    return solution

            for alg in algs[i]:
                self.pos = [[j for j in i] for i in resetPos]
                self.Scramble(alg)
                algPos = [[j for j in i] for i in self.pos]

                for move in moves:
                    self.pos = [[j for j in i] for i in algPos]
                    self.Scramble([move])
                    posTuple = tuple([tuple(i) for i in self.pos])

                    if posTuple not in addingPosDict:
                        if tuple([tuple(i) for i in self.pos]) in checkingPosDict:
                            solution = alg + [move] + self.Inverse(checkingPosDict[tuple([tuple(i) for i in self.pos])])
                            if i % 2 == 1:
                                solution = self.Inverse(solution)
                            return solution
                        addingPosDict[posTuple] = alg + [move]
                        algs[i + 1].append(alg + [move])


cube = Cube()

f = open("scrambles.txt", "r")
g = open("solutions.txt", "w")
h = open("results.txt", "w")

runTimes = [[] for i in range(12)]

numScrambles = 0
for line in f:
    print(numScrambles + 1)
    scram = line.strip()

    cube.Scramble(scram.split())
    startTime = time.process_time()
    solution = cube.FastSolve()
    runTime = time.process_time() - startTime
    runTimes[len(solution)].append(runTime)

    cube.pos = [[j for j in i] for i in cube.solvedPos]

    g.write("Solution: {}           Length: {}          Run time: {}\n"
            .format(' '.join(solution), len(solution), runTime))
    cube.pos = [[j for j in i] for i in cube.solvedPos]
    numScrambles += 1

averageLength = 0
averageRunTime = 0
for i in range(12):
    averageLength += len(runTimes[i]) * i
    for time in runTimes[i]:
        averageRunTime += time

averageLength /= numScrambles
averageRunTime /= numScrambles

flatRuntimes = []
for i in runTimes:
    flatRuntimes += i

h.write("Number of scrambles: {}\n".format(numScrambles))
h.write("Average solution length: {}\n".format(averageLength))
h.write("Average run time: {}\n".format(averageRunTime))
h.write("Best run time: {}\n".format(min(flatRuntimes)))
h.write("Worst run time: {}\n".format(max(flatRuntimes)))
h.write("\n")

for i in range(12):
    avg = 0
    for time in runTimes[i]:
        avg += time
    if len(runTimes[i]) != 0:
        avg /= len(runTimes[i])
    else:
        avg = -1
    h.write("{} solutions of length {} ({}%)                "
            "Average run time: {}\n".format(len(runTimes[i]), i, round(len(runTimes[i]) * 100000 / numScrambles) / 1000, avg))

f.close()
g.close()
h.close()
