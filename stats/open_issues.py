#! /usr/local/bin/python3.9
from github import Github
from encrypt import *
import os 

g = Github(privacy_key)
repo = g.get_repo(gta_bug_repo)
issues = repo.get_issues(state='open')
chrome="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk"

s=""
for iss in issues:
    labels = [lab.name for lab in iss.labels]
    if "Fixed" in labels: continue
    s+=iss.html_url + " "
cmd=chrome+ " "+ str(s)
print(cmd)
os.system(cmd)

