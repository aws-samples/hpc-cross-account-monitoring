# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

#!/usr/bin/env python3
import os

import aws_cdk as cdk
import aws_cdk.aws_sqs as sqs


from lib.hpc_ec2_state_notfn_stack import HPCClusterAvailabilityNotfnStack

# Update EC2 cluster tag keyname pattern here
EC2_TAG_KEY_PATTERN = "HPC"
# Update EC2 cluster tag value pattern here
EC2_TAG_VAL_PATTERN = "HPC"

app = cdk.App()
main_stack = HPCClusterAvailabilityNotfnStack(
    app, "HPCClusterAvailabilityNotfnStack", EC2_TAG_KEY_PATTERN, EC2_TAG_VAL_PATTERN)
sns_topic = main_stack.hpc_notfn_topic

app.synth()
