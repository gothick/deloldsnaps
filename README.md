# deloldsnaps
Delete old AWS EC2 snapshots

My own simple quickly-hacked together script to clear old snapshots out of EC2. May be useful for anyone who's 
trying to manage snapshots with boto3. Note that if you're managing an enterprise, you probably want to be using
the [Amazon Data Lifecycle Manager](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-lifecycle.html);
I'm just running my own web server for fun.
