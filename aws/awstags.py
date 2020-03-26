#!/usr/bin/env python3
#
# Check EC2 objects for desired tag. If found, print the object ID followed by
# the tag value. Otherwise, print the name and null.
#
# Author: Justin Cook <jhcook@secnix.com>

import argparse, json, sys

try:
  import boto3
  from botocore.exceptions import ClientError
except ImportError as e:
  print(e)
  sys.exit(1)

def parse_args():
  """Parse the command-line arguments and return accordingly. Nothing special
  here.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument("tag_names", help="comma-separated list of tags",
                      type=str)
  parser.add_argument("aws_region", help="AWS region to interrogate",
                      type=str)
  parser.add_argument("aws_profile", help="AWS profile to use", type=str)
  return parser.parse_args()

def search_tags(tag_names, obj):
  for tag_name in tag_names:
    print(f"{tag_name}:", end=" ")
    try:
      for tag in obj['Tags']:
        if tag['Key'] == tag_name:
          print(f"{tag['Value']}")
          break
      else:
        print("null")
    except KeyError:
      print("null")

def fetch_instances(ec2):
  """Get the instances
  {
    'Reservations': [
        {
            'Groups': [
                {
                    'GroupName': 'string',
                    'GroupId': 'string'
                },
            ],
            'Instances': [
                {
                    'AmiLaunchIndex': 123,
                    'ImageId': 'string',
                    'InstanceId': 'string',
                    'InstanceType': 't1.micro'|'t2.nano'|'t2.micro'|'t2.small'|'t2.medium'|'t2.large'|'t2.xlarge'|'t2.2xlarge'|'t3.nano'|'t3.micro'|'t3.small'|'t3.medium'|'t3.large'|'t3.xlarge'|'t3.2xlarge'|'t3a.nano'|'t3a.micro'|'t3a.small'|'t3a.medium'|'t3a.large'|'t3a.xlarge'|'t3a.2xlarge'|'m1.small'|'m1.medium'|'m1.large'|'m1.xlarge'|'m3.medium'|'m3.large'|'m3.xlarge'|'m3.2xlarge'|'m4.large'|'m4.xlarge'|'m4.2xlarge'|'m4.4xlarge'|'m4.10xlarge'|'m4.16xlarge'|'m2.xlarge'|'m2.2xlarge'|'m2.4xlarge'|'cr1.8xlarge'|'r3.large'|'r3.xlarge'|'r3.2xlarge'|'r3.4xlarge'|'r3.8xlarge'|'r4.large'|'r4.xlarge'|'r4.2xlarge'|'r4.4xlarge'|'r4.8xlarge'|'r4.16xlarge'|'r5.large'|'r5.xlarge'|'r5.2xlarge'|'r5.4xlarge'|'r5.8xlarge'|'r5.12xlarge'|'r5.16xlarge'|'r5.24xlarge'|'r5.metal'|'r5a.large'|'r5a.xlarge'|'r5a.2xlarge'|'r5a.4xlarge'|'r5a.8xlarge'|'r5a.12xlarge'|'r5a.16xlarge'|'r5a.24xlarge'|'r5d.large'|'r5d.xlarge'|'r5d.2xlarge'|'r5d.4xlarge'|'r5d.8xlarge'|'r5d.12xlarge'|'r5d.16xlarge'|'r5d.24xlarge'|'r5d.metal'|'r5ad.large'|'r5ad.xlarge'|'r5ad.2xlarge'|'r5ad.4xlarge'|'r5ad.8xlarge'|'r5ad.12xlarge'|'r5ad.16xlarge'|'r5ad.24xlarge'|'x1.16xlarge'|'x1.32xlarge'|'x1e.xlarge'|'x1e.2xlarge'|'x1e.4xlarge'|'x1e.8xlarge'|'x1e.16xlarge'|'x1e.32xlarge'|'i2.xlarge'|'i2.2xlarge'|'i2.4xlarge'|'i2.8xlarge'|'i3.large'|'i3.xlarge'|'i3.2xlarge'|'i3.4xlarge'|'i3.8xlarge'|'i3.16xlarge'|'i3.metal'|'i3en.large'|'i3en.xlarge'|'i3en.2xlarge'|'i3en.3xlarge'|'i3en.6xlarge'|'i3en.12xlarge'|'i3en.24xlarge'|'i3en.metal'|'hi1.4xlarge'|'hs1.8xlarge'|'c1.medium'|'c1.xlarge'|'c3.large'|'c3.xlarge'|'c3.2xlarge'|'c3.4xlarge'|'c3.8xlarge'|'c4.large'|'c4.xlarge'|'c4.2xlarge'|'c4.4xlarge'|'c4.8xlarge'|'c5.large'|'c5.xlarge'|'c5.2xlarge'|'c5.4xlarge'|'c5.9xlarge'|'c5.12xlarge'|'c5.18xlarge'|'c5.24xlarge'|'c5.metal'|'c5d.large'|'c5d.xlarge'|'c5d.2xlarge'|'c5d.4xlarge'|'c5d.9xlarge'|'c5d.12xlarge'|'c5d.18xlarge'|'c5d.24xlarge'|'c5d.metal'|'c5n.large'|'c5n.xlarge'|'c5n.2xlarge'|'c5n.4xlarge'|'c5n.9xlarge'|'c5n.18xlarge'|'cc1.4xlarge'|'cc2.8xlarge'|'g2.2xlarge'|'g2.8xlarge'|'g3.4xlarge'|'g3.8xlarge'|'g3.16xlarge'|'g3s.xlarge'|'g4dn.xlarge'|'g4dn.2xlarge'|'g4dn.4xlarge'|'g4dn.8xlarge'|'g4dn.12xlarge'|'g4dn.16xlarge'|'cg1.4xlarge'|'p2.xlarge'|'p2.8xlarge'|'p2.16xlarge'|'p3.2xlarge'|'p3.8xlarge'|'p3.16xlarge'|'p3dn.24xlarge'|'d2.xlarge'|'d2.2xlarge'|'d2.4xlarge'|'d2.8xlarge'|'f1.2xlarge'|'f1.4xlarge'|'f1.16xlarge'|'m5.large'|'m5.xlarge'|'m5.2xlarge'|'m5.4xlarge'|'m5.8xlarge'|'m5.12xlarge'|'m5.16xlarge'|'m5.24xlarge'|'m5.metal'|'m5a.large'|'m5a.xlarge'|'m5a.2xlarge'|'m5a.4xlarge'|'m5a.8xlarge'|'m5a.12xlarge'|'m5a.16xlarge'|'m5a.24xlarge'|'m5d.large'|'m5d.xlarge'|'m5d.2xlarge'|'m5d.4xlarge'|'m5d.8xlarge'|'m5d.12xlarge'|'m5d.16xlarge'|'m5d.24xlarge'|'m5d.metal'|'m5ad.large'|'m5ad.xlarge'|'m5ad.2xlarge'|'m5ad.4xlarge'|'m5ad.8xlarge'|'m5ad.12xlarge'|'m5ad.16xlarge'|'m5ad.24xlarge'|'h1.2xlarge'|'h1.4xlarge'|'h1.8xlarge'|'h1.16xlarge'|'z1d.large'|'z1d.xlarge'|'z1d.2xlarge'|'z1d.3xlarge'|'z1d.6xlarge'|'z1d.12xlarge'|'z1d.metal'|'u-6tb1.metal'|'u-9tb1.metal'|'u-12tb1.metal'|'u-18tb1.metal'|'u-24tb1.metal'|'a1.medium'|'a1.large'|'a1.xlarge'|'a1.2xlarge'|'a1.4xlarge'|'a1.metal'|'m5dn.large'|'m5dn.xlarge'|'m5dn.2xlarge'|'m5dn.4xlarge'|'m5dn.8xlarge'|'m5dn.12xlarge'|'m5dn.16xlarge'|'m5dn.24xlarge'|'m5n.large'|'m5n.xlarge'|'m5n.2xlarge'|'m5n.4xlarge'|'m5n.8xlarge'|'m5n.12xlarge'|'m5n.16xlarge'|'m5n.24xlarge'|'r5dn.large'|'r5dn.xlarge'|'r5dn.2xlarge'|'r5dn.4xlarge'|'r5dn.8xlarge'|'r5dn.12xlarge'|'r5dn.16xlarge'|'r5dn.24xlarge'|'r5n.large'|'r5n.xlarge'|'r5n.2xlarge'|'r5n.4xlarge'|'r5n.8xlarge'|'r5n.12xlarge'|'r5n.16xlarge'|'r5n.24xlarge'|'inf1.xlarge'|'inf1.2xlarge'|'inf1.6xlarge'|'inf1.24xlarge',
                    'KernelId': 'string',
                    'KeyName': 'string',
                    'LaunchTime': datetime(2015, 1, 1),
                    'Monitoring': {
                        'State': 'disabled'|'disabling'|'enabled'|'pending'
                    },
                    'Placement': {
                        'AvailabilityZone': 'string',
                        'Affinity': 'string',
                        'GroupName': 'string',
                        'PartitionNumber': 123,
                        'HostId': 'string',
                        'Tenancy': 'default'|'dedicated'|'host',
                        'SpreadDomain': 'string',
                        'HostResourceGroupArn': 'string'
                    },
                    'Platform': 'Windows',
                    'PrivateDnsName': 'string',
                    'PrivateIpAddress': 'string',
                    'ProductCodes': [
                        {
                            'ProductCodeId': 'string',
                            'ProductCodeType': 'devpay'|'marketplace'
                        },
                    ],
                    'PublicDnsName': 'string',
                    'PublicIpAddress': 'string',
                    'RamdiskId': 'string',
                    'State': {
                        'Code': 123,
                        'Name': 'pending'|'running'|'shutting-down'|'terminated'|'stopping'|'stopped'
                    },
                    'StateTransitionReason': 'string',
                    'SubnetId': 'string',
                    'VpcId': 'string',
                    'Architecture': 'i386'|'x86_64'|'arm64',
                    'BlockDeviceMappings': [
                        {
                            'DeviceName': 'string',
                            'Ebs': {
                                'AttachTime': datetime(2015, 1, 1),
                                'DeleteOnTermination': True|False,
                                'Status': 'attaching'|'attached'|'detaching'|'detached',
                                'VolumeId': 'string'
                            }
                        },
                    ],
                    'ClientToken': 'string',
                    'EbsOptimized': True|False,
                    'EnaSupport': True|False,
                    'Hypervisor': 'ovm'|'xen',
                    'IamInstanceProfile': {
                        'Arn': 'string',
                        'Id': 'string'
                    },
                    'InstanceLifecycle': 'spot'|'scheduled',
                    'ElasticGpuAssociations': [
                        {
                            'ElasticGpuId': 'string',
                            'ElasticGpuAssociationId': 'string',
                            'ElasticGpuAssociationState': 'string',
                            'ElasticGpuAssociationTime': 'string'
                        },
                    ],
                    'ElasticInferenceAcceleratorAssociations': [
                        {
                            'ElasticInferenceAcceleratorArn': 'string',
                            'ElasticInferenceAcceleratorAssociationId': 'string',
                            'ElasticInferenceAcceleratorAssociationState': 'string',
                            'ElasticInferenceAcceleratorAssociationTime': datetime(2015, 1, 1)
                        },
                    ],
                    'NetworkInterfaces': [
                        {
                            'Association': {
                                'IpOwnerId': 'string',
                                'PublicDnsName': 'string',
                                'PublicIp': 'string'
                            },
                            'Attachment': {
                                'AttachTime': datetime(2015, 1, 1),
                                'AttachmentId': 'string',
                                'DeleteOnTermination': True|False,
                                'DeviceIndex': 123,
                                'Status': 'attaching'|'attached'|'detaching'|'detached'
                            },
                            'Description': 'string',
                            'Groups': [
                                {
                                    'GroupName': 'string',
                                    'GroupId': 'string'
                                },
                            ],
                            'Ipv6Addresses': [
                                {
                                    'Ipv6Address': 'string'
                                },
                            ],
                            'MacAddress': 'string',
                            'NetworkInterfaceId': 'string',
                            'OwnerId': 'string',
                            'PrivateDnsName': 'string',
                            'PrivateIpAddress': 'string',
                            'PrivateIpAddresses': [
                                {
                                    'Association': {
                                        'IpOwnerId': 'string',
                                        'PublicDnsName': 'string',
                                        'PublicIp': 'string'
                                    },
                                    'Primary': True|False,
                                    'PrivateDnsName': 'string',
                                    'PrivateIpAddress': 'string'
                                },
                            ],
                            'SourceDestCheck': True|False,
                            'Status': 'available'|'associated'|'attaching'|'in-use'|'detaching',
                            'SubnetId': 'string',
                            'VpcId': 'string',
                            'InterfaceType': 'string'
                        },
                    ],
                    'OutpostArn': 'string',
                    'RootDeviceName': 'string',
                    'RootDeviceType': 'ebs'|'instance-store',
                    'SecurityGroups': [
                        {
                            'GroupName': 'string',
                            'GroupId': 'string'
                        },
                    ],
                    'SourceDestCheck': True|False,
                    'SpotInstanceRequestId': 'string',
                    'SriovNetSupport': 'string',
                    'StateReason': {
                        'Code': 'string',
                        'Message': 'string'
                    },
                    'Tags': [
                        {
                            'Key': 'string',
                            'Value': 'string'
                        },
                    ],
                    'VirtualizationType': 'hvm'|'paravirtual',
                    'CpuOptions': {
                        'CoreCount': 123,
                        'ThreadsPerCore': 123
                    },
                    'CapacityReservationId': 'string',
                    'CapacityReservationSpecification': {
                        'CapacityReservationPreference': 'open'|'none',
                        'CapacityReservationTarget': {
                            'CapacityReservationId': 'string'
                        }
                    },
                    'HibernationOptions': {
                        'Configured': True|False
                    },
                    'Licenses': [
                        {
                            'LicenseConfigurationArn': 'string'
                        },
                    ],
                    'MetadataOptions': {
                        'State': 'pending'|'applied',
                        'HttpTokens': 'optional'|'required',
                        'HttpPutResponseHopLimit': 123,
                        'HttpEndpoint': 'disabled'|'enabled'
                    }
                },
            ],
            'OwnerId': 'string',
            'RequesterId': 'string',
            'ReservationId': 'string'
        },
    ],
    'NextToken': 'string'
  }
  """
  return ec2.describe_instances()

def fetch_volumes(ec2):
  """Get the volumes
  {
    'Volumes': [
        {
            'Attachments': [
                {
                    'AttachTime': datetime(2015, 1, 1),
                    'Device': 'string',
                    'InstanceId': 'string',
                    'State': 'attaching'|'attached'|'detaching'|'detached'|'busy',
                    'VolumeId': 'string',
                    'DeleteOnTermination': True|False
                },
            ],
            'AvailabilityZone': 'string',
            'CreateTime': datetime(2015, 1, 1),
            'Encrypted': True|False,
            'KmsKeyId': 'string',
            'OutpostArn': 'string',
            'Size': 123,
            'SnapshotId': 'string',
            'State': 'creating'|'available'|'in-use'|'deleting'|'deleted'|'error',
            'VolumeId': 'string',
            'Iops': 123,
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            'VolumeType': 'standard'|'io1'|'gp2'|'sc1'|'st1',
            'FastRestored': True|False,
            'MultiAttachEnabled': True|False
        },
    ],
    'NextToken': 'string'
}
"""
  return ec2.describe_volumes()

def fetch_snapshots(ec2, account_id):
  """Get the snapshots
  {
    'Snapshots': [
        {
            'DataEncryptionKeyId': 'string',
            'Description': 'string',
            'Encrypted': True|False,
            'KmsKeyId': 'string',
            'OwnerId': 'string',
            'Progress': 'string',
            'SnapshotId': 'string',
            'StartTime': datetime(2015, 1, 1),
            'State': 'pending'|'completed'|'error',
            'StateMessage': 'string',
            'VolumeId': 'string',
            'VolumeSize': 123,
            'OwnerAlias': 'string',
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },
    ],
    'NextToken': 'string'
  }
  """
  return ec2.describe_snapshots(OwnerIds = [account_id,])

def fetch_amis(ec2):
  """Get the AMIs
  {
    'Images': [
        {
            'Architecture': 'i386'|'x86_64'|'arm64',
            'CreationDate': 'string',
            'ImageId': 'string',
            'ImageLocation': 'string',
            'ImageType': 'machine'|'kernel'|'ramdisk',
            'Public': True|False,
            'KernelId': 'string',
            'OwnerId': 'string',
            'Platform': 'Windows',
            'PlatformDetails': 'string',
            'UsageOperation': 'string',
            'ProductCodes': [
                {
                    'ProductCodeId': 'string',
                    'ProductCodeType': 'devpay'|'marketplace'
                },
            ],
            'RamdiskId': 'string',
            'State': 'pending'|'available'|'invalid'|'deregistered'|'transient'|'failed'|'error',
            'BlockDeviceMappings': [
                {
                    'DeviceName': 'string',
                    'VirtualName': 'string',
                    'Ebs': {
                        'DeleteOnTermination': True|False,
                        'Iops': 123,
                        'SnapshotId': 'string',
                        'VolumeSize': 123,
                        'VolumeType': 'standard'|'io1'|'gp2'|'sc1'|'st1',
                        'KmsKeyId': 'string',
                        'Encrypted': True|False
                    },
                    'NoDevice': 'string'
                },
            ],
            'Description': 'string',
            'EnaSupport': True|False,
            'Hypervisor': 'ovm'|'xen',
            'ImageOwnerAlias': 'string',
            'Name': 'string',
            'RootDeviceName': 'string',
            'RootDeviceType': 'ebs'|'instance-store',
            'SriovNetSupport': 'string',
            'StateReason': {
                'Code': 'string',
                'Message': 'string'
            },
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            'VirtualizationType': 'hvm'|'paravirtual'
        },
    ]
  }
  """
  return ec2.describe_images(Owners=['self'])


if __name__ == '__main__':
  # Read the command line for the tag name(s) and AWS information
  cmdargs = parse_args()
  tag_names = cmdargs.tag_names.split(',')

  # Setup the default AWS profile and region
  boto3.setup_default_session(profile_name=cmdargs.aws_profile, 
                              region_name=cmdargs.aws_region)
  account_id = boto3.client('sts').get_caller_identity().get('Account')
  ec2 = boto3.client('ec2')

  # Get the objects from AWS
  instances = fetch_instances(ec2)
  volumes = fetch_volumes(ec2)
  snapshots = fetch_snapshots(ec2, account_id)
  amis = fetch_amis(ec2)

  # Display instance tags
  for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
      print(f"\n***** {instance['InstanceId']} *****")
      search_tags(tag_names, instance)

  # Now let's display volumes
  for volume in volumes['Volumes']:
    print(f"\n***** {volume['VolumeId']} *****")
    search_tags(tag_names, volume)

  # Now lets display snapshots
  for snapshot in snapshots['Snapshots']:
    print(f"\n***** {snapshot['SnapshotId']} *****")
    search_tags(tag_names, snapshot)

  # Finally, let's display AMIs
  for ami in amis['Images']:
    print(f"\n***** {ami['ImageId']} *****")
    search_tags(tag_names, ami)

  #cya