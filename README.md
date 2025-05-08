# Mining the Cloud (Israel / me-south-1 Edition)

## Overview
This project demonstrates a sophisticated, object-oriented attack chain that would be detected by Cortex XDR, Cortex Cloud, and XSIAM. It simulates a malicious actor (NullFrog) who:
1. Gains initial access using compromised AWS credentials
2. Performs reconnaissance of AWS resources
3. Attempts privilege escalation
4. Deploys containerized crypto-mining operations
5. Attempts data exfiltration

## Technology Stack
- **Pulumi**: Infrastructure as code for AWS resource creation
- **boto3**: AWS API interactions for attack simulation
- **faker**: Generates realistic fake data for exfiltration and logs
- **Python (OOP)**: Clean, modular, and extensible codebase

## Security Product Integration
This attack scenario is designed to demonstrate the capabilities of Cortex products and XSIAM:
- **Cortex XDR**: Detects endpoint anomalies, suspicious process execution, behavioral analysis, and file system changes
- **Cortex Cloud**: Identifies cloud workload threats, container security issues, and suspicious IAM activities
- **XSIAM**: Correlates security events, provides automated response, and offers security intelligence

## Attack Chain Details
1. **Initial Access & Reconnaissance**
   - Uses compromised AWS credentials
   - Enumerates IAM roles and S3 buckets
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
   - Attempts data exfiltration to S3
   - Makes suspicious API calls

4. **Impact**
   - Simulates crypto-mining activity
   - Generates suspicious log entries
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
  - Data exfiltration patterns
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
   git clone https://example.com/mining-the-cloud.git
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


