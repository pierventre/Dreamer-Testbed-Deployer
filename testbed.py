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
# Testbed Class.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

import sys
from testbed_node import *
from mapping_parser import *
from testbed_deployer_utils import *
from ingress_classification import *
from coexistence_mechanisms import *
import copy
import os

class TestbedFactory(object):

	def __init__(self, verbose):
		self.verbose = verbose

	def getTestbedOSHI(self, type_testbed, type_tunnel):
		if type_testbed == "OFELIA":
			return TestbedOSHIOFELIA(type_tunnel, "10.0.0.0/255.0.0.0", self.verbose)
		elif type_testbed == "GOFF":
			return TestbedOSHIGOFF(type_tunnel, "10.0.0.0/255.0.0.0", self.verbose)
		else:
			print "Testbed %s Not Supported...Exit" %(type_testbed)
			sys.exit(-1)

	def getTestbedRouter(self, type_testbed, type_tunnel):
		if type_testbed == "OFELIA":
			return TestbedRouterOFELIA(type_tunnel, "10.0.0.0/255.0.0.0", self.verbose)
		elif type_testbed == "GOFF":
			return TestbedRouterGOFF(type_tunnel, "10.0.0.0/255.0.0.0", self.verbose)
		else:
			print "Testbed %s Not Supported...Exit" %(type_testbed)
			sys.exit(-1)

class Testbed(object):

	def __init__(self):
		self.user = None
		self.pwd = None
		self.nameToNode = {}
		self.tunneling = None
		self.vniBase = 1

	def getNodeByName(self, key):
		return self.nameToNode[key]

	def newVNI(self):
		ret = self.vniBase
		self.vniBase = self.vniBase + 1
		return ret

class TestbedRouter(Testbed):
	
	def __init__(self):
		Testbed.__init__(self)
		self.routs = []
		self.l2sws = []
		self.euhs = []
		self.ospfnets = []
		self.routerinfo = []
		self.euhsinfo = []
		self.l2swinfo = []
		self.ospfBase = 1
		self.nameToOSPFNet = {}

	def addRouter(self, nodeproperties, name=None):
		if len(self.routerinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Router"
			sys.exit(-2)

		if not name:
			name = self.newRoutName()

		rou = self.routerinfo[0]
		rou.name = name
		self.routerinfo.remove(rou)
		router = Router(rou, self.vlan, self.user, self.pwd, self.tunneling, nodeproperties.loopback)
		self.routs.append(router)
		self.nameToNode[router.name] = router
		return router

	def newRoutName(self):
		index = str(len(self.routs) + 1)
		name = "rou%s" % index
		return name

	def addL2Switch(self, name=None):
		if len(self.l2swsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of L2Sw"
			sys.exit(-2)

		if not name:
			name = self.newL2swName()

		l2sw = self.l2swsinfo[0]
		l2sw.name = name
		self.l2swsinfo.remove(l2sw)
		l2switch = L2Switch(l2sw, self.vlan, self.user, self.pwd, self.tunneling)
		self.l2sws.append(l2switch)
		self.nameToNode[l2switch.name] = l2switch
		return l2switch

	def newL2swName(self):
		index = str(len(self.l2sws) + 1)
		name = "swi%s" % index
		return name

	def addEuh(self, name=None):
		if len(self.euhsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Host"
			sys.exit(-2)

		if not name:
			name = self.newEuhName()

		euh = self.euhsinfo[0]
		euh.name = name
		self.euhsinfo.remove(euh)
		euh = Host(euh, self.vlan, self.user, self.pwd, self.tunneling)
		self.euhs.append(euh)
		self.nameToNode[euh.name] = euh
		return euh

	def newEuhName(self):
		index = str(len(self.euhs) + 1)
		name = "euh%s" % index
		return name

	def addLink(self, lhs, rhs, linkproperty):
		
		lhs = self.getNodeByName(lhs)	
		rhs = self.getNodeByName(rhs)
	

		(lhs_eth, lhs_eth_ip) = lhs.next_eth()
		(rhs_eth, rhs_eth_ip) = rhs.next_eth()
		
		
		lhs_tap_port = lhs.newTapPort()
		rhs_tap_port = rhs.newTapPort()

		ospf_net = self.addOSPFNet(linkproperty.net)
		lhs_ip = linkproperty.ipLHS
		rhs_ip = linkproperty.ipRHS
		lhs_ospf_net = copy.deepcopy(ospf_net)
		rhs_ospf_net = copy.deepcopy(ospf_net)
		vni = self.newVNI()

		(lhs_vi, lhs_tap, lhs_ospf_net) = lhs.addIntf([rhs_eth_ip, lhs_eth, lhs_tap_port, rhs_tap_port, lhs_ospf_net, lhs_ip, rhs_ip, vni])
		(rhs_vi, rhs_tap, rhs_ospf_net) = rhs.addIntf([lhs_eth_ip, rhs_eth, rhs_tap_port, lhs_tap_port, rhs_ospf_net, rhs_ip, lhs_ip, vni])
		
		return [(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)]

	def newOSPFNetName(self):
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return "NET%s" % ret
		
	def addOSPFNet(self, ip):
		found = False
		for ospfnet in self.ospfnets:
			if ip == ospfnet.net:
				found = True
				break
		if found == False:
			name = self.newOSPFNetName()
			net = OSPFNetwork(name, ip)
			self.ospfnets.append(net)
			self.nameToOSPFNet[name] = net
		else:
			net = ospfnet 
		return net

	def configureMGMT(self):
		header =open('headerMGMT.txt','r')
		management = open('management.sh','w')
		lines = header.readlines()
		for line in lines:
			management.write(line)
		management.write("declare -a DSH_GROUPS=(ROUTER EUH L2SW)\n")
		router = "declare -a ROUTER=(" + " ".join("%s" % rout.mgt_ip for rout in self.routs)+ ")\n"
		euh = "declare -a EUH=(" + " ".join("%s" % euh.mgt_ip for euh in self.euhs) + ")\n"
		l2sw = "declare -a L2SW=(" + " ".join("%s" % l2sw.mgt_ip for l2sw in self.l2sws) + ")\n"
		machine = "declare -a NODE_LIST=(" + " ".join("%s" % node.mgt_ip for name, node in self.nameToNode.iteritems()) + ")\n"	
		management.write(router)
		management.write(euh)
		management.write(l2sw)
		management.write(machine)

class TestbedOSHI( Testbed ):

	OF_V = "OpenFlow13"
	
	def __init__(self):
		Testbed.__init__(self)
		self.cr_oshs = []
		self.pe_oshs = []
		self.cers = []
		self.ctrls = []
		#self.l2sws = []
		self.ospfnets = []
		self.coex = {}
		self.peosinfo = []
		self.crosinfo = []
		self.ctrlsinfo = []
		self.cersinfo = []
		#self.l2swsinfo = []
		self.nameToOSPFNet = {}
		self.oshiToControllers = {}
		self.cerToPEO = {}
		self.vllcfgline = []
		self.ospfBase = 1

	def addCrOshi(self, nodeproperties, name=None):
		if len(self.crosinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Core Oshi"
			sys.exit(-2)

		if not name:
			name = self.newCrName()

		cro = self.crosinfo[0]
		cro.name = name
		self.crosinfo.remove(cro)
		oshi = Oshi(cro, self.vlan, self.user, self.pwd, self.tunneling, nodeproperties.loopback, self.OF_V)
		self.cr_oshs.append(oshi)
		self.nameToNode[oshi.name] = oshi
		return oshi

	def newCrName(self):
		index = str(len(self.cr_oshs) + 1)
		name = "cro%s" % index
		return name	

	def addPeOshi(self, nodeproperties, name=None):
		if len(self.peosinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Provider Edge Oshi"
			sys.exit(-2)

		if not name:
			name = self.newPeName()

		peo = self.peosinfo[0]
		peo.name = name
		self.peosinfo.remove(peo)
		oshi = Oshi(peo, self.vlan, self.user, self.pwd, self.tunneling, nodeproperties.loopback, self.OF_V)
		self.pe_oshs.append(oshi)
		self.nameToNode[oshi.name] = oshi
		return oshi

	def newPeName(self):
		index = str(len(self.pe_oshs) + 1)
		name = "peo%s" % index
		return name		
	
	def addController(self, port, name=None):
		if len(self.ctrlsinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Controller"
			sys.exit(-2)

		if not name:
			name = self.newCtrlName()

		ctrl = self.ctrlsinfo[0]
		ctrl.name = name
		self.ctrlsinfo.remove(ctrl)
		ctrl = Controller(ctrl, self.vlan, port, self.user, self.pwd, self.tunneling)
		self.ctrls.append(ctrl)
		self.nameToNode[ctrl.name] = ctrl
		return ctrl

	def newCtrlName(self):
		index = str(len(self.ctrls) + 1)
		name = "ctr%s" % index
		return name

	def addCer(self, name=None):
		if len(self.cersinfo) == 0:
			print "Error The Testbed Provided Is Not Enough Big For The Creation Of Host"
			sys.exit(-2)

		if not name:
			name = self.newCerName()

		cer = self.cersinfo[0]
		cer.name = name
		self.cersinfo.remove(cer)
		cer = Host(cer, self.vlan, self.user, self.pwd, self.tunneling)
		self.cers.append(cer)
		self.nameToNode[cer.name] = cer
		return cer

	def newCerName(self):
		index = str(len(self.cers) + 1)
		name = "cer%s" % index
		return name

	#def addL2Switch(self, name):
	#	if len(self.l2swsinfo) == 0:
	#		print "Error The Testbed Provided Is Not Enough Big For The Creation Of L2Sw"
	#		sys.exit(-2)
	#	l2sw = self.l2swsinfo[0]
	#	l2sw.name = name
	#	self.l2swsinfo.remove(l2sw)
	#	l2switch = L2Switch(l2sw, self.vlan, self.user, self.pwd, self.tunneling)
	#	self.l2sws.append(l2switch)
	#	self.nameToNode[l2switch.name] = l2switch
	#	return l2switch
		
	# Allocation OF OVS equipment, We Use A RR Behavior;
	#def roundrobinallocation(self):
	#	ctrl_to_allocate = []
	#	for ctrl in self.ctrls:
	#		if len(ctrl.ips) > 0:
	#			ctrl_to_allocate.append(ctrl)
	#	if len(ctrl_to_allocate) == 1:
	#		for osh in self.oshs:
	#			osh.setControllers([ctrl_to_allocate[0].ips[0]], [ctrl_to_allocate[0].port])
	#		for aos in self.aoss:
	#			aos.setControllers([ctrl_to_allocate[0].ips[0]], [ctrl_to_allocate[0].port])
	#
	#	elif len(ctrl_to_allocate) >= 2:
	#		i = 0
	#		j = 0
	#		for osh in self.oshs:
	#			i = i % len(ctrl_to_allocate)
	#			j = (i + 1) % len(ctrl_to_allocate)
	#			ip_1 = ctrl_to_allocate[i].ips[0]
	#			ip_2 = ctrl_to_allocate[j].ips[0]
	#			p_1 = ctrl_to_allocate[i].port
	#			p_2 = ctrl_to_allocate[j].port
	#			osh.setControllers([ip_1, ip_2], [p_1, p_2])
	#			i = i + 1
	#		i = 0
	#		j = 0
	#		for aos in self.aoss:
	#			i = i % len(ctrl_to_allocate)
	#			j = (i + 1) % len(ctrl_to_allocate)
	#			ip_1 = ctrl_to_allocate[i].ips[0]
	#			ip_2 = ctrl_to_allocate[j].ips[0]
	#			p_1 = ctrl_to_allocate[i].port
	#			p_2 = ctrl_to_allocate[j].port
	#			aos.setControllers([ip_1, ip_2], [p_1, p_2])
	#			i = i + 1
	#	else:
	#		print "Warning No Controller Added - Information Will Not Be Generated"

	def completeAllocation(self):
		ips = []
		ports = []
		for ctrl in self.ctrls:
			if len(ctrl.ips) > 0:
				ips.append(ctrl.ips[0])
				ports.append(ctrl.port)
		if len(ips) > 0:
			for cro in self.cr_oshs:
				cro.setControllers(ips, ports)
			for peo in self.pe_oshs:
				peo.setControllers(ips, ports)
		else:
			print "Warning No Controller Added - Information Will Not Be Generated"
		
	def addLink(self, lhs, rhs, linkproperties):
		
		lhs = self.getNodeByName(lhs)	
		rhs = self.getNodeByName(rhs)
	

		(lhs_eth, lhs_eth_ip) = lhs.next_eth()
		(rhs_eth, rhs_eth_ip) = rhs.next_eth()
		
		
		lhs_tap_port = lhs.newTapPort()
		rhs_tap_port = rhs.newTapPort()
		
		ospf_net = self.addOSPFNet(linkproperties.net)
		lhs_ip = linkproperties.ipLHS
		rhs_ip = linkproperties.ipRHS
		lhs_ospf_net = copy.deepcopy(ospf_net)
		rhs_ospf_net = copy.deepcopy(ospf_net)
		vni = self.newVNI()

		(lhs_vi, lhs_tap, lhs_ospf_net) = lhs.addIntf([rhs_eth_ip, lhs_eth, lhs_tap_port, rhs_tap_port, lhs_ospf_net, lhs_ip, rhs_ip, vni])
		(rhs_vi, rhs_tap, rhs_ospf_net) = rhs.addIntf([lhs_eth_ip, rhs_eth, rhs_tap_port, lhs_tap_port, rhs_ospf_net, rhs_ip, lhs_ip, vni])

		if linkproperties.ingr.type != None:
			factory = IngressFactory()
			if isinstance(lhs, Oshi):
				PEO = lhs.name
				CER = rhs.name
				ingr = factory.getIngr(self.coex['coex_type'], self.coex['coex_data'], linkproperties.ingr.type, linkproperties.ingr.data, 
				lhs_tap, lhs_vi, 'br-dreamer', self.OF_V)
			elif isinstance(rhs, Oshi):
				PEO = rhs.name
				CER = lhs.name
				ingr = factory.getIngr(self.coex['coex_type'], self.coex['coex_data'], linkproperties.ingr.type, linkproperties.ingr.data, 
				rhs_tap, rhs_vi, 'br-dreamer', self.OF_V)
			self.cerToPEO[CER] = PEO
			self.addIngressClassification(CER, PEO, ingr)

		return [(lhs_vi, lhs_tap, lhs_ospf_net), (rhs_vi, rhs_tap, rhs_ospf_net)]

	def addVLL(self, lhs_cer, rhs_cer, vllproperties):

		lhs_peo = self.cerToPEO[lhs_cer]
		rhs_peo = self.cerToPEO[rhs_cer]
	
		lhs_cer = self.getNodeByName(lhs_cer)	
		rhs_cer = self.getNodeByName(rhs_cer)
		lhs_peo = self.getNodeByName(lhs_peo)	
		rhs_peo = self.getNodeByName(rhs_peo)

		(lhs_cer_eth, lhs_cer_eth_ip) = lhs_cer.next_eth()
		(lhs_peo_eth, lhs_peo_eth_ip) = lhs_peo.next_eth()
		
		
		lhs_cer_tap_port = lhs_cer.newTapPort()
		lhs_peo_tap_port = lhs_peo.newTapPort()
		

		lhs_cer_ospf_net = self.addOSPFNet(vllproperties.net)
		lhs_cer_ip = vllproperties.ipLHS
		lhs_peo_ip = "0.0.0.0"
		vni = self.newVNI()
			
				
		
		(lhs_cer_vi, lhs_cer_tap, temp) = lhs_cer.addIntf([lhs_peo_eth_ip, lhs_cer_eth, lhs_cer_tap_port, lhs_peo_tap_port, lhs_cer_ospf_net, 
		lhs_cer_ip, lhs_peo_ip, vni])
		(lhs_peo_vi, lhs_peo_tap, lhs_peo_ospf_net) = lhs_peo.addIntf([lhs_cer_eth_ip, lhs_peo_eth, lhs_peo_tap_port, lhs_cer_tap_port, None, 
		lhs_peo_ip, lhs_cer_ip, vni])

		(rhs_cer_eth, rhs_cer_eth_ip) = rhs_cer.next_eth()
		(rhs_peo_eth, rhs_peo_eth_ip) = rhs_peo.next_eth()
		
		
		rhs_cer_tap_port = rhs_cer.newTapPort()
		rhs_peo_tap_port = rhs_peo.newTapPort()

		rhs_cer_ospf_net = copy.deepcopy(lhs_cer_ospf_net)
		rhs_cer_ip = vllproperties.ipRHS
		rhs_peo_ip = "0.0.0.0"
		vni = self.newVNI()

		(rhs_cer_vi, rhs_cer_tap, temp) = rhs_cer.addIntf([rhs_peo_eth_ip, rhs_cer_eth, rhs_cer_tap_port, rhs_peo_tap_port, rhs_cer_ospf_net, 
		rhs_cer_ip, rhs_peo_ip, vni])
		(rhs_peo_vi, rhs_peo_tap, rhs_peo_ospf_net) = rhs_peo.addIntf([rhs_cer_eth_ip, rhs_peo_eth, rhs_peo_tap_port, rhs_cer_tap_port, None, 
		rhs_peo_ip, rhs_cer_ip, vni])

		self.addLineToCFG(lhs_peo.dpid, lhs_peo_tap, rhs_peo.dpid, rhs_cer_tap)

	def addLineToCFG(self, lhs_dpid, lhs_tap, rhs_dpid, rhs_tap):
		lhs_dpid = ':'.join(s.encode('hex') for s in lhs_dpid.decode('hex'))
		rhs_dpid = ':'.join(s.encode('hex') for s in rhs_dpid.decode('hex'))
		self.vllcfgline.append(("%s|%s|%s|%s|0|0|\n" %(lhs_dpid, rhs_dpid, lhs_tap.name, rhs_tap.name)))
		
	def newOSPFNetName(self):
		ret = self.ospfBase
		self.ospfBase = self.ospfBase + 1
		return "NET%s" % ret
	
	def addOSPFNet(self, ip):
		found = False
		for ospfnet in self.ospfnets:
			if ip == ospfnet.net:
				found = True
				break
		if found == False:
			name = self.newOSPFNetName()
			net = OSPFNetwork(name, ip)
			self.ospfnets.append(net)
			self.nameToOSPFNet[name] = net
		else:
			net = ospfnet 
		return net

	# Check if a structure is empty
	def is_empty(self, struct):
		if struct:
		    return False
		else:
		    return True

	# XXX Depends on type of testbed
	def configure(self):
		raise NotImplementedError("Abstract Method")
	
	def generateLMErules(self):
		header =open('headerLME.txt','r')
		testbed = open('lmerules.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		testbed.close()
		for cro in self.cr_oshs:
			cro.generateLMErules(self.coex)
		for peo in self.pe_oshs:
			peo.generateLMErules(self.coex)

	def configureMGMT(self):
		header =open('headerMGMT.txt','r')
		management = open('management.sh','w')
		lines = header.readlines()
		for line in lines:
			management.write(line)
		management.write("declare -a DSH_GROUPS=(OSHI CER CTRL)\n")
		temp = []
		for cro in self.cr_oshs:
			temp.append(cro)
		for peo in self.pe_oshs:
			temp.append(peo)
		oshi = "declare -a OSHI=(" + " ".join("%s" % osh.mgt_ip for osh in temp) + ")\n"
		cer = "declare -a CER=(" + " ".join("%s" % cer.mgt_ip for cer in self.cers) + ")\n"
		ctrl = "declare -a CTRL=(" + " ".join("%s" % ctrl.mgt_ip for ctrl in self.ctrls) + ")\n"
		#l2sw = "declare -a L2SW=(" + " ".join("%s" % l2sw.mgt_ip for l2sw in self.l2sws) + ")\n"
		machine = "declare -a NODE_LIST=(" + " ".join("%s" % node.mgt_ip for name, node in self.nameToNode.iteritems()) + ")\n"	
		management.write(oshi)
		management.write(cer)
		management.write(ctrl)
		management.write(machine)

	def generateVLLCfg(self):
		cfg = open('vll_pusher.cfg','w')
		for line in self.vllcfgline:
			cfg.write(line)
		cfg.close()

	def addCoexistenceMechanism(self, coex_type, coex_data):
		if self.coex != {}:
			print "Error Coex mechanism already created"
			sys.exit(-1)
		
		if coex_type is None:
			print("ERROR Coex Type is None\n")
			sys.exit(-2)

		if coex_data is None:
			print("ERROR Coex Data is None\n")
			sys.exit(-2)

		self.coex['coex_type']=coex_type
		self.coex['coex_data']=coex_data

	def addIngressClassification(self, cedge, peo, ingress):
		cedge = self.getNodeByName(cedge)	
		peo = self.getNodeByName(peo)
		peo.addIngress(ingress)
		# TODO management cedge

# XXX configure() depends On Luca Prete' s Bash Script
class TestbedRouterGOFF( TestbedRouter ):
	def __init__(self, tunneling, ipnet, verbose=True):
		TestbedRouter.__init__(self)
		self.parser = MappingParserRouterTestbed(path_json = "router_goff_mapping.map", verbose = verbose)
		(self.routerinfo, self.l2swsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.ipnet = ipnet
		self.tunneling = tunneling	
	
	def configure(self):
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=GOFF\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		testbed.write("# general configuration - end\n")
		testbed.close()
		for router in self.routs:
			router.configure([self.ipnet])	
		for l2switch in self.l2sws:
			l2switch.configure()	
		for euh in self.euhs:
			euh.configure([self.ipnet])
					
# XXX configure() depends On Luca Prete' s Bash Script
class TestbedOSHIGOFF( TestbedOSHI ):
	
	def __init__(self, tunneling, ipnet, verbose=True):
		TestbedOSHI.__init__(self)
		self.parser = MappingParserOSHITestbed(path_json = "oshi_goff_mapping.map", verbose = verbose)
		(self.crosinfo, self.peosinfo, self.ctrlsinfo, self.cersinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.ipnet = ipnet
		self.tunneling = tunneling

	
	def configure(self):
		self.completeAllocation()
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=GOFF\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		if self.coex == {}:
			print "Error No Coexistence Mechanism Created"
			sys.exit(-2)
		coexFactory = CoexFactory()
		coex = coexFactory.getCoex(self.coex['coex_type'], self.coex['coex_data'], [], [], None, self.OF_V)
		testbed.write(coex.serialize())
		testbed.write("# general configuration - end\n")
		testbed.close()
		for cro in self.cr_oshs:
			cro.configure([self.ipnet])
		for peo in self.pe_oshs:
			peo.configure([self.ipnet])
		for cer in self.cers:
			cer.configure([self.ipnet])
		#for l2switch in self.l2sws:
		#	l2switch.configure()
		for ctrl in self.ctrls:
			ctrl.configure([self.ipnet])

# XXX configure() depends On Luca Prete' s Bash Script
class TestbedRouterOFELIA( TestbedRouter ):

	# Init Function
	def __init__( self, tunneling, ipnet, verbose=True):	
		TestbedRouter.__init__(self)
		self.parser = MappingParserRouterTestbed(path_json = "router_ofelia_mapping.map", verbose = verbose)
		(self.routerinfo, self.l2swsinfo, self.euhsinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.ipnet = ipnet
		#XXX START MGMT INFO
		self.mgmtnet = "10.216.0.0/255.255.0.0"
		self.mgmtgw = "10.216.32.1"
		self.mgmtintf = "eth0"
		#XXX END MGMT INFO		
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.tunneling = tunneling

	def configure(self):
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		mgmtnetdata = (self.mgmtnet.split("/"))
		mgmtnet = mgmtnetdata[0]
		mgmtmask = mgmtnetdata[1]
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=OFELIA\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		testbed.write("declare -a MGMTNET=(%s %s %s %s)\n" %(mgmtnet, mgmtmask, self.mgmtgw, self.mgmtintf))		
		testbed.write("# general configuration - end\n")
		testbed.close()
		for router in self.routs:
			router.configure([self.ipnet])
		for l2switch in self.l2sws:
			l2switch.configure()	
		for euh in self.euhs:
			euh.configure([self.ipnet])

# XXX configure() depends On Luca Prete' s Bash Script
class TestbedOSHIOFELIA( TestbedOSHI ):

	# Init Function
	def __init__( self, tunneling, ipnet, verbose=True):
		TestbedOSHI.__init__(self)
		self.parser = MappingParserOSHITestbed(path_json = "oshi_ofelia_mapping.map", verbose = verbose)
		(self.crosinfo, self.peosinfo, self.ctrlsinfo, self.cersinfo) = self.parser.getNodesInfo()
		self.vlan = self.parser.vlan
		self.verbose = verbose
		self.ipnet = ipnet
		#XXX START MGMT INFO
		self.mgmtnet = "10.216.0.0/255.255.0.0"
		self.mgmtgw = "10.216.32.1"
		self.mgmtintf = "eth0"
		#XXX END MGMT INFO		
		self.user = self.parser.user
		self.pwd = self.parser.pwd
		self.tunneling = tunneling
	
	def configure(self):
		self.completeAllocation()
		header =open('header.txt','r')
		testbed = open('testbed.sh','w')
		lines = header.readlines()
		for line in lines:
			testbed.write(line)
		mgmtnetdata = (self.mgmtnet.split("/"))
		mgmtnet = mgmtnetdata[0]
		mgmtmask = mgmtnetdata[1]
		testbed.write("# general configuration - start\n")
		testbed.write("TESTBED=OFELIA\n")
		testbed.write("TUNNELING=%s\n" % self.tunneling)
		if self.coex == {}:
			print "Error No Coexistence Mechanism Created"
			sys.exit(-2)
		coexFactory = CoexFactory()
		coex = coexFactory.getCoex(self.coex['coex_type'], self.coex['coex_data'], [], [], None, self.OF_V)
		testbed.write(coex.serialize())
		testbed.write("declare -a MGMTNET=(%s %s %s %s)\n" %(mgmtnet, mgmtmask, self.mgmtgw, self.mgmtintf))		
		testbed.write("# general configuration - end\n")
		testbed.close()
		for cro in self.cr_oshs:
			cro.configure([self.ipnet])
		for peo in self.pe_oshs:
			peo.configure([self.ipnet])
		#for l2switch in self.l2sws:
		#	l2switch.configure()
		for cer in self.cers:
			cer.configure([self.ipnet])
		for ctrl in self.ctrls:
			ctrl.configure([self.ipnet])
