# Major Project Report: Cybersecurity Assessment & Security Reporting Framework

**Project Domain:** Enterprise Cybersecurity Assessment & Automated Reporting  
**Prepared for:** Trionix Tech Major Project Evaluation  
**Author / Intern:** Cybersecurity Engineering Intern  
**Date:** November 21, 2026  
**Status:** Completed & Validated  

---

## Executive Summary
This Major Project presents an end-to-end Cybersecurity Assessment and Automated Reporting Framework conducted against an authorized, vulnerable network node (**Metasploitable 2**, IP: `192.168.56.101`) originating from a security workstation (**Kali Linux**, IP: `192.168.56.102`).

Using a multi-tool assessment pipeline—comprising **Nmap**, **Wireshark/TShark**, **Linux CLI tools**, **Nikto**, **Enum4linux**, and **Hydra**—we evaluated 27 listening services and identified critical security weaknesses, including unauthenticated remote root shells, backdoor triggers, cleartext transport protocols, and weak credential practices.

---

## Assessment Tools & Artifacts
* **Nmap (`scans/`):** Full 65,535 TCP port scan, UDP top ports, OS fingerprinting, and NSE vulnerability scripts.
* **Wireshark & TShark (`captures/`):** Valid Libpcap files (`telnet_cleartext_traffic.pcap`, `ftp_cleartext_traffic.pcap`) and stream reconstruction reports.
* **Linux CLI Audits (`evidence/`):** Socket statistics (`ss -tulpn`), process ownership (`ps aux`), firewall rules (`iptables -L`), web assessments (`nikto`), and SMB shares (`enum4linux`).
* **Reporting Engine (`framework/`):** Python-based framework that computes CVSS v3.1 scores and generates formal Word documents and JSON summaries.

---

## Discovered Vulnerability Matrix (CVSS v3.1)

| Finding / CVE | Port | CVSS v3.1 | Severity | Key Threat Vector |
| :--- | :--- | :--- | :--- | :--- |
| **vsftpd 2.3.4 Backdoor (CVE-2011-2523)** | 21/TCP | **9.8** | **CRITICAL** | Smiley `:)` username opens root shell on port 6200 |
| **Samba username map script (CVE-2007-2447)** | 139,445/TCP | **9.8** | **CRITICAL** | Remote command execution under root privileges |
| **Unauthenticated Bindshell (Ingreslock)** | 1524/TCP | **10.0** | **CRITICAL** | Direct interactive root shell without password challenge |
| **DistCC Compiler Daemon (CVE-2004-2687)** | 3632/TCP | **9.8** | **CRITICAL** | Arbitrary remote command execution on compilation daemon |
| **UnrealIRCd 3.2.8.1 Backdoor (CVE-2010-2075)** | 6667/TCP | **9.8** | **CRITICAL** | Trojaned backdoor executed via IRC `DEBUG` command |
| **Telnet Plaintext Credential Exposure** | 23/TCP | **7.5** | **HIGH** | Wireshark packet capture reveals passwords in cleartext |
| **FTP Plaintext Transport** | 21/TCP | **7.5** | **HIGH** | Unencrypted `USER` and `PASS` commands exposed to sniffing |
| **SNMPv1 Public Community String** | 161/UDP | **7.5** | **HIGH** | Unauthenticated disclosure of processes and network interfaces |
| **NFS Insecure Export Shares** | 2049/TCP,UDP | **8.1** | **HIGH** | Unrestricted remote mount with `no_root_squash` |
| **MySQL Remote Root Access (Empty Password)** | 3306/TCP | **8.9** | **HIGH** | Database listener exposed with blank root credential |
| **Apache Tomcat Default Manager Credentials** | 8180/TCP | **8.1** | **HIGH** | WAR package upload yielding web shell (`tomcat:tomcat`) |

---

## Enterprise Hardening Roadmap
1. **Default-Deny Ingress Firewall:** Deploy `iptables`/`ufw` with default drop rules.
2. **Decommission Cleartext Daemons:** Replace Telnet and FTP with OpenSSH and SFTP.
3. **Isolate Database Listeners:** Bind MySQL and PostgreSQL strictly to `127.0.0.1`.
4. **Enforce Strong Credentials & Keys:** Disable password SSH logins in favor of Ed25519 keys.
5. **Modernize SNMP:** Upgrade to SNMPv3 with `authPriv` (SHA + AES).
