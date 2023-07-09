"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3, ec2
# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

instances = ["loki-instance-1","loki-instance-2","loki-instance-3","loki-instance-4"]

lokeshsg = ec2.SecurityGroup('lokes-sg',description='ec2 security group')

AllowHttp = ec2.SecurityGroupRule('AllowHttp',type='ingress',cidr_blocks=['0.0.0.0/0'],from_port=80,to_port=80,protocol="TCP",security_group_id=lokeshsg.id)

AllowSSH = ec2.SecurityGroupRule('AllowSSH',type='ingress',cidr_blocks=['0.0.0.0/0'],from_port=22,to_port=22,protocol="TCP",security_group_id=lokeshsg.id)
AllowAll = ec2.SecurityGroupRule('AllowAll',type='egress',cidr_blocks=['0.0.0.0/0'],from_port=0,to_port=0,protocol="-1",security_group_id=lokeshsg.id)
ec2_instance_names = []
ec2_public_dns = []
ec2_public_ip = []
for i in instances:
    ec2_instance = ec2.Instance(i,ami='ami-053b0d53c279acc90',
                                key_name='loki',
                                instance_type='t2.micro'
                                vpc_security_group_ids=[lokeshsg.id],
                                tags = {
                                    "Name": i
                                })
    ec2_instance_names.append(ec2_instance.id)
    ec2_public_ip.append(ec2_instance.public_ip)
    ec2_public_dns.append(ec2_instance.public_dns)

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)
pulumi.export('SecurityGroupName',lokeshsg.id)
pulumi.export('EC2_intances',ec2_instance_names)
pulumi.export('Public_ip',ec2_public_ip)
pulumi.export('Public_dns',ec2_public_dns)

