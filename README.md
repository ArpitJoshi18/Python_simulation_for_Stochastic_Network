# Python_simulation_for_Stochastic_Network
  The purpose of this project is to better understand queuing models and scheduling dynamics in stochastic networks using python. This project also gives out information about simulation of wireless network in python script. This script was used in the project to plot queue lengths at different nodes of stochastic networks. 

# Stochastic_network.py 

  Purpose of developing this python script is to better understand queuing models and scheduling dynamics in stochastic networks. This project also gives out information about simulation of wireless network in python script. This script was used to plot queue lengths at different nodes of stochastic networks. 
  Max-weight algorithm along with backpressure routing were implied for the routing aspects of the network. These techniques are developed in a way to help gain best quality of service using this network. This is because of the fact that wireless connections cannot simultaneously contact the server at the same time. In wired connection, user is directly connected with server and because of that, user does not face any traffic issues. Although in case of wireless networks, every user is connected to server using 802.11 links which can be activated by any user. To avoid collision and to provide better QoS to the users, such algorithms are used to equally time-share the server. This networks are known as stochastic network. 
  Stochastic networks are the networks which vary with time. For this project, one of the stochastic network was developed over python. 
Stochastic network simulated in the python script can be found here : https://github.com/ArpitJoshi18/Python_simulation_for_Stochastic_Network/blob/master/topology.JPG
	
	
  As seen in the topology of a network, user-1 : cell-tower & user 2- cell-tower link can be activated in even time slot (any one of the link). Similarly Cell-tower-Nfx server & cell-tower-FBI server link can be chose for the connection. 
  
# Max-weight algorithm & Back-pressure algorithm 
  Max-weight & backpressure algorithm helps determining what link should be activated first and which goes next. It is done by several techniques. Max-weight checks the maximum weight/queue at any node and gives out results accordingly. Backpressure algorithm checks the difference between two nodes (link) to determine which link should be activated. Python code executed in this project executes these algorithm on the stochastic network. 
	
    
  More details on max-weight can be found here : 
  
  

