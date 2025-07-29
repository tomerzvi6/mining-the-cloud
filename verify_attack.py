#!/usr/bin/env python3
"""
Attack Impact Verification Script
This script independently verifies whether the attack simulation was successful
by checking for the presence of attack artifacts in AWS.
"""

import boto3
import json
from datetime import datetime, timedelta

def check_cloudtrail_events():
    """Check CloudTrail for attack-related events"""
    print("\n=== CLOUDTRAIL EVENT ANALYSIS ===")
    
    try:
        # Check for recent CloudTrail events
        cloudtrail = boto3.client('cloudtrail')
        
        # Look for events in the last 24 hours
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        # Search for specific attack indicators
        attack_indicators = [
            'ListRoles',
            'CreateRole', 
            'DescribeInstances',
            'RunInstances',
            'PutObject'
        ]
        
        for indicator in attack_indicators:
            try:
                response = cloudtrail.lookup_events(
                    LookupAttributes=[
                        {
                            'AttributeKey': 'EventName',
                            'AttributeValue': indicator
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time
                )
                
                if response['Events']:
                    print(f"✅ Found {len(response['Events'])} {indicator} events:")
                    for event in response['Events'][:3]:  # Show first 3 events
                        print(f"   - {event['EventTime']}: {event['EventName']} by {event.get('Username', 'Unknown')}")
                else:
                    print(f"❌ No {indicator} events found in the last 24 hours")
                    
            except Exception as e:
                print(f"⚠️  Error checking {indicator} events: {e}")
                
    except Exception as e:
        print(f"❌ Error accessing CloudTrail: {e}")

def check_iam_roles():
    """Check for attack-related IAM roles"""
    print("\n=== IAM ROLE VERIFICATION ===")
    
    try:
        iam = boto3.client('iam')
        roles = iam.list_roles()
        
        attack_roles = []
        for role in roles['Roles']:
            if any(keyword in role['RoleName'].lower() for keyword in ['nullfrog', 'escalation', 'attack']):
                attack_roles.append(role)
        
        if attack_roles:
            print(f"✅ Found {len(attack_roles)} suspicious IAM roles:")
            for role in attack_roles:
                print(f"   - {role['RoleName']} (Created: {role['CreateDate']})")
        else:
            print("❌ No suspicious IAM roles found")
            
    except Exception as e:
        print(f"❌ Error checking IAM roles: {e}")

def check_ec2_instances():
    """Check for attack-related EC2 instances"""
    print("\n=== EC2 INSTANCE VERIFICATION ===")
    
    try:
        ec2 = boto3.client('ec2')
        instances = ec2.describe_instances()
        
        attack_instances = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                # Check instance tags for attack indicators
                if instance.get('Tags'):
                    for tag in instance['Tags']:
                        if any(keyword in tag['Value'].lower() for keyword in ['nullfrog', 'mining', 'attack', 'demo']):
                            attack_instances.append(instance)
                            break
                
                # Check instance name
                if instance.get('InstanceId') and any(keyword in instance['InstanceId'].lower() for keyword in ['nullfrog', 'attack']):
                    attack_instances.append(instance)
        
        if attack_instances:
            print(f"✅ Found {len(attack_instances)} suspicious EC2 instances:")
            for instance in attack_instances:
                print(f"   - {instance['InstanceId']} ({instance['State']['Name']})")
                if instance.get('Tags'):
                    for tag in instance['Tags']:
                        if tag['Key'] in ['Name', 'Owner', 'Purpose']:
                            print(f"     {tag['Key']}: {tag['Value']}")
        else:
            print("❌ No suspicious EC2 instances found")
            
    except Exception as e:
        print(f"❌ Error checking EC2 instances: {e}")

def check_s3_buckets():
    """Check for attack-related S3 buckets"""
    print("\n=== S3 BUCKET VERIFICATION ===")
    
    try:
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        
        attack_buckets = []
        for bucket in buckets['Buckets']:
            try:
                # Check bucket tags
                tags = s3.get_bucket_tagging(Bucket=bucket['Name'])
                for tag in tags['TagSet']:
                    if any(keyword in tag['Value'].lower() for keyword in ['nullfrog', 'attack', 'exfil']):
                        attack_buckets.append(bucket)
                        break
            except:
                # Check bucket name
                if any(keyword in bucket['Name'].lower() for keyword in ['nullfrog', 'attack', 'exfil']):
                    attack_buckets.append(bucket)
        
        if attack_buckets:
            print(f"✅ Found {len(attack_buckets)} suspicious S3 buckets:")
            for bucket in attack_buckets:
                print(f"   - {bucket['Name']} (Created: {bucket['CreationDate']})")
        else:
            print("❌ No suspicious S3 buckets found")
            
    except Exception as e:
        print(f"❌ Error checking S3 buckets: {e}")

def check_security_groups():
    """Check for attack-related security groups"""
    print("\n=== SECURITY GROUP VERIFICATION ===")
    
    try:
        ec2 = boto3.client('ec2')
        security_groups = ec2.describe_security_groups()
        
        attack_sgs = []
        for sg in security_groups['SecurityGroups']:
            # Check security group name and description
            if any(keyword in sg['GroupName'].lower() for keyword in ['nullfrog', 'attack', 'miner']):
                attack_sgs.append(sg)
            elif any(keyword in sg.get('Description', '').lower() for keyword in ['nullfrog', 'attack', 'miner']):
                attack_sgs.append(sg)
            # Check tags
            elif sg.get('Tags'):
                for tag in sg['Tags']:
                    if any(keyword in tag['Value'].lower() for keyword in ['nullfrog', 'attack', 'miner']):
                        attack_sgs.append(sg)
                        break
        
        if attack_sgs:
            print(f"✅ Found {len(attack_sgs)} suspicious security groups:")
            for sg in attack_sgs:
                print(f"   - {sg['GroupName']} ({sg['GroupId']})")
                print(f"     Description: {sg.get('Description', 'N/A')}")
        else:
            print("❌ No suspicious security groups found")
            
    except Exception as e:
        print(f"❌ Error checking security groups: {e}")

def generate_attack_report():
    """Generate a comprehensive attack impact report"""
    print("=" * 60)
    print("ATTACK IMPACT VERIFICATION REPORT")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Run all verification checks
    check_cloudtrail_events()
    check_iam_roles()
    check_ec2_instances()
    check_s3_buckets()
    check_security_groups()
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Review CloudTrail logs for suspicious API patterns")
    print("2. Check your security monitoring tools (Cortex XDR, Cortex Cloud, XSIAM)")
    print("3. Investigate any resources found with 'NullFrog' or attack-related tags")
    print("4. Consider implementing additional security controls")
    print("5. Clean up any test resources created during the simulation")

if __name__ == "__main__":
    generate_attack_report() 