# Python for Networking Devices - Elisa Jasinska

## Introduction

The Internet is a series of tubes and at the end of those tubes are: networking devices! To form the Internet as we
know it, each provider network has to be managed, maintained and interconnected. Traditional Network Engineering is
moving more and more towards automated device and service management, a task often performed in Python due to the
availability of many useful libraries. We will walk you though common tasks in Network Engineering and introduce a
number of Python libraries that are helpful in accessing and managing networking equipment.

## Network Device Access

Traditionally networking devices are managed via their command line interface (CLI). The CLI is accessible though
various forms of transport. Originally Telnet has been used, later on devices started to support SSH. SSH provides
additional security mechanisms over Telnet, but its usability doesn't differ much, it's still a CLI.

Configuration commands are sent via the CLI, line by line, and enable or disable specific functionality on the device.
For example, to add a Border Gateway Protocol (BGP) neighbor on your router, your config might need to contain a block
similar to this one:
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

The configurations differ per vendor, the above example would add BGP neighbor on a Juniper device, but for a Cisco
device, you might need to send commands like this:
```
router bgp 23
neighbor 10.10.10.2 remote-as 42
address-family ipv4 unicast
next-hop-self
```

The drawback of entering configurations line by line is the same as with any other device (a server for instance):
errors might occur somewhere along the way, which will result in only a part of the configuration being committed to
the device - the change is not transactional.

### Netconf

Nowadays Netconf is the new hype in the networking world. With underlying SSH transport it supports the same security
feature set, but in addition it offers support for transactions, structured data and error reporting. Netconf allows
to submit multiple changes at a time via an RPC call, encoded as XML, and sends back an XML object with the result in
return.

Even though Netconf is an RFC standard and vendors should implement it the same way - they don't.
Not every vendor supports the full Netconf feature set, if they offer support for it at all, in which case you are
stuck with managing your devices line by line via the CLI after all.

In addition to configuring specific functionality on the device, 'show commands' are used to retrieve operational or
state data of the router. For example, output like this can be retrieved upon requesting the current ARP table on an
Arista device:
```
eos.edge1>show arp
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
root@qfx.edge1> show arp
MAC Address       Address         Name                      Interface           Flags
00:1f:9e:92:16:fb 10.220.88.1     10.220.88.1               vlan.0              none
00:19:e8:45:ce:80 10.220.88.22    10.220.88.22              vlan.0              none
f0:ad:4e:01:d9:33 10.220.88.100   10.220.88.100             vlan.0              none
Total entries: 3
```

Not only can the 'show commands' to execute on the device differ per vendor, they also provide different text format
output, which in case of CLI access has to be parsed individually. Netconf-like access methods support the retrieval
of structured data, which is slightly better, but this still doesn’t cover fields not provided in one vendor vs.
another (like for example the lack of an age timer in the Juniper output above).

## Generic Access Libraries

To access devices directly via their SSH or Netconf interface, generic Python libraries such as
[pexpect](https://github.com/pexpect/pexpect), [paramiko](https://github.com/paramiko/paramiko) and
[ncclient](https://github.com/ncclient/ncclient) can be used. They allow for programmatic access from scripts
(for network engineers who are trying to figure out how to code ;) ) but don't provide any ease of use in terms of
vendor specificity. You will still have to deal with the little differences the vendors bring: different login
procedures or additional escape chars, different configuration syntax, differences in 'show commands' or
differences with the varying support of Netconf on each device.

## Specific Network Vendor Libraries

Since Python became more and more popular amongst network engineers, network vendors started to provide their own
libraries to facilitate device interaction - to mention a few:

* Arista's [pyeapi](https://github.com/arista-eosplus/pyeapi)
* Cisco IOS-XR [pyiosxr](https://github.com/fooelisa/pyiosxr)
* Juniper's [py-junos-eznc](https://github.com/Juniper/py-junos-eznc )

Each of them supports their specific device with its specific capabilities. Juniper's py-junos-eznc provides access
via Netconf, whereas pyiosxr 'mimics' Netconf support (which is not directly available) via SSH and pexpect.
They ease config operations on the devices by providing functions to send config, replace or merge it in one go, or
to retreive the configuration. Each of those libs is very specific to the vendors device and takes all its nits into
account, but a lot of times networks are designed to use a mix of vendors, in which case one library won't suffice.

## Multivendor Libraries

Managing configurations in a multivendor environment takes on a whole different level. In addition to managing
differences per device-role, differences in access have to be considered. Each device role needs a similar base
configuration for example (syslog servers, NTP servers, dns servers) but different BGP neighbors on devices in
different locations, plus a different methodology to upload the configs to the device. Vendor specific libs can be
used for each of them individually, however managing the use of different libraries per vendor is quite painful.

In an effort to improve upon this situation, wrappers around a set of libraries have been built to unify multivendor
access to networking devices. For example [netmiko](https://github.com/ktbyers/netmiko), which is a
wrapper around paramiko and provides easy SSH access for plenty of networking equipment. On the Netconf front, or to
be more specific, access which supports transactions on the device, a project called
[napalm](https://github.com/napalm-automation/napalm) has been started, which unifies a set of vendor libraries
into a single set of methods.

Of course there are also standardization efforts, like open config or Netconf, which aim to improve upon this
situation. But as far as standards go, interworkings between different vendors have been proven to take a lot of time
and effort, and typically aren't on the market as quickly as the engineers would like.

## Summary

How to start if you are looking to introduce automation into your network? Start by reviewing your network
design and determine what vendors are in use. If it is one single vendor and they provide a library, use that. If you
operate a mix of vendors, check if the multivendor module napalm supports all of them. If neither is an option, you
can decide to use a lower level access wrapper like netmiko, but you will have to give up on using more advanced
functionality that is provided by the libraries.

And all of this, to get a few lines of config onto your router:

```
set system login message "> telnet xxx.xxx.xxx.xxx\nTrying xxx.xxx.xxx.xxx…\nConnected to telnet.example.com.\nEscape character is '^]'.\n\nlol (tty0)\n\nlogin:\n"
```
EOF
