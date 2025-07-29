#!/usr/bin/env python3
"""
Real-time Attack Monitoring Script
This script monitors AWS resources in real-time to detect when the attack simulation
is successful and provides immediate feedback.
"""

import boto3
import time
import json
from datetime import datetime, timedelta

class AttackMonitor:
    def __init__(self):
        self.attack_indicators = {
            'iam_roles': [],
            'ec2_instances': [],
            's3_buckets': [],
            'security_groups': [],
            'cloudtrail_events': []
        }
        self.start_time = datetime.now()
        
    def check_iam_roles(self):
        """Check for new attack-related IAM roles"""
        try:
            iam = boto3.client('iam')
            roles = iam.list_roles()
            
            new_attack_roles = []
            for role in roles['Roles']:
                if any(keyword in role['RoleName'].lower() for keyword in ['nullfrog', 'escalation', 'attack']):
                    if role['RoleName'] not in [r['RoleName'] for r in self.attack_indicators['iam_roles']]:
                        new_attack_roles.append(role)
                        self.attack_indicators['iam_roles'].append(role)
            
            if new_attack_roles:
                print(f"🚨 NEW IAM ROLE DETECTED: {len(new_attack_roles)} attack-related roles created!")
                for role in new_attack_roles:
                    print(f"   - {role['RoleName']} (Created: {role['CreateDate']})")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error checking IAM roles: {e}")
            return False
    
    def check_ec2_instances(self):
        """Check for new attack-related EC2 instances"""
        try:
            ec2 = boto3.client('ec2')
            instances = ec2.describe_instances()
            
            new_attack_instances = []
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    # Check if this is an attack-related instance
                    is_attack_instance = False
                    if instance.get('Tags'):
                        for tag in instance['Tags']:
                            if any(keyword in tag['Value'].lower() for keyword in ['nullfrog', 'mining', 'attack', 'demo']):
                                is_attack_instance = True
                                break
                    
                    if is_attack_instance:
                        instance_id = instance['InstanceId']
                        if instance_id not in [i['InstanceId'] for i in self.attack_indicators['ec2_instances']]:
                            new_attack_instances.append(instance)
                            self.attack_indicators['ec2_instances'].append(instance)
            
            if new_attack_instances:
                print(f"🚨 NEW EC2 INSTANCE DETECTED: {len(new_attack_instances)} attack-related instances launched!")
                for instance in new_attack_instances:
                    print(f"   - {instance['InstanceId']} ({instance['State']['Name']})")
                    if instance.get('Tags'):
                        for tag in instance['Tags']:
                            if tag['Key'] in ['Name', 'Owner', 'Purpose']:
                                print(f"     {tag['Key']}: {tag['Value']}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error checking EC2 instances: {e}")
            return False
    
    def check_s3_buckets(self):
        """Check for new attack-related S3 buckets"""
        try:
            s3 = boto3.client('s3')
            buckets = s3.list_buckets()
            
            new_attack_buckets = []
            for bucket in buckets['Buckets']:
                # Check if this is an attack-related bucket
                is_attack_bucket = False
                try:
                    tags = s3.get_bucket_tagging(Bucket=bucket['Name'])
                    for tag in tags['TagSet']:
                        if any(keyword in tag['Value'].lower() for keyword in ['nullfrog', 'attack', 'exfil']):
                            is_attack_bucket = True
                            break
                except:
                    # Check bucket name
                    if any(keyword in bucket['Name'].lower() for keyword in ['nullfrog', 'attack', 'exfil']):
                        is_attack_bucket = True
                
                if is_attack_bucket:
                    bucket_name = bucket['Name']
                    if bucket_name not in [b['Name'] for b in self.attack_indicators['s3_buckets']]:
                        new_attack_buckets.append(bucket)
                        self.attack_indicators['s3_buckets'].append(bucket)
            
            if new_attack_buckets:
                print(f"🚨 NEW S3 BUCKET DETECTED: {len(new_attack_buckets)} attack-related buckets created!")
                for bucket in new_attack_buckets:
                    print(f"   - {bucket['Name']} (Created: {bucket['CreationDate']})")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error checking S3 buckets: {e}")
            return False
    
    def check_security_groups(self):
        """Check for new attack-related security groups"""
        try:
            ec2 = boto3.client('ec2')
            security_groups = ec2.describe_security_groups()
            
            new_attack_sgs = []
            for sg in security_groups['SecurityGroups']:
                # Check if this is an attack-related security group
                is_attack_sg = False
                if any(keyword in sg['GroupName'].lower() for keyword in ['nullfrog', 'attack', 'miner']):
                    is_attack_sg = True
                elif any(keyword in sg.get('Description', '').lower() for keyword in ['nullfrog', 'attack', 'miner']):
                    is_attack_sg = True
                elif sg.get('Tags'):
                    for tag in sg['Tags']:
                        if any(keyword in tag['Value'].lower() for keyword in ['nullfrog', 'attack', 'miner']):
                            is_attack_sg = True
                            break
                
                if is_attack_sg:
                    sg_id = sg['GroupId']
                    if sg_id not in [s['GroupId'] for s in self.attack_indicators['security_groups']]:
                        new_attack_sgs.append(sg)
                        self.attack_indicators['security_groups'].append(sg)
            
            if new_attack_sgs:
                print(f"🚨 NEW SECURITY GROUP DETECTED: {len(new_attack_sgs)} attack-related security groups created!")
                for sg in new_attack_sgs:
                    print(f"   - {sg['GroupName']} ({sg['GroupId']})")
                    print(f"     Description: {sg.get('Description', 'N/A')}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error checking security groups: {e}")
            return False
    
    def check_cloudtrail_events(self):
        """Check for recent attack-related CloudTrail events"""
        try:
            cloudtrail = boto3.client('cloudtrail')
            
            # Look for events in the last 5 minutes
            end_time = datetime.now()
            start_time = end_time - timedelta(minutes=5)
            
            attack_events = [
                'ListRoles',
                'CreateRole', 
                'DescribeInstances',
                'RunInstances',
                'PutObject'
            ]
            
            new_events = []
            for event_name in attack_events:
                try:
                    response = cloudtrail.lookup_events(
                        LookupAttributes=[
                            {
                                'AttributeKey': 'EventName',
                                'AttributeValue': event_name
                            }
                        ],
                        StartTime=start_time,
                        EndTime=end_time
                    )
                    
                    for event in response['Events']:
                        event_key = f"{event['EventTime']}_{event['EventName']}_{event.get('Username', 'Unknown')}"
                        if event_key not in [e['key'] for e in self.attack_indicators['cloudtrail_events']]:
                            new_events.append({
                                'key': event_key,
                                'event': event
                            })
                            self.attack_indicators['cloudtrail_events'].append({
                                'key': event_key,
                                'event': event
                            })
                            
                except Exception as e:
                    continue
            
            if new_events:
                print(f"🚨 NEW CLOUDTRAIL EVENTS DETECTED: {len(new_events)} suspicious API calls!")
                for event_data in new_events:
                    event = event_data['event']
                    print(f"   - {event['EventTime']}: {event['EventName']} by {event.get('Username', 'Unknown')}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error checking CloudTrail events: {e}")
            return False
    
    def generate_summary(self):
        """Generate a summary of all detected attack artifacts"""
        print("\n" + "=" * 60)
        print("ATTACK MONITORING SUMMARY")
        print("=" * 60)
        print(f"Monitoring started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        total_artifacts = (
            len(self.attack_indicators['iam_roles']) +
            len(self.attack_indicators['ec2_instances']) +
            len(self.attack_indicators['s3_buckets']) +
            len(self.attack_indicators['security_groups']) +
            len(self.attack_indicators['cloudtrail_events'])
        )
        
        print(f"Total attack artifacts detected: {total_artifacts}")
        print(f"- IAM Roles: {len(self.attack_indicators['iam_roles'])}")
        print(f"- EC2 Instances: {len(self.attack_indicators['ec2_instances'])}")
        print(f"- S3 Buckets: {len(self.attack_indicators['s3_buckets'])}")
        print(f"- Security Groups: {len(self.attack_indicators['security_groups'])}")
        print(f"- CloudTrail Events: {len(self.attack_indicators['cloudtrail_events'])}")
        
        if total_artifacts > 0:
            print("\n🎯 ATTACK SUCCESSFUL!")
            print("The simulation has successfully created attack artifacts.")
            print("Check your security monitoring tools for detection.")
        else:
            print("\n⏳ ATTACK IN PROGRESS...")
            print("No attack artifacts detected yet.")
            print("The simulation may still be running or has failed.")
    
    def monitor(self, duration_minutes=30, check_interval_seconds=10):
        """Monitor for attack indicators in real-time"""
        print("=" * 60)
        print("REAL-TIME ATTACK MONITORING")
        print("=" * 60)
        print(f"Monitoring for {duration_minutes} minutes")
        print(f"Check interval: {check_interval_seconds} seconds")
        print("Press Ctrl+C to stop monitoring early")
        print("=" * 60)
        
        end_time = self.start_time + timedelta(minutes=duration_minutes)
        
        try:
            while datetime.now() < end_time:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking for attack indicators...")
                
                # Check all indicators
                iam_detected = self.check_iam_roles()
                ec2_detected = self.check_ec2_instances()
                s3_detected = self.check_s3_buckets()
                sg_detected = self.check_security_groups()
                ct_detected = self.check_cloudtrail_events()
                
                if any([iam_detected, ec2_detected, s3_detected, sg_detected, ct_detected]):
                    print("🎯 ATTACK INDICATORS DETECTED!")
                else:
                    print("✅ No new attack indicators found")
                
                time.sleep(check_interval_seconds)
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Monitoring stopped by user")
        
        # Generate final summary
        self.generate_summary()

def main():
    monitor = AttackMonitor()
    monitor.monitor(duration_minutes=30, check_interval_seconds=10)

if __name__ == "__main__":
    main() 