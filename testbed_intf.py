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
# Interfaces Classes.
#
# @author Pier Luigi Ventre <pl.ventre@gmail.com>
# @author Giuseppe Siracusano <a_siracusano@tin.it>
# @author Stefano Salsano <stefano.salsano@uniroma2.it>
#
# XXX Depends On Dreamer-Setup-Script

class Intf:
	
	def __init__(self, name):
		self.name = name

class EthIntf(Intf):
	
	def __init__(self, name, ip, netbit, netmask):
		Intf.__init__(self,name)
		self.ip = ip
		self.netbit = netbit
		self.netmask = netmask
	
	def serialize(self):
		return "declare -a %s=(%s %s.%s.%s.%s)\n" % (self.name, self.ip, self.netmask[0], self.netmask[1], self.netmask[2], self.netmask[3])

	def __str__(self):
		return "{'name':'%s', 'ip':'%s/%s', 'netmask':'%s.%s.%s.%s'}" %(self.name, self.ip, self. netbit, self.netmask[0], self.netmask[1], self.netmask[2], self.netmask[3])

class TapIntf(Intf):
	def __init__(self, name, endipname):
		Intf.__init__(self,name)
		self.endipname = endipname
	
	def serialize(self):
		raise NotImplementedError("Abstract Method")
	
	def __str__(self):
		return "{'name':'%s', 'endip':'%s'}" % (self.name, self.endipname)


class TapOpenVPNIntf(TapIntf):
	
	def __init__(self, name, localport, remoteport, endipname):
		TapIntf.__init__(self, name, endipname)
		self.localport = localport
		self.remoteport = remoteport
	
	def serialize(self):
		return "declare -a %s=(%s %s %s)\n" % (self.name, self.localport, self.remoteport, self.endipname)
	
	def __str__(self):
		return "{'name':'%s', 'localport':'%s', 'remoteport':'%s', 'endip':'%s'}" % (self.name, self.localport, self.remoteport, self.endipname)

class TapOpenVPNHostIntf(TapOpenVPNIntf):
	
	def __init__(self, name, localport, remoteport, endipname, ip, netbit):
		TapOpenVPNIntf.__init__(self,name, localport, remoteport, endipname)
		self.ip = ip
		self.netbit = netbit

	def serialize(self):
		return "declare -a %s=(%s %s %s/%s %s)\n" % (self.name, self.localport, self.remoteport, self.ip, self.netbit, self.endipname)
	
	def __str__(self):
		return "{'name':'%s', 'localport':'%s', 'remoteport':'%s', 'ip:':'%s/%s', 'endip':'%s'}" % (self.name, self.localport, self.remoteport, self.ip, self.netbit, self.endipname)

class TapOpenVPNRouterIntf(TapOpenVPNHostIntf):
	
	def __init__(self, name, localport, remoteport, endipname, ip, netbit, hello_int, cost):
		TapOpenVPNHostIntf.__init__(self,name, localport, remoteport, endipname, ip, netbit)
		self.hello_int = hello_int
		self.cost = cost

	def serialize(self):
		return "declare -a %s=(%s %s %s/%s %s %s %s)\n" % (self.name, self.localport, self.remoteport, self.ip, self.netbit, self.cost, self.hello_int, self.endipname)
	
	def __str__(self):
		return "{'name':'%s', 'localport':'%s', 'remoteport':'%s', 'ip':'%s/%s', 'cost':'%s', 'hello_int':'%s', 'endip':'%s'}" % (self.name, self.localport, self.remoteport, self.ip, self.netbit, self.cost, self.hello_int, self.endipname)

class TapVXLANIntf(TapIntf):
	
	def __init__(self, name, VNI, endipname):
		TapIntf.__init__(self, name, endipname)
		self.VNI = VNI
	
	def serialize(self):
		return "declare -a %s=(%s %s)\n" % (self.name, self.VNI, self.endipname)
	
	def __str__(self):
		return "{'name':'%s', 'VNI':'%s', 'endip':'%s'}" % (self.name, self.VNI, self.endipname)

class ViIntf(Intf):
	
	def __init__(self, name, ip, netbit):
		Intf.__init__(self, name)
		self.ip = ip
		self.netbit = netbit
	
	def serialize(self):
		return "declare -a %s=(%s/%s)\n" %(self.name, self.ip, self.netbit)

	def __str__(self):
		return "{'name':'%s', 'ip':'%s', 'netbit':'%s'}" % (self.name, self.ip, self.netbit)


class ViRouterIntf(ViIntf):
	
	def __init__(self, name, ip, netbit, hello_int, cost):
		ViIntf.__init__(self, name, ip, netbit)
		self.hello_int = hello_int
		self.cost = cost
	
	def serialize(self):
		return "declare -a %s=(%s/%s %s %s)\n" %(self.name, self.ip, self.netbit, self.cost, self.hello_int)

	def __str__(self):
		return "{'name':'%s', 'ip':'%s', 'netbit':'%s', 'hello_int':'%s', 'cost':'%s'}" % (self.name, self.ip, self.netbit, self.cost, self.hello_int)

class LoIntf(Intf):
	
	def __init__(self, ip, name="LOOPBACK", netbit=32, hello_int=1, cost=1):
		Intf.__init__(self,name)
		self.ip = ip
		self.netbit = netbit
		self.hello_int = hello_int
		self.cost = cost
	
	def serialize(self):
		return "declare -a %s=(%s/%s %s %s)\n" %(self.name, self.ip, self.netbit, self.cost, self.hello_int)

	def __str__(self):
		return "{'name':'%s', 'ip':'%s', 'netbit':'%s', 'hello_int':'%s', 'cost':'%s'}" % (self.name, self.ip, self.netbit, self.cost, self.hello_int)


"""
	Cemetery of code
	class TapVXLANIPIntf(TapVXLANIntf):
	
		def __init__(self, name, VNI, endipname, ip, netbit):
			TapVXLANIntf.__init__(self,name, VNI, endipname)
			self.ip = ip
			self.netbit = netbit

		def serialize(self):
			return "declare -a %s=(%s %s/%s %s)\n" % (self.name, self.VNI, self.ip, self.netbit, self.endipname)
	
		def __str__(self):
			return "{'name':'%s', 'VNI':'%s', 'ip:':'%s/%s', 'endip':'%s'}" % (self.name, self.VNI, self.ip, self.netbit, self.endipname)
"""
