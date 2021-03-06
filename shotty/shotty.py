import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def instances():
    """Commands for instances"""

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or [] }
        print("ID: " + i.id + " | TYPE: " + i.instance_type + \
        " | AZ: " + i.placement['AvailabilityZone'] + " | STATE: " + i.state['Name'] + \
        " | PBL DNS: " + i.public_dns_name + "| PROJECT: " + tags.get('Project', '<no project>'))

    return

@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Stopping instance {0} ...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)
    for i in instances:
        print("Starting instance {0} ...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    instances()
