import matplotlib.pyplot as plt
import numpy as np

#The following convention is used: node 0 = user 1, node 1 = user 2, node 2 = cell tower,
#node 3 = Netflix server, node 4 = FBI server.

t_nodes = 5 #number of transmitting nodes
r_nodes = 5 #number of receiving nodes
time_slots = 1000000 #length of simulation

#Queue Lengths
q = np.zeros((t_nodes, r_nodes, time_slots), dtype=int)
empirical_average_q = np.zeros((t_nodes, r_nodes, time_slots))

#Average Arrival Rate
netflix_arrivals_node0 = 0.1
FBI_arrivals_node0 = 0.38
netflix_arrivals_node1 = 0.1
FBI_arrivals_node1 = 0.38

#Feasible Transmission Schedules
M = np.zeros((t_nodes,r_nodes,time_slots), dtype=int)

M[:,:,0] = np.array([[0,0,2,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
M[:,:,1] = np.array([[0,0,0,0,0],[0,0,2,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
M[:,:,2] = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,2,0],[0,0,0,0,0],[0,0,0,0,0]])
M[:,:,3] = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,2],[0,0,0,0,0],[0,0,0,0,0]])

maxweightM = np.zeros((4,time_slots), dtype=int)

s = np.zeros((t_nodes, r_nodes, time_slots), dtype=int)

c02 = np.zeros(time_slots)
c12 = np.zeros(time_slots)
c23 = np.zeros(time_slots)
c24 = np.zeros(time_slots)

for k in range(time_slots):

    #Find the weights
    if k%2 == 0: #even timeslots
        c02[k] = max(q[0, 3, k] - q[2, 3, k], q[0, 4, k] - q[2, 4, k], 0) #find max queue differential on link 02
        c12[k] = max(q[1, 3, k] - q[2, 3, k], q[1, 4, k] - q[2, 4, k], 0) #find max queue differential on link 12

        for l in range(2):
            maxweightM[l, k] = c02[k] * M[0, 2, l] + c12[k] * M[1, 2, l]
    else: #odd time slots
        c23[k] = q[2, 3, k] - q[3, 3, k] #find weight on link 23
        c24[k] = q[2, 4, k] - q[4, 4, k] #find wieght on link 24

        for l in range(2,4):
            maxweightM[l, k] = c23[k] * M[2, 3, l] + c24[k] * M[2, 4, l]

    #Use the maxweight algorithm to find feasible transmission schedules
    s[:, :, k] = M[:, :, np.argmax(maxweightM[:, k])] #find max-weight feasible transmission schedule

    #update the queues
    if k < time_slots-1:

        a03 = np.random.binomial(1, netflix_arrivals_node0) #Netflix traffic at node 0
        a04 = np.random.binomial(1, FBI_arrivals_node0) #FBI traffic at node 0
        a13 = np.random.binomial(1, netflix_arrivals_node1) #Netflix traffic at node 1
        a14 = np.random.binomial(1, FBI_arrivals_node1) #FBI traffic at node 1

        q[0, 3, k + 1] += a03 #Netflix traffic arrving at node 0
        q[0, 4, k + 1] += a04 #FBI traffic arrving at node 0
        q[1, 3, k + 1] += a13 #Netflix traffic arriving at node 1
        q[1, 4, k + 1] += a14 #FBI traffic arrving at node 1

        if k%2==0: #even time slots

            if q[0, 3, k] - q[2, 3, k] > q[0, 4, k] - q[2, 4, k]: #Netflix traffic has max queue differential on link 02
                q[0, 3, k + 1] += max(q[0, 3, k] - s[0, 2, k], 0) #Netflix traffic leaving node 0
                q[0, 4, k + 1] += q[0, 4, k] #FBI traffic stays at node 0
                q[2, 3, k + 1] += min(s[0, 2, k], q[0, 3, k]) #Netflix traffic arriving at cell tower from node 0
            else:
                q[0, 3, k + 1] += q[0, 3, k] #Netflix traffic stays at node 0
                q[0, 4, k + 1] += max(q[0, 4, k] - s[0, 2, k], 0) #FBI traffic leaving node 0
                q[2, 4, k + 1] += min(s[0, 2, k], q[0, 4, k]) #FBI traffic arriving at cell tower from node 0

            if q[1, 3, k]-q[2, 3, k] > q[1, 4, k]-q[2, 4, k]: #Netflix traffic has max queue differential on link 12
                q[1, 3, k + 1] += max(q[1, 3, k] - s[1, 2, k], 0) #Netflix traffic leaving node 1
                q[1, 4, k + 1] += q[1, 4, k] #FBI traffic stays at node 1
                q[2, 3, k + 1] += min(s[1, 2, k], q[1, 3, k]) #Netflix traffic arriving at cell tower from node 1
            else:
                q[1, 4, k + 1] = max(q[1, 4, k] - s[1, 2, k], 0) #FBI traffic leaving node 1
                q[1, 3, k + 1] += q[1, 3, k] #Netflix traffic stays at node 1
                q[2, 4, k + 1] += min(s[1, 2, k], q[1, 4, k]) #FBI traffic arriving at cell tower from node 1
        else: #odd timeslots

            q[0, 3, k + 1] += q[0, 3, k]
            q[0, 4, k + 1] += q[0, 4, k]
            q[1, 3, k + 1] += q[1, 3, k]
            q[1, 4, k + 1] += q[1, 4, k]

            q[2, 3, k + 1] = max(q[2, 3, k] - s[2, 3, k], 0)  # Netflix traffic leaving cell tower
            q[2, 4, k + 1] = max(q[2, 4, k] - s[2, 4, k], 0)  # FBI traffic leaving cell tower

for i in range(time_slots):
    if i < time_slots - 1:
        empirical_average_q[:,:,i + 1] = ((i + 1) * empirical_average_q[:,:,i] + q[:,:,i + 1]) / (i + 2)


t = np.arange(0,time_slots,dtype=int)
a = plt.scatter(t,empirical_average_q[0,3,:], color = 'b') #netflix traffic at user 1
b = plt.scatter(t,empirical_average_q[1,4,:], color = 'c') #FBI traffic at user 1
c = plt.scatter(t,empirical_average_q[1,3,:], color = 'y') #netflix traffic at user 2
d = plt.scatter(t,empirical_average_q[1,4,:], color = 'g') #FBI traffic at userr 2
e = plt.scatter(t,empirical_average_q[2,3,:], color = 'm') #netflix traffic at cell tower
f = plt.scatter(t,empirical_average_q[2,4,:], color = 'r') #FBI traffic at cell tower

plt.legend((a, b, c, d, e, f),
           ('U1-Nfx', 'U1-FBI', 'U2-Nfx', 'U2-FBI', 'CT-Nfx', 'CT-FBI'),
           scatterpoints=1,
           loc='lower left',
           ncol=3,
           fontsize=8)



plt.show()
