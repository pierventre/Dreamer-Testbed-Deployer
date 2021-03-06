#!/usr/bin/python

##############################################################################################
# Copyright (C) 2014 Pier Luigi Ventre - (Consortium GARR and University of Rome "Tor Vergata")
# Copyright (C) 2014 Giuseppe Siracusano, Stefano Salsano - (CNIT and University of Rome "Tor Vergata")
# www.garr.it - www.uniroma2.it/netgroup - www.cnit.it
#
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Nodes Classes.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

import re
from testbed_intf import *
from testbed_deployer_utils import EndIP
from testbed_deployer_utils import OSPFNetwork
from coexistence_mechanisms import CoexFactory
import sys
#import paramiko
from subprocess import Popen


#TODO Integration with psShell
# TODO Integrity Check, before starting the creation of the testbed.sh

class Node:
	
	ipBaseTestbed=[192,168, 1, 0]
	netbitTestbed=16
	netmaskTestbed=[255, 255, 0, 0]
	
	def __init__( self, name, mgt_ip, intfs, user, pwd):
		self.name = name
		self.mgt_ip = mgt_ip
		self.eths = []
		self.nameToEths = {}
		self.user = user
		self.pwd = pwd
		self.chan = None
		self.conn = None
		self.process = None
		#self.connect()
		for eth in intfs:
			eth_intf = EthIntf(eth, self.next_testbedAddress(), self.netbitTestbed, self.netmaskTestbed)
			self.eths.append(eth_intf)
			self.nameToEths[eth] = eth_intf

	def next_testbedAddress(self):
		self.ipBaseTestbed[3] = (self.ipBaseTestbed[3] + 1) % 256
		if self.ipBaseTestbed[3] == 0:
			self.ipBaseTestbed[2] = (self.ipBaseTestbed[2] + 1) % 256
		if self.ipBaseTestbed[2] == 255 and self.ipBaseTestbed[3] == 255:
			print "Ip Testbed Address Sold Out"
			sys.exit(-2)
		return "%s.%s.%s.%s" %(self.ipBaseTestbed[0], self.ipBaseTestbed[1], self.ipBaseTestbed[2], self.ipBaseTestbed[3])

	def connect(self):
		self.conn = paramiko.SSHClient()
		self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.conn.connect(self.mgt_ip,username=self.user, password=self.pwd)
		self.chan = self.conn.invoke_shell()
		self.wait_command('', False) 

	def run(self, command, verbose=True):
		buff = ''
		self.chan.send(command+"\r")
		buff = self.wait_command(command, verbose)
		return buff

	def exe(self, command):
		buff = ''
		stdin, stdout, stderr = self.conn.exec_command(command)
		stdin.close()
		for line in stdout.read().splitlines():
			buff+= line+'\n'
		return buff    
        
	def wait_command(self,command, verbose):
		buff = ''
		i = 0
		s = re.compile('[^#]# ')
		u = re.compile('[$] ')
		if (verbose):
			sys.stdout.flush()    
		while not u.search(buff) and not s.search(buff):
			resp = self.chan.recv(9999)
			if (verbose):
				sys.stdout.write(resp)
			buff += resp
		if (verbose):
			sys.stdout.write("\n")
		return buff

	def close(self):
		self.conn.close()
		if self.process:
			self.process.terminate()

	def xterm(self):
		self.process = Popen(['xterm', '-e','sshpass','-p',self.pwd, 'ssh','-o', 'StrictHostKeyChecking=no', self.user+'@'+self.mgt_ip]) 

	def start(self):
		raise NotImplementedError("Abstract Method")

	def stop(self):
		raise NotImplementedError("Abstract Method")

	def configure(self):
		raise NotImplementedError("Abstract Method")

	def addIntf(self, param):
		raise NotImplementedError("Abstract Method")

	def ethsSerialization(self):
		return "declare -a INTERFACES=(" + " ".join("%s" % eth.name for eth in self.eths) + ")\n"

class L2Switch(Node):

	def __init__( self, name, mgt_ip, intfs, vlan, user, pwd, tunneling):
		Node.__init__(self, name, mgt_ip, intfs, user, pwd)
		self.vlan = vlan
		self.endips = []
		self.nameToEndIps = {}
		self.taps = []
		self.nameToTaps = {}
		self.tunneling = tunneling
		
		self.endIPBase = 1
		self.tapBase = 1
		self.ethIndex = 0
		self.tapPortBase = 1190

	def addIntf(self, param):
		if len(param) != 8:
				print "Error L2sw.addIntf Invalid Parameter"
				sys.exit(-2)
		tap = self.addTap(param)
		return (None, tap, None)

	def addEndIP(self, remoteIP, localIntf):
		name = self.newEndIPName()
		endip = EndIP(name, remoteIP, localIntf)
		self.endips.append(endip)
		self.nameToEndIps[name] = endip
		return endip
		
	def newEndIPName(self):
		ret = self.endIPBase
		self.endIPBase = self.endIPBase + 1
		return "endip%s" % ret

	def newTapName(self):
		ret = self.tapBase
		self.tapBase = self.tapBase + 1
		return "tap%s" % ret
	
	def newTapPort(self):
		self.tapPortBase = self.tapPortBase + 1
		return self.tapPortBase
	
	def addTap(self, param):
		name = self.newTapName()
		remote_ip = param[0]
		local_eth = param[1]
		endip = self.addEndIP(remote_ip, local_eth)
		if self.tunneling == "OpenVPN":
			local_port = param[2]
			remote_port =param[3]
			tap = TapOpenVPNIntf(name, local_port, remote_port, endip.name)
		elif self.tunneling == "VXLAN":
			VNI = param[7]
			tap = TapVXLANIntf(name, VNI, endip.name)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap
	
	def next_eth(self):
		ret = (self.eths[self.ethIndex].name, self.eths[self.ethIndex].ip)
		self.ethIndex = (self.ethIndex + 1) % len(self.eths) 		
		return ret
	
	def tapsSerialization(self):
		return "declare -a TAP=(" + " ".join("%s" % tap.name for tap in self.taps) + ")\n"
	
	def configure(self, params=[]):
		testbed = open('testbed.sh','a')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write("BRIDGENAME=%s\n" % self.name)
		testbed.write(self.ethsSerialization())
		for eth in self.eths:
			testbed.write(eth.serialize())
		testbed.write(self.tapsSerialization())
		for tap in self.taps:
			testbed.write(tap.serialize())
		for endip in self.endips:
			testbed.write(endip.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()

# XXX Static Route could change in future
class Host(Node):

	def __init__( self, name, mgt_ip, intfs, vlan, user, pwd, tunneling):
		Node.__init__(self, name, mgt_ip, intfs, user, pwd)
		self.vlan = vlan
		self.endips = []
		self.nameToEndIps = {}
		self.taps = []
		self.staticroutes = []
		self.nameToTaps = {}
		self.tunneling = tunneling
		self.vis = []
		self.nameToVis = {}
		
		self.endIPBase = 1
		self.tapBase = 1
		self.ethIndex = 0
		self.tapPortBase = 1190
		self.viBase = 1	

	def addIntf(self, param):
		if len(param) != 8:
				print "Error Host.addIntf Invalid Parameter"
				sys.exit(-2)
		default_gw = param[6]
		self.staticroutes.append(default_gw)
		tap = self.addTap(param)
		if self.tunneling == "OpenVPN":
			return (None, tap, None)
		else:
			vi = self.addVi(param)
			return (vi, tap, None)

	def newViName(self):
		ret = self.viBase
		self.viBase = self.viBase + 1
		return "vitap%s" % ret
	
	def addVi(self, param):
		name = self.newViName()
		net = param[4]
		ip = param[5]
		vi = ViIntf(name, ip, net.netbitOSPF)
		self.vis.append(vi)
		self.nameToVis[name] = vi
		return vi

	def addEndIP(self, remoteIP, localIntf):
		name = self.newEndIPName().upper()
		endip = EndIP(name, remoteIP, localIntf)
		self.endips.append(endip)
		self.nameToEndIps[name] = endip
		return endip
		
	def newEndIPName(self):
		ret = self.endIPBase
		self.endIPBase = self.endIPBase + 1
		return "endip%s" % ret

	def newTapName(self):
		ret = self.tapBase
		self.tapBase = self.tapBase + 1
		return "tap%s" % ret
	
	def newTapPort(self):
		self.tapPortBase = self.tapPortBase + 1
		return self.tapPortBase
	
	def addTap(self, param):
		name = self.newTapName()
		remote_ip = param[0]
		local_eth = param[1]
		endip = self.addEndIP(remote_ip, local_eth)
		if self.tunneling == "OpenVPN":
			local_port = param[2]
			remote_port =param[3]
			net = param[4]
			tap_ip = param[5]
			tap = TapOpenVPNHostIntf(name, local_port, remote_port, endip.name, tap_ip, net.netbitOSPF)
		elif self.tunneling == "VXLAN":
			VNI = param[7]
			tap = TapVXLANIntf(name, VNI, endip.name)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap
	
	def next_eth(self):
		ret = (self.eths[self.ethIndex].name, self.eths[self.ethIndex].ip)
		self.ethIndex = (self.ethIndex + 1) % len(self.eths) 		
		return ret
	
	def tapsSerialization(self):
		return "declare -a TAP=(" + " ".join("%s" % tap.name for tap in self.taps) + ")\n"
	
	def visSerialization(self):
		return "declare -a VI=(" + " ".join("%s" % vi.name for vi in self.vis) + ")\n"

	def configure(self, params=[]):
		ipbase = params[0]
		testbed = open('testbed.sh','a')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write(self.ethsSerialization())
		for eth in self.eths:
			testbed.write(eth.serialize())
		testbed.write(self.tapsSerialization())
		for tap in self.taps:
			testbed.write(tap.serialize())
		ip_and_mask = ipbase.split("/")
		if self.tunneling == "VXLAN":
			testbed.write(self.visSerialization())
			for vi in self.vis:
				testbed.write(vi.serialize())
			testbed.write("declare -a STATICROUTE=(%s %s %s %s)\n" %( ip_and_mask[0], ip_and_mask[1], self.staticroutes[0], self.vis[0].name))
		else:
			testbed.write("declare -a STATICROUTE=(%s %s %s %s)\n" %( ip_and_mask[0], ip_and_mask[1], self.staticroutes[0], self.taps[0].name))
		for endip in self.endips:
			testbed.write(endip.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()
	
class Controller(Host):

	def __init__( self, name, mgt_ip, intfs, vlan, port, user, pwd, tunneling):
		Host.__init__(self, name, mgt_ip, intfs, vlan, user, pwd, tunneling)
		self.port = port
		self.ips = []

	def addIP(self, ip):
		if ip not in self.ips:
			self.ips.append(ip)

	def addIntf(self, param):
		ip = param[5]
		self.addIP(ip)
		return Host.addIntf(self, param)

	
class IPHost(Host):
		
	def __init__(self, name, mgt_ip, intfs, vlan, user, pwd, tunneling, loopback):
		Host.__init__(self, name, mgt_ip, intfs, vlan, user, pwd, tunneling)
		self.loopback = LoIntf(ip=loopback)
		self.staticroutes = None
		self.ospfnets = []
		self.nameToNets = {}
		self.ospfNetBase = 1
		loopbacknet = OSPFNetwork("fake", "%s/32" % self.loopback.ip )
		self.addOSPFNet(loopbacknet)

	def addEndIP(self, remoteIP, localIntf):
		name = self.newEndIPName()
		endip = EndIP(name, remoteIP, localIntf)
		self.endips.append(endip)
		self.nameToEndIps[name] = endip
		return endip

	def newOSPFNetName(self):
		ret = self.ospfNetBase
		self.ospfNetBase = self.ospfNetBase + 1
		return "NET%s" % ret		
		
	def addOSPFNet(self, net):
		found = False
		for ospfnet in self.ospfnets:
			if net.net == ospfnet.net:
				found = True
				break
		if found == False:
			name = self.newOSPFNetName()
			net.name = name
			self.ospfnets.append(net)
			self.nameToNets[name] = net
		else:
			net = ospfnet 
		return net

	def ospfnetsSerialization(self):
		return "declare -a OSPFNET=(" + " ".join("%s" % net.name for net in self.ospfnets) + ")\n"

class Router(IPHost):

	def __init__( self, name, mgt_ip, intfs, vlan, user, pwd, tunneling, loopback):
		IPHost.__init__(self, name, mgt_ip, intfs, vlan, user, pwd, tunneling, loopback)
	
	def addIntf(self, param):
		if len(param) != 8:
			print "Error Router.addIntf Invalid Parameter"
			sys.exit(-2)
		ospf_net = param[4]
		ospf_net = self.addOSPFNet(ospf_net)
		param[4] = ospf_net
		tap = self.addTap(param)
		if self.tunneling == "OpenVPN":
			return (None, tap, ospf_net)
		else:
			vi = self.addVi(param)
			return (vi, tap, None)
	
	def addVi(self, param):
		name = self.newViName()
		net = param[4]
		ip = param[5]
		vi = ViRouterIntf(name, ip, net.netbitOSPF, net.hello_int, net.cost)
		self.vis.append(vi)
		self.nameToVis[name] = vi
		return vi

	def addTap(self, param):
		name = self.newTapName()
		remote_ip = param[0]
		local_eth = param[1]
		endip = self.addEndIP(remote_ip, local_eth)
		if self.tunneling == "OpenVPN":
			local_port = param[2]
			remote_port =param[3]
			net = param[4]
			tap_ip = param[5]
			tap = TapOpenVPNRouterIntf(name, local_port, remote_port, endip.name, tap_ip, net.netbitOSPF, net.hello_int, net.cost)
		elif self.tunneling == "VXLAN":
			VNI = param[7]
			tap = TapVXLANIntf(name, VNI, endip.name)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap

	def configure(self, params=[]):
		ipbase = params[0]
		testbed = open('testbed.sh','a')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("ROUTERPWD=dreamer\n")
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write(self.loopback.serialize())
		testbed.write(self.ethsSerialization())
		for eth in self.eths:
			testbed.write(eth.serialize())
		testbed.write(self.tapsSerialization())
		for tap in self.taps:
			testbed.write(tap.serialize())
		for endip in self.endips:
			testbed.write(endip.serialize())
		if self.tunneling == "VXLAN":
			testbed.write(self.visSerialization())
			for vi in self.vis:
				testbed.write(vi.serialize())
		testbed.write(self.ospfnetsSerialization())
		for net in self.ospfnets:
			testbed.write(net.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()

class Oshi(IPHost):

	dpidLen = 16

	def __init__( self, name, mgt_ip, intfs, vlan, user, pwd, tunneling, loopback, OF_V, CR, cluster_id):
		IPHost.__init__(self, name, mgt_ip, intfs, vlan, user, pwd, tunneling, loopback)

		if cluster_id == "default":
			cluster_id = "0"
		cluster_id = int(cluster_id)
		if CR:
			cluster_id = cluster_id + 128	
	
		extrainfo = '%02x000000' % cluster_id

		self.dpid = self.loopbackDpid(self.loopback.ip, extrainfo)
		self.vis = []
		self.nameToVis = {}
		self.ctrls = []
		self.ingressfuncs = []
		self.OF_V = OF_V

		self.vsf_to_port = {}
		self.pwtaps = []
		self.pwtapBase = 1
		self.CR = CR

	def loopbackDpid(self, loopback, extrainfo):
		splitted_loopback = loopback.split('.')
		hexloopback = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, splitted_loopback))
		dpid = "%s%s" %(extrainfo, hexloopback)
		if len(dpid)>16:
			print "Unable To Derive DPID From Loopback and ExtraInfo";
			sys.exit(-1)
		return dpid

	def defaultDpid( self ):
		"Derive dpid from switch name, s1 -> 1"
		try:
			dpid = int( re.findall( r'\d+', self.name )[ 0 ] )
			dpid = hex( dpid )[ 2: ]
			dpid = '0' * ( self.dpidLen - len( dpid ) ) + dpid
			return dpid
		except IndexError:
			raise Exception( 'Unable to derive default datapath ID - '
							 'please either specify a dpid or use a '
							 'canonical switch name such as s23.' )	
	
	def setControllers(self, ips, ports):
		for i in range (0, len(ips)):
			key = ips[i] + " " + str(ports[i])
			if key in self.ctrls:
				continue
			self.ctrls.append(key)
	
	def addTap(self, param):
		if len(param) != 8:
				print "Error OSHI.addTapIP Invalid Parameter"
				sys.exit(-2)
		name = self.newTapName()
		remote_ip = param[0]
		local_eth = param[1]
		net = param[4]
		endip = self.addEndIP(remote_ip, local_eth)
		if self.tunneling == "OpenVPN":
			local_port = param[2]
			remote_port =param[3]
			tap = TapOpenVPNIntf(name, local_port, remote_port, endip.name)
		elif self.tunneling == "VXLAN":
			VNI = param[7]
			tap = TapVXLANIntf(name, VNI, endip.name)
		self.taps.append(tap)
		self.nameToTaps[name] = tap
		return tap

	def addPWTap(self, param):
		if len(param) != 8:
				print "Error OSHI.addTapIP Invalid Parameter"
				sys.exit(-2)
		name = self.newPWTapName()
		remote_ip = param[0]
		local_eth = param[1]
		net = param[4]
		endip = self.addEndIP(remote_ip, local_eth)
		if self.tunneling == "OpenVPN":
			local_port = param[2]
			remote_port =param[3]
			tap = TapOpenVPNIntf(name, local_port, remote_port, endip.name)
		elif self.tunneling == "VXLAN":
			VNI = param[7]
			tap = TapVXLANIntf(name, VNI, endip.name)
		self.pwtaps.append(tap)
		self.nameToTaps[name] = tap
		return tap

	def addIntf(self, param):
		if len(param) != 8:
			print "Error Oshi.addIntf Invalid Parameter"
			sys.exit(-2)
		ospf_net = param[4]
		vi_ip = param[5]
		if ospf_net != None:
			ospf_net = self.addOSPFNet(ospf_net)
			vi = self.addVi(vi_ip, ospf_net.netbitOSPF, ospf_net.hello_int, ospf_net.cost)
		else:
			vi = self.addVi(vi_ip, 32, 60, 1)
		tap = self.addTap(param)
		return (vi, tap, ospf_net)
	
	def newViName(self):
		ret = self.viBase
		self.viBase = self.viBase + 1
		return "vi%s" % ret

	def newPWTapName(self):
		ret = self.pwtapBase
		self.pwtapBase = self.pwtapBase + 1
		return "pwtap%s" % ret
	
	def addVi(self, ip, netbit, hello_int, cost):
		name = self.newViName()
		vi = ViRouterIntf(name, ip, netbit, hello_int, cost)
		self.vis.append(vi)
		self.nameToVis[name] = vi
		return vi 		
	
	def controllersSerialization(self):
		i = 1
		names = []
		serialized_line = ""
		for ctrl in self.ctrls:
			name = "CTRL" + str(i)
			names.append(name)
			serialized_line = serialized_line + ("declare -a %s=(%s)\n" %(name, ctrl))			
			i = i + 1			
		ret = "declare -a CTRL=(" + " ".join(names) + ")\n" + serialized_line
		return ret

	def pwtapsSerialization(self):
		return "declare -a PWTAP=(" + " ".join("%s" % pwtap.name for pwtap in self.pwtaps) + ")\n"

	def vitapsSerialization(self):
		vitaps = []
		for i in range(len(self.vis)+1, (len(self.vis)+21)):		
			vitaps.append("vi%s" % str(i))
		return "declare -a VITAP=(" + " ".join("%s" % vitap for vitap in vitaps) + ")\n"

	def configure(self, params):
		ipbase = params[0]
		testbed = open('testbed.sh','a')
		testbed.write("# %s - start\n" % self.mgt_ip)
		testbed.write("HOST=%s\n" % self.name)
		testbed.write("ROUTERPWD=dreamer\n")
		testbed.write("DPID=%s\n" % self.dpid)
		testbed.write("SLICEVLAN=%s\n" % self.vlan)
		testbed.write("BRIDGENAME=br-dreamer\n")
		testbed.write(self.controllersSerialization())
		testbed.write(self.loopback.serialize())
		testbed.write(self.ethsSerialization())
		for eth in self.eths:
			testbed.write(eth.serialize())
		testbed.write(self.tapsSerialization())
		for tap in self.taps:
			testbed.write(tap.serialize())
		if len(self.pwtaps) > 0:
			testbed.write(self.pwtapsSerialization())
		for pwtap in self.pwtaps:
			testbed.write(pwtap.serialize())
		for endip in self.endips:
			testbed.write(endip.serialize())
		testbed.write(self.visSerialization())
		for vi in self.vis:
			testbed.write(vi.serialize())
		if len(self.ingressfuncs) > 0:
			testbed.write(self.vitapsSerialization())
		testbed.write(self.ospfnetsSerialization())
		for net in self.ospfnets:
			testbed.write(net.serialize())
		testbed.write("# %s - end\n" % self.mgt_ip)
		testbed.close()

	def addIngress(self, ingress):
		self.ingressfuncs.append(ingress)
		return ingress
		
	def generateLMErules(self, coex):
		lmerules = open('lmerules.sh', 'a')
		lmerules.write("# %s - start\n" % self.mgt_ip)

		"""
		temp_vi=[]
		temp_tap=[]
		for vi in self.vis:
			tapname = "tap%s" %(self.strip_number(vi.name))
			TAP = None
			for tap in self.taps:
				if tapname == tap.name:
					TAP = tap
					break
			if TAP != None:
				temp_vi.append(vi)
				temp_tap.append(TAP)

		"""

		coexFactory = CoexFactory()
		coex = coexFactory.getCoex(coex['coex_type'], coex['coex_data'], self.taps, self.vis, "br-dreamer", self.OF_V)
		lmerules.write("# %s - start\n" % coex.type)
		lmerules.write(coex.serializeRules())
		lmerules.write("# %s - end\n" % coex.type)
		for ingress in self.ingressfuncs:
			lmerules.write("# %s - start\n" % ingress.type)
			lmerules.write(ingress.serialize())
			lmerules.write("# %s - end\n" % ingress.type)

		"""
		if self.name == "peo5":
			lmerules.write("# FAKE - start\n")
			i = 0
			z = 0
			while z < (i*1000):
				lmerules.write("ovs-ofctl add-flow %s \"table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s\"\n" %("br-dreamer", 0, 300, (z+100), (z+101)))
				lmerules.write("ovs-ofctl add-flow %s \"table=%s,hard_timeout=0,priority=%s,in_port=%s,action=output:%s\"\n" %("br-dreamer", 0, 300, (z+101), (z+100)))
				z = z + 2
			lmerules.write("# FAKE - end\n")
		"""

		lmerules.write("# %s - end\n" % self.mgt_ip)
		lmerules.close()

	def getPWintf(self, vsfname):

		index = self.vsf_to_port.get(vsfname, None)
		if not index:
			index = 0
			index = index + 1
			self.vsf_to_port[vsfname] = index
		else:
			index = index + 2
			self.vsf_to_port[vsfname] = index
		intf = "r%s-eth%s" %(vsfname, index)
		return intf

	def strip_number(self, vi):
		intf = str(vi)
		intf_pattern = re.search(r'vi\d+$', intf)
		if intf_pattern is None:
			print "ERROR bad name for intf"
			sys.exit(-2)
		return int(intf[2:])
		

class VSF(object):

	def __init__( self, name):
		self.name = name
		self.pws = []		

	def addPW( self, peo_tap, local_vtep, remote_vtep):
		pw = { 'cer_intf':peo_tap.name, 'local_vtep':{'ip':local_vtep.IP, 'mac':local_vtep.MAC}, 'remote_vtep':{'ip':remote_vtep.IP, 'mac':remote_vtep.MAC} }
		self.pws.append(pw)
	
	def serialize( self ):
		return { 'name':self.name, 'pws':self.pws}

		

