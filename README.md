# What is getinsights?
It's a small python tool (``getinsights.py``) which allows you to get Red Hat Insights information locally in a shell on your Red Hat Enterprise Linux 8 server.

## Contributing
Please send me pull request if you can improve this tool. Design priciple is: Try to extract as much information as possible, locally.

## Normal mode
Running ``check_insights.py`` without arguments displays all issues identified by Red Hat Insights for your system.

## Monitoring mode
Running ``check_insights.py`` with ``--mon true`` enters the tool into monitoring mode. It allows for a simple integration from Red Hat Insights to you monitoring tool of choice. Below, example integration with Nagios is shown.

![Example integration to Nagios](nagios-insights.png)

In monitoring mode the tool looks at:

* Total number of issues for your system
* Number of security related issues
* Number of performance related issues
* Number of stability related issues
* Number of availability related issues

You can then also for each of above things set custom thresholds for warning and critical, if warning or critical levels are reached, the tool exists with a non-zero exit code to indicate OK, wanring or critical. You can customize exit codes if you like. 

The tools integrates out-of-the-box with popular open source monitoring solution Nagios as it uses the default exit codes to indicate warning (1) and critical (2) and unknown (3) in Nagios.

If we breach critical level for one of the items above, we exit indicating critical state, also if other items are OK.

## Usage and view default values
1) Download getinsights to your system:
```
# wget https://raw.githubusercontent.com/mglantz/getinsights/main/getinsights.py -O /usr/local/sbin/getinsights
```
2) Set correct permissions
```
chmod a+rx /usr/local/sbin/getinsights
```

2) Run
```
# getinsights --help
```

# Example use-cases
Here's a list of example use-cases.

## Using the tool for monitoring purposes.
Consider using https://github.com/mglantz/get_insight instead. This tool was designed for that specific purpose.

## Check all Red Hat Insights issues for your system.

```
getinsights
```

## Check all Red Hat Insights security issues for your systems.

```
# getinsights --sec
```


## Check all Red Hat Insights availability issues for your systems.

```
# getinsights --avail
```

## Check all Red Hat Insights stability issues for your systems.

```
# getinsights --stab
```

## Check all Red Hat Insights performance issues for your systems.

```
# getinsights --perf
```

# Example output:

```
# getinsights
Rule_id:     hardening_yum|HARDENING_YUM_GPG_3RD_6
Rule type:   Security
Summary:     Recommended security practices for configuring yum repositories are not being followed. Package verification is
disabled for third-party yum repositories. Verification ensures that packages have not been altered from original
source.

Description: Recommended security practices for configuring yum repositories are not being followed. Package verification is
disabled for yum repositories. Verification ensures that packages have not been altered from original
source. The current settings might be required by your use case or needed for your other software configurations.
However, any deviation from the recommended practices should be carefully considered.

Red Hat recommends that you review the yum settings for all your reported servers, revise them, and leave detected,
potentially problematic settings only where necessary.

Impact:      Decreased Security
Likelihood:  1
Total risk:  1
Needs reboot: False
Publish date: 2017-11-02T12:00:00Z
--------------
Rule_id:     decreased_vm_network_performance|VHOST_NET_KERNEL_MODULE_NOT_LOADED
Rule type:   Performance
Summary:     VM network performance is decreased when the vhost_net kernel feature is not enabled.

Description: The `vhost_net` kernel module is used to accelerate the Host kernel using the `virtio-net` module. If it is **not loaded**, the VM network performance is decreased.

Impact:      Network Performance Loss
Likelihood:  4
Total risk:  3
Needs reboot: False
Publish date: 2020-09-26T06:20:00Z
--------------
Red Hat Insights found: Total issues: 2. Security issues: 1. Availability issues: 0. Stability issues: 0. Performance issues: 1
```
