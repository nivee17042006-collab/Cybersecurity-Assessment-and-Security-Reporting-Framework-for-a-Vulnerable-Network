#!/usr/bin/env python3
"""
Generate Libpcap (.pcap) capture files for Wireshark analysis.
Demonstrates cleartext credential sniffing over Telnet (Port 23) and FTP (Port 21).
"""

import struct
import time
import os

def create_pcap(filename, packets):
    global_header = struct.pack('<IHHiIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)
    with open(filename, 'wb') as f:
        f.write(global_header)
        for ts_sec, ts_usec, pkt_data in packets:
            f.write(struct.pack('<IIII', ts_sec, ts_usec, len(pkt_data), len(pkt_data)))
            f.write(pkt_data)
    print(f"[+] Successfully created PCAP: {filename} ({os.path.getsize(filename)} bytes)")

def build_eth_ip_tcp(src_mac, dst_mac, src_ip, dst_ip, src_port, dst_port, seq, ack, flags, payload=b""):
    eth = dst_mac + src_mac + b'\x08\x00'
    ip_ver_ihl = (4 << 4) | 5
    ip_tot_len = 20 + 20 + len(payload)
    ip_src = bytes([int(x) for x in src_ip.split('.')])
    ip_dst = bytes([int(x) for x in dst_ip.split('.')])
    ip_hdr = struct.pack('!BBHHHBBH4s4s', ip_ver_ihl, 0, ip_tot_len, 54321, 0x4000, 64, 6, 0, ip_src, ip_dst)
    tcp_hdr = struct.pack('!HHIIBBHHH', src_port, dst_port, seq, ack, (5 << 4), flags, 64240, 0, 0)
    return eth + ip_hdr + tcp_hdr + payload

def generate_pcaps():
    kali_mac = b'\x08\x00\x27\x01\x02\x03'
    meta_mac = b'\x08\x00\x27\x48\x8a\x23'
    kali_ip = "192.168.56.102"
    meta_ip = "192.168.56.101"
    now = int(time.time())

    # --- Telnet Capture ---
    telnet_pkts = [
        (now, 100000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49152, 23, 1000, 0, 0x02)),
        (now, 101000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 23, 49152, 5000, 1001, 0x12)),
        (now, 102000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49152, 23, 1001, 5001, 0x10)),
        (now, 105000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 23, 49152, 5001, 1001, 0x18, b"\r\nUbuntu 8.04\r\nmetasploitable login: ")),
        (now, 120000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49152, 23, 1001, 5030, 0x18, b"msfadmin\r\n")),
        (now, 125000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 23, 49152, 5030, 1011, 0x18, b"Password: ")),
        (now, 140000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49152, 23, 1011, 5040, 0x18, b"msfadmin\r\n")),
        (now, 150000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 23, 49152, 5040, 1021, 0x18, b"\r\nLast login: Fri Nov 20 from 192.168.56.1\r\nmsfadmin@metasploitable:~$ "))
    ]
    t_path = os.path.join(os.path.dirname(__file__), "..", "captures", "telnet_cleartext_traffic.pcap")
    create_pcap(t_path, telnet_pkts)

    # --- FTP Capture ---
    ftp_pkts = [
        (now, 200000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49153, 21, 2000, 0, 0x02)),
        (now, 201000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 21, 49153, 6000, 2001, 0x12)),
        (now, 202000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49153, 21, 2001, 6001, 0x10)),
        (now, 205000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 21, 49153, 6001, 2001, 0x18, b"220 (vsFTPd 2.3.4)\r\n")),
        (now, 210000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49153, 21, 2001, 6021, 0x18, b"USER msfadmin\r\n")),
        (now, 215000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 21, 49153, 6021, 2016, 0x18, b"331 Please specify the password.\r\n")),
        (now, 220000, build_eth_ip_tcp(kali_mac, meta_mac, kali_ip, meta_ip, 49153, 21, 2016, 6054, 0x18, b"PASS msfadmin\r\n")),
        (now, 225000, build_eth_ip_tcp(meta_mac, kali_mac, meta_ip, kali_ip, 21, 49153, 6054, 2031, 0x18, b"230 Login successful.\r\n"))
    ]
    f_path = os.path.join(os.path.dirname(__file__), "..", "captures", "ftp_cleartext_traffic.pcap")
    create_pcap(f_path, ftp_pkts)

if __name__ == "__main__":
    generate_pcaps()
