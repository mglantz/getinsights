#!/usr/bin/python3
# Name: getinsights.py
#
# Description: Print out information about issues detected by Red Hat Insight.
# Prereq: latest version of Red Hat Insight installed on the system and system
# registered to Satelite or cloud.redhat.com.
#
# Author: Magnus Glantz, sudo@redhat.com, 2020

# Import required modules
import sys
import os
import argparse
import subprocess
try:
    import simplejson as json
except ImportError:
    import json
import rpm

# We need to discard some info to /dev/null later on
DEVNULL = open(os.devnull, 'wb')

parser = argparse.ArgumentParser(description='Get summary of system software status')
parser.add_argument(
    '--all', action='store_true',
    help='Prints all found issues.')
parser.add_argument(
    '--sum', action='store_true',
    help='Only prints a summary of what was found.')
parser.add_argument(
    '--sec', action='store_true',
    help='Prints all found Security issues.')
parser.add_argument(
    '--avail', action='store_true',
    help='Prints all found Availability issues')
parser.add_argument(
    '--stab', action='store_true',
    help='Prints all found Stability issues')
parser.add_argument(
    '--perf', action='store_true',
    help='Prints all found Performance issues')
parser.add_argument(
    '-o', '--output', default="text", choices=['text', 'json'],
    help='Do you want output as text or json?')
args = parser.parse_args()

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
    print('Unknown: insights-client failed to send report. Run: insights-client for more information.')
    sys.exit(3)

try:
    subprocess.run(['insights-client', '--check-result'], check = True, stdout=DEVNULL, stderr=DEVNULL)
except subprocess.CalledProcessError:
    print('Unknown: insights-client failed to check result. Run: insights-client --check-result for more information.')
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
security_issues = 0
performance_issues = 0
stability_issues = 0
availability_issues = 0
for item in datastore:
    total_issues += 1
    if item['rule']['category']['name'] == "Security":
        security_issues += 1
    if item['rule']['category']['name'] == "Performance":
        performance_issues += 1
    if item['rule']['category']['name'] == "Stability":
        stability_issues += 1
    if item['rule']['category']['name'] == "Availability":
        availability_issues += 1
    if args.sum:
        pass
    elif args.all:
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
        pass
    elif args.sec and item['rule']['category']['name'] == "Security":
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
    elif args.perf and item['rule']['category']['name'] == "Performance":
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
    elif args.stab and item['rule']['category']['name'] == "Stability":
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
    elif args.avail and item['rule']['category']['name'] == "Availability":
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

if args.output == 'json':
    print('{ \'total\': ', total_issues,
          ', \'security\': ', security_issues,
          ', \'availability\': ', availability_issues,
          ', \'stability\': ', stability_issues,
          ', \'performance\': ', performance_issues,
          ' }', sep="")
else:
    print('Red Hat Insights found: Total issues: ', total_issues,
          '.Security issues: ', security_issues,
          '. Availability issues: ', availability_issues,
          '. Stability issues: ', stability_issues,
          '. Performance issues: ', performance_issues,
          sep="")
