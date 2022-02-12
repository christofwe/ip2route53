import os
from requests import get

from datetime import datetime

import boto3
from botocore.exceptions import ClientError

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
HOSTED_ZONE_ID = os.environ['HOSTED_ZONE_ID']
DOMAIN_NAME = os.environ['DOMAIN_NAME']

local = datetime.now()
timestamp = local.strftime("%Y-%m-%dT%H:%M:%SZ")

external_ip = get('https://api.ipify.org').content.decode('utf8')

try:
  route53 = boto3.client("route53")

  response = route53.change_resource_record_sets(
    HostedZoneId=HOSTED_ZONE_ID,
    ChangeBatch={
      'Comment': 'string',
      'Changes': [
        {
          'Action': 'UPSERT',
          'ResourceRecordSet': {
            'Name': DOMAIN_NAME,
            'Type': 'A',
            'TTL': 900,
            'ResourceRecords': [
              {
                'Value': external_ip
              }
            ]
          }
        }
      ]
    }
  )

  print(f"{timestamp} HTTPStatusCode: {response['ResponseMetadata']['HTTPStatusCode']} Status: {response['ChangeInfo']['Status']}")

except ClientError as client_error:
  print(f"{timestamp} ClientError: {client_error}")
