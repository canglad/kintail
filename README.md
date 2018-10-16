# kintail

A python script that continuously pulls records from an AWS Kinesis data stream and prints them on the screen. It was initially developed to help monitor AWS CloudTrail events for troubleshooting purpose. By using this tool, it can significantly make troubleshooting much more efficient as CloudTrail/CloudWatch events will be received and printed to the screen very quickly (usually within a minute), comparing to the usual CloudTrail logs delivery to S3 buckets which has up to 15 minutes delay. The results can also be piped through other handy Unix text processing tools for further filtering and analysis.

## Usage
    python kintail.py
    usage: kintail.py [-h] [--profile PROFILE] [--region REGION] [--no-separator]
                      [--interval INTERVAL] [--json] [--debug]
                      stream-name

## Prerequisites
- You should be familiar with AWS
- You should know how to configure and use AWS CLI
- This script requires AWS SDK Boto3

## Setup
If have not done so, install the AWS SDK Boto3 module by:
`sudo pip install boto3`

## Run using default AWS profile
`python kintail.py <your_kinesis_stream_name>`

## Run using a specific AWS profile
`python kintail.py --profile <your_aws_profile_name> <your_kinesis_stream_name>`

## Run using a specific AWS profile with output formatted for JASON
`python kintail.py --profile <your_aws_profile_name> --json <your_kinesis_stream_name>`

## Get help
`python kintail.py -h`
