from autotags import AutoTagAWSResources
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]', description='Python Boto3 AWS Framework')
    parser.add_argument('--key', action='store', dest='key', help='AWS Key')
    parser.add_argument('--secret', action='store', dest='secret', help='AWS Secret')
    args = parser.parse_args()

    if args.key is None:
        raise ValueError("Error: AWS Key is missing!")
    elif args.secret is None:
        raise ValueError("Error: AWS Secret is missing!")

    ec2conn = AutoTagAWSResources(key=args.key, secret=args.secret)
    instances = ec2conn.get_all_instances()
    for instance_id, region in instances.items():
        print(instance_id, region)
        owner = ec2conn.get_resource_owner(instance_id, region)
        print(owner)
