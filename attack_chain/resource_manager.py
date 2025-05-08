import pulumi
import pulumi_aws as aws

class ResourceManager:
    def __init__(self):
        self.security_group = None
        self.ecr_repo = None
        self.s3_bucket = None
        self.iam_role = None
        self.spot_instance = None

    def create_security_group(self):
        self.security_group = aws.ec2.SecurityGroup(
            "nullfrog-sg",
            description="Security group for attack demonstration",
            ingress=[
                {
                    "protocol": "tcp",
                    "from_port": 22,
                    "to_port": 22,
                    "cidr_blocks": ["0.0.0.0/0"],
                    "description": "SSH access - would be detected by Cortex XDR and XSIAM"
                },
                {
                    "protocol": "tcp",
                    "from_port": 80,
                    "to_port": 80,
                    "cidr_blocks": ["0.0.0.0/0"],
                    "description": "HTTP access - would be detected by Cortex XDR and XSIAM"
                }
            ],
            egress=[
                {
                    "protocol": "-1",
                    "from_port": 0,
                    "to_port": 0,
                    "cidr_blocks": ["0.0.0.0/0"],
                    "description": "All outbound traffic - would be detected by Cortex Cloud and XSIAM"
                }
            ],
            tags={
                "Name": "NullFrogMinerSG",
                "Environment": "Demo",
                "SecurityLevel": "High"
            }
        )
        return self.security_group

    def create_ecr_repository(self):
        self.ecr_repo = aws.ecr.Repository(
            "nullfrog-repo",
            name="nullfrog-miner",
            image_tag_mutability="MUTABLE",
            tags={
                "Purpose": "AttackDemo",
                "Owner": "NullFrog"
            }
        )
        return self.ecr_repo

    def create_s3_bucket(self):
        self.s3_bucket = aws.s3.Bucket(
            "nullfrog-exfil-bucket",
            acl="private",
            tags={
                "Purpose": "DataExfiltration",
                "Owner": "NullFrog"
            }
        )
        return self.s3_bucket

    def create_iam_role(self):
        # Minimal IAM role for EC2 with S3 and ECR access (for demo)
        assume_role_policy = '{"Version": "2012-10-17", "Statement": [{"Action": "sts:AssumeRole", "Principal": {"Service": "ec2.amazonaws.com"}, "Effect": "Allow", "Sid": ""}]}'
        self.iam_role = aws.iam.Role(
            "NullFrogProfile",
            assume_role_policy=assume_role_policy,
            tags={
                "Purpose": "AttackDemo",
                "Owner": "NullFrog"
            }
        )
        return self.iam_role

    def create_spot_instance(self, user_data_script, security_group_id, iam_instance_profile):
        base_ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["amazon"],
            filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}],
        )
        self.spot_instance = aws.ec2.SpotInstanceRequest(
            "tempModelTestingSpotInstance",
            instance_type="t3.micro",
            ami=base_ami.id,
            user_data=user_data_script,
            vpc_security_group_ids=[security_group_id],
            spot_type="one-time",
            instance_interruption_behavior="terminate",
            iam_instance_profile=iam_instance_profile,
            tags={
                "Name": "Temp_Model_Testing",
                "Owner": "NullFrog",
                "Purpose": "CryptoMiningDemo",
                "SecurityLevel": "High"
            },
        )
        return self.spot_instance 