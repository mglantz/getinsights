#!/usr/bin/python3
# Name: getinsights.py
#
# Description: Print out information about issues detected by Red Hat Insight.
# Prereq: latest version of Red Hat Insight installed on the system and system registered to Satelite or cloud.redhat.com.
#
# Author: Magnus Glantz, sudo@redhat.com, 2020

# Import required modules
import sys 
import os
import subprocess
try:
    import simplejson as json
except ImportError:
    import json
import rpm

# We need to discard some info to /dev/null later on
DEVNULL = open(os.devnull, 'wb')

allset = "false"
summary = "false"
sec = "false"
avail = "false"
stab = "false"
perf = "false"

# Argument parsing and --help
for argument in sys.argv:
    if "--help" in argument:
        print('Usage: getsinsights | getinsights [options]')
        print('Options')
        print('--all    Prints all found issues. This is also what you get with no arguments passed.')
        print('--sum    Only prints a summary of what was found.')
        print('--sec    Prints all found Security issues.')
        print('--avail  Prints all found Availability issues')
        print('--stab   Prints all found Stability issues')
        print('--perf   Prints all found Performance issues')
        sys.exit(0)
    elif "--sec" in argument:
        sec = "true"
    elif "--avail" in argument:
       avail = "true"
    elif "-stab" in argument:
        stab = "true"
    elif "--perf" in argument:
        perf = "true"
    elif "--sum" in argument:
        summary = "true" 
    else:
        allset = "true"

if sec == "true" or avail == "true" or stab == "true" or perf == "true" or summary == "true":
    allset = "false"

# Check for the insights-client package, if it's not installed, nothing below will work.
ts = rpm.TransactionSet()
mi = ts.dbMatch( 'name', 'insights-client' )

rpmhit=0
for h in mi:
    if h['name'] == 'insights-client':
        rpmhit=1
        break

if rpmhit == 0:
    print('Unknown: Package insights-client not installed (or too old). Install using: dnf install insights-client')
    sys.exit(3)

# Check if the system has registered to Satellite or cloud.redhat.com
if not os.path.isfile('/etc/insights-client/.registered'):
    print('Unknown: You need to register to Red Hat Insights by running: insights-client register')
    sys.exit(3)

# Remove .lastupload identifier if it exists
if os.path.isfile('/etc/insights-client/.lastupload'):
    os.remove('/etc/insights-client/.lastupload')
        
try:
    subprocess.run(['insights-client'], check = True, stdout=DEVNULL, stderr=DEVNULL)
except subprocess.CalledProcessError:
    print('Unknown: insights-client failed to check in. Run: insights-client --check-result for more information.')
    sys.exit(3)

# Remove stdout file
if os.path.isfile('/tmp/insights-result'):
    os.remove('/tmp/insights-result')

try:
    os.system('insights-client --show-result >/tmp/insights-result')
    if not os.system('insights-client --show-result >/tmp/insight-result') == 0:
        raise Exception('insights-client command failed')
except:
    print('Unknown: insights-client failed to get results. Run: insights-client --show-results for more information.')
    sys.exit(3)

if not os.path.isfile('/etc/insights-client/.lastupload'):
    print('Unknown: insights-client failed to get result from cloud.redhat.com. Run: insights-client --show-results for more information.')
    sys.exit(3)

# Open the existing json file for loading into a variable
with open('/tmp/insights-result') as f:
    datastore = json.load(f)

# Count how many hit we have in total
total_issues = 0
for item in datastore:
    total_issues += 1
    if allset == "true":
        print('Rule_id:     ', item['rule']['rule_id'], sep="")
        print('Rule type:   ', item['rule']['category']['name'], sep="")
        print('Summary:     ', item['rule']['summary'], sep="")
        print('Description: ', item['rule']['generic'], sep="") 
        print('Impact:      ', item['rule']['impact']['name'], sep="")
        print('Likelihood:  ', item['rule']['likelihood'], sep="")
        print('Total risk:  ', item['rule']['total_risk'], sep="")
        print('Needs reboot: ', item['rule']['reboot_required'], sep="")
        print('Publish date: ', item['rule']['publish_date'], sep="")
        print('--------------')
    elif sec == "true":
        if item['rule']['category']['name'] == "Security":
            print('Rule_id:     ', item['rule']['rule_id'], sep="")
            print('Rule type:   ', item['rule']['category']['name'], sep="")
            print('Summary:     ', item['rule']['summary'], sep="")
            print('Description: ', item['rule']['generic'], sep="")
            print('Impact:      ', item['rule']['impact']['name'], sep="")
            print('Likelihood:  ', item['rule']['likelihood'], sep="")
            print('Total risk:  ', item['rule']['total_risk'], sep="")
            print('Needs reboot: ', item['rule']['reboot_required'], sep="")
            print('Publish date: ', item['rule']['publish_date'], sep="")
            print('--------------')
    elif perf == "true":
        if item['rule']['category']['name'] == "Performance":
            print('Rule_id:     ', item['rule']['rule_id'], sep="")
            print('Rule type:   ', item['rule']['category']['name'], sep="")
            print('Summary:     ', item['rule']['summary'], sep="")
            print('Description: ', item['rule']['generic'], sep="")
            print('Impact:      ', item['rule']['impact']['name'], sep="")
            print('Likelihood:  ', item['rule']['likelihood'], sep="")
            print('Total risk:  ', item['rule']['total_risk'], sep="")
            print('Needs reboot: ', item['rule']['reboot_required'], sep="")
            print('Publish date: ', item['rule']['publish_date'], sep="")
            print('--------------')
    elif stab == "true":
        if item['rule']['category']['name'] == "Stability":
            print('Rule_id:     ', item['rule']['rule_id'], sep="")
            print('Rule type:   ', item['rule']['category']['name'], sep="")
            print('Summary:     ', item['rule']['summary'], sep="")
            print('Description: ', item['rule']['generic'], sep="")
            print('Impact:      ', item['rule']['impact']['name'], sep="")
            print('Likelihood:  ', item['rule']['likelihood'], sep="")
            print('Total risk:  ', item['rule']['total_risk'], sep="")
            print('Needs reboot: ', item['rule']['reboot_required'], sep="")
            print('Publish date: ', item['rule']['publish_date'], sep="")
            print('--------------')
    elif avail == "true":
        if item['rule']['category']['name'] == "Availability":
            print('Rule_id:     ', item['rule']['rule_id'], sep="")
            print('Rule type:   ', item['rule']['category']['name'], sep="")
            print('Summary:     ', item['rule']['summary'], sep="")
            print('Description: ', item['rule']['generic'], sep="")
            print('Impact:      ', item['rule']['impact']['name'], sep="")
            print('Likelihood:  ', item['rule']['likelihood'], sep="")
            print('Total risk:  ', item['rule']['total_risk'], sep="")
            print('Needs reboot: ', item['rule']['reboot_required'], sep="")
            print('Publish date: ', item['rule']['publish_date'], sep="")
            print('--------------')
    elif summary == "true":
        pass


# Count how many of those are security issues
security_issues = 0
for item in datastore:
   if item['rule']['category']['name'] == "Security":
      security_issues += 1

# Count how many of those are performance issues
performance_issues = 0
for item in datastore:
    if item['rule']['category']['name'] == "Performance":
        performance_issues += 1

# Count how many of those are stability issues
stability_issues = 0
for item in datastore:
    if item['rule']['category']['name'] == "Stability":
        stability_issues += 1

# Count how many of those are availability issues
availability_issues = 0
for item in datastore:
    if item['rule']['category']['name'] == "Availability":
        availability_issues += 1

print('Red Hat Insights found: Total issues: ',total_issues,'. Security issues: ', security_issues,'. Availability issues: ', availability_issues, '. Stability issues: ', stability_issues, '. Performance issues: ', performance_issues, sep="")
