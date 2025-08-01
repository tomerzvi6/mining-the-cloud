from abc import ABC, abstractmethod
import boto3
from .logger import AttackLogger

class AttackStep(ABC):
    @abstractmethod
    def run(self):
        pass

class ReconnaissanceStep(AttackStep):
    def __init__(self, fake_data_generator):
        self.fake_data_generator = fake_data_generator
        self.logger = AttackLogger()

    def run(self):
        # This action will be logged in AWS CloudTrail
        self.logger.log_reconnaissance("IAM Roles", "boto3.list_roles()")
        self.logger.log_reconnaissance("EC2 Instances", "boto3.describe_instances()")
        
        iam = boto3.client('iam')
        ec2 = boto3.client('ec2')
        try:
            roles = iam.list_roles()
            self.logger.log_cloudtrail_event("ListRoles", "IAM")
        except Exception as e:
            pass
        try:
            instances = ec2.describe_instances()
            self.logger.log_cloudtrail_event("DescribeInstances", "EC2")
        except Exception as e:
            pass

class PrivilegeEscalationStep(AttackStep):
    def __init__(self):
        self.logger = AttackLogger()
        
    def run(self):
        # This action will be logged in AWS CloudTrail
        role_name = 'NullFrogEscalation'
        self.logger.log_privilege_escalation(role_name)
        
        iam = boto3.client('iam')
        try:
            iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}]}',
                Description='Simulated privilege escalation role',
            )
            self.logger.log_cloudtrail_event("CreateRole", f"IAM Role: {role_name}")
        except Exception as e:
            pass

class LateralMovementStep(AttackStep):
    def __init__(self, fake_data_generator):
        self.fake_data_generator = fake_data_generator
        self.logger = AttackLogger()

    def run(self):
        # This action will be logged in AWS CloudTrail
        self.logger.log_lateral_movement("EC2 Environment")
        
        ec2 = boto3.client('ec2')
        try:
            ec2.describe_instances()
            self.logger.log_cloudtrail_event("DescribeInstances", "EC2 (Lateral Movement)")
        except Exception as e:
            pass

class ImpactStep(AttackStep):
    def __init__(self, fake_data_generator):
        self.fake_data_generator = fake_data_generator
        self.logger = AttackLogger()

    def run(self):
        # This action will be logged in AWS CloudTrail
        self.logger.log_impact("Data Exfiltration", "S3 Bucket")
        
        s3 = boto3.client('s3')
        fake_data = self.fake_data_generator.generate_exfil_data()
        
        # Try to find a bucket with "nullfrog" in the name (created by ResourceManager)
        try:
            buckets = s3.list_buckets()
            target_bucket = None
            for bucket in buckets['Buckets']:
                if 'nullfrog' in bucket['Name'].lower():
                    target_bucket = bucket['Name']
                    break
            
            if target_bucket:
                s3.put_object(Bucket=target_bucket, Key='exfiltrated_data.txt', Body=fake_data)
                self.logger.log_cloudtrail_event("PutObject", f"S3 Bucket: {target_bucket}")
            else:
                self.logger.log_attack_step("IMPACT", "No suitable S3 bucket found for data exfiltration")
        except Exception as e:
            self.logger.log_attack_step("IMPACT", f"Failed to exfiltrate data: {str(e)}")
