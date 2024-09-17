# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0


#!/usr/bin/env python3
import os

import aws_cdk as cdk
import aws_cdk.aws_sqs as sqs


from lib.hpc_state_cloudwatch_dashboard_stack import HPCClusterStateDashboardStack

# Update Lambda log group name as per individual hpc cluster account CDK 
LAMBDA_LOG_GRP_NAME="/aws/lambda/hpc-cluster-notifications-function"

app = cdk.App()

stack3 = HPCClusterStateDashboardStack(app,"HPCClusterStateDashboardStack",LAMBDA_LOG_GRP_NAME)

app.synth()
