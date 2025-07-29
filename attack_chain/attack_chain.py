from .resource_manager import ResourceManager
from .steps import ReconnaissanceStep, PrivilegeEscalationStep, LateralMovementStep, ImpactStep
import boto3

class AttackChain:
    def __init__(self, resource_manager: ResourceManager, fake_data_generator):
        self.resource_manager = resource_manager
        self.fake_data_generator = fake_data_generator

    def reconnaissance(self):
        step = ReconnaissanceStep(self.fake_data_generator)
        step.run()

    def privilege_escalation(self):
        step = PrivilegeEscalationStep()
        step.run()

    def lateral_movement(self):
        step = LateralMovementStep(self.fake_data_generator)
        step.run()

    def impact(self):
        step = ImpactStep(self.fake_data_generator)
        step.run()

    def assess_impact(self):
        """Assess the impact of the attack by verifying created resources"""
        print("\n=== ATTACK IMPACT ASSESSMENT ===")
        
        # Check IAM roles
        try:
            iam = boto3.client('iam')
            roles = iam.list_roles()
            nullfrog_roles = [role for role in roles['Roles'] if 'NullFrog' in role['RoleName']]
            if nullfrog_roles:
                print(f"✅ PRIVILEGE ESCALATION SUCCESSFUL: Found {len(nullfrog_roles)} NullFrog roles")
                for role in nullfrog_roles:
                    print(f"   - {role['RoleName']}")
            else:
                print("❌ PRIVILEGE ESCALATION FAILED: No NullFrog roles found")
        except Exception as e:
            print(f"❌ ERROR checking IAM roles: {e}")

        # Check EC2 instances
        try:
            ec2 = boto3.client('ec2')
            instances = ec2.describe_instances()
            nullfrog_instances = []
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    if instance.get('Tags'):
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Owner' and 'NullFrog' in tag['Value']:
                                nullfrog_instances.append(instance)
            
            if nullfrog_instances:
                print(f"✅ IMPACT SUCCESSFUL: Found {len(nullfrog_instances)} NullFrog instances")
                for instance in nullfrog_instances:
                    print(f"   - Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
            else:
                print("❌ IMPACT FAILED: No NullFrog instances found")
        except Exception as e:
            print(f"❌ ERROR checking EC2 instances: {e}")

        # Check S3 buckets
        try:
            s3 = boto3.client('s3')
            buckets = s3.list_buckets()
            nullfrog_buckets = []
            for bucket in buckets['Buckets']:
                try:
                    tags = s3.get_bucket_tagging(Bucket=bucket['Name'])
                    for tag in tags['TagSet']:
                        if tag['Key'] == 'Owner' and 'NullFrog' in tag['Value']:
                            nullfrog_buckets.append(bucket)
                except:
                    continue
            
            if nullfrog_buckets:
                print(f"✅ DATA EXFILTRATION SETUP: Found {len(nullfrog_buckets)} NullFrog S3 buckets")
                for bucket in nullfrog_buckets:
                    print(f"   - {bucket['Name']}")
            else:
                print("❌ DATA EXFILTRATION SETUP FAILED: No NullFrog S3 buckets found")
        except Exception as e:
            print(f"❌ ERROR checking S3 buckets: {e}")

        # Check security groups
        try:
            security_groups = ec2.describe_security_groups()
            nullfrog_sgs = []
            for sg in security_groups['SecurityGroups']:
                if sg.get('Tags'):
                    for tag in sg['Tags']:
                        if tag['Key'] == 'Name' and 'NullFrog' in tag['Value']:
                            nullfrog_sgs.append(sg)
            
            if nullfrog_sgs:
                print(f"✅ INFRASTRUCTURE SETUP: Found {len(nullfrog_sgs)} NullFrog security groups")
                for sg in nullfrog_sgs:
                    print(f"   - {sg['GroupName']} ({sg['GroupId']})")
            else:
                print("❌ INFRASTRUCTURE SETUP FAILED: No NullFrog security groups found")
        except Exception as e:
            print(f"❌ ERROR checking security groups: {e}")

        print("\n=== CLOUDTRAIL DETECTION ===")
        print("All API calls have been logged to AWS CloudTrail.")
        print("Check your security monitoring tools for:")
        print("- Suspicious API call patterns")
        print("- Unusual resource creation")
        print("- Privilege escalation attempts")
        print("- Geographic anomalies")

    def run(self):
        # --- STORY CONTEXT ---
        # The attacker obtained AWS credentials by accessing the in-org LLM (Large Language Model) web interface.
        # The DevOps user had once pasted their AWS access and secret key into the LLM, which was saved in its memory.
        # The attacker gained access to the LLM via a stolen session cookie and used prompt injection to extract the keys.
        # These long-term credentials (no MFA) are now used to attack the us-east-1 region.
        # ----------------------
        # Create resources first
        sg = self.resource_manager.create_security_group()
        ecr = self.resource_manager.create_ecr_repository()
        s3 = self.resource_manager.create_s3_bucket()
        iam_role = self.resource_manager.create_iam_role()
        # Simulate attack chain
        self.reconnaissance()
        self.privilege_escalation()
        self.lateral_movement()
        self.impact()
        # Assess the impact
        self.assess_impact() 