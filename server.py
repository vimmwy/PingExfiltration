import argparse
import scapy.all as scapy
from scapy.all import sniff

BIG_DATA = ""

def exfiltrated(packet: scapy.Packet):
    if packet.haslayer("ICMP") and packet.haslayer("IP"):
        if packet["ICMP"].type == 8:
            data = bytes(packet["ICMP"].payload)
            result = data.decode(errors='ignore')            
            if result.startswith(args.separator):
                global BIG_DATA
                BIG_DATA += result[len(args.separator):]
                return
            if BIG_DATA:
                result = BIG_DATA + result
                BIG_DATA = ""
            print("========================\nFROM: {}\n========================".format(packet["IP"].src))
            if args.raw:
                print(result.replace("\n", "\\n").replace("\r", "\\r") or "<no data>")
            else:
                print(result or "<no data>")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ICMP Echo Request Listener")
    parser.add_argument("-i", "--interface", type=str, required=False, help="Network interface to listen on")
    parser.add_argument("-r", "--raw", required=False, action="store_true", help="Display raw packet data")
    parser.add_argument("--src", type=str, required=False, help="Filter packets by source IP address")
    parser.add_argument("-s", "--separator", type=str, default="-:-", help="Separator for chunked data")

    args = parser.parse_args()
    print(f"Listening on interface: {args.interface if args.interface else 'default'}")
    if args.raw:
        print("Raw mode enabled: special characters will be escaped.")
    if args.interface:
        if args.src:
            sniff(prn=exfiltrated, filter=f"icmp and src host {args.src}", iface=args.interface)
        else:
            sniff(prn=exfiltrated, filter="icmp", iface=args.interface)
    else:
        if args.src:
            sniff(prn=exfiltrated, filter=f"icmp and src host {args.src}")
        else:
            sniff(prn=exfiltrated, filter="icmp")
