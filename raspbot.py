import re
import time
import json
import psutil
import subprocess
import smtplib
import socket
from slackclient import SlackClient


slack_client = SlackClient("xoxb-333999126405-krJFcCP8YyyIHAIu609JHC1o")


# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "pibot":
        slack_user_id = user.get('id')
        break

# Get ip
def getIp():
    arg='ip route list'
    p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = split_data[split_data.index('src')+1]
    my_ip = 'Your ip is %s' %  ipaddr
    return my_ip;

# Start connection
if slack_client.rtm_connect():
    print "Connected!"

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):

                print "Message received: %s" % json.dumps(message, indent=2)

                message_text = message['text'].\
                    split("<@%s>" % slack_user_id)[1].\
                    strip()

                if re.match(r'.*(cpu).*', message_text, re.IGNORECASE):
                    cpu_pct = psutil.cpu_percent(interval=1, percpu=False)

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="My CPU is at %s%%." % cpu_pct,
                        as_user=True)

                if re.match(r'.*(memory|ram).*', message_text, re.IGNORECASE):
                    mem = psutil.virtual_memory()
                    mem_pct = mem.percent

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="My RAM is at %s%%." % mem_pct,
                        as_user=True)

                if re.match(r'.*(ip).*', message_text, re.IGNORECASE):
                    ip = getIp();
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="My ip is: %s%%." % ip,
                        as_user=True)

        time.sleep(1)