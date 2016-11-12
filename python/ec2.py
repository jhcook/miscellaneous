#!/usr/bin/env python2.7

"""
This script creates a number of instances in Amazon AWS which in turn fetch
the specified version of Jetty, install, and then run.

Example: ./aws -n [number of instances] [Jetty version]

Author: Justin Cook <jhcook@secnix.com>

TODO: More error checking and correction, but as long as the link is reliable,
      it works reliable.
"""

import sys
import boto
from optparse import OptionParser
from time import sleep
from boto.ec2.connection import EC2Connection
from boto.exception import EC2ResponseError

class SecnixEC2(object):
    """
    This object provides a sane interface to AWS EC2 and allows creation
    of a custom cloud infrastructure.
    """
    def __init__(self, rname=None):
        """
        Create an EC2Connection instance pointing to the region of choice.
        Region defaults to us-east-1. A list is created to keep track of 
        all generated ids.
        """
        if rname:
            self.conn = boto.ec2.connect_to_region(rname)
        else:
            self.conn = EC2Connection()
        self.ids = []

    def create_security(self):
        """
        Ensure that a custom security group is created with necessary access
        to all guests. If this group already exists an error will return,
        but it is ignored silently.
        """
        try:
            adm = self.conn.create_security_group('secnix_admin',
                                                  'Secnix Administrators')
            adm.authorize('tcp', 22, 22, '0.0.0.0/0')
        except EC2ResponseError:
            pass

    def create_instance(self):
        """
        Create an instance using the correct AMI and instance type for the
        region. Associate keys so access will be enabled.
        TODO: 1) Right now instances are started serially. This can be done in
                 parallel, but the code needs slightly modified.
              2) Clean up the code for user data passed to the install.
              3) Pass in image_id and instance_type or at least make it 
                 dynamic.
        """
        m = self.conn.run_instances(image_id='ami-c37474b7',
                                    instance_type='t1.micro',
                                    key_name='ec2-secnix-key',
                      security_groups=self.conn.get_all_security_groups(),
                      user_data="""#!/bin/bash
yum -y install httpd
service httpd start
""")
        while m.instances[0].state != 'running':
            sleep(5) 
            m.instances[0].update()
        self.ids.append(m.instances[0].id)
        return m.instances[0]

    def destroy_instances(self):
        """
        Stop and terminate all instances this instance has started.
        """
        self.conn.stop_instances(instance_ids=self.ids)
        self.conn.terminate_instances(instance_ids=self.ids)

def parse_cmdline():
    usage = 'usage: %prog -n [number instances]'
    parser = OptionParser(usage=usage)
    parser.add_option('-n', '--number', dest='instnum',
                      help='number of instances to start')
    opts, args = parser.parse_args()
    if not opts.instnum:
        parser.error('please provide a number of instances')
    return opts, args

if __name__ == '__main__':
    opts, args = parse_cmdline()
    try:
        cloud = SecnixEC2('eu-west-1')
        cloud.create_security()
        for i in range(0, int(opts.instnum)):
            mach = cloud.create_instance()
            print mach.public_dns_name
        raw_input('Press <enter> when ready to destroy')
        cloud.destroy_instances()
    except EC2ResponseError, e:
        print e
        sys.exit(1)
