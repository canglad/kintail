# Copyright 2018 @ https://github.com/usefulandsecure
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import time
import json

import boto3
import boto3.session

# use the command line parameter parser
parser = argparse.ArgumentParser()
parser.add_argument("--profile", help="specify the profile")
parser.add_argument("--region", help="specify the AWS region to use")
parser.add_argument("--no-separator", help="don't add a separator line between log entries", action="store_true")
parser.add_argument("--interval", help="specify the interval (seconds) between each poll, default 10 seconds", type=int, default=10)
parser.add_argument("--json", help="if specified, prints out the record in parsed JSON format", action="store_true")
parser.add_argument("--debug", help="print out debug info", action="store_true")
parser.add_argument("stream-name", help="specify the name of the Kinesis stream")
args = parser.parse_args()

my_profile = args.profile
my_region = args.region
my_stream_name = getattr(args, "stream-name")
my_interval = args.interval
my_debug = args.debug
my_jason = args.json

if my_interval < 1:
  print ("argument interval must be no less than 1")
  exit(1)

# create a boto3 session
my_session = boto3.session.Session(profile_name=my_profile, region_name=my_region)
my_client = my_session.client('kinesis')

# enumerate all the shards, caveat: not checking if there are still more shards (e.g., more than 100 shards by default)
# if you have more than 100 shards, you need to modify the logic here to loop through the rest of the shards not returned in one single call
tmp = my_client.describe_stream(StreamName=my_stream_name)
my_shards = []
for shard in tmp['StreamDescription']['Shards']:
  shard_id = shard['ShardId']
  shard_iterator = my_client.get_shard_iterator(StreamName=my_stream_name, ShardId=shard_id, ShardIteratorType='LATEST')
  my_shards.append({"id": shard_id, "iterator": shard_iterator['ShardIterator']})

# loop for retrieving records from the shards as data comes in
flag = True
while flag:
  flag = False
  for shard in my_shards:
    if not 'iterator' in shard:
      # skip the closed shard
      continue
    record_response = my_client.get_records(ShardIterator=shard['iterator'])
    if 'NextShardIterator' in record_response:
      if my_debug:
        print('checking records from shard ' + shard['id'] + ' ...')
      flag = True
      shard['iterator'] = record_response['NextShardIterator']
      if record_response['Records']:
        if my_debug:
          print('Found records from shard ' + shard['id'] + ' ...')
        for rec in record_response['Records']:
          if my_jason:
            print(json.dumps(json.loads(rec['Data']), indent=4, sort_keys=True))
          else:
            print (rec['Data'])
          if not args.no_separator:
            print ('===========================================')
    else:
      if my_debug:
        print('shard ' + shard['id'] + ' is closed, skipping...')
      # mark this closed shard
      shard.pop('iterator', None)

  time.sleep(my_interval)
