#!/usr/bin/env python3
"""
AWS Unused Security Groups Identifier

This script identifies security groups in AWS that are not attached to any resources.
It checks for attachments across EC2 instances, RDS instances, ELB/ALB, Lambda functions,
and other AWS services that use security groups.
"""

import boto3
import json
import sys
from typing import List, Dict, Set
from botocore.exceptions import ClientError, NoCredentialsError


class UnusedSecurityGroupsFinder:
    def __init__(self, region_name: str = None):
        """
        Initialize the security groups finder.
        
        Args:
            region_name: AWS region to check. If None, uses default region.
        """
        try:
            self.session = boto3.Session()
            self.region = region_name or self.session.region_name or 'us-east-1'
            
            self.ec2_client = boto3.client('ec2', region_name=self.region)
            self.rds_client = boto3.client('rds', region_name=self.region)
            self.elbv2_client = boto3.client('elbv2', region_name=self.region)
            self.elb_client = boto3.client('elb', region_name=self.region)
            self.lambda_client = boto3.client('lambda', region_name=self.region)
            self.ecs_client = boto3.client('ecs', region_name=self.region)
            
        except NoCredentialsError:
            print("ERROR: AWS credentials not configured.")
            print("Please configure AWS credentials using one of these methods:")
            print("1. AWS CLI: aws configure")
            print("2. Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY")
            print("3. IAM roles (if running on EC2)")
            sys.exit(1)
    
    def get_all_security_groups(self) -> List[Dict]:
        """Get all security groups in the region."""
        try:
            response = self.ec2_client.describe_security_groups()
            return response['SecurityGroups']
        except ClientError as e:
            print(f"Error fetching security groups: {e}")
            return []
    
    def get_security_groups_used_by_ec2(self) -> Set[str]:
        """Get security group IDs used by EC2 instances."""
        used_sgs = set()
        try:
            paginator = self.ec2_client.get_paginator('describe_instances')
            for page in paginator.paginate():
                for reservation in page['Reservations']:
                    for instance in reservation['Instances']:
                        if instance['State']['Name'] != 'terminated':
                            for sg in instance.get('SecurityGroups', []):
                                used_sgs.add(sg['GroupId'])
        except ClientError as e:
            print(f"Error checking EC2 instances: {e}")
        
        return used_sgs
    
    def get_security_groups_used_by_rds(self) -> Set[str]:
        """Get security group IDs used by RDS instances."""
        used_sgs = set()
        try:
            paginator = self.rds_client.get_paginator('describe_db_instances')
            for page in paginator.paginate():
                for db_instance in page['DBInstances']:
                    for sg in db_instance.get('VpcSecurityGroups', []):
                        used_sgs.add(sg['VpcSecurityGroupId'])
            
            try:
                paginator = self.rds_client.get_paginator('describe_db_clusters')
                for page in paginator.paginate():
                    for cluster in page['DBClusters']:
                        for sg in cluster.get('VpcSecurityGroups', []):
                            used_sgs.add(sg['VpcSecurityGroupId'])
            except ClientError:
                pass  # Clusters might not be available in all regions
                
        except ClientError as e:
            print(f"Error checking RDS instances: {e}")
        
        return used_sgs
    
    def get_security_groups_used_by_load_balancers(self) -> Set[str]:
        """Get security group IDs used by load balancers."""
        used_sgs = set()
        
        try:
            paginator = self.elbv2_client.get_paginator('describe_load_balancers')
            for page in paginator.paginate():
                for lb in page['LoadBalancers']:
                    for sg_id in lb.get('SecurityGroups', []):
                        used_sgs.add(sg_id)
        except ClientError as e:
            print(f"Error checking ELBv2 load balancers: {e}")
        
        try:
            paginator = self.elb_client.get_paginator('describe_load_balancers')
            for page in paginator.paginate():
                for lb in page['LoadBalancerDescriptions']:
                    for sg_id in lb.get('SecurityGroups', []):
                        used_sgs.add(sg_id)
        except ClientError as e:
            print(f"Error checking ELB load balancers: {e}")
        
        return used_sgs
    
    def get_security_groups_used_by_lambda(self) -> Set[str]:
        """Get security group IDs used by Lambda functions."""
        used_sgs = set()
        try:
            paginator = self.lambda_client.get_paginator('list_functions')
            for page in paginator.paginate():
                for function in page['Functions']:
                    vpc_config = function.get('VpcConfig', {})
                    for sg_id in vpc_config.get('SecurityGroupIds', []):
                        used_sgs.add(sg_id)
        except ClientError as e:
            print(f"Error checking Lambda functions: {e}")
        
        return used_sgs
    
    def get_security_groups_used_by_ecs(self) -> Set[str]:
        """Get security group IDs used by ECS services."""
        used_sgs = set()
        try:
            clusters_response = self.ecs_client.list_clusters()
            
            for cluster_arn in clusters_response['clusterArns']:
                services_response = self.ecs_client.list_services(cluster=cluster_arn)
                
                if services_response['serviceArns']:
                    services_detail = self.ecs_client.describe_services(
                        cluster=cluster_arn,
                        services=services_response['serviceArns']
                    )
                    
                    for service in services_detail['services']:
                        network_config = service.get('networkConfiguration', {})
                        awsvpc_config = network_config.get('awsvpcConfiguration', {})
                        for sg_id in awsvpc_config.get('securityGroups', []):
                            used_sgs.add(sg_id)
        except ClientError as e:
            print(f"Error checking ECS services: {e}")
        
        return used_sgs
    
    def get_security_groups_used_by_network_interfaces(self) -> Set[str]:
        """Get security group IDs used by network interfaces (ENIs)."""
        used_sgs = set()
        try:
            paginator = self.ec2_client.get_paginator('describe_network_interfaces')
            for page in paginator.paginate():
                for eni in page['NetworkInterfaces']:
                    for sg in eni.get('Groups', []):
                        used_sgs.add(sg['GroupId'])
        except ClientError as e:
            print(f"Error checking network interfaces: {e}")
        
        return used_sgs
    
    def get_security_groups_referenced_by_rules(self) -> Set[str]:
        """Get security group IDs that are referenced by other security group rules."""
        referenced_sgs = set()
        try:
            all_sgs = self.get_all_security_groups()
            for sg in all_sgs:
                for rule in sg.get('IpPermissions', []):
                    for user_id_group_pair in rule.get('UserIdGroupPairs', []):
                        referenced_sgs.add(user_id_group_pair['GroupId'])
                
                for rule in sg.get('IpPermissionsEgress', []):
                    for user_id_group_pair in rule.get('UserIdGroupPairs', []):
                        referenced_sgs.add(user_id_group_pair['GroupId'])
        except ClientError as e:
            print(f"Error checking security group rules: {e}")
        
        return referenced_sgs
    
    def find_unused_security_groups(self) -> List[Dict]:
        """Find all unused security groups."""
        print(f"Analyzing security groups in region: {self.region}")
        print("This may take a few minutes...")
        
        all_sgs = self.get_all_security_groups()
        if not all_sgs:
            print("No security groups found or error occurred.")
            return []
        
        print(f"Found {len(all_sgs)} total security groups")
        
        print("Checking EC2 instances...")
        used_by_ec2 = self.get_security_groups_used_by_ec2()
        
        print("Checking RDS instances...")
        used_by_rds = self.get_security_groups_used_by_rds()
        
        print("Checking Load Balancers...")
        used_by_lb = self.get_security_groups_used_by_load_balancers()
        
        print("Checking Lambda functions...")
        used_by_lambda = self.get_security_groups_used_by_lambda()
        
        print("Checking ECS services...")
        used_by_ecs = self.get_security_groups_used_by_ecs()
        
        print("Checking Network Interfaces...")
        used_by_eni = self.get_security_groups_used_by_network_interfaces()
        
        print("Checking Security Group rule references...")
        referenced_in_rules = self.get_security_groups_referenced_by_rules()
        
        all_used_sgs = (used_by_ec2 | used_by_rds | used_by_lb | 
                       used_by_lambda | used_by_ecs | used_by_eni | 
                       referenced_in_rules)
        
        print(f"Found {len(all_used_sgs)} security groups in use")
        
        unused_sgs = []
        for sg in all_sgs:
            sg_id = sg['GroupId']
            sg_name = sg['GroupName']
            
            if sg_name == 'default':
                continue
                
            if sg_id not in all_used_sgs:
                unused_sgs.append({
                    'GroupId': sg_id,
                    'GroupName': sg_name,
                    'Description': sg.get('Description', ''),
                    'VpcId': sg.get('VpcId', 'EC2-Classic'),
                    'Tags': sg.get('Tags', [])
                })
        
        return unused_sgs
    
    def print_results(self, unused_sgs: List[Dict]):
        """Print the results in a formatted way."""
        if not unused_sgs:
            print("\n✅ No unused security groups found!")
            return
        
        print(f"\n🔍 Found {len(unused_sgs)} unused security groups:")
        print("=" * 80)
        
        for sg in unused_sgs:
            print(f"Security Group ID: {sg['GroupId']}")
            print(f"Name: {sg['GroupName']}")
            print(f"Description: {sg['Description']}")
            print(f"VPC ID: {sg['VpcId']}")
            
            if sg['Tags']:
                print("Tags:")
                for tag in sg['Tags']:
                    print(f"  {tag['Key']}: {tag['Value']}")
            else:
                print("Tags: None")
            
            print("-" * 40)
    
    def export_to_json(self, unused_sgs: List[Dict], filename: str = None):
        """Export results to JSON file."""
        if filename is None:
            filename = f"unused_security_groups_{self.region}.json"
        
        with open(filename, 'w') as f:
            json.dump(unused_sgs, f, indent=2, default=str)
        
        print(f"\n📄 Results exported to: {filename}")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Find unused AWS security groups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python unused_security_groups.py                    # Use default region
  python unused_security_groups.py --region us-west-2 # Specify region
  python unused_security_groups.py --export results.json # Export to file
        """
    )
    
    parser.add_argument(
        '--region', '-r',
        help='AWS region to check (default: from AWS config)'
    )
    
    parser.add_argument(
        '--export', '-e',
        help='Export results to JSON file'
    )
    
    parser.add_argument(
        '--all-regions', '-a',
        action='store_true',
        help='Check all available regions'
    )
    
    args = parser.parse_args()
    
    if args.all_regions:
        ec2 = boto3.client('ec2')
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        
        all_unused = []
        for region in regions:
            print(f"\n{'='*60}")
            print(f"Checking region: {region}")
            print('='*60)
            
            try:
                finder = UnusedSecurityGroupsFinder(region)
                unused_sgs = finder.find_unused_security_groups()
                finder.print_results(unused_sgs)
                
                for sg in unused_sgs:
                    sg['Region'] = region
                all_unused.extend(unused_sgs)
                
            except Exception as e:
                print(f"Error checking region {region}: {e}")
        
        if args.export:
            with open(args.export, 'w') as f:
                json.dump(all_unused, f, indent=2, default=str)
            print(f"\n📄 All results exported to: {args.export}")
        
        print(f"\n🔍 Total unused security groups across all regions: {len(all_unused)}")
    
    else:
        finder = UnusedSecurityGroupsFinder(args.region)
        unused_sgs = finder.find_unused_security_groups()
        finder.print_results(unused_sgs)
        
        if args.export:
            finder.export_to_json(unused_sgs, args.export)


if __name__ == "__main__":
    main()
