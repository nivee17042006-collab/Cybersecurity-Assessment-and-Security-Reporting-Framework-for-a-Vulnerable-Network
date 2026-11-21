#!/bin/bash
# ==============================================================================
# Script: run_full_assessment.sh
# Project: Major Project - Cybersecurity Assessment & Reporting Framework
# Author: Cybersecurity Engineering Intern
# Organization: Trionix Tech
# Target Environment: Controlled Isolated Network (Kali Linux -> Metasploitable 2)
# ==============================================================================

set -e

TARGET_IP="${1:-192.168.56.101}"
CAPTURE_IFACE="${2:-vboxnet0}"
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "===================================================================="
echo "   CYBERSECURITY ASSESSMENT & REPORTING FRAMEWORK (MAJOR PROJECT)   "
echo "===================================================================="
echo "[*] Target Host      : ${TARGET_IP}"
echo "[*] Sniffer Interface: ${CAPTURE_IFACE}"
echo "[*] Base Directory   : ${BASE_DIR}"
echo "[*] Timestamp        : $(date)"
echo ""

if [[ $EUID -ne 0 ]]; then
   echo "[!] Error: Root privileges required for raw packet analysis and sniffing."
   exit 1
fi

# Step 1: Start Wireshark / TShark Packet Sniffer in Background
echo "[+] Step 1: Launching TShark packet capture for Telnet & FTP cleartext..."
mkdir -p "${BASE_DIR}/captures"
tshark -i "${CAPTURE_IFACE}" -f "tcp port 21 or tcp port 23" -w "${BASE_DIR}/captures/live_sniff.pcap" -a duration:30 > /dev/null 2>&1 &
SNIFFER_PID=$!
echo "[+] Sniffer running in background (PID: ${SNIFFER_PID})"

# Step 2: Nmap Multi-Vector Network Assessment
echo "[+] Step 2: Executing Comprehensive Nmap Port & Service Fingerprinting..."
mkdir -p "${BASE_DIR}/scans"
nmap -sS -sU -sV -O -p T:1-65535,U:53,69,111,137,161,2049 -T4 "${TARGET_IP}" -oN "${BASE_DIR}/scans/nmap_enterprise_full_assessment.nmap" -oX "${BASE_DIR}/scans/nmap_assessment_report.xml"

# Step 3: Nmap Vulnerability Scripting (NSE)
echo "[+] Step 3: Executing Nmap Scripting Engine (NSE) Vulnerability Audits..."
nmap --script vuln -p 21,22,23,25,80,139,445,1524,3306,3632,5432,6667,8180 "${TARGET_IP}" -oN "${BASE_DIR}/scans/nmap_enterprise_vuln_scripts.nmap"

# Step 4: Web Vulnerability Audit (Nikto)
echo "[+] Step 4: Performing Web Application Vulnerability Scan (Nikto)..."
mkdir -p "${BASE_DIR}/evidence"
nikto -h "http://${TARGET_IP}" -output "${BASE_DIR}/evidence/02_nikto_web_assessment.txt" || true

# Step 5: SMB & NetBIOS Security Audit (Enum4linux)
echo "[+] Step 5: Executing SMB Null Session & Share Enumeration (Enum4linux)..."
enum4linux -a "${TARGET_IP}" > "${BASE_DIR}/evidence/03_enum4linux_smb_audit.txt" || true

# Step 6: Wait for packet sniffer completion
wait ${SNIFFER_PID} 2>/dev/null || true
echo "[+] Step 6: Packet capture complete."

# Step 7: Execute Python Assessment & Reporting Framework
echo "[+] Step 7: Executing Reporting Engine & Compiling Word Report (.docx)..."
python3 "${BASE_DIR}/framework/security_assessment_framework.py"

echo "===================================================================="
echo "[✓] Major Project Assessment & Reporting Completed Successfully!"
echo "===================================================================="
