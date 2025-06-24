from abc import ABC, abstractmethod
import boto3

class AttackStep(ABC):
    @abstractmethod
    def run(self):
        pass

class ReconnaissanceStep(AttackStep):
    def __init__(self, fake_data_generator):
        self.fake_data_generator = fake_data_generator

    def run(self):
        # This action will be logged in AWS CloudTrail
        iam = boto3.client('iam')
        ec2 = boto3.client('ec2')
        try:
            roles = iam.list_roles()
        except Exception as e:
            pass
        try:
            instances = ec2.describe_instances()
        except Exception as e:
            pass

class PrivilegeEscalationStep(AttackStep):
    def run(self):
        # This action will be logged in AWS CloudTrail
        iam = boto3.client('iam')
        try:
            iam.create_role(
                RoleName='NullFrogEscalation',
                AssumeRolePolicyDocument='{"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "ec2.amazonaws.com"}, "Action": "sts:AssumeRole"}]}',
                Description='Simulated privilege escalation role',
            )
        except Exception as e:
            pass

class LateralMovementStep(AttackStep):
    def __init__(self, fake_data_generator):
        self.fake_data_generator = fake_data_generator

    def run(self):
        # This action will be logged in AWS CloudTrail
        ec2 = boto3.client('ec2')
        try:
            ec2.describe_instances()
        except Exception as e:
            pass

class ImpactStep(AttackStep):
    def __init__(self, fake_data_generator):
        self.fake_data_generator = fake_data_generator

    def run(self):
        # This action will be logged in AWS CloudTrail
        s3 = boto3.client('s3')
        fake_data = self.fake_data_generator.generate_exfil_data()
        try:
            s3.put_object(Bucket=self.s3_bucket_name, Key='exfiltrated_data.txt', Body=fake_data)
        except Exception as e:
            pass #TODO: Log this to CloudTrail
