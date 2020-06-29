import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    "List EC2 instances"
    for i in ec2.instances.all():
            print("ID: " + i.id + " | TYPE: " + i.instance_type + \
            " | AZ: " + i.placement['AvailabilityZone'] + " | STATE: " + i.state['Name'] + \
            " | PBL DNS: " + i.public_dns_name)

if __name__ == '__main__':
    list_instances()
