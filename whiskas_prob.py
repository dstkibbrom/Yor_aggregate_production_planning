from pulp import *


prob=LpProblem("The wiskas trial",LpMinimize)


x1 = LpVariable("ChickenPercent", 0, None, LpInteger)
x2 = LpVariable("BeefPercent", 0)

prob += 0.013 * x1 + 0.008 * x2, "Total Cost of Ingredients per can"
