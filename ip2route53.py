import os
from requests import get

from datetime import datetime, timedelta
import pytz

import boto3
from botocore.exceptions import ClientError

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
HOSTED_ZONE_ID = os.environ['HOSTED_ZONE_ID']
DOMAIN_NAME = os.environ['DOMAIN_NAME']
INFLUXDB_URL = os.environ['INFLUXDB_URL']
INFLUXDB_TOKEN = os.environ['INFLUXDB_TOKEN']
INFLUXDB_ORG = os.environ['INFLUXDB_ORG']
INFLUXDB_BUCKET = os.environ['INFLUXDB_BUCKET']

tz = pytz.timezone(os.environ['TZ'])
local = tz.localize(datetime.now())
timestamp = local.strftime("%Y-%m-%dT%H:%M:%S%Z%z")

influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
influx_write_api = influx_client.write_api(write_options=SYNCHRONOUS)


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
            'TTL': 28800,
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

  print(f"{timestamp} HTTPStatusCode: {response['ResponseMetadata']['HTTPStatusCode']} Status: {response['ChangeInfo']['Status']} Ip: {external_ip}")

except ClientError as client_error:
  print(f"{timestamp} ClientError: {client_error}")


data_point = Point("ip_address").tag("type", "report").field("ipv4", external_ip)

influx_write_api.write(bucket=INFLUXDB_BUCKET, record=data_point)
influx_client.close()