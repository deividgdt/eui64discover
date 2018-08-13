# -*- coding: UTF-8 -*-
# - EUI 64 Discover

import os, commands as cmd
filename = "eui64discoverdump"

os.system("echo '    ________  ___________ __ __     ____  _________ __________ _    ____________'")
os.system("echo '   / ____/ / / /  _/ ___// // /    / __ \/  _/ ___// ____/ __ \ |  / / ____/ __ \'")
os.system("echo '  / __/ / / / // // __ \/ // /_   / / / // / \__ \/ /   / / / / | / / __/ / /_/ /'")
os.system("echo ' / /___/ /_/ // // /_/ /__  __/  / /_/ // / ___/ / /___/ /_/ /| |/ / /___/ _, _/'")
os.system("echo '/_____/\____/___/\____/  /_/    /_____/___//____/\____/\____/ |___/_____/_/ |_|'")  
os.system("echo 'by @deividgdt'")
os.system("echo ''")
os.system("echo 'Buscando direcciones MAC en el fichero...'")
os.system("sleep 3")

#Funcion principal
def llipv6add(macrq):
 bitsgp = bin(int((cmd.getoutput("echo %(macrq)s | cut -f 1 -d':' 2> /dev/null" %locals())), 16))[2:].zfill(8)
 bitslst = []
 for bit in bitsgp:
  bitslst.append(bit)
 if bitslst[6] == "0":
  bitslst[6] = "1"
 else:
  bitslst[6] = "0"
 hexf = hex(int("".join(bitslst), 2))[2:].zfill(2)
 macf = hexf+macrq[2:]
 ipv6 = "fe80::"+macf[:2]+macf[3:6]+macf[6:8]+"ff:fe"+macf[9:12]+macf[12:14]+macf[15:18]
 return ipv6

#Extraccion de MACs
macslst = [mac for mac in (cmd.getoutput("sudo tcpdump -er %(filename)s | egrep -o '(..:){5}..' | sort | uniq" %locals())).split()]
del(macslst[:7])

#Bucle para la parte final del proceso EUI-64.
ipv6lst = []
for mac in macslst:
 ipv6final = llipv6add(mac)
 ipv6lst.append(ipv6final)

os.system("echo 'Comprobando el estado de los dispositivos en IPv6...'")
os.system("sleep 3")

#Comprobacion del estado de los host IPv6
for ipv6 in ipv6lst:
 stoutping6 = os.system("ping6 -c1 %(ipv6)s 1> /dev/null" %locals())
 if stoutping6 != 0:
  hstate = "--> Host down"
 else:
  hstate = "--> Host up"
 print ipv6+hstate
