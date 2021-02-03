from github import Github
from encrypt import privacy_key, ta_bug_repo, sf_bug_repo
import os 
g = Github(privacy_key)
repo = g.get_repo(sf_bug_repo)

for issue in repo.get_issues():
    labels = [lab.name for lab in issue.labels]
    if "Confirmed" in labels:
        os.system("open "+issue.html_url)
