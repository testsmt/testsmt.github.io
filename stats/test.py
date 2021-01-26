from github import Github
from encrypt import privacy_key, ta_bug_repo, sf_bug_repo
g = Github(privacy_key)
repo = g.get_repo("muchang/fusion_bugs")
print(repo)