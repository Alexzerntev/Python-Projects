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
car0_throughput_phase1 = 'exp1_car0_throughput_phase1_result'
clinet_throughput_phase1 = 'exp1_clinet_throughput_phase1_result'

# latency vars
car0_latency_phase1 = 'exp1_car0_latency_phase1_result'
car3_latency_phase1 = 'exp1_car3_latency_phase1_result'

# iperf mesurments
car0_car3_phase1 = 'exp1_car0_car3_phase1_result'
car3_client_phase1 = 'exp1_car3_client_phase1_result'


# phase 2 #################################################

# throughput vars
car0_throughput_phase2 = 'exp1_car0_throughput_phase2_result'
client_throughput_phase2 = 'exp1_client_throughput_phase2_result'

# latency vars
car0_latency_phase2 = 'exp1_car0_latency_phase2_result'

# iperf mesurment
car0_client_phase2 = 'exp1_car0_client_phase2_result'


# phase 3 #################################################

# throughput vars
car0_throughput_phase3 = 'exp1_car0_throughput_phase3_result'
client_throughput_phase3 = 'exp1_client_throughput_phase3_result'

# latency vars
car0_latency_phase3 = 'exp1_car0_latency_phase3_result'

# iperf mesurment
car0_client_phase3 = 'exp1_car0_client_phase3_result'


def apply_experiment(car, client, switch):
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

    # rule: match (switch): in_port 1 action: output: 4 flows
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')

    # adding route entries to route table

    # car 0 sees client via v2i
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')

    # client sees car 0 via car 3 v2v
    client.cmd('ip route add 200.0.10.100 via 200.0.10.150')

    # Sipmple ping to mesure latency
    car[0].cmd('ping 192.168.1.7  -c 20 >> %s &' % car0_latency_phase1)
    car[3].cmd('ping 200.0.10.2  -c 20 >> %s &' % car3_latency_phase1)

    # car0 (client) to car3 (server) mesurment
    car[3].cmd('iperf -s -u -i 1 >> %s &' % car0_car3_phase1)
    car[0].cmd('iperf -c 192.168.1.7 -u -i 1 -t 20')

    # car3 (client) to client (server) mesurment
    client.cmd('iperf -s -u -i 1 >> %s &' % car3_client_phase1)
    car[3].cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # mesuring througput which is file_size/time
    # as is of vanet.py of paper author
    timeout = time.time() + task_time
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"bytes\" >> %s' %
                       car0_throughput_phase1)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' %
                       clinet_throughput_phase1)
            i += 0.5

    print "Moving nodes"
    car[0].moveNodeTo('150,100,0')
    car[1].moveNodeTo('120,100,0')
    car[2].moveNodeTo('90,100,0')
    car[3].moveNodeTo('70,100,0')

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

    # rule: match (switch): in_port 2 action: output: 4 flows
    # rule: match (switch): in_port 3 action: output: 4 flows
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2,3')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')

    # removing previusly added rules
    car[0].cmd('ip route del 200.0.10.2 via 200.0.10.50')
    client.cmd('ip route del 200.0.10.100 via 200.0.10.150')

    # Sipmple ping to mesure latency
    car[0].cmd('ping 200.0.10.2 -c 20 >> %s &' % car0_latency_phase2)

    # car0-client
    client.cmd('iperf -s -u -i 1 >> %s &' % car0_client_phase2)
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # mesuring througput which is file_size/time
    # as is of vanet.py of paper author
    timeout = time.time() + task_time
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"bytes\" >> %s' %
                       car0_throughput_phase2)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' %
                       client_throughput_phase2)
            i += 0.5

    print "Moving nodes"
    car[0].moveNodeTo('190,100,0')
    car[1].moveNodeTo('150,100,0')
    car[2].moveNodeTo('120,100,0')
    car[3].moveNodeTo('90,100,0')

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

    # rule: match (switch): in_port 2 action: output: 4 flows
    os.system('ovs-ofctl mod-flows switch in_port=1,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=3,actions=drop')
    os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
    os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')

    # Sipmple ping to mesure latency
    car[0].cmd('ping 200.0.10.2 -c 20 >> %s &' % car0_latency_phase3)

    client.cmd('iperf -s -u -i 1 >> %s &' % car0_client_phase3)
    car[0].cmd('iperf -c 200.0.10.2 -u -i 1 -t 20')

    # mesuring througput which is file_size/time
    # as is of vanet.py of paper author
    timeout = time.time() + task_time
    currentTime = time.time()
    i = 0
    while True:
        if time.time() > timeout:
            break
        if time.time() - currentTime >= i:
            car[0].cmd('ifconfig bond0 | grep \"bytes\" >> %s' %
                       car0_throughput_phase3)
            client.cmd('ifconfig client-eth0 | grep \"bytes\" >> %s' %
                       client_throughput_phase3)
            i += 0.5


def topology():
    "Create a network."
    net = Mininet(controller=Controller, link=TCLink,
                  switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
    global gnet
    gnet = net

    print "*** Creating nodes"
    car = []
    for x in range(0, 4):
        car.append(x)
    for x in range(0, 4):
        car[x] = net.addCar('car%s' % (x), wlans=2, ip='10.0.0.%s/8' % (x + 1),
                            mac='00:00:00:00:00:0%s' % x, mode='b')

    eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000',
                                 mode='ac', channel='1', position='80,75,0', range=60)
    eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000',
                                 mode='ac', channel='6', position='180,75,0', range=70)
    rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000',
                              mode='g', channel='11', position='140,120,0', range=40)
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

    i = 1
    j = 2
    for c in car:
        c.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (c, i))
        c.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (c, i))
        c.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

    i = 1
    j = 2
    for v in net.vehiclesSTA:
        v.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (v, j))
        v.cmd('ifconfig %s-mp0 10.0.0.%s/24 up' % (v, i))
        v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for v1 in net.vehiclesSTA:
        i = 1
        j = 1
        for v2 in net.vehiclesSTA:
            if v1 != v2:
                v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    client.cmd('ifconfig client-eth0 200.0.10.2')
    net.vehiclesSTA[0].cmd('ifconfig car0STA-eth0 200.0.10.50')

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

    car[3].cmd('ifconfig car3-wlan0 200.0.10.150')

    client.cmd('ip route add 192.168.1.8 via 200.0.10.150')
    client.cmd('ip route add 10.0.0.1 via 200.0.10.150')

    net.vehiclesSTA[3].cmd('ip route add 200.0.10.2 via 192.168.1.7')
    net.vehiclesSTA[3].cmd('ip route add 200.0.10.100 via 10.0.0.1')
    net.vehiclesSTA[0].cmd('ip route add 200.0.10.2 via 10.0.0.4')

    car[0].cmd('ip route add 10.0.0.4 via 200.0.10.50')
    car[0].cmd('ip route add 192.168.1.7 via 200.0.10.50')
    car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
    car[3].cmd('ip route add 200.0.10.100 via 192.168.1.8')

    """plot graph"""
    net.plotGraph(max_x=250, max_y=250)

    net.startGraph()

    # Uncomment and modify the two commands below to stream video using VLC
    #car[0].cmdPrint(
    #    "vlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
    #client.cmdPrint("vlc rtp://@200.0.10.2:5004 &")

    car[0].moveNodeTo('95,100,0')
    car[1].moveNodeTo('80,100,0')
    car[2].moveNodeTo('65,100,0')
    car[3].moveNodeTo('50,100,0')

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
