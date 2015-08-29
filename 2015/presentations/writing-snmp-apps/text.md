
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

Here we queried publically available SNMP Manager at *demo.snmplabs.com*
for a value of MIB variable named *sysDescr.0*. The same operation can
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

That code is somewhat verbose for a reason: PySNMP API exposes many SNMP
details to programmer giving her great power and flexibility (attentive
readers may have spotted a Python generator in the code). But before we
dive into the details let me remind our readers basic SNMP design and how
PySNMP architecture maps into it.

A bit of background
-------------------

Back in early days of computer networking, as local networks grew in size
and complexity, keeping an eye on expanding farm of computers, applications
and other network equipment became a hassle to system administrators.
Besides simple ping-like methods of testing hosts and services
availability, it became a necessity to gather more detailed information on
systems health.  Manual configuration of increasing number of networked
boxes did not scale well.

At that time there was no single predominant packet switching technology
like we see today. Large organizations were busy developing their own
network stacks each equipped with some form of network management
facilities. Ultimately, in early 90's, Internet Protocol Suite wins this
competition practically eliminating all other rivals. For TCP/IP network
management they offered SNMP, which remains principal technology even
today.

As a technology, SNMP defines application layer protocol, data model and
data objects. The protocol, which evolved a great deal since its initial
introduction in early 80's, serves as a more or less secure, lightweight
and fault-tolerant communication channel between parties.  SNMP data model
maps all interesting nuances of host or application internals to named
variables organized into hierarchy. Concrete collection of variables is
domain-specific, it is formally defined in MIBs -- files written in a
domain-specific language.

Although SNMP designers were trying to kill two birds with one stone,
offering both information collection and versatile remote configuration
features, the latter never really enjoyed much popularity among
implementers. Thus most frequently, SNMP is used for gathering some or all
variables from hosts or applications being managed. 

With SNMP architecture, managed host or application should have a component
called SNMP Agent. It acts as an intermediate having access to
host/application internals and being able to funnel that information over
SNMP to interested parties in form of SNMP variables. 

The other part of the system is called SNMP Manager, this component is
always looking for SNMP variables either by querying SNMP Agents or
listening for notifications they may produce whenever something happens to
them. 

PySNMP structure
----------------

|:---------------------------------:|
|       ASN.1 Types and Codecs      |
|       SNMP Packet Structures      |
|      SNMPv3 Security Modules      |
| SNMPv3 Message Processing Modules |
|  SNMP Engine & Network Transports |
|     Standard SNMP Applications    |
|                |                  |
|                                   |


