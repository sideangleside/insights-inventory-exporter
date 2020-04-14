# insights-inventory-exporter
Script to export inventory from cloud.redhat.com


# Help
~~~
#./insights-inventory-exporter.py -h
Usage: insights-inventory-exporter.py [options]

Options:
  -h, --help            show this help message and exit
  -l LOGIN, --login=LOGIN
                        Login user
  -f FILENAME, --filename=FILENAME
                        Login user
  -p PASSWORD, --password=PASSWORD
                        Password for specified user. Will prompt if omitted
  -s SERVER, --server=SERVER
                        FQDN of server - omit https://
  -v, --verbose         Verbose output
  -d, --debug           Debugging output (debug output enables verbose)
~~~

# Modes

The `insights-inventory-exporter.py` script has two methods of printing inventory.
By default, it connects to cloud.redhat.com's API in order to retrieve a list of
hosts which are in inventory.

Additionally, it has an **offline** mode, which requires usage of the `-f|--filename`
option. The offline mode is suitable for debugging. It simply requires the output of
`curl -u $user:$password https://cloud.redhat.com/api/inventory/v1/hosts`

# Example output
~~~
================================================================================
ip-172-31-33-244.us-east-2.compute.internal Reported by -> puptoo
  Facts
    Namespace - rhsm
      RH_PROD,[u'250', u'479']
      SYSPURPOSE_SLA,Premium
      IS_VIRTUAL,True
      orgId,1234567
      CPU_CORES,1
      MEMORY,1
      SYNC_TIMESTAMP,2020-04-07T00:44:22.606Z
      CPU_SOCKETS,1
      ARCHITECTURE,x86_64
================================================================================
~~~
