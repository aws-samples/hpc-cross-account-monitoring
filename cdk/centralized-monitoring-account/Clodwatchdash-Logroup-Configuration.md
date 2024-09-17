<b>Step 1: Login to AWS Console for Centralized Account </b><br>
<b>Step 2: Navigate to CloudWatch > Dashboards > HPC-Cluster-Instance-States-Dashboard </b><br>
<br>
<b>Step 3: For First Widget (Instance State Changes Over Time) select Edit option from right hand side menu, refer to below screenshot </b><br>
<br>
![Solution diagram](../../assets/cloudwatch-dashbaord-1.png) <br>
<br>
<b>Step 4: This will open Log Insights page, on this page Select LogGroups with "/aws/lambda/hpc-cluster-notifications-function" name from all different Individual Accounts mapped to Monitoring Account. </b><br>
![Solution diagram](../../assets/cloudwatch-dashbaord-2.png)<br>
<br>
<b>Step 5: Save changes in LogInsights Page, this will update the Dashboard configuration for the specific widget. </b><br>
<b>Repeat this process (Step 3 -5) for three remaining the Widgets on Dashboard. </b><br>
<br>
![Solution diagram](../../assets/cloudwatch-dashbaord-3.png)<br>
<br>
![Solution diagram](../../assets/cloudwatch-dashbaord-4.png)<br>
<b>Step 6: Once all Widgets are updated, then Save the dashboard configuration by clicking Save on Top of Dashboard. </b><br>
<br>
![Solution diagram](../../assets/cloudwatch-dashbaord-5.png) <br>
<br>
