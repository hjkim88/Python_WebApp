import boto3

### class for DB controling
### It has a function for creating a new AWS EC2 instance
class AWSControl:
    def __init__(self, account):
        self.account = account

    ### new instance creation
    def create_new_instance(self, region_name, image_id, machine, sg_id, disk_size, key_name):
        ### connect to the EC2 of AWS
        ec2 = boto3.resource('ec2', region_name=region_name)

        ### create an instance with the given info
        instance = ec2.create_instances(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=machine,
            SecurityGroupIds=[
                sg_id
            ],
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'VolumeSize': int(disk_size),
                        'VolumeType': 'gp2'
                    }
                }
            ],
            KeyName=key_name)

        ### time is needed for the instance creation. Wait until the creation
        instance[0].wait_until_running()
        instance[0].reload()

        ### return the R studio server credentials
        return [instance[0].public_dns_name, instance[0].id]
