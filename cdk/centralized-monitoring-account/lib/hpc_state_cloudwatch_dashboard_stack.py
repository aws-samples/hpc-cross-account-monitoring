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
    # aws_sqs as sqs,
)
import aws_cdk.aws_cloudwatch as cloudwatch

from constructs import Construct

class HPCClusterStateDashboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, hpc_notfn_lambda_cloudwah_log_grp, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        instance_state_over_time = cloudwatch.LogQueryWidget(
            log_group_names=[hpc_notfn_lambda_cloudwah_log_grp],
            view=cloudwatch.LogQueryVisualizationType.TABLE,
            title = "Instance State Changes over time",
            query_lines=  ["fields @timestamp,   instance_id, instance_state, hpc_cluster_name, account_id", " filter strcontains(@message, \"log-insight-hpc-cluster\") "," sort @timestamp desc"],            
            height=6,
            width=24,
            )
        instance_state_over_time.position(0,0)
        
        latest_state_all_cluster = cloudwatch.LogQueryWidget(
            log_group_names=[hpc_notfn_lambda_cloudwah_log_grp],
            view=cloudwatch.LogQueryVisualizationType.TABLE,
            title = "Latest Instance States for all Clusters",
            query_lines=  ["fields instance_state,  instance_id , hpc_cluster_name"," stats latest(instance_state) as lastest_instance_state by instance_id , hpc_cluster_name, account_id"," filter strcontains(@message, \"log-insight-hpc-cluster\")"," sort @timestamp desc"],
            height=3,
            width=24,
            ) 
        latest_state_all_cluster.position(6,0)
        
        no_of_stopped_instances_per_cluster = cloudwatch.LogQueryWidget(
            log_group_names=[hpc_notfn_lambda_cloudwah_log_grp],
            view=cloudwatch.LogQueryVisualizationType.TABLE,
            title = "No of Stopped Instances Per Cluster",
            query_lines=  ["#fields instance_state,  instance_id , hpc_cluster_name "," stats latest(instance_state) as lastest_instance_state , count_distinct (instance_id) as no_of_stopped_instances by instance_id , hpc_cluster_name, account_id "," filter strcontains(@message, \"log-insight-hpc-cluster\")", "filter lastest_instance_state = \"stopped\" "," sort @timestamp desc\n| display no_of_stopped_instances, hpc_cluster_name, account_id"],
            height=4,
            width=8
            ) 
        no_of_stopped_instances_per_cluster.position(9,0)

        no_of_running_instances_per_cluster = cloudwatch.LogQueryWidget(
            log_group_names=[hpc_notfn_lambda_cloudwah_log_grp],
            view=cloudwatch.LogQueryVisualizationType.TABLE,
            title = "No of Running Instances Per Cluster",
            query_lines=  ["#fields instance_state,  instance_id , hpc_cluster_name "," stats latest(instance_state) as lastest_instance_state , count_distinct (instance_id) as no_of_running_instances by instance_id , hpc_cluster_name, account_id "," filter strcontains(@message, \"log-insight-hpc-cluster\")", "filter lastest_instance_state = \"running\" "," sort @timestamp desc\n| display no_of_stopped_instances, hpc_cluster_name, account_id"],           
            height=4,
            width=8
            ) 
        no_of_running_instances_per_cluster.position(9,0)
    
        

        dashboard = cloudwatch.Dashboard(self, "MyDashboard",
            dashboard_name="Cross-Account-HPC-Cluster-Monitoring-"+ self.region, 
            end="end",
            period_override=cloudwatch.PeriodOverride.AUTO,
            start="start",
            widgets=[[instance_state_over_time,latest_state_all_cluster,no_of_stopped_instances_per_cluster, no_of_running_instances_per_cluster]   ]
        )
    