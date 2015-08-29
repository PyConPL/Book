
Writing SNMP Apps in Python
===========================

Introduction
------------

Network management is important for keeping your ever growing network
infrastructure healthy and secure. SNMP is a well established
technology designed to identify and access key operational metrics of
networked hosts, routers and all sorts of industrial equipment.

As we all know, many organizations around the world use Python for
their IT automation needs, including network management. Over the
course of last decade, many SNMP implementations appeared. Some are
Python bindings to C-based [Net-SNMP library](http://www.net-snmp.org),
which is by many considered being a reference implementation for SNMP 
technology. Others are pure-Python modules addressing specific SNMP features.

Among many SNMP libraries in existence in the Python landscape, right
from the start, PySNMP project aims at complete and universal SNMP
implementation offering its users full power of SNMP technology across
all computing platforms. Having taken this project seriously, PySNMP
developers also designed a couple of foundation libraries:
[PyASN1] (http://pyasn1.sf.net) and [PySMI](http://pysmi.sf.net) as a
byproduct of their PySNMP work.

Hello, SNMP world!
------------------

Most frequent and well understood SNMP operation is about fetching a
value for a SNMP variable. In UNIX environment it is traditionally
done with snmpget tool:

    $ snmpget -v2c -c public demo.snmplabs.com sysDescr.0
    SNMPv2-MIB::sysDescr.0 = STRING: SunOS zeus.snmplabs.com 4.1.3_U1 1 sun4m

Here we queried publically available SNMP Manager at demo.snmplabs.com
for a value of MIB variable named sysDescr.0. The same operation can
be performed right from your Python prompt:
        
    from pysnmp.entity.rfc3413.oneliner.cmdgen import *

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget(('demo.snmplabs.com', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
     )

     if errorIndication:
         print(errorIndication)
     elif errorStatus:
         print('%s at %s' % (errorStatus.prettyPrint(),
                             varBinds[int(errorIndex)-1][0]
                             if errorIndex else '?'))
     else:
         for varBind in varBinds:
              print(' = '.join([x.prettyPrint() for x in varBind ]))





