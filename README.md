# Mining the Cloud (Israel / ap-northeast-3 Edition)

## Overview
This project demonstrates a sophisticated, object-oriented attack chain that would be detected by Cortex XDR, Cortex Cloud, and XSIAM. It simulates a malicious actor ("NullFrog") executing a multi-stage cloud attack on AWS, focusing on common misconfigurations and modern attack techniques.

The entire simulation is engineered to tell a realistic attacker story, leaving a clear trail of forensic artifacts in AWS CloudTrail for security tools to analyze.

## Attack Story
- **The Organization:** A company expanding into the ap-northeast-3 (Israel) AWS region for a new project. Security controls (like detailed CloudTrail monitoring, MFA enforcement, and strict IAM policies) are robust in their primary US/EU regions, but the new ap-northeast-3 environment was left out of standard security automation and monitoring during a rushed deployment.
- **The LLM Leak:** The team uses a general-purpose, home-made LLM assistant (similar to ChatGPT or Gemini, but not a commercial product) to help with coding, troubleshooting, and general questions. One day, a DevOps engineer accidentally pastes their AWS access key and secret key into the LLM's chat interface while debugging a script. The LLM, by default, retains chat history.
- **Attacker's Entry:** An attacker, "NullFrog," creates a fake website using Bolt AI that mimics the real LLM login page. The attacker sends a phishing email to a team member, luring them to the fake site. The user enters their credentials, which the attacker then uses to log in to the real LLM website.
- **Prompt Injection & Data Extraction:** Once inside, the attacker uses prompt injection techniques to query the LLM and extract the stored AWS keys from its chat history.
- **The Compromise:** The attacker now possesses long-term IAM user credentials for a member of the "DevOps" group. Crucially, these credentials are not protected by MFA. The associated IAM role has overly broad permissions in the under-monitored ap-northeast-3 region.
- **Attack Execution:**
  - **Initial Access:** NullFrog uses the stolen keys to access the AWS account in the ap-northeast-3 region, hoping to remain undetected.
  - **Reconnaissance:** They enumerate IAM roles and EC2 instances to map the environment.
  - **Privilege Escalation:** They create a new IAM role with elevated privileges, exploiting the permissive policies of the compromised DevOps user.
  - **Lateral Movement & Impact:** NullFrog's ultimate goal is resource abuse. They use their newly acquired privileges to launch a spot EC2 instance configured for crypto-mining. This simulation focuses on privilege escalation and resource abuse, not data exfiltration.

## Why this is realistic
- **LLM Risk:** Data leakage through internal or public LLMs via prompt injection is an emerging and significant threat vector.
- **Regional Security Gaps:** Organizations often have inconsistent security postures across different cloud regions, especially in newer or less critical environments.
- **Common Misconfigurations:** Over-permissioned IAM users and a lack of MFA remain two of the most common and exploitable security weaknesses in cloud environments.
- **Detectable by Design:** All malicious actions are performed via standard AWS API calls, which are automatically logged in AWS CloudTrail, making them visible to modern security platforms.

## Technology Stack
- **Pulumi:** Infrastructure as Code (IaC) for provisioning AWS resources.
- **boto3:** The AWS SDK for Python, used to programmatically execute the attack steps.
- **faker:** A Python library to generate realistic fake data for log entries.
- **Python (OOP):** The project is built with a clean, modular, and object-oriented design for maintainability.
- **AWS CloudTrail:** The native logging service that captures all API calls, serving as the primary source for detection.

## Project Structure & Technical Walkthrough
The project is built with a clean, modular, object-oriented design for maintainability and reusability.

- **main.py:** The primary entry point. It orchestrates the entire simulation by initializing and running the AttackChain.
- **attack_chain/resource_manager.py:** Manages all AWS resource creation (security groups, IAM roles, EC2 spot instances) using Pulumi, separating infrastructure logic from the attack simulation.
- **attack_chain/steps.py:** Contains the individual attack phases, each implemented as a distinct class inheriting from an AttackStep abstract base class.
- **attack_chain/attack_chain.py:** The central orchestrator. This class connects all the attack steps and executes them sequentially to tell the attack story.
- **attack_chain/fake_data.py:** Employs the faker library to generate realistic fake log entries.
- **attack_chain/logger.py:** Handles the logging of suspicious activities to the console for demonstration purposes.

## Attack Flow: Step-by-Step

1. **Setup (`main.py`):** The `main()` function instantiates `ResourceManager` and `FakeDataGenerator`, passes them to the `AttackChain`, and finally calls `attack_chain.run()`.

2. **Resource Provisioning:** `AttackChain.run()` first calls `ResourceManager` methods to create the necessary S3 bucket (for logging) and an initial IAM role, setting the stage for the attack.

3. **Reconnaissance (`ReconnaissanceStep`):**
   - **Action:** The attacker uses `boto3.client('iam').list_roles()` and `boto3.client('ec2').describe_instances()` to enumerate resources and understand the environment.
   - **Detection:** These initial API calls are logged in AWS CloudTrail, providing immediate visibility into suspicious reconnaissance activities from a new user or location.

4. **Privilege Escalation (`PrivilegeEscalationStep`):**
   - **Action:** The attacker uses `boto3.client('iam').create_role()` to attempt creating a new, highly privileged IAM role.
   - **Detection:** This action is a critical indicator of privilege escalation and is fully logged in CloudTrail. Security tools can flag the creation of a new role with excessive permissions as a high-severity alert.

5. **Lateral Movement (`LateralMovementStep`):**
   - **Action:** The attacker uses `boto3.client('ec2').describe_instances()` again to confirm their view of the environment and identify potential targets for resource deployment.
   - **Detection:** Continued enumeration from the new role can be correlated with the previous privilege escalation event, mapping out a clear lateral movement pattern in CloudTrail.

6. **Impact (`ImpactStep`):**
   - **Action:** The attacker launches a crypto-mining operation. In the simulation, this is achieved by calling the `ResourceManager` to provision a new EC2 spot instance (`create_spot_instance`). This instance is configured with a user-data script that would typically run crypto-mining software (e.g., stress, xmrig).
   - **Detection:** The launching of an EC2 instance by a newly created role is highly suspicious. Furthermore, any activity on the instance (like running mining tools) would be caught by an endpoint agent like Cortex XDR. The resource consumption and API calls are logged in CloudTrail.

## Detection and Security Integration
This simulation is designed to be detected by the Palo Alto Networks Cortex suite and XSIAM by analyzing the trail of evidence left in AWS CloudTrail and on the affected resources.

### How to Detect This Attack

**Cortex XDR Detection:**
- Suspicious Process Execution: Detects anomalous processes on the EC2 instance, such as stress or actual crypto-mining binaries (xmrig).
- File System Modifications: Alerts on the creation of suspicious cron jobs or backdoor scripts (e.g., in /etc/cron.d/backdoor).
- Network Activity: Flags unusual outbound network patterns consistent with mining pools.
- Privileged Container Execution: Identifies if the miner was deployed within a privileged container.

**Cortex Cloud Detection:**
- IAM Privilege Escalation: Immediately flags the CreateRole event as a potential threat.
- API Call Anomalies: Detects the unusual sequence of API calls (ListRoles -> CreateRole -> RunInstances) originating from a single user.
- CloudTrail Log Analysis: Continuously analyzes CloudTrail to identify deviations from normal behavior, such as API calls made from an unusual region.

**XSIAM Detection:**
- Security Event Correlation: Stitches together the disparate alerts from CloudTrail and Cortex XDR into a single, coherent attack story, linking the initial IAM reconnaissance to the eventual EC2 deployment.
- Automated Response: Can trigger automated playbooks to isolate the EC2 instance, disable the newly created IAM role, and suspend the compromised user credentials.
- Behavioral Analysis: Identifies that the pattern of API calls and resource creation is anomalous compared to the established baseline for the DevOps user group.

## Quickstart

### Clone the Repo & Enter Folder
```bash
git clone https://github.com/tomerzvi6/mining-the-cloud.git
cd mining-the-cloud/
```

### Configure AWS Credentials
```bash
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
```

### Deploy the Attack Scenario
This step uses Pulumi to provision the initial AWS resources needed for the attack.
```bash
pulumi up
```

### Run the Attack Chain (OOP Entrypoint)
This step executes the Python script that simulates the attacker's actions.
```bash
python main.py
```

### Monitor Attack Impact (Optional)
Run the real-time monitoring script to track attack progress:
```bash
python monitor_attack.py
```

### Verify Attack Success
After running the attack, verify its impact:
```bash
python verify_attack.py
```

## LLM Chatbot Simulation

This project includes an internal LLM-based chatbot that simulates how sensitive information, such as AWS credentials, can be leaked via prompt injection attacks. The chatbot is a general, home-made internal tool (not a commercial product) that mimics a real-world scenario where a DevOps engineer accidentally pastes credentials into a chat interface, and an attacker can later extract them using clever prompts. This tool demonstrates the risks of LLMs retaining sensitive context and the importance of securing internal AI assistants.

### Attack Simulation Flow
- The attacker creates a fake website using Bolt AI that mimics the internal LLM login page.
- The attacker sends a phishing email to a user, luring them to the fake site.
- The user enters their credentials into the fake site.
- The attacker uses the stolen credentials to log in to the real internal LLM website and perform prompt injection attacks to extract sensitive information.

### Running the Chatbot

To launch the chatbot interface, use Streamlit:

```bash
python -m streamlit run .\Acme_chatbot.py
```

This will open a web interface where you can interact with the simulated internal chatbot and experiment with prompt injection scenarios.

## Assessing Attack Impact

### How to Know if the Attack Worked

The attack simulation is designed to leave clear forensic artifacts that can be detected through multiple methods:

#### 1. **Built-in Impact Assessment**
The attack chain now includes automatic impact assessment that runs after the simulation completes. It checks for:
- ✅ IAM roles with "NullFrog" or "escalation" in the name
- ✅ EC2 instances tagged with attack indicators
- ✅ S3 buckets created for data exfiltration
- ✅ Security groups configured for the attack

#### 2. **Real-time Monitoring**
Use the monitoring script to track attack progress in real-time:
```bash
python monitor_attack.py
```
This will continuously check for new attack artifacts and alert you when they're detected.

#### 3. **Post-Attack Verification**
Run the verification script to check for all attack artifacts:
```bash
python verify_attack.py
```
This provides a comprehensive report of all detected attack indicators.

#### 4. **AWS Console Verification**
Manually check these resources in your AWS console:
- **IAM Roles**: Look for roles with "NullFrog" or "escalation" in the name
- **EC2 Instances**: Check for instances tagged with "NullFrog" or "CryptoMiningDemo"
- **S3 Buckets**: Look for buckets with "NullFrog" or "exfil" tags
- **Security Groups**: Check for security groups named "nullfrog-sg"

#### 5. **CloudTrail Analysis**
All attack actions are logged in AWS CloudTrail. Look for these events:
- `ListRoles` - Initial reconnaissance
- `CreateRole` - Privilege escalation
- `DescribeInstances` - Lateral movement
- `RunInstances` - Resource deployment
- `PutObject` - Data exfiltration

#### 6. **Security Tool Detection**
The attack is designed to be detected by:
- **Cortex XDR**: Suspicious process execution and file modifications
- **Cortex Cloud**: IAM privilege escalation and API call anomalies
- **XSIAM**: Security event correlation and behavioral analysis

### Success Indicators

The attack is considered successful if you see:
1. **IAM Role Creation**: A new role named "NullFrogEscalation" or similar
2. **Resource Deployment**: EC2 instances or S3 buckets with attack-related tags
3. **CloudTrail Events**: Suspicious API call patterns in the logs
4. **Security Alerts**: Detection by your security monitoring tools

### Failure Indicators

The attack may have failed if:
- No new IAM roles are created
- No EC2 instances are launched
- No suspicious CloudTrail events are logged
- All API calls return permission errors

## Note
This is a demonstration project for educational and security research purposes only. Always ensure you have explicit and proper authorization before running security tests in any environment.


