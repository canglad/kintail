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
`python kintail.py --profile <your_aws_profile_name> --jason <your_kinesis_stream_name>`

## Get help
`python kintail.py -h`

## Sample Use Case: Monitor CloudTrail
This is a common use case, very useful when you need to troubleshoot something with unexepcted behavior or unclear error message. For example, sometimes when you are creating complex services through AWS Management Console, you may get an error message like "Can not contact the server". But behind the scene, it may be just an IAM permission issue. Another example, if you are expecting an AWS service deliver something on your behalf, but nothing happened, you can investigate the CloudTrail and see what might be the issue, very often, permission not properly granted.
1. Create a Kinesis Data Stream with 1 shard
2. Create a CloudTrail which captures CloudTrails from all regions and sends them to CloudWatch
3. In CloudWatch, create a Rule which sends events that interests you to the Kinesis Data Stream you created in step 1
4. Use this tool to monitor the Kinesis Data Stream

## Sample Output
    $ python kintail.py --profile myprofile cloudtrail-stream
    {"version":"0","id":"bf05ae66-d1f2-4d8a-2159-xxxx","detail-type":"AWS Console Sign In via CloudTrail","source":"aws.signin","account":"892xxxxxxxxx","time":"2018-04-05T15:03:42Z","region":"us-east-1","resources":[],"detail":{"eventVersion":"1.05","userIdentity":{"type":"AssumedRole","principalId":"AROXXXXXXXXXXXXXXXXX:youradmin","arn":"arn:aws:sts::892xxxxxxxxx:assumed-role/admin/youradmin","accountId":"892xxxxxxxxx","sessionContext":{"attributes":{"mfaAuthenticated":"false","creationDate":"2018-04-05T15:03:41Z"},"sessionIssuer":{"type":"Role","principalId":"AROXXXXXXXXXXXXXXXXX","arn":"arn:aws:iam::892xxxxxxxxx:role/admin","accountId":"892xxxxxxxxx","userName":"admin"}}},"eventTime":"2018-04-05T15:03:42Z","eventSource":"signin.amazonaws.com","eventName":"ConsoleLogin","awsRegion":"global","sourceIPAddress":"72.xx.xxx.xx","userAgent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0","requestParameters":null,"responseElements":{"ConsoleLogin":"Success"},"additionalEventData":{"MobileVersion":"No","MFAUsed":"No"},"eventID":"e00e0b1e-762a-44f6-b0cf-xxxx","eventType":"AwsConsoleSignIn"}}
    ===========================================
    {"version":"0","id":"6499cff6-3276-b147-ba6d-xxxx","detail-type":"AWS API Call via CloudTrail","source":"aws.cloudtrail","account":"892xxxxxxxxx","time":"2018-04-05T15:04:27Z","region":"us-east-1","resources":[],"detail":{"eventVersion":"1.05","userIdentity":{"type":"AssumedRole","principalId":"AROXXXXXXXXXXXXXXXXX:youradmin","arn":"arn:aws:sts::892xxxxxxxxx:assumed-role/admin/youradmin","accountId":"892xxxxxxxxx","accessKeyId":"ASXXXXXXXXXXXXXXXX","sessionContext":{"attributes":{"mfaAuthenticated":"false","creationDate":"2018-04-05T15:03:41Z"},"sessionIssuer":{"type":"Role","principalId":"AROXXXXXXXXXXXXXXXXX","arn":"arn:aws:iam::892xxxxxxxxx:role/admin","accountId":"892xxxxxxxxx","userName":"admin"}}},"eventTime":"2018-04-05T15:04:27Z","eventSource":"cloudtrail.amazonaws.com","eventName":"LookupEvents","awsRegion":"us-east-1","sourceIPAddress":"72.xx.xxx.xx","userAgent":"console.amazonaws.com","requestParameters":{"maxResults":5},"responseElements":null,"requestID":"45173338-bc61-4d12-acd4-xxxx","eventID":"248567f1-206a-45fc-8c4b-xxxx","eventType":"AwsApiCall"}}
    ===========================================
    {"version":"0","id":"72ffbeeb-d106-cc8d-169b-xxxx","detail-type":"AWS API Call via CloudTrail","source":"aws.events","account":"892xxxxxxxxx","time":"2018-04-05T15:06:08Z","region":"us-east-1","resources":[],"detail":{"eventVersion":"1.05","userIdentity":{"type":"AssumedRole","principalId":"AROXXXXXXXXXXXXXXXXX:youradmin","arn":"arn:aws:sts::892xxxxxxxxx:assumed-role/admin/youradmin","accountId":"892xxxxxxxxx","accessKeyId":"ASXXXXXXXXXXXXXXXX","sessionContext":{"attributes":{"mfaAuthenticated":"false","creationDate":"2018-04-05T15:03:41Z"},"sessionIssuer":{"type":"Role","principalId":"AROXXXXXXXXXXXXXXXXX","arn":"arn:aws:iam::892xxxxxxxxx:role/admin","accountId":"892xxxxxxxxx","userName":"admin"}}},"eventTime":"2018-04-05T15:06:08Z","eventSource":"events.amazonaws.com","eventName":"TestEventPattern","awsRegion":"us-east-1","sourceIPAddress":"72.xx.xxx.xx","userAgent":"AWS CloudWatch Console","requestParameters":{"eventPattern":"{ \"detail.foo\": [\"bar\"] }","event":"{\"id\":\"e00c66cb-fe7a-4fcc-81ad-xxxx\",\"time\":\"2015-05-05T01:29:23Z\",\"received-at\":\"2015-05-05T01:29:23Z\",\"region\":\"us-east-1\",\"account\":\"123456789012\",\"source\":\"aws.ec2\",\"detail-type\":\"text/plain\",\"detail\":{\"foo\": \"bar\"}}"},"responseElements":null,"requestID":"de94117c-38e2-11e8-b6e4-xxxx","eventID":"85dc8df3-9bce-474f-a267-xxxx","eventType":"AwsApiCall","apiVersion":"2015-10-07"}}
    ===========================================
    
    
