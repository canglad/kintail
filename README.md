# kintail

A python script that continuously pulls records from an AWS Kinesis data stream and prints them on the screen.

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
