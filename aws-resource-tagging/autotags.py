#!/usr/bin/env python3

import boto3
import logging
import threading
from botocore.exceptions import ClientError

FORMAT = "[%(levelname)-s %(asctime)-s %(threadName)-s ] %(message)s"
logging.basicConfig(filename='ec2-tagging.logs', level=logging.INFO, format=FORMAT)


class AutoTagAWSResources(object):

    instances = {}

    def __init__(self, key, secret):
        """
        AWS Config Keys & Secrets
        :AWS KEY: key
        :AWS SECRET: secret
        """
        self.key = key
        self.secret = secret

    def get_connection(self, conn_type='client', region='us-east-1', resource='ec2'):
        """
        Returns AWS Python Boto3 Connection
        :params:conn_type: Boto3 Connection Type - client or resource - Default is client
        :params: region: AWS Region Name - Default if us-east-1
        :params: resource: Boto3 Resource Type - Default is ec2
        :returns boto3 connection:
        """
        logging.info("Starting a new connection for {} resource in {} region.".format(resource, region))
        try:
            if conn_type == 'resource':
                connection = boto3.resource(resource, aws_access_key_id=self.key, aws_secret_access_key=self.secret, region_name=region)
            else:
                connection = boto3.client(resource, aws_access_key_id=self.key, aws_secret_access_key=self.secret, region_name=region)
        except ClientError as e:
            logging.error("Connection Error : {}".format(e))
#        except Exception as e:
#            logging.error("Exception : {}".format(e))
        else:
            logging.info("Successfully Connected using {} Connection!!".format(conn_type))
            return connection

    def get_regions(self):
        """
        Returns the list of all AWS REGIONS
        :return: regions
        """
        conn = self.get_connection()
        try:
            logging.info("Fetching AWS Regions.")
            regions = [region['RegionName'] for region in conn.describe_regions()['Regions']]
        except ClientError as e:
            logging.error("Connection Error : {}".format(e))
        else:
            logging.info("Successfully Fetched AWS Regions!!")
            return regions

    def get_instances(self, region):
        """
        Returns a list of all the EC2 instances of given AWS Region
        :param: region: AWS Region
        :return: instances
        """
        conn = self.get_connection(region=region)
        try:
            logging.info("Fetching AWS EC2 list for {} Region".format(region))
            response = conn.describe_instances()
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    self.instances[instance['InstanceId']] = region
                    logging.info("Fetched {} EC2 instance of AWS {} Region".format(instance['InstanceId'], region))
        except ClientError as e:
            logging.error("Connection Error : {}".format(e))
        else:
            return self.instances

    def get_all_instances(self):
        """
        Returns a list of all the EC2 instances irrespective of the AWS Regions.
        :return: instances
        """
        threads = []
        regions = self.get_regions()
        for region in regions:
            thread = threading.Thread(target=self.get_instances, args=(region,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
        return self.instances

    def get_resource_owner(self, instance_id, region):
        """
        Returns the name of Owner who initially created the EC2 instance based on CloudTrail Events
        :param instance_id: EC2 Instance ID
        :param region: AWS Region Name
        :return owner: Owner of the EC2 instance
        """
        owner = None
        conn = self.get_connection(resource='cloudtrail', region=region)
        try:
            logging.info("Looking up events for {} EC2 instance in AWS {} Region".format(instance_id, region))
            response = conn.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName', 'AttributeValue': instance_id}])
            for a in range(0, len(response['Events'])):
                for b in range(0, (len(response['Events'][a]['Resources']))):
                    if response['Events'][a]['EventName'] == 'RunInstances' and response['Events'][a]['Resources'][b]['ResourceType'] == "AWS::EC2::Instance":
                        owner = response['Events'][a]['Username']
        except KeyError as e:
            logging.error("Unable to lookup for events : {}".format(e))
        else:
            return owner

    def update_ec2_tags(self, instance_id, region, **tags):
        """
        Update EC2 Instance tags
        :param instance_id: EC2 Instance ID
        :param region: AWS Region Name
        :param tags: Tags to set - "Owner=Vijay","OwnerEmail=vgosai@redhat.com","Environment=Production","CostCenter=711","Team=CP-DevOps"
        :return:
        """
        conn = self.get_connection(conn_type='resource', region=region)
        ec2info = conn.Instance(instance_id)
        logging.info("Starting EC2 Instance tagging for {} Instance in {} Region".format(instance_id, region))
        if ec2info.tags:
            if list(filter(lambda x: x['Key'] == "Owner", ec2info.tags)):
                logging.info("Owner tag is already present for EC {} instance, hence, no changes were made!!".format(instance_id))
                print("Owner tag is already present for EC {} instance, hence, no changes were made!!".format(instance_id))
            else:
                for k, v in tags.items():
                    conn.create_tags(Resources=[instance_id], Tags=[{'Key': k, 'Value': v}])
                    logging.info("Successfully added tags for EC2 {} instance".format(instance_id))
                print("Successfully added tags for EC2 {} instance".format(instance_id))
        else:
            for k, v in tags.items():
                conn.create_tags(Resources=[instance_id], Tags=[{'Key': k, 'Value': v}])
                logging.info("Successfully added tags for EC2 {} instance".format(instance_id))
            print("Successfully added tags for EC2 {} instance".format(instance_id))

        print("Tagging is Completed for EC {} Instance!!".format(instance_id))
