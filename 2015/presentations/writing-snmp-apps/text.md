
Writing SNMP Apps in Python
===========================

*Ilya Etingof, ietingof@redhat.com*

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
all computing platforms. Having taken this project seriously,
[PySNMP](http://pysnmp.sf.net) developers also designed a couple of 
foundation libraries: [PyASN1] (http://pyasn1.sf.net) and 
[PySMI](http://pysmi.sf.net) as a byproduct of their PySNMP work.

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
special domain-specific language, subset of ASN.1.

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

Library orientation
-------------------

The PySNMP library is structured internally along the lines of 
[RFC3411](http://www.ietf.org/rfc/rfc3411.txt). Components that are not
unique to SNMP are put into stand-alone Python packages to promote
reusability.

SNMP protocol is defined in terms of ASN.1 data structures, SNMP messages
travelling the wire are encoded in BER. For those purposes PySNMP relies on
generic implementation of ASN.1 types and codecs distributed as a dedicated
Python package under the name of [PyASN1](http://pyasn1.sf.net).

SNMP-level data processing is performed by a collection of SNMP Message 
Processing ([RFC3412](http://www.ietf.org/rfc/rfc3412.txt)) and Security
([RFC3414](http://www.ietf.org/rfc/rfc3414.txt)) modules living in 
*pysnmp.proto...* sub-package. All crypto operations are offloaded to
the third-party [PyCrypto](https://www.dlitz.net/software/pycrypto/)
package.

Base classes acting as a wireframe for SMI objects
([RFC2587](http://www.ietf.org/rfc/rfc2578.txt)) are defined in
*pysnmp.smi.*... They carry out both of MIB purposes:
for SNMP Manager apps, it's a hierarchical database of MIB variables
served by remote SNMP Agent. Agents can use PySNMP SMI objects for
interfacing with backend host or system being managed.

PySNMP is designed to run in asynchronous I/O environment.  Its I/O
subsystem is built around a set of abstract classes (*pysnmp.carrier...*)
whose purpose is to facilitate basing SNMP engine on top of a third-party
I/O framework. The library is shipped with a handful of ready-to-use
bindings to popular asynchronous cores including *asyncore*, *asyncio* and
*Twisted*.

All SNMP services are delivered through and components are orchestrated
by the SNMP Engine entity (*pysnmp.entity.engine*).

So called Standard SNMP Applications
[RFC3413](http://www.ietf.org/rfc/rfc3413.txt) are shipped in
*pysnmp.entity.erf3413...*. They all employ SNMP Engine instance for their
operations.

A more concise and higher-level programming interface to most frequently
used Standard SNMP Applications is offered via
*pysnmp.entity.rfc3413.oneliner...* modules. We will use their API
throughout this article.

At this point we end up with a fully-functional SNMP entity that can run in
standard Manager, Agent and Proxy roles. However one SNMP feature is
still missing and that is MIB support. More often than not, MIBs are used
in the context of SNMP operations. However, other uses are not impossible.
For example one may want to transform MIB structures into XML/HTML form or
generate code in some programming language implementing MIB features. That
was the rationale behind PySNMP developers' decision to isolate MIB parsing
from SNMP Engine implementation and put it into a dedicated Python package
called [PySMI](http://pysmi.sf.net).

Being optional, PySMI will be discovered and automatically used by Manager
applications, running on top of high-level PySNMP API, for MIB variable
names and types resolution.

Common operations
-----------------

Besides reading known scalar variables we mentioned earlier, SNMP is able
to fetch a range of variable including those not known in advance. The
following code fetches all variables related to host's interface table:

    from pysnmp.entity.rfc3413.oneliner.cmdgen import *

    for errorIndication, errorStatus, errorIndex, varBinds in \
            nextCmd(SnmpEngine(),
                            CommunityData('public'),
                            UdpTransportTarget(('demo.snmplabs.com', 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')),
                            ObjectType(ObjectIdentity('IF-MIB', 'ifType'))):

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                varBinds[int(errorIndex)-1][0]
                                if errorIndex else '?'
                )
            )
            break
        else:
            for varBind in varBinds:
                print(' = '.join([ x.prettyPrint() for x in varBind ]))

In this example we iterate remote SNMP Agent over two MIB variables
(*IF-MIB::ifDescr* and *IF-MIB::ifType*) which are in fact two columns 
of SNMP table.

Any operation carried out through high-level API involves Python generator.
Each invocation of such generator translates into SNMP message being sent 
and response processed. Generator functions are specific to SNMP message
type and are uniformly initialized with:

* SNMP Engine object: this is the umbrella object coordinating all
  SNMP operations. It's used by SNMP applications like Command Generator
  application featured in example.
* SNMP authentication method: that can be SNMPv1/v2c Community Name or
  [RFC3414](http://www.ietf.org/rfc/rfc3414.txt) *UsmUser* object
  conveying USM username, encryption and ciphering keys.
* Kind of I/O to use for this communication, endpoints addresses and
  other transport-specific options
* SNMP Context Engine ID and Context Name: these are only applicable
  to SNMPv3 operations and can be used to identify a non-default remote
  SNMP Engine instance or specific instance of MIB variables collection 
  behind remote SNMP Engine.
* Sequence of MIB variables to query. Sometimes MIB variable name should
  be accompanied with a value to transfer to remote SNMP entity. Such value
  could be passes through *ObjectType()* initializer.

As for return values, on each iteration generator give us a tuple of
result items:

* errorIndication: if evaluates to True, it indicates some fatal problem
  occurred to local or remote SNMP engine. Most likely a timeout or
  authentication problem.
* errorStatus and errorIndex: if errorIndex is not zero, that indicates
  a problem with particular MIB variable put into request. The errorStatus
  object provides more information on the nature of the problem.
* varBinds: is a list of two-element tuples, each correspond to MIB variable
  and its value.

As we can send data back into running generator, our script could be 
modified to cherry-pick smaller sequences of adjacent MIB variables or even
individual scalars:

    from pysnmp.entity.rfc3413.oneliner.cmdgen import *

    queue = [ [ ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets')) ],
              [ ObjectType(ObjectIdentity('IF-MIB', 'ifOutOctets')) ] ]

    iter = nextCmd(SnmpEngine(),
                   UsmUserData('usr-md5-none', 'authkey1'),
                   UdpTransportTarget(('demo.snmplabs.com', 161)),
                   ContextData())

    next(iter)

    while queue:
        errorIndication, errorStatus, errorIndex, varBinds = iter.send(queue.pop())
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    varBinds[int(errorIndex)-1][0] if errorIndex else '?'
                )
            )
        else:
            for varBind in varBinds:
                print(' = '.join([ x.prettyPrint() for x in varBind ]))

At any moment SNMP Agent may consider reporting specific events to
SNMP Manager.  Such SNMP Notification message might include relevant
variables that help both Manager software and human reader learning
the details of the event being reported.

    from pysnmp.entity.rfc3413.oneliner.ntforg import *

    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(SnmpEngine(),
                         UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
                         UdpTransportTarget(('demo.snmplabs.com', 162)),
                         ContextData(),
                         'trap',
                         NotificationType(ObjectIdentity('IF-MIB', 'linkDown'))
    )

    if errorIndication:
        print(errorIndication)

Like MIB variables, SNMP Notifications are identified by Object Identifier
(OID). Notifications are specified in MIBs along with MIB variables
that should be reported in notification message. This is MIB specification
of the above notification (from IF-MIB.txt):

    linkDown NOTIFICATION-TYPE
        OBJECTS { ifIndex, ifAdminStatus, ifOperStatus }
        STATUS  current
        DESCRIPTION
                "A linkDown trap signifies that the SNMP entity, acting in
                an agent role, has detected that the ifOperStatus object for
                one of its communication links is about to enter the down
                state from some other state (but not from the notPresent
                state).  This other state is indicated by the included value
                of ifOperStatus."
        ::= { snmpTraps 3 }

Referring to MIBs
-----------------

Surprisingly, SNMP can work without MIBs! Protocol itself does not depend
on them. MIBs are designed as complimentary database to make SNMP
data more human readable and convenient to deal with.

PySNMP library is designed to work without MIBs. You can always refer to
a MIB variable via Object Identifier:

    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'), OctetString('my host')) 

Whenever data type has to be specified, that can be done by passing
corresponding PyASN1 type. Otherwise both variable identifier and
data type associated with a variable would be looked up at MIB.

    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0), 'my host') 

For MIB resolution to work PySNMP application must load up MIB module
being looked up. Internally, PySNMP represents MIBs as Python modules
containing objects each representing MIB variable:

    # pysnmp/smi/mibs/SNMPv2-MIB.py:
    # ...
    sysDescr = MibScalar((1, 3, 6, 1, 2, 1, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess("readonly")

Conversion of original, ASN.1 MIB text files into PySNMP-compliant Python
modules is done behind the scenes by PySMI. Normally, PySNMP users do not
need to bother explicitly invoking PySMI services. PySNMP would call PySMI
automatically provided PySMI package is installed and requested MIB module
is available.

Users can point their PySNMP applications to either local MIB repositories
or remote ones that are accessible through HTTP or FTP:

    from pysnmp.entity.rfc3413.oneliner.cmdgen import *

    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget(('demo.snmplabs.com', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('IF-MIB', 'ifInOctets', 1).addAsn1MibSource('file:///usr/share/snmp', 'http://mibs.snmplabs.com/asn1/@mib@'))
       )
    )

To figure out what MIBs are implemented by particular SNMP Agent, Manager
could query *SNMPv2-MIB::sysORTable* MIB variables:

    $ snmpwalk -v2c -c public demo.snmplabs.com sysORTable
    SNMPv2-MIB::sysORID.1 = OID: SNMPv2-MIB::snmpMIB
    SNMPv2-MIB::sysORID.2 = OID: SNMP-VIEW-BASED-ACM-MIB::vacmBasicGroup
    SNMPv2-MIB::sysORID.3 = OID: SNMP-MPD-MIB::snmpMPDCompliance
    SNMPv2-MIB::sysORID.4 = OID: SNMP-USER-BASED-SM-MIB::usmMIBCompliance
    SNMPv2-MIB::sysORID.5 = OID: SNMP-FRAMEWORK-MIB::snmpFrameworkMIBCompliance
    ...

An efficient Manager could then optimize its behavior by fetching required
MIBs and querying MIB variables from those MIBs.

SNMP Agents
-----------

PySNMP could act as a full-blown SNMP Agent supporting most of standard
SNMP features pretty much out out the box. When building SNMP Agent, most
development efforts normally go into establishing mapping between
something to be monitored and MIB variable to be reported back to SNMP
Manager.

Multiple solutions exist at different levels of PySNMP library. Probably
the simplest approach is to subclass *MibScalarInstance()*, representing
specific MIB variable, so that relevant information is returned when
queried or some action is performed when MIB variable is modified:

    # __MY_MIB.py:
    # ...
    class FileStorage(MibScalarInstance):
        file = '/var/run/agent/store'

        def getValue(self, name, idx):
            with f in open(self.file):
                return self.getSyntax().clone(f.read())

        def setValue(self, value, name, idx):
            with f in open(self.file, 'w'):
                f.write(value)
            return self.getValue(name, idx)

    # Register our MIB variable implementation
    mibBuilder.exportSymbols(
        '__MY_MIB', FileStorage((1,3,6,5,1,1,2,3,1), (0,), OctetString())
    )

Sometimes it is easier to bypass most of PySNMP SMI implementation by
provisioning your own instance of MIB Controller object to SNMP Agent:

    class EchoMibInstrumController(AbstractMibInstrumController):
        def readVars(self, varBinds, acInfo):
                return [ (ov[0], OctetString('Would read OID %s' % varBind[0])) for varBind in varBinds]

        def writeVars(self, varBinds, acInfo):
                return [ (varBind[0], OctetString('Would set OID %s to %s' % varBind)) for varBind in varBinds]

    snmpContext.registerContextName(
        OctetString('my-context'), EchoMibInstrumController()
    )

    GetCommandResponder(snmpEngine, snmpContext)
    SetCommandResponder(snmpEngine, snmpContext)

Real-world applications
-----------------------

Over the years PySNMP developers created a couple of software products
based on PySNMP library. That kind of reality check experience influenced
PySNMP design a great deal.

[SNMP Simulator](http://snmpsim.sf.net) is probably the most sophisticated
free and open source SNMP Agent emulation software at the time being. This
tool can create an illusion that large SNMP-managed network of various
devices exists in your virtual laboratory. Emulated devices try to look live
by reporting changing data. MIB variables can be configured to change
according to some formula. Modified data can be made persistent by keeping
MIB variables in SQL or noSQL database. 

SNMP simulation toolkit also offers utilities that can capture SNMP traffic
from real SNMP Agents, store captured MIB variables so that they could then
be replayed by SNMP simulator. Another way to gather a collection of MIB
variables to simulate is to populate MIB it from ASN.1 MIB file.

Another large project is [SNMP Proxy Forwarded](http://snmpfwd.sf.net). That
tool is designed to work as transparent, application-level firewall passing
SNMP traffic between open and protected network segments. SNMP protocol
version translation could be performed on the fly, sophisticated SNMP data
filtering and modification could be performed, response caching and request
rate limiting could be set up to reduce SNMP load on end devices.

Finally, we ship a pure-Python version of SNMP
[command-line tools](https://pypi.python.org/pypi/pysnmp-apps)
that try to mimic their Net-SNMP prototypes.

References
----------

1. [PySNMP project site](http://pysnmp.sf.net)
2. [SNMP RFCs](http://www.snmp.com/protocol/snmp_rfcs.shtml)
3. [Practical Guide to SNMPv3 and Network Management](http://www.amazon.com/Practical-Guide-Snmpv3-Network-Management/dp/0130214531/ref=pd_sim_14_4?ie=UTF8&refRID=0KNXDXE2XYXV13SX137H)
4. [Understanding SNMP MIBs](http://www.amazon.com/Understanding-SNMP-MIBs-David-Perkins/dp/0134377087/ref=pd_sim_14_3?ie=UTF8&refRID=1N65YA65G01KJAKR6PD1)
