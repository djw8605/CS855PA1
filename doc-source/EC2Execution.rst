
EC2 Execution
=============

EC2 Execution is done by submitting jobs to `HTCondor <http://research.cs.wisc.edu/htcondor/>`_ that start `EC2 Spot Instances <http://research.cs.wisc.edu/htcondor/manual/v7.9/5_3Grid_Universe.html#SECTION00636000000000000000>`_.

Preparing Submission
--------------------

Submission is done with `HTCondor <http://research.cs.wisc.edu/htcondor/>`_.  An EC2 Submission file was created::

   universe = grid
   grid_resource = ec2 https://ec2.amazonaws.com/
   executable = /bin/true

   # Amazon Linux AMI
   ec2_ami_id = ami-04cf5c6d

   ec2_access_key_id = access_key
   ec2_secret_access_key = secret_key
   ec2_keypair_file = keyfile.$(CLUSTER)
   ec2_security_groups = bosco
   ec2_instance_type = m1.small
   ec2_spot_price = 0.04
   ec2_user_data_file = ami-run.sh
   ec2_tag_concat = true
   periodic_remove = JobStatus == 2 && (time() - EnteredCurrentStatus) > 60*120
   log = ec2.log
   queue
   
As you can see, ``ec2_user_data_file`` is set to ami-run.sh.  This ami-run.sh contains the script that will be executed at the first start of the instance::

   #!/bin/sh

   rpm -Uvh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
   yum -y install yum-priorities git

   # Checkout the project
   git clone git://github.com/djw8605/CS855PA1.git

   # Start the server
   cd CS855PA1
   git checkout PA3
   python src/ATMServer.py
   
Each instance will run this script since the `Amazon Linux AMI <https://aws.amazon.com/amazon-linux-ami/>`_ contains `CloudInit <https://help.ubuntu.com/community/CloudInit>`_.

Addionally, the submit file has a ``periodic_remove`` statement that will kill the instance after 2 hours of execution.

Testing Execution
-----------------

Testing was done by SSHing into the EC2 instance and running the Clients against another EC2 instance::

   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 inquiry 1 100
   Current value of account 100 is $1000.00
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 deposit 1 100 200
   Successful deposit of $200.00 to account 100
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 inquiry 1 100
   Current value of account 100 is $1200.00
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 abort_transaction 1
   Customer 1 aborts their transaction
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 begin_transaction 1
   Customer 1 starts their transaction
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 inquiry 1 100
   Current value of account 100 is $1000.00
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 deposit 1 100 200
   Successful deposit of $200.00 to account 100
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 withdraw 1 100 50
   Successful withdraw of $50.00 to account 100
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 inquiry 1 100
   Current value of account 100 is $1150.00
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 end_transaction 1
   Customer 1 commits their transaction
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 begin_transaction 1
   Customer 1 starts their transaction
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 inquiry 1 100
   Current value of account 100 is $1150.00
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 deposit 1 100 200
   Successful deposit of $200.00 to account 100
   
And on C2::

   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 begin_transaction 2
   Customer 2 starts their transaction
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 inquiry 2 200
   Current value of account 200 is $1000.00
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 inquiry 2 100
   <blocking...>
   Current value of account 100 is $1350.00
   $ python ATMClient.py ec2-54-224-134-194.compute-1.amazonaws.com 9000 abort_transaction 2
   Customer 2 aborts their transaction
   
This testing shows that the blocking and locking mechanism works.

