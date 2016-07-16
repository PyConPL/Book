#Python for Networking Devices - Elisa Jasinska

##Introduction

The Internet is a series of tubes and at the end of those tubes are: networking devices! To form the Internet as we
know it, each provider network has to be managed, maintained and interconnected. Traditional Network Engineering is
moving more and more towards automated device and service management, a task often performed in Python due to the
availability of many useful libraries. We will walk you though common tasks in Network Engineering and introduce a
number of Python libraries that are helpful in accessing and managing networking equipment.

##Network Device Access

Traditionally networking devices are managed via their command line interface (CLI). The CLI is accessible though
various forms of transport. Originally Telnet has been used, later on devices started to support SSH. SSH provides
additional security mechanisms over Telnet, but its usability doesn't differ much, it's still a CLI.

Configuration commands are send via the CLI, line by line, and enable or disable specific functionality on the device.
For example, to configure a BGP neighbor on your router, your might have to add a config block similar to this one:
```
protocols {
    bgp {
        group external-peers {
            type external;
            neighbor 10.10.10.2 {
                peer-as 42;
            }
        }
    }
}
```

The configurations differ per vendor, the above example would add  BGP neighbor on a Juniper device, but for a Cisco
device, you might need to send commands like this:
```
router bgp 23
neighbor 10.10.10.2 remote-as 42
address-family ipv4 unicast
next-hop-self
```

The drawback of entering configurations line by line is the same as with any other device (a server for instance)
errors might occur somewhere along the way, which will result in only a part of the configuration being committed to
the device - the change is not transactional.

Nowadays Netconf is the new hype in the networking world. With underlying SSH transport it supports the same security
feature set, but in addition it offers support  for transactions, structured data and error returns. Netconf allows to
submit multiple changes at a time via an RPC call, encoded as XML and returns an XML object with the result in return.

Even though Netconf is an RFC standard and supposedly vendors should implement it in a similar fashion - they don't.
Not every vendor supports the full Netconf feature set, if they offer support for it at all, in which case you are
stuck with managing your devices line by line via the CLI after all.

In addition to configuring specific functionality on the device, 'show commands' are used to retrieve operational or
state data of the router. For example, output like this can be retrieved upon requesting the current ARP table on an
Arista device:
```
Address         Age (min)  Hardware Addr   Interface
10.220.88.1             0  001f.9e92.16fb  Vlan1, Ethernet1
10.220.88.21            0  1c6a.7aaf.576c  Vlan1, not learned
10.220.88.28            0  5254.00ee.446c  Vlan1, not learned
10.220.88.29            0  5254.0098.69b6  Vlan1, not learned
10.220.88.30            0  5254.0092.13bb  Vlan1, not learned
10.220.88.38            0  0001.00ff.0001  Vlan1, not learned
```

On a Juniper device, it will look more like this:
```
MAC Address       Address         Name                      Interface           Flags
00:1f:9e:92:16:fb 10.220.88.1     10.220.88.1               vlan.0              none
00:19:e8:45:ce:80 10.220.88.22    10.220.88.22              vlan.0              none
f0:ad:4e:01:d9:33 10.220.88.100   10.220.88.100             vlan.0              none
Total entries: 3
```

Not only can the show commands to execute on the device differ per vendor, they also provide different text format
output, which in case of CLI access has to be parsed individually. Netconf like access methods support the retrieval
of structured data, which is slightly better, but this still doesn’t cover fields not provided in one vendor vs.
another (like for example the lack of an age timer in the Juniper output above).

##Generic Access Libraries

To access devices directly via their SSH or Netconf interface, generic python libraries such as
[pexpect](https://github.com/pexpect/pexpect), [paramiko](https://github.com/paramiko/paramiko) and
[ncclient](https://github.com/ncclient/ncclient) can be used. They allow for programmatic access from scripts
(for network engineers who are trying to figure out how to code ;) ) but don't provide any ease of use in terms of
vendor specificity. You will still have to deal with the little differences the vendors bring, different login
procedured or additional escape chars). You will take care of different lines of configuration or show commands you
need to pass into paramiko or pexpect for each device or vendor, or with the varying support of netconf on each
device for ncclient.

##Specific Network Vendor Libraries

Since Python became more and more popular amongst network engineers, network vendors started to provide their own
libraries to facilitate device interaction - to mention a few: 

* Arista's [pyeapi](https://github.com/arista-eosplus/pyeapi)
* Cisco IOS-XR [pyiosxr](https://github.com/fooelisa/pyiosxr)
* Juniper's [py-junos-eznc](https://github.com/Juniper/py-junos-eznc )

Each of them supports their specific device with its specific capabilities. Juniper's py-junos-eznc  provides access
via Netconf, whereas pyiosxr 'mimics' netconf support (which is not directly available) via SSH (pexpect). They ease
config operations on the devices, such as replacing or merging configurations in one go, or . Each of them very
specific to the vendors capabilities though. 

##Multivendor Libraries

Especially in a multivendor environment managing configurations takes on a whole different level. In addition to
managing differences (and similarities) per device, for example a similar base configuration (syslog servers, NTP
servers, dns servers) but different BGP neighbors on devices in different locations. Different access methods have to
be taken into account, one via SSH the other via Netconf. Maintaining scripts with various libraries per vendor is a
pain in the a**.

Efforts to improve this  have been started, for example with [netmiko](https://github.com/ktbyers/netmiko) which is a
wrapper around paramiko and provides easy SSH access for plenty of networking equipment. On the Netconf front, or to
be more specific, access which supports transactions on the device, a project called
[napalm](https://github.com/napalm-automation/napalm) has been started last year.

Of course there are also standardization efforts, like open config or Netconf already, but as far as standards go
interworkings between different vendors have been proven to take a lot of time and effort and not be on the market as
quickly as the engineers would like.

<!---
##How to deal with your configuration management?

Independent of the library you use to access your devices, configurations still need to be managed per device (and
vendor). For a more programatic approach, we use templating 

We use configuration templating and process enforcement tools (such as jinja2, ansibe) that are helpful in creating
procedures for your work environment.
--->

##The End

And all of this, to get a few lines of config onto your router:

```
set system login message "> telnet xxx.xxx.xxx.xxx\nTrying xxx.xxx.xxx.xxx…\nConnected to telnet.example.com.\nEscape character is '^]'.\n\nlol (tty0)\n\nlogin:\n"
```
EOF
