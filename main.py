import boto3
import botocore
from datetime import datetime, timedelta, timezone

dry_run = False

daily_retention_limit = datetime.now(timezone.utc) - timedelta(days=30)
monthly_retention_limit = datetime.now(timezone.utc) - timedelta(days=365)
print('Deleting ec2 snapshots older than:')
print(f'  Daily retention limit: {daily_retention_limit}')
print(f'  Monthly retention limit: {monthly_retention_limit}')

ec2 = boto3.client('ec2')
snapshots = ec2.describe_snapshots(OwnerIds=['self'])

for snapshot in snapshots['Snapshots']:
    snapshot_time = snapshot['StartTime']
    snapshot_id = snapshot['SnapshotId']
    try:
        if snapshot_time < daily_retention_limit:
            print(f'Considering snapshot {snapshot_id} for deletion, as snapshot time {snapshot_time} is earlier than {daily_retention_limit}')
            if snapshot_time < monthly_retention_limit:
                print(f'Deleting snapshot {snapshot_id} as {snapshot_time} is older than monthly retention limit')
                ec2.delete_snapshot(SnapshotId=snapshot_id, DryRun=dry_run)
            else:
                if snapshot_time.day == 1:
                    print(f'Retaining snapshot {snapshot_id} as {snapshot_time} falls on first day of the month.')
                else:
                    print(f'Deleting snapshot {snapshot_id} as {snapshot_time} does not fall on first day of the month.')
                    ec2.delete_snapshot(SnapshotId=snapshot_id, DryRun=dry_run)
        else:
            print(f'Snapshot {snapshot_id} is within retention limit (snapshot time: {snapshot_time}.)')
    except botocore.exceptions.ClientError as error:
        print (f'AWS client error code {error.response["Error"]["Code"]}')
        if error.response["Error"]["Code"] == 'DryRunOperation':
            print('Ignoring Dry-Run failure')
        else:
            print (error)
            raise error
