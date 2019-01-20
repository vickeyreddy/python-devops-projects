#!/usr/bin/env python3

import argparse
from autotags import AutoTagAWSResources


def main(key, secret, region):
    ec2conn = AutoTagAWSResources(key=key, secret=secret)
    instances = ec2conn.get_instances(region=region)
    for instance_id, region in instances.items():
        owner = ec2conn.get_resource_owner(instance_id, region)
        ec2conn.update_ec2_tags(instance_id, region, Owner="{}".format(owner), OwnerEmail="{}@redhat.com".format(owner), Project="None", CostCode="None", Purpose="None", Role="None", Environment="None")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]', description='Python Boto3 AWS Framework')
    parser.add_argument('--key', action='store', dest='key', help='AWS Key')
    parser.add_argument('--secret', action='store', dest='secret', help='AWS Secret')
    parser.add_argument('--region', action='store', dest='region', default='us-east-1', help='AWS Region')

    args = parser.parse_args()

    if args.key is None:
        raise ValueError("Error: AWS Key cannot be Null!")
    elif args.secret is None:
        raise ValueError("Error: AWS Secret cannot be Null!")
    elif args.region is None:
        raise ValueError("Error: AWS Region cannot be Null!")
    main(args.key, args.secret, args.region)
