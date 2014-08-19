#!/bin/bash
############################################################
##            DREAMER IP/SDN Hyibrid LME rules            ##
##                                                        ##
##      Parameters to be set by the user for the LME      ##
##	    bootstrap configuration process  				  ##
##                                                        ##
############################################################
# HowTO
#
# PLEASE, DO NOT USE WHITE SPACES
#
# LME bootstrap rules, each line is an Open vSwitch rule 
################################################################ ISTRUCTIONS END ###############################################################
# 62.40.110.49 - start
# COEXA - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap6,action=output:vi6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi6,action=output:tap6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap1,actions=mod_vlan_vid:1,goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,actions=strip_vlan,output:tap1"
# INGRB - end
# 62.40.110.49 - end
# 62.40.110.16 - start
# COEXA - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# 62.40.110.16 - end
# 62.40.110.149 - start
# COEXA - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap1,actions=mod_vlan_vid:1,goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,actions=strip_vlan,output:tap1"
# INGRB - end
# 62.40.110.149 - end
# 62.40.110.45 - start
# COEXA - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap6,action=output:vi6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi6,action=output:tap6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap3,actions=mod_vlan_vid:1,goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,actions=strip_vlan,output:tap3"
# INGRB - end
# 62.40.110.45 - end
# 62.40.110.8 - start
# COEXA - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap6,action=output:vi6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi6,action=output:tap6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap3,actions=mod_vlan_vid:1,goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,actions=strip_vlan,output:tap3"
# INGRB - end
# 62.40.110.8 - end
# 62.40.110.147 - start
# COEXA - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,dl_vlan=1,actions=goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap1,action=output:vi1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi1,action=output:tap1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap2,action=output:vi2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi2,action=output:tap2"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap3,action=output:vi3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,action=output:tap3"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap4,action=output:vi4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi4,action=output:tap4"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap5,action=output:vi5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi5,action=output:tap5"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=tap6,action=output:vi6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi6,action=output:tap6"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x88cc,action=controller"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=301,dl_type=0x8942,action=controller"
# COEXA - end
# INGRB - start
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=0,hard_timeout=0,priority=300,in_port=tap3,actions=mod_vlan_vid:1,goto_table:1"
ovs-ofctl -O OpenFlow13 add-flow br-dreamer "table=1,hard_timeout=0,priority=300,in_port=vi3,actions=strip_vlan,output:tap3"
# INGRB - end
# 62.40.110.147 - end
