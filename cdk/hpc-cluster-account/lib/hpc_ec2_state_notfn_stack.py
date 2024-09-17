# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0


import typing
import aws_cdk as core

from aws_cdk import (
    # Duration,
    Stack,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_sns as sns,
    aws_iam as iam,
    aws_kms as kms
    # aws_sqs as sqs,
)
from constructs import Construct


class HPCClusterAvailabilityNotfnStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ec2_tag_key_pattern, ec2_tag_value_pattern, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        sns_KMS_Key = HPCClusterAvailabilityNotfnStack.getSNSKmsKey(self)
        # 1) Create SNS Topic
        l_hpc_notfn_topic = sns.Topic(self, 'hpc_cluster_availability_notfn',
                                      display_name='HPC Cluster Availability  notification Topic',
                                      master_key = sns_KMS_Key)

        # 2) deploy lambda function
        base_lambda = HPCClusterAvailabilityNotfnStack.lambdaDeploy(
            self, l_hpc_notfn_topic, ec2_tag_key_pattern, ec2_tag_value_pattern)

        # 3) add EC2 API access to Lambda function

        base_lambda.add_to_role_policy(
            HPCClusterAvailabilityNotfnStack.createLambdaEC2ReadPolicy())

        # 4) Grant Publishing permission to Lambda
        l_hpc_notfn_topic.grant_publish(base_lambda)

        # 5) prepare resources EventBus, EventPattern, Rule-Target
        eventPattern = events.EventPattern(source=["aws.ec2"], detail_type=[
                                           "EC2 Instance State-change Notification"])
        lambdaTarget1 = targets.LambdaFunction(handler=base_lambda)

        # 6) create rule using resources: EventBus, EventPattern, Rule-Targets: Lambda and State-Machine
        event_rule = events.Rule(scope=self,
                                 id="ec2-state-notfn-lambda-1",
                                 rule_name="ec2-state-change-notfn-lambda",
                                 description="Send Ec2 State change Notifications to Lambda",
                                 # event_bus=eventBus, Dont specify event bus for using "default eventbus"
                                 event_pattern=eventPattern,
                                 )
        event_rule.add_target(lambdaTarget1)

        self.hpc_notfn_topic = l_hpc_notfn_topic

        self.lambda_log_grp_name = "/aws/lambda/"+base_lambda.function_name

        core.CfnOutput(self, "LambdaLogGroup", value=self.lambda_log_grp_name)
        core.CfnOutput(self, "SNSTopicName",
                       value=l_hpc_notfn_topic.topic_name)

    @staticmethod
    def lambdaDeploy(this, f_hpc_notfn_topic, ec2_tag_key_pattern, ec2_tag_value_pattern) -> None:
        base_lambda = _lambda.Function(this, 'hpc-cluster-notifications-function',
                                       function_name='hpc-cluster-notifications-function',
                                       handler='hpc-cluster-notifications.lambda_handler',
                                       runtime=_lambda.Runtime.PYTHON_3_12,
                                       code=_lambda.Code.from_asset(
                                           'lambda-function'),
                                       timeout=core.Duration.seconds(30),
                                       reserved_concurrent_executions=5,
                                       environment={
                                           "HPC_NOTFN_SNS_TOPIC_ARN": f_hpc_notfn_topic.topic_arn,
                                           "HPC_CLUSTER_NAME_TAG_KEY": ec2_tag_key_pattern,
                                           "HPC_CLUSTER_NAME_TAG_VALUE": ec2_tag_value_pattern,
                                       },
                                       )
        return base_lambda

    @staticmethod
    def createLambdaEC2ReadPolicy() -> None:
        lambda_ec2_read_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ec2:Describe*", "elasticloadbalancing:Describe*",
                     "autoscaling:Describe*"],
            resources=["*"]
        )
        return lambda_ec2_read_policy

    @staticmethod
    def getSNSKmsKey(this):
        default_sns_key = kms.Alias.from_alias_name(this, "myKey", "alias/aws/sns")
        return default_sns_key
        

    @property
    def hpc_notfn_topic(self):
        return type(self).hpc_notfn_topic

    @hpc_notfn_topic.setter
    def hpc_notfn_topic(self, val):
        type(self).hpc_notfn_topic = val

    @property
    def lambda_log_grp_name(self):
        return type(self).lambda_log_grp_name

    @lambda_log_grp_name.setter
    def lambda_log_grp_name(self, val):
        type(self).lambda_log_grp_name = val
    