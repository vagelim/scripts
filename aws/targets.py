#!/usr/bin/env python3
import sys
import boto3


def main(search, ip):
    """Takes a string "`search` and IP `ip`, updates all target groups to add `ip` to groups whose names contain `search` string, then deregisters unhealthy targets from same target groups."""
    lb = boto3.client('elbv2')
    tgs = lb.describe_target_groups()['TargetGroups']

    # Limit to target groups that contain search string
    match_tgs = [x for x in tgs if search in x['TargetGroupName']]

    for tg in match_tgs:
        # Register target
        lb.register_targets(TargetGroupArn=tg['TargetGroupArn'], Targets=[{'Id': ip}])

        # Find and deregister unhealthy targets
        unhealthy_targets = [x for x in lb.describe_target_health(TargetGroupArn=tg['TargetGroupArn'])['TargetHealthDescriptions'] if x['TargetHealth']['State'] == 'unhealthy']
        uh_targets = [x['Target'] for x in unhealthy_targets]
        if uh_targets:
            lb.deregister_targets(TargetGroupArn=tg['TargetGroupArn'], Targets=uh_targets)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Updates all matching target groups with given ip.\nUsage:\n\t{sys.argv[0]} target-group-string ip")
    else:
        main(sys.argv[1], sys.argv[2])
