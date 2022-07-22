from gekko import GEKKO
import numpy as np
from scipy.special import factorial
import matplotlib.pyplot as plt

m = GEKKO(remote=False)

ESS1_Capacity = 1000
ESS2_Capacity = 1000

SOC1_Init = 500
SOC2_Init = 500

SOC1_Min = 100
SOC2_Min = 100

SOC1_Max = 950
SOC2_Max = 950

ESS1_DE = .95
ESS2_DE = .95

ESS1_CE = .95
ESS2_CE = .95

SOC1_FMin = 100
SOC2_FMin = 100

SOC1_FMax = 700
SOC2_FMax = 700

ESS1_Min = 10
ESS2_Min = 10

ESS1_Max = 500
ESS2_Max = 500

ESS1_Wc = 100
ESS2_Wc = 50

Load = [m.Param(value=46),
        m.Param(value=47),
        m.Param(value=45),
        m.Param(value=45),
        m.Param(value=46),
        m.Param(value=47),
        m.Param(value=45),
        m.Param(value=52),
        m.Param(value=74),
        m.Param(value=77),
        m.Param(value=78),m.Param(value=76),m.Param(value=62),m.Param(value=67), m.Param(value=69),m.Param(value=68),m.Param(value=67),m.Param(value=58),m.Param(value=52),m.Param(value=49),m.Param(value=50),m.Param(value=50),m.Param(value=52),m.Param(value=52)]

PV =  [m.Param(value=0), m.Param(value=0),m.Param(value=0),m.Param(value=0),m.Param(value=0),m.Param(value=0),m.Param(value=1),m.Param(value=16),m.Param(value=48),m.Param(value=75),m.Param(value=93),m.Param(value=102),m.Param(value=105),m.Param(value=100), m.Param(value=78),m.Param(value=60),m.Param(value=30),m.Param(value=4),m.Param(value=0),m.Param(value=0),m.Param(value=0),m.Param(value=0),m.Param(value=0),m.Param(value=0)]
SMP = [m.Param(value=102.3),m.Param(value=98.56),m.Param(value=98.56),m.Param(value=91.57),m.Param(value=93.61),m.Param(value=94.37),m.Param(value=102.5),m.Param(value=104.24),m.Param(value=108.06),m.Param(value=109.89),m.Param(value=109.89),m.Param(value=109.61),m.Param(value=107.62),m.Param(value=111.83),m.Param(value=113.92),m.Param(value=114.33),m.Param(value=114.33),m.Param(value=114.33),m.Param(value=114.41),m.Param(value=114.41),m.Param(value=111.3),m.Param(value=108.52),m.Param(value=106.41),m.Param(value=107.2)]


P_ESS1_Ch = [m.Var(lb=0) for t in range(24)]
P_ESS2_Ch = [m.Var(lb=0) for t in range(24)]


P_ESS1_Dis = [m.Var(lb=0) for t in range(24)]
P_ESS2_Dis = [m.Var(lb=0) for t in range(24)]


SOC1 = [m.Var() for t in range(24)]
SOC2 = [m.Var() for t in range(24)]


u_ch1 = [m.Var(lb=0, ub=1, integer=True) for t in range(24)]
u_ch2 = [m.Var(lb=0, ub=1, integer=True) for t in range(24)]


u_dis1 = [m.Var(lb=0, ub=1, integer=True) for t in range(24)]
u_dis2 = [m.Var(lb=0, ub=1, integer=True) for t in range(24)]


m.Equation([PV[t]+P_ESS1_Dis[t] + P_ESS2_Dis[t] == Load[t]+P_ESS1_Ch[t]+P_ESS2_Ch[t] for t in range(24)])
m.Equation([P_ESS1_Ch[t] >= u_ch1[t] * ESS1_Min for t in range(24)])
m.Equation([P_ESS2_Ch[t] >= u_ch2[t] * ESS2_Min for t in range(24)])

m.Equation([P_ESS1_Ch[t] <= u_ch1[t] * ESS1_Max for t in range(24)])
m.Equation([P_ESS2_Ch[t] <= u_ch2[t] * ESS2_Max for t in range(24)])

m.Equation([P_ESS1_Dis[t] >= u_dis1[t]*ESS1_Min for t in range(24)])
m.Equation([P_ESS2_Dis[t] >= u_dis2[t]*ESS2_Min for t in range(24)])

m.Equation([P_ESS1_Dis[t] <= u_dis1[t]*ESS1_Max for t in range(24)])
m.Equation([P_ESS2_Dis[t] <= u_dis2[t]*ESS2_Max for t in range(24)])

m.Equation([u_ch1[t] + u_dis1[t] == 1 for t in range(24)])
m.Equation([u_ch2[t] + u_dis2[t] == 1 for t in range(24)])

m.Equation(SOC1_FMin <= SOC1[23])
m.Equation(SOC2_FMin <= SOC2[23])

m.Equation([SOC1_FMax >= SOC1[23]])
m.Equation([SOC2_FMax >= SOC2[23]])

m.Equation([SOC1_Min <= SOC1[t] for t in range(24)])
m.Equation([SOC2_Min <= SOC2[t] for t in range(24)])

m.Equation([SOC1_Max >= SOC1[t] for t in range(24)])
m.Equation([SOC2_Max >= SOC2[t] for t in range(24)])

# m.Equation(SOC1[0] == SOC1_Init)
# m.Equation(SOC2[0] == SOC2_Init)
# m.Equation([SOC1[t] == SOC1[t-1] + (P_ESS1_Ch[t-1]*ESS1_CE) -(P_ESS1_Dis[t-1]) for t in range(1,24)])
# m.Equation([SOC2[t] == SOC2[t-1] + (P_ESS2_Ch[t-1]*ESS2_CE) -(P_ESS2_Dis[t-1]) for t in range(1,24)])

P_Mar = m.sum([(SMP[t]*PV[t])+(P_ESS1_Dis[t] * SMP[t]) + (P_ESS2_Dis[t]*SMP[t]) - (P_ESS1_Ch[t] * SMP[t])
               - (SMP[t]*P_ESS2_Ch[t]) for t in range(24)])

P_ESS1 = m.sum([P_ESS1_Ch[t]+P_ESS1_Dis[t] for t in range(24)])
P_ESS2 = m.sum([P_ESS2_Ch[t] + P_ESS2_Dis[t] for t in range(24)])

WC_total = P_ESS1*ESS1_Wc + P_ESS2*ESS2_Wc
Revenue = P_Mar - WC_total
m.Maximize(Revenue)
m.options.SOLVER=1
m.options.IMODE = 2
m.solve()

for t in range(24):
    print(SOC1[t].Value, SOC2[t].Value, P_ESS1_Ch[t].Value, P_ESS2_Ch[t].Value, u_ch1[t].Value, u_dis1[t].Value)
T=range(24)
plt.plot(T, P_ESS1_Ch, 'g-',label="P_ESS1_Ch")
plt.plot(T, P_ESS2_Ch, 'b-',label="P_ESS2_Ch")
plt.plot(T, P_ESS1_Dis, 'r-',label="P_ESS1_Dis")
plt.plot(T, P_ESS2_Dis, 'y-',label="P_ESS2_Dis")
plt.plot(T, PV, '#121212', label="PV")
plt.plot(T, Load, '#0090FF', label="Load")
# plt.plot(T, PV, 'r-',label="PV")
plt.xlabel('Time')
plt.ylabel('Power')
plt.legend(loc='best')
# plt.legend(['Data','Linear','Quadratic','Cubic'],loc='best')
plt.style.use('ggplot')
plt.show()


plt.show()