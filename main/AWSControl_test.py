import boto3


client = boto3.client('ec2', region_name="us-east-2")
keyPairResponse = client.create_key_pair(KeyName='stjudekey')
keyPairResponse['KeyMaterial']

response = client.describe_security_groups(GroupIds=['sg-083318f5f7e5b1504'])
print(response)

ec2 = boto3.resource('ec2', region_name="us-east-2")
instance = ec2.create_instances(
    ImageId = 'ami-09aea2adb48655672',
    MinCount = 1,
    MaxCount = 1,
    InstanceType = 't2.micro',
    SecurityGroupIds=[
        'sg-083318f5f7e5b1504'
    ],
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'VolumeSize': 30,
                'VolumeType': 'gp2'
            }
        }
    ],
    KeyName = 'stjudekey')

instance[0].wait_until_running()
instance[0].reload()
print(instance[0].public_dns_name)
print (instance[0].id)

instance[0].terminate()
