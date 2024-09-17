# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3
import os


def lambda_handler(event, context):
    print(event)

    aws_account_id = event["account"]
    instance_id = event["detail"]["instance-id"]
    instance_state = event["detail"]["state"]
    event_timestamp = event["time"]

    ec2instance = get_instance_details(instance_id)

    is_hpc_cluster_response = is_instance_hpc_cluster(ec2instance)
    send_to_sns_flag = is_hpc_cluster_response["HPCClusterInstanceFlag"]
    ec2_tags = ec2instance.tags
    print(" send_to_sns %s for instance id %s" %
          (str(send_to_sns_flag), instance_id))

    if (send_to_sns_flag):
        hpc_cluster_name = is_hpc_cluster_response["HPCClusterName"]
        publishCloudWatchMetric(instance_id, instance_state,
                                event_timestamp, hpc_cluster_name, aws_account_id, ec2_tags)
        send_to_sns(instance_id, instance_state)
    else:
        print(" Not a HPC Cluster EC2, notification to SNS skipped for instance id %s" % (
            instance_id))
    return {
        'statusCode': 200,
        'body': json.dumps('Ec2 Lambda SNS notification!')
    }


def get_instance_details(f_instance_id):
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(f_instance_id)
    return ec2instance


def is_instance_hpc_cluster(ec2instance):
    hpc_cluster_tag_key_pattern = os.environ["HPC_CLUSTER_NAME_TAG_KEY"]
    hpc_cluster_tag_value_pattern = os.environ["HPC_CLUSTER_NAME_TAG_VALUE"]
    is_hpc_cluster_response = {"HPCClusterInstanceFlag": False}
    # or hpc_cluster_tag_value_pattern in tags["Value"]
    for tags in ec2instance.tags:
        if (hpc_cluster_tag_key_pattern in tags["Key"] or hpc_cluster_tag_value_pattern in tags["Value"]):
            is_hpc_cluster_response["HPCClusterInstanceFlag"] = True
            is_hpc_cluster_response["HPCClusterName"] = tags["Value"]
    return is_hpc_cluster_response


def send_to_sns(f_instance_id, f_instance_state):
    print(" inside send_to_sns")

    hpc_sns_topic = os.environ['HPC_NOTFN_SNS_TOPIC_ARN']
    print("SNS Topic ARN %s" % (hpc_sns_topic))

    message = {"instance_id": f_instance_id,
               "message_text": "instance state changed for HPC Cluster EC2 instance", "instance_state":  f_instance_state}
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=hpc_sns_topic,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json')
    print("Notification Sent to  SNS %s" % (response))


def publishCloudWatchMetric(instance_id, instance_state, timestamp, cluster_name, aws_account_id, ec2_tags):
    print("insdie publishCloudWatchMetric")
    log_metric_data = {
        'MetricName': 'log-insight-hpc-cluster',
        "instance_id": instance_id,
        "instance_state": instance_state,
        "hpc_cluster_name": cluster_name,
        "account_id": aws_account_id,
        "ec2_instance_tags": ec2_tags
    }
    print(log_metric_data)
