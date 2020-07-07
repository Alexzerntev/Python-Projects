# !/usr/bin/python

"""
Task 1: Implementation of the experiment described in the paper with title: 
"From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks"
http://ieeexplore.ieee.org/document/7859348/ 
"""

import os
import time
import matplotlib.pyplot as plt
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI

import sys
gnet = None

# Implement the graphic function in order to demonstrate the network measurements
# Hint: You can save the measurement in an output file and then import it here


def graphic():
    pass


# output data files

# phase 1 #################################################

# throughput vars
clinet_throughput_phase1 = 'exp2_clinet_throughput_phase1_result'
car_throughput_phase1 = 'exp2_car_throughput_phase1_result'

# latency vars
car_latency_phase1 = 'exp2_car_latency_phase1_result'

# iperf mesurments
car_client_phase1 = 'exp2_car_client_phase1_result'


# phase 2 #################################################

# throughput vars
clinet_throughput_phase2 = 'exp2_clinet_throughput_phase2_result'
car_throughput_phase2 = 'exp2_car_throughput_phase2_result'

# latency vars
car_latency_phase2 = 'exp2_car_latency_phase2_result'

# iperf mesurments
car_client_phase2 = 'exp2_car_client_phase2_result'

# phase 3 #################################################

# throughput vars
clinet_throughput_phase3 = 'exp2_clinet_throughput_phase3_result'
car_throughput_phase3 = 'exp2_car_throughput_phase3_result'

# latency vars
car_latency_phase3 = 'exp2_car_latency_phase3_result'

# iperf mesurments
car_client_phase3 = 'exp2_car_client_phase3_result'


def apply_experiment(cars, client, switch):
    car = cars[0]
    task_time = 20

    # time.sleep(2)
    print "Applying first phase"

    ################################################################################
    #   1) Add the flow rules below and the necessary routing commands
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #   Hint 2: For the routing commands check the configuration
    #           at the beginning of the experiment.
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #               ***************** Insert code below *********************
    #################################################################################

    # first rule car sending via eNodeB1 and RSU1
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1,3')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')

    # car sees client via v2i
    car.cmd('ip route add 200.0.10.2 via 200.0.10.100')

    # Sipmple ping to mesure latency
    car.cmd('ping 200.0.10.2 -c 20 >> %s &' % car_latency_phase1)

    # car3 (client) to client (server) mesurment
    client.cmd('iperf -s -u -i 1 >> %s &' % car_client_phase1)
    car.cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # mesuring througput which is file_size/time
    # as is of vanet.py of paper author
    timeout = time.time() + task_time
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            car.cmd('ifconfig bond0 | grep \"bytes\" >> %s' %
                    car_throughput_phase1)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' %
                       clinet_throughput_phase1)
            i += 0.5

    print "Moving nodes"
    car.moveNodeTo('150,100,0')

    # time.sleep(2)
    print "Applying second phase"
    ################################################################################
    #   1) Add the flow rules below and the necessary routing commands
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #   Hint 2: For the routing commands check the configuration
    #           you have added before.
    #           Remember that now the car connects to RSU1 and eNodeB2
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #           ***************** Insert code below *********************
    #################################################################################

    # second rule car sending via RSU1 and eNodeB2
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2,3')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')

    # Sipmple ping to mesure latency
    car.cmd('ping 200.0.10.2 -c 20 >> %s &' % car_latency_phase2)

    # car3 (client) to client (server) mesurment
    client.cmd('iperf -s -u -i 1 >> %s &' % car_client_phase2)
    car.cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # mesuring througput which is file_size/time
    # as is of vanet.py of paper author
    timeout = time.time() + task_time
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            car.cmd('ifconfig bond0 | grep \"bytes\" >> %s' %
                    car_throughput_phase2)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' %
                       clinet_throughput_phase2)
            i += 0.5

    print "Moving nodes"
    car.moveNodeTo('195,100,0')

    # time.sleep(2)
    print "Applying third phase"

    ################################################################################
    #   1) Add the flow rules below and routing commands if needed
    #
    #   Hint 1: For the OpenFlow rules you can either delete and add rules
    #           or modify rules (using mod-flows command)
    #   Example: os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:2')
    #
    #
    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
    #
    #           ***************** Insert code below *********************
    #################################################################################

    # second rule car sending via only eNodeB2
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')

    # Sipmple ping to mesure latency
    car.cmd('ping 200.0.10.2  -c 20 >> %s &' % car_latency_phase3)

    # car3 (client) to client (server) mesurment
    client.cmd('iperf -s -u -i 1 >> %s &' % car_client_phase3)
    car.cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # mesuring througput which is file_size/time
    # as is of vanet.py of paper author
    timeout = time.time() + task_time
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            car.cmd('ifconfig bond0 | grep \"bytes\" >> %s' %
                    car_throughput_phase3)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' %
                       clinet_throughput_phase3)
            i += 0.5


def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink,
                  switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car = []
    car.append(0)
    car[0] = net.addCar('car0', wlans=2, ip='10.0.0.1/8',
                        mac='00:00:00:00:00:00', mode='b')

    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000',
                                 mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000',
                                 mode='ac', channel='6', position='180,75,0', range=70)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000',
                              mode='g', channel='11', position='140,120,0', range=52)
    c1 = net.addController('c1', controller=Controller)
    client = net.addHost('client')
    switch = net.addSwitch('switch', dpid='4000000000000000')

    net.plotNode(client, position='125,230,0')
    net.plotNode(switch, position='125,200,0')

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Creating links"
    net.addLink(eNodeB1, switch)
    net.addLink(eNodeB2, switch)
    net.addLink(rsu1, switch)
    net.addLink(switch, client)

    print "*** Starting network"
    net.build()
    c1.start()
    eNodeB1.start([c1])
    eNodeB2.start([c1])
    rsu1.start([c1])
    switch.start([c1])

    for sw in net.vehicles:
        sw.start([c1])

    client.cmd('ifconfig client-eth0 200.0.10.2')

    # Broadcast policy: transmits everything on all slave interfaces. This mode provides fault tolerance.
    car[0].cmd('modprobe bonding mode=3')
    # Network device configuration, bonding car phisical architecture into one interface
    car[0].cmd('ip link add bond0 type bond')
    car[0].cmd('ip link set bond0 address 02:01:02:03:04:08')
    car[0].cmd('ip link set car0-eth0 down')
    car[0].cmd('ip link set car0-eth0 address 00:00:00:00:00:11')
    car[0].cmd('ip link set car0-eth0 master bond0')
    car[0].cmd('ip link set car0-wlan0 down')
    car[0].cmd('ip link set car0-wlan0 address 00:00:00:00:00:15')
    car[0].cmd('ip link set car0-wlan0 master bond0')
    car[0].cmd('ip link set car0-wlan1 down')
    car[0].cmd('ip link set car0-wlan1 address 00:00:00:00:00:13')
    car[0].cmd('ip link set car0-wlan1 master bond0')
    car[0].cmd('ip addr add 200.0.10.100/24 dev bond0')
    car[0].cmd('ip link set bond0 up')

    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()

    # Uncomment and modify the two commands below to stream video using VLC
    # car[0].cmdPrint(
    #    "vlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
    #client.cmdPrint("vlc rtp://@200.0.10.2:5004 &")

    car[0].moveNodeTo('95,100,0')

    os.system('ovs-ofctl del-flows switch')

    time.sleep(3)

    apply_experiment(car, client, switch)

    # Uncomment the line below to generate the graph that you implemented
    # graphic()

    # kills all the xterms that have been opened
    os.system('pkill xterm')

    print "*** Running CLI"
    CLI(net)

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    try:
        topology()
    except:
        type = sys.exc_info()[0]
        error = sys.exc_info()[1]
        traceback = sys.exc_info()[2]
        print ("Type: %s" % type)
        print ("Error: %s" % error)
        print ("Traceback: %s" % traceback)
        if gnet != None:
            gnet.stop()
        else:
            print "No network was created..."
