from abc import ABC, abstractmethod
import boto3

class AttackStep(ABC):
    @abstractmethod
    def run(self):
        pass

class ReconnaissanceStep(AttackStep):
    def __init__(self, logger, fake_data_generator):
        self.logger = logger
        self.fake_data_generator = fake_data_generator

    def run(self):
        # This action will be logged in AWS CloudTrail
        self.logger.log_suspicious_activity("[Recon] Enumerating IAM roles and EC2 instances in me-south-1...")
        iam = boto3.client('iam')
        ec2 = boto3.client('ec2')
        try:
            roles = iam.list_roles()
            self.logger.log_suspicious_activity(f"[Recon] Found {len(roles.get('Roles', []))} IAM roles.")
        except Exception as e:
            self.logger.log_suspicious_activity(f"[Recon] IAM enumeration failed: {e}")
        try:
            instances = ec2.describe_instances()
            self.logger.log_suspicious_activity(f"[Recon] Found EC2 instances: {instances}")
        except Exception as e:
            self.logger.log_suspicious_activity(f"[Recon] EC2 enumeration failed: {e}")

class PrivilegeEscalationStep(AttackStep):
    def __init__(self, logger):
        self.logger = logger

    def run(self):
        # This action will be logged in AWS CloudTrail
        self.logger.log_suspicious_activity("[PrivEsc] Attempting to create a new IAM role...")
        iam = boto3.client('iam')
        try:
            iam.create_role(
                RoleName='NullFrogEscalation',
                AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}]}',
                Description='Simulated privilege escalation role',
            )
            self.logger.log_suspicious_activity("[PrivEsc] Created new IAM role NullFrogEscalation.")
        except Exception as e:
            self.logger.log_suspicious_activity(f"[PrivEsc] IAM role creation failed: {e}")

class LateralMovementStep(AttackStep):
    def __init__(self, logger, fake_data_generator):
        self.logger = logger
        self.fake_data_generator = fake_data_generator

    def run(self):
        # This action will be logged in AWS CloudTrail
        self.logger.log_suspicious_activity("[Lateral] Simulating container deployment and EC2 access...")
        # Simulate container deployment (log only)
        self.logger.log_suspicious_activity("[Lateral] Deployed privileged container (simulated).")
        # Simulate EC2 access
        ec2 = boto3.client('ec2')
        try:
            ec2.describe_instances()
            self.logger.log_suspicious_activity("[Lateral] Accessed EC2 instances (simulated).")
        except Exception as e:
            self.logger.log_suspicious_activity(f"[Lateral] EC2 access failed: {e}")

class ImpactStep(AttackStep):
    def __init__(self, logger, fake_data_generator):
        self.logger = logger
        self.fake_data_generator = fake_data_generator

    def run(self):
        # This action will be logged in AWS CloudTrail
        self.logger.log_suspicious_activity("[Impact] Simulating crypto-mining on EC2 instance...")
        # Simulate mining (log only)
        self.logger.log_suspicious_activity("[Impact] Started crypto-mining process (simulated).")
        # No S3 exfiltration, as the attack is focused on resource abuse

        # Simulate data exfiltration
        s3 = boto3.client('s3')
        fake_data = self.fake_data_generator.generate_exfil_data()
        try:
            s3.put_object(Bucket=self.s3_bucket_name, Key='exfiltrated_data.txt', Body=fake_data)
            self.logger.log_suspicious_activity(f"[Impact] Exfiltrated data to S3 bucket {self.s3_bucket_name}.")
        except Exception as e:
            self.logger.log_suspicious_activity(f"[Impact] Data exfiltration failed: {e}") 