# Mining the Cloud (Israel / me-south-1 Edition)

## Overview
This project demonstrates a sophisticated, object-oriented attack chain that would be detected by Cortex XDR, Cortex Cloud, and XSIAM. It simulates a malicious actor (NullFrog) who:

### Attack Story
- **The Organization:** Acme Corp, a company expanding into the me-south-1 AWS region for a new project. Security controls (like CloudTrail, MFA, and IAM policies) are strong in main regions, but me-south-1 was left out of automation and monitoring.
- **The LLM Leak:** The DevOps team uses an internal LLM (Large Language Model, like a private ChatGPT) to help with coding and troubleshooting. One day, a DevOps engineer accidentally pastes their AWS access and secret key into the LLM during a support chat. The LLM retains chat history.
- **Attacker's Entry:** An attacker gains access to the LLM's web interface by stealing a session cookie from a team member (e.g., via phishing). Using prompt injection, the attacker extracts the stored AWS keys from the LLM's memory.
- **Credentials:** The attacker now has long-term IAM user credentials (no MFA) for a DevOps user in the 'DevOps' group, which has broad permissions in me-south-1.
- **Attack Execution:**
  1. **Initial Access:** Attacker uses the stolen keys to access AWS in me-south-1.
  2. **Reconnaissance:** Enumerates IAM roles and EC2 instances.
  3. **Privilege Escalation:** Attempts to create a new IAM role with admin privileges.
  4. **Lateral Movement:** Launches a privileged EC2 instance (crypto-miner) using the new role.
  5. **Impact:** Abuses cloud resources for mining. No S3 exfiltration, as the attack is focused on resource abuse and privilege escalation.

### Why this is realistic
- LLMs are increasingly used in orgs, and prompt injection/data leakage is a real risk.
- Many orgs have inconsistent security across regions.
- Over-permissioned DevOps users and lack of MFA are common.
- The attack is fully logged in AWS CloudTrail, making it detectable by modern security tools.

## Technology Stack
- **Pulumi**: Infrastructure as code for AWS resource creation
- **boto3**: AWS API interactions for attack simulation
- **faker**: Generates realistic fake data for logs
- **Python (OOP)**: Clean, modular, and extensible codebase

## Security Product Integration
This attack scenario is designed to demonstrate the capabilities of Cortex products and XSIAM:
- **Cortex XDR**: Detects endpoint anomalies, suspicious process execution, behavioral analysis, and file system changes
- **Cortex Cloud**: Identifies cloud workload threats, container security issues, and suspicious IAM activities
- **XSIAM**: Correlates security events, provides automated response, and offers security intelligence

## Attack Chain Details
1. **Initial Access & Reconnaissance**
   - Uses compromised AWS credentials (leaked via LLM)
   - Enumerates IAM roles and EC2 instances
   - Creates suspicious security groups
   - Performs API reconnaissance

2. **Privilege Escalation**
   - Attempts to create new IAM roles
   - Deploys privileged containers
   - Modifies security group rules
   - Enumerates existing roles and permissions

3. **Lateral Movement**
   - Deploys containerized mining operations
   - Accesses multiple AWS services
   - Makes suspicious API calls

4. **Impact**
   - Simulates crypto-mining activity
   - Generates suspicious log entries (all actions are logged in CloudTrail)
   - Creates network traffic patterns
   - Modifies system files and permissions
   - Executes automated attack scripts

## Detection Points
- **Cortex XDR Detection**:
  - Suspicious process execution (stress, curl)
  - File system modifications (/etc/cron.d/backdoor)
  - Network activity patterns
  - Privileged container execution
  - Log file modifications

- **Cortex Cloud Detection**:
  - Cloud workload anomalies
  - Container security violations
  - IAM privilege escalation attempts
  - AWS API call anomalies

- **XSIAM Detection**:
  - Security event correlation
  - Automated response triggers
  - API call patterns
  - IAM activity anomalies
  - Container behavior analysis
  - File system change monitoring

## Quickstart
1. **Clone the Repo & Enter Folder**  
   ```bash
   git clone https://github.com/tomerzvi6/mining-the-cloud.git
   cd mining-the-cloud/
   ```

2. **Configure AWS Credentials**
   ```bash
   export AWS_ACCESS_KEY_ID="your_access_key"
   export AWS_SECRET_ACCESS_KEY="your_secret_key"
   ```

3. **Deploy the Attack Scenario**
   ```bash
   pulumi up
   ```

4. **Run the Attack Chain (OOP Entrypoint)**
   ```bash
   python main.py
   ```

## Note
This is a demonstration project for educational purposes only. Always ensure you have proper authorization before running security tests in any environment.


