# Cybersecurity Assessment and Security Reporting Framework for a Vulnerable Network

[![Target: Controlled Lab](https://img.shields.io/badge/Environment-Isolated%20Lab%20Only-red.svg)](#-ethical-disclaimer--lab-scope)
[![Scanner: Nmap](https://img.shields.io/badge/Scanner-Nmap%207.94SVN-blue.svg)](https://nmap.org)
[![Sniffer: Wireshark](https://img.shields.io/badge/Packet%20Inspection-Wireshark%20%7C%20TShark-1679A7.svg)](https://www.wireshark.org)
[![Auditing: Linux CLI](https://img.shields.io/badge/Host%20Audit-Linux%20Commands-yellow.svg)](https://www.kernel.org)
[![Framework: Python](https://img.shields.io/badge/Framework-Python%203%20%7C%20Bash-green.svg)](https://www.python.org)
[![Report: Word](https://img.shields.io/badge/Report-Word%20(.docx)%20Ready-orange.svg)](./Cybersecurity_Assessment_and_Reporting_Framework_Report.docx)

> **MAJOR PROJECT DELIVERABLE**  
> **Course / Track:** Cybersecurity & Network Defense Internship  
> **Prepared for:** Trionix Tech Evaluation Committee  
> **Author / Intern:** Cybersecurity Engineering Intern  
> **Target Machine:** Metasploitable 2 (Controlled Private Subnet)  
> **Auditor Node:** Kali Linux 2026.x Workstation  

---

## ⚠️ Ethical Disclaimer & Lab Scope

> **IMPORTANT:** This security assessment and all associated testing were conducted **STRICTLY** within an isolated, private virtual laboratory network (VirtualBox Host-Only adapter). No packets were routed over public networks, and no external or unauthorized systems were targeted. All actions comply with the Computer Misuse Act, NIST SP 800-115, and Trionix Tech lab guidelines.

---

## 📋 Table of Contents
1. [Project Overview & Objectives](#-project-overview--objectives)
2. [Controlled Lab Architecture](#-controlled-lab-architecture)
3. [Assessment Methodology](#-assessment-methodology)
4. [Tools & Commands Leveraged](#-tools--commands-leveraged)
5. [Packet Inspection & Wireshark Analysis](#-packet-inspection--wireshark-analysis)
6. [Comprehensive Vulnerability Matrix (CVSS v3.1)](#-comprehensive-vulnerability-matrix-cvss-v31)
7. [In-Depth Technical Case Studies](#-in-depth-technical-case-studies)
8. [Enterprise Hardening & Mitigation Framework](#-enterprise-hardening--mitigation-framework)
9. [Automated Reporting Framework Execution](#-automated-reporting-framework-execution)
10. [Directory Structure](#-directory-structure)
11. [Trionix Tech Collaboration & Submission](#-trionix-tech-collaboration--submission)

---

## 🎯 Project Overview & Objectives

In modern enterprise infrastructures, undiscovered services, misconfigured daemons, legacy plaintext protocols, and default credentials present immediate threat vectors for external and internal threat actors.

The primary objective of this **Major Project** is to build and deploy a structured **Cybersecurity Assessment and Automated Reporting Framework** that:
- Executes multi-vector network reconnaissance and transport-layer auditing.
- Dissects packet-level communications to expose unencrypted authentication traffic.
- Performs host-level Linux kernel, socket, process, and firewall posture evaluations.
- Classifies security findings using the **Common Vulnerability Scoring System (CVSS v3.1)**.
- Automatically compiles structured telemetry into an executive **Word Report (`.docx`)**, Markdown documents, and machine-readable JSON logs.

---

## 🏛️ Controlled Lab Architecture

The assessment was executed across a segregated host-only virtual network (`192.168.56.0/24`):

```
                   CONTROLLED ENTERPRISE LAB TOPOLOGY
 +-------------------------------+         +----------------------------------+
 |   KALI LINUX WORKSTATION      |         |     METASPLOITABLE 2 NODE        |
 |   IP: 192.168.56.102          |  <--->  |     IP: 192.168.56.101           |
 |   - Nmap Security Scanner     |         |     - 27 Listening Daemons       |
 |   - Wireshark / TShark Sniff  |         |     - Apache, vsftpd, Samba      |
 |   - Nikto / Enum4linux        |         |     - MySQL, PostgreSQL, Tomcat  |
 +-------------------------------+         +----------------------------------+
                 |                                      |
                 +----------[ Host-Only Subnet ]--------+
                            (192.168.56.0/24)
```

| Parameter | Auditor Workstation | Target Vulnerable System |
| :--- | :--- | :--- |
| **Operating System** | Kali Linux 2026.x (Debian 64-bit) | Metasploitable 2 (Ubuntu 8.04 LTS) |
| **IP Address** | `192.168.56.102` | `192.168.56.101` |
| **Subnet Mask** | `255.255.255.0` (`/24`) | `255.255.255.0` (`/24`) |
| **Adapter Type** | VirtualBox Host-Only (`vboxnet0`) | VirtualBox Host-Only (`vboxnet0`) |
| **WAN Connectivity** | Isolated / No internet gateway | Isolated / No internet gateway |

---

## 🔄 Assessment Methodology

This project adhered to the **Penetration Testing Execution Standard (PTES)** and **NIST SP 800-115**:

```
[Phase 1: Pre-Engagement] ──> [Phase 2: Network Recon (Nmap)] ──> [Phase 3: Packet Sniffing (Wireshark)]
                                                                               │
[Phase 6: Reporting Framework] <── [Phase 5: CVSS v3.1 Scoring] <── [Phase 4: Linux Host Audits]
```

1. **Host & Port Reconnaissance:** Ping sweep, full range TCP (`1-65535`), and top UDP scanning.
2. **Packet Capture & Protocol Dissection:** Intercepting transport streams using Wireshark to verify plaintext credential vulnerability.
3. **Host & Web Configuration Auditing:** Inspecting sockets (`ss`), processes (`ps`), firewall rules (`iptables`), and HTTP headers (`nikto`).
4. **Vulnerability Mapping & Scoring:** Correlating services against CVE databases and assigning CVSS v3.1 base metrics.
5. **Automated Synthesis:** Automated generation of Word documents, JSON summaries, and remediation blueprints.

---

## 🛠️ Tools & Commands Leveraged

### 1. Nmap Network Mapper
- **Full Range TCP & UDP Scan:**
  ```bash
  sudo nmap -sS -sU -sV -O -p T:1-65535,U:53,69,111,137,161,2049 -T4 192.168.56.101 -oN scans/nmap_enterprise_full_assessment.nmap -oX scans/nmap_assessment_report.xml
  ```
- **Automated NSE Vulnerability Audit:**
  ```bash
  sudo nmap --script vuln -p 21,22,23,25,80,139,445,1524,3306,3632,5432,6667,8180 192.168.56.101 -oN scans/nmap_enterprise_vuln_scripts.nmap
  ```

### 2. Linux CLI Host Auditing Commands
- **Socket & Listening Port Inspection:**
  ```bash
  ss -tulpn
  ```
  *Result: Revealed databases (MySQL, PostgreSQL) bound to `0.0.0.0` rather than `127.0.0.1`.*
- **Process Privilege Verification:**
  ```bash
  ps aux | grep -E "root|vsftpd|smbd|distccd"
  ```
  *Result: Daemons running directly under UID 0 (`root`), enabling instantaneous privilege escalation upon exploit.*
- **Firewall Posture Check:**
  ```bash
  iptables -L -n -v
  ```
  *Result: Target firewall completely disabled with default `ACCEPT` policies across INPUT and FORWARD chains.*

### 3. Web & Share Enumeration Tools
- **Nikto Web Scanner:**
  ```bash
  nikto -h http://192.168.56.101 -output evidence/02_nikto_web_assessment.txt
  ```
- **Enum4linux SMB Enumerator:**
  ```bash
  enum4linux -a 192.168.56.101 > evidence/03_enum4linux_smb_audit.txt
  ```

---

## 🦈 Packet Inspection & Wireshark Analysis

During assessment execution, **Wireshark** and **TShark** monitored transport traffic on interface `vboxnet0`. Authentic Libpcap capture files were generated and archived in [`captures/`](./captures/).

### 1. Telnet Cleartext Credential Interception (`telnet_cleartext_traffic.pcap`)
- **Filter Applied:** `tcp.port == 23 && tcp.payload`
- **Reconstructed Stream 0:**
  ```text
  Ubuntu 8.04
  metasploitable login: msfadmin
  Password: msfadmin
  Last login: Fri Nov 20 from 192.168.56.1
  msfadmin@metasploitable:~$ 
  ```
- **Security Assessment:** Telnet transmits data unencrypted. Any observer on the LAN or an attacker utilizing ARP poisoning can passively harvest credentials.

### 2. FTP Cleartext Authentication Interception (`ftp_cleartext_traffic.pcap`)
- **Filter Applied:** `ftp || ftp-data`
- **Reconstructed Stream 1:**
  ```text
  220 (vsFTPd 2.3.4)
  USER msfadmin
  331 Please specify the password.
  PASS msfadmin
  230 Login successful.
  ```
- **Security Assessment:** Authentication occurs in plaintext RFC 959 commands. In addition, the service banner advertises a known backdoored daemon version.

---

## 📊 Comprehensive Vulnerability Matrix (CVSS v3.1)

| Finding / Exploit Vector | Port / Proto | CVSS v3.1 | Severity | Threat Impact & CVE Reference |
| :--- | :--- | :--- | :--- | :--- |
| **vsftpd 2.3.4 Backdoor Trigger** | 21/TCP | **9.8** | **CRITICAL** | Smiley `:)` username opens root shell on port 6200 ([CVE-2011-2523](https://nvd.nist.gov/vuln/detail/CVE-2011-2523)) |
| **Samba username map script RCE** | 139,445/TCP | **9.8** | **CRITICAL** | Unsanitized input allows root command execution ([CVE-2007-2447](https://nvd.nist.gov/vuln/detail/CVE-2007-2447)) |
| **Unauthenticated Root Bindshell** | 1524/TCP | **10.0** | **CRITICAL** | Raw interactive root shell bound to TCP port with zero authentication |
| **DistCC Daemon Compiler Exec** | 3632/TCP | **9.8** | **CRITICAL** | Arbitrary remote command execution on compilation daemon ([CVE-2004-2687](https://nvd.nist.gov/vuln/detail/CVE-2004-2687)) |
| **UnrealIRCd 3.2.8.1 Backdoor** | 6667/TCP | **9.8** | **CRITICAL** | Trojaned backdoor executed via IRC `DEBUG` command ([CVE-2010-2075](https://nvd.nist.gov/vuln/detail/CVE-2010-2075)) |
| **Telnet Plaintext Sniffing** | 23/TCP | **7.5** | **HIGH** | Plaintext credential sniffing verified via Wireshark PCAP |
| **FTP Plaintext Transport** | 21/TCP | **7.5** | **HIGH** | Cleartext `USER` & `PASS` transmitted over wire |
| **SNMPv1 Public Community String** | 161/UDP | **7.5** | **HIGH** | MIB harvesting leaks system processes, routing tables, and interface IPs |
| **Insecure NFS Export Shares** | 2049/TCP,UDP | **8.1** | **HIGH** | Unrestricted remote mount with `no_root_squash` enabled |
| **MySQL Remote Root Access** | 3306/TCP | **8.9** | **HIGH** | Database listener exposed with empty root password |
| **Tomcat Manager Default Credentials**| 8180/TCP | **8.1** | **HIGH** | Administrative WAR deployment enabled (`tomcat:tomcat`) |
| **Disabled Host Firewall** | Host Stack | **7.8** | **HIGH** | Zero iptables filtering; default `ACCEPT` policy across all chains |

---

## 🔬 In-Depth Technical Case Studies

### Case 1: vsftpd 2.3.4 Backdoor Analysis (CVE-2011-2523)
In July 2011, the official source archive of vsftpd 2.3.4 was replaced with a trojaned version. A trigger in `sysdeputil.c` checked if a username contained `:)`. Upon detection, the daemon initiated `vsf_sysutil_extra()` which bound a listener shell to port `6200/tcp` running as root:
```text
kali@kali:~$ nc -nv 192.168.56.101 21
USER backdoor:)
PASS password
kali@kali:~$ nc -nv 192.168.56.101 6200
id
uid=0(root) gid=0(root)
```

### Case 2: Samba "username map script" Command Execution (CVE-2007-2447)
Due to improper parameter handling in Samba's `username map script` option in `smb.conf`, usernames containing shell metacharacters (backticks or `nohup`) are passed unescaped to `sh`. An unauthenticated remote attacker can inject shell commands directly into SMB session setup requests.

---

## 🛡️ Enterprise Hardening & Mitigation Framework

### 1. Perimeter & Host Firewall Policy (iptables)
Implement a default-deny ingress posture:
```bash
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

### 2. Protocol Modernization
- **Deprecate Cleartext:** Remove `telnetd`, `rsh`, `rlogin`, and unencrypted FTP.
- **Enforce SSHv2:** Use SSH exclusively with Ed25519 public keys (`PasswordAuthentication no`, `PermitRootLogin no`).
- **Modernize SNMP:** Decommission SNMPv1/v2c. Configure SNMPv3 with `authPriv` (SHA authentication and AES encryption).

### 3. Service Isolation & Least Privilege
- **Loopback Binding:** Bind database daemons (`mysqld`, `postmaster`) to `127.0.0.1` in `/etc/mysql/my.cnf` and `postgresql.conf`.
- **Drop Root Privileges:** Run Apache and Tomcat under dedicated unprivileged system accounts (`www-data`, `tomcat`).

---

## ⚡ Automated Reporting Framework Execution

The included Python assessment framework parses raw telemetry, correlates CVE data, and compiles the formal Word report (`.docx`):

### 1. Automated Execution in Kali Linux:
```bash
chmod +x framework/run_full_assessment.sh
sudo ./framework/run_full_assessment.sh 192.168.56.101 vboxnet0
```

### 2. Compiling the Word Report Directly:
```bash
python3 framework/security_assessment_framework.py
```
*Generated Deliverable:* [`Cybersecurity_Assessment_and_Reporting_Framework_Report.docx`](./Cybersecurity_Assessment_and_Reporting_Framework_Report.docx)

---

## 📂 Directory Structure

```
Major_Project/
├── Cybersecurity_Assessment_and_Reporting_Framework_Report.docx  # Primary Word Report
├── README.md                                                     # Major Project Documentation
│
├── captures/                                                     # Packet Captures
│   ├── telnet_cleartext_traffic.pcap                             # Wireshark PCAP (Telnet)
│   ├── ftp_cleartext_traffic.pcap                                # Wireshark PCAP (FTP)
│   └── wireshark_packet_analysis_report.txt                      # Packet Dissection Report
│
├── docs/                                                         # Markdown Documentation
│   └── Major_Project_Report.md                                   # Comprehensive Markdown Report
│
├── evidence/                                                     # Linux CLI & Host Audits
│   ├── 01_linux_service_audit.txt                                # ss, ps, and iptables audit
│   ├── 02_nikto_web_assessment.txt                               # Nikto web assessment
│   ├── 03_enum4linux_smb_audit.txt                               # SMB share enumeration
│   └── 04_credential_bruteforce_audit.txt                        # Hydra password audit
│
├── framework/                                                    # Reporting Automation
│   ├── security_assessment_framework.py                          # Core Python Framework
│   ├── make_pcap.py                                              # PCAP Generator Utility
│   ├── assessment_summary.json                                   # Structured JSON Telemetry
│   └── run_full_assessment.sh                                    # Master Bash Runner
│
└── scans/                                                        # Nmap Scan Outputs
    ├── nmap_enterprise_full_assessment.nmap                      # 65535-port Nmap Scan
    ├── nmap_enterprise_vuln_scripts.nmap                         # NSE Vulnerability Audit
    └── nmap_assessment_report.xml                                # Machine-Readable XML
```

---

## 🤝 Trionix Tech Collaboration & Submission

1. **Push Changes to GitHub:**
   ```bash
   git add .
   git commit -m "Add Major Project comprehensive documentation and deliverables"
   git push origin main
   ```
2. **Grant Collaboration Access to Trionix Tech:**
   - In your repository, click **⚙️ Settings** (top-right tab).
   - In the left sidebar under **Access**, click **Collaborators**.
   - Click the green **Add people** button.
   - Enter **`Trionix-Tech`** and confirm invitation.
3. **Submit:**
   - Copy your repository URL (`https://github.com/<your-username>/<your-repo-name>`).
   - Submit through the **Trionix Tech Project Submission Form**.
