
from genie.testbed import load


commands = '''
show clock
terminal length 0
show version
show users
show startup-config
show running-config
show vlan
show ip interface brief
show interface
show interfaces status
show etherchannel summary
show etherchannel detail
show spanning-tree
show spanning-tree summary
show processes cpu sorted | exclude 0.00
show processes cpu history
show interfaces counters errors
show logging
show cdp neighbors
show cdp neighbors detail
show mac address-table
show ip arp
show clock
'''

commands_wlc = '''
show clock
terminal length 0
show version
show users
show startup-config
show running-config
show vlan
show ip interface brief
show interface
show interfaces status
show etherchannel summary
show etherchannel detail
show spanning-tree
show spanning-tree summary
show processes cpu sorted | exclude 0.00
show processes cpu history
show interfaces counters errors
show logging
show cdp neighbors
show cdp neighbors detail
show mac address-table
show ip arp
show ap auto-rf dot11 24ghz
show ap auto-rf dot11 5ghz
show ap auto-rf dot11 dual-band
show ap capwap retransmit
show ap config general
show ap image
show ap location summary
show ap location stats
show ap status
show ap summary
show ap tag summary
show ap uptime
show ap wlan summary
show ap dot11 24ghz summary
show ap dot11 5ghz summary
show wlan summary
show wlan all
show wireless band-select
show wireless certification config
show wireless client summary
show wireless client summary detail
show wireless client ap dot11 24ghz
show wireless client ap dot11 5ghz
show wireless detail
show wireless device-tracking database ip
show wireless interface summary
show wireless mobility summary
show wireless stats ap discovery
show wireless stats ap join summary
show wireless summary
show wireless tag policy all
show wireless tag policy summary
show wireless tag rf all
show wireless tag rf summary
show wireless tag site all
show wireless tag site summary
show wireless vlan details
show wireless profile policy summary
show clock
'''

# devices
test = ["SW01"]
a    = ["SW02","SW03"]

tb = load("devices.yaml")
for device in test:
    target = tb.devices[device]
    target.connect()
    target.execute(commands, error_pattern=[])
    target.disconnect()
