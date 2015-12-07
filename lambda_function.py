from __future__ import print_function

import json
import boto3
from decimal import Decimal

print('Loading function')


def lambda_handler(event, context):
  #print("Received event: " + json.dumps(event, indent=2))
  client = boto3.client('cloudwatch')

  for record in event['Records']:
    # print(record['eventID'])
    # print(record['eventName'])
    # print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))
    print(record['dynamodb']['NewImage'])
    response = client.put_metric_data(
      Namespace='PI_FARM',
      MetricData=[
        {
          'MetricName': 'temperature',
          'Dimensions': [
            {
              'Name': 'Device',
              'Value': record['dynamodb']['NewImage']['payload']['M']['deviceid']['S']
            },
          ],
          'Timestamp': record['dynamodb']['NewImage']['timestamp']['S'],
          'Value': Decimal(record['dynamodb']['NewImage']['payload']['M']['temp']['S']),
          'Unit': 'None'
        },
      ]
    )

    response = client.put_metric_data(
      Namespace='PI_FARM',
      MetricData=[
        {
          'MetricName': 'humidity',
          'Dimensions': [
            {
              'Name': 'Device',
              'Value': record['dynamodb']['NewImage']['payload']['M']['deviceid']['S']
            },
          ],
          'Timestamp': record['dynamodb']['NewImage']['timestamp']['S'],
          'Value': Decimal(record['dynamodb']['NewImage']['payload']['M']['hum']['S']),
          'Unit': 'Percent'
        },
      ]
    )

    response = client.put_metric_data(
      Namespace='PI_FARM',
      MetricData=[
        {
          'MetricName': 'lux',
          'Dimensions': [
            {
              'Name': 'Device',
              'Value': record['dynamodb']['NewImage']['payload']['M']['deviceid']['S']
            },
          ],
          'Timestamp': record['dynamodb']['NewImage']['timestamp']['S'],
          'Value': Decimal(record['dynamodb']['NewImage']['payload']['M']['lx']['S']),
          'Unit': 'None'
        },
      ]
    )

    response = client.put_metric_data(
      Namespace='PI_FARM',
      MetricData=[
        {
          'MetricName': 'moisture',
          'Dimensions': [
            {
              'Name': 'Device',
              'Value': record['dynamodb']['NewImage']['payload']['M']['deviceid']['S']
            },
          ],
          'Timestamp': record['dynamodb']['NewImage']['timestamp']['S'],
          'Value': Decimal(record['dynamodb']['NewImage']['payload']['M']['moi']['S']),
          'Unit': 'None'
        },
      ]
    )

  return 'Successfully processed {} records.'.format(len(event['Records']))
