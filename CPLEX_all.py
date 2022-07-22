
from docplex.mp.model import Model

m = Model(name='Revenue maximization')

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


Load = [46, 47,45,45,46,47,45,52,74,77,78,76,62,67, 69,68,67,58,52,49,50,50,52,52]

PV =  [0, 0,0,0,0,0,1,16,48,75,93,102,105,100, 78,60,30,4,0,0,0,0,0,0]

SMP = [102.3,98.56,98.56,91.57,93.61,94.37,102.5,104.24,108.06,109.89,
       109.89,109.61,107.62,111.83,113.92,114.33,114.33,114.33,114.41,114.41,111.3,108.52,106.41,107.2]

P_ESS1_Ch = [m.continuous_var(0, name="P_ESSone_ch"+str(i)) for i in range(24)]
P_ESS2_Ch = [m.continuous_var(0, name="P_ESStwo_ch"+str(i)) for i in range(24)]


P_ESS1_Dis = [m.continuous_var(0, name="P_ESSone_Dis"+str(i)) for i in range(24)]
P_ESS2_Dis = [m.continuous_var(0, name="P_ESStwo_Dis"+str(i)) for i in range(24)]

SOC1 = [m.continuous_var(0,name="SOC1"+str(i)) for i in range(24)]
SOC2 = [m.continuous_var(0,name="SOC2"+str(i)) for i in range(24)]

u_ch1 = [m.continuous_var(lb=0, ub=1,name="u_chone"+str(i)) for i in range(24)]
u_ch2 = [m.continuous_var(lb=0, ub=1, name="u_chtwo"+str(i)) for i in range(24)]

u_dis1 = [m.continuous_var(lb=0, ub=1,name="u_disone"+str(i)) for i in range(24)]
u_dis2 = [m.continuous_var(lb=0, ub=1, name="u_distwo"+str(i)) for i in range(24)]

for t in range(24):
       m.add_constraint(PV[t]+P_ESS1_Dis[t] + P_ESS2_Dis[t] == Load[t]+P_ESS1_Ch[t]+P_ESS2_Ch[t])

for t in range(24):
       m.add_constraint(P_ESS1_Ch[t] >= u_ch1[t] * ESS1_Min)

for t in range(24):
       m.add_constraint(P_ESS2_Ch[t] >= u_ch2[t] * ESS2_Min)

for t in range(24):
       m.add_constraint(P_ESS1_Ch[t] <= u_ch1[t] * ESS1_Max)

for t in range(24):
       m.add_constraint(P_ESS2_Ch[t] <= u_ch2[t] * ESS2_Max)

for t in range(24):
       m.add_constraint(P_ESS1_Dis[t] >= u_dis1[t]*ESS1_Min)

for t in range(24):
       m.add_constraint(P_ESS2_Dis[t] >= u_dis2[t]*ESS2_Min)

for t in range(24):
       m.add_constraint(P_ESS1_Dis[t] <= u_dis1[t]*ESS1_Max)

for t in range(24):
       m.add_constraint(P_ESS2_Dis[t] <= u_dis2[t]*ESS2_Max)

for t in range(24):
       m.add_constraint(u_ch1[t] + u_dis1[t] == 1)

for t in range(24):
       m.add_constraint(u_ch2[t] + u_dis2[t] == 1)


m.add_constraint(SOC1_FMin <= SOC1[23])
m.add_constraint(SOC2_FMin <= SOC2[23])

m.add_constraint(SOC1_FMax >= SOC1[23])
m.add_constraint(SOC2_FMax >= SOC2[23])

for t in range(24):
       m.add_constraint(SOC1_Min <= SOC1[t])

for t in range(24):
       m.add_constraint(SOC2_Min <= SOC2[t])

for t in range(24):
       m.add_constraint(SOC1_Max >= SOC1[t])

for t in range(24):
       m.add_constraint(SOC2_Max >= SOC2[t])



P_Mar = m.sum([(SMP[t]*PV[t])+(P_ESS1_Dis[t] * SMP[t]) + (P_ESS2_Dis[t]*SMP[t]) - (P_ESS1_Ch[t] * SMP[t])- (SMP[t]*P_ESS2_Ch[t]) for t in range(24)])


P_ESS1 = m.sum([P_ESS1_Ch[t]+P_ESS1_Dis[t] for t in range(24)])
P_ESS2 = m.sum([P_ESS2_Ch[t] + P_ESS2_Dis[t] for t in range(24)])

WC_total = P_ESS1*ESS1_Wc + P_ESS2*ESS2_Wc
Revenue = P_Mar - WC_total
m.maximize(Revenue)

m.print_information()
m.solve(log_output=True)

m.print_solution()