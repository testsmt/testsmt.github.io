#! /usr/bin/python3.7
"""
Script to generate bug statistics, i.e. counts and bug report link.
Note that privacy_key, ta_bug_repo, sf_bug_repo have to be provided by the user
in a file encrpyt.py located in the same folder.
"""
from github import Github
from encrypt import privacy_key, ta_bug_repo, sf_bug_repo
import argparse

def has_labels(issue,labels):
    issue_labels = [l.name for l in issue.labels]
    if type(labels) == str:
        return labels in issue_labels
    for l in labels:
        if not l in issue_labels: return False
    return True

def get_stats(repo_url):
    repo = g.get_repo(repo_url)
    issues = repo.get_issues(state='open')
    z3, cvc4, z3_fixed, cvc4_fixed =[],[],[],[]
    z3_default, cvc4_default, z3_fixed_default, cvc4_fixed_default = [], [], [], []
    z3_soundness, cvc4_soundness, z3_fixed_soundness, cvc4_fixed_soundness = [],[],[],[]
    z3_refutation, z3_solution, cvc4_refutation, cvc4_solution = [],[],[],[]
    for i in issues:
        if has_labels(i, "Z3"): z3.append(i)
        if has_labels(i, "CVC4"): cvc4.append(i)
        if has_labels(i, ["Z3","Fixed"]): z3_fixed.append(i)
        if has_labels(i, ["CVC4","Fixed"]): cvc4_fixed.append(i)
        if has_labels(i, ["Z3","default"]): z3_default.append(i)
        if has_labels(i, ["CVC4","default"]): cvc4_default.append(i)
        if has_labels(i, ["Z3","Fixed","default"]): z3_fixed_default.append(i)
        if has_labels(i, ["CVC4","Fixed","default"]): cvc4_fixed_default.append(i)
        if has_labels(i, ["Z3", "Soundness"]): z3_soundness.append(i)
        if has_labels(i, ["CVC4", "Soundness"]): cvc4_soundness.append(i)
        if has_labels(i, ["Z3", "Fixed", "Soundness"]): z3_fixed_soundness.append(i)
        if has_labels(i, ["CVC4","Fixed", "Soundness"]): cvc4_fixed_soundness.append(i)
        if has_labels(i, ["Z3","refutation_soundness"]): z3_refutation.append(i)
        if has_labels(i, ["Z3","solution_soundness"]): z3_solution.append(i)
        if has_labels(i, ["CVC4","refutation_soundness"]): cvc4_refutation.append(i)
        if has_labels(i, ["CVC4","solution_soundness"]): cvc4_solution.append(i)
    res = [z3, cvc4, z3_fixed, cvc4_fixed, z3_default, cvc4_default, z3_fixed_default,\
          cvc4_fixed_default, z3_soundness, cvc4_soundness, z3_fixed_soundness, cvc4_fixed_soundness,\
          z3_refutation, z3_solution,cvc4_refutation,cvc4_solution]
    return res


"""
[Summary: XXXX (total) / XXXX (fixed)]
[Z3 bugs: XXXX(total) / XXXX (fixed)]
[CVC4 bugs: XXXX ((total) / XXXX(fixed)]
[Bugs in default mode (Z3): XXXX (total) / XXXX(fixed)]
[Bugs in default mode (CVC4): XXXX (total) / XXXX(fixed)]
[Soundness bugs (Z3): XXXX (total) / XXXX (fixed)]
[Soundness bugs (CVC4): XXXX (total) / XXXX (fixed)]
"""
def print_counts(sf_stats,ta_stats):
    summary_total, summary_fixed = len(sf_stats[0]) + len(sf_stats[1]) + len(ta_stats[0]) + len(ta_stats[1]),\
                                   len(sf_stats[2]) + len(sf_stats[3]) + len(ta_stats[2]) + len(ta_stats[3])
    z3_total, z3_fixed = len(sf_stats[0]) + len(ta_stats[0]), len(sf_stats[2]) + len(ta_stats[2])
    z3_total, z3_fixed = len(sf_stats[0]) + len(ta_stats[0]), len(sf_stats[2]) + len(ta_stats[2])
    cvc4_total, cvc4_fixed = len(sf_stats[1]) + len(ta_stats[1]), len(sf_stats[3]) + len(ta_stats[3])
    z3_default, z3_fixed_default = len(sf_stats[4]) + len(ta_stats[4]), len(sf_stats[6]) + len(ta_stats[6])
    cvc4_default, cvc4_fixed_default = len(sf_stats[5]) + len(ta_stats[5]), len(sf_stats[7]) + len(ta_stats[7])
    z3_soundness, z3_fixed_soundness = len(sf_stats[8]) + len(ta_stats[8]),len(sf_stats[10]) + len(ta_stats[10])
    cvc4_soundness, cvc4_fixed_soundness = len(sf_stats[9]) + len(ta_stats[9]),len(sf_stats[11]) + len(ta_stats[11])

    print("<p>[Summary: <b>{0}</b> (total) / <b>{1}</b> (fixed)]<br>".format(summary_total, summary_fixed))
    print("<p>[Z3 bugs: <b>{0}</b> (total) / <b>{1}</b> (fixed)]<br>".format(z3_total, z3_fixed))
    print("[CVC4 bugs: <b>{0}</b> (total) / <b>{1}</b> (fixed)]<br>".format(cvc4_total, cvc4_fixed))
    print("<p>[Bugs in default mode (Z3): <b>{0}</b> (total) / <b>{1}</b> (fixed)]<br>".format(z3_default, z3_fixed_default))
    print("[Bugs in default mode (CVC4): <b>{0}</b> (total) / <b>{1}</b> (fixed)]<br>".format(cvc4_default, cvc4_fixed_default))
    print("<p>[Soundness bugs (Z3): <b>{0}</b> (total) / <b>{1}</b> (fixed)]<br>".format(z3_soundness, z3_fixed_soundness))
    print("[Soundness bugs (CVC4): <b>{0}</b> (total) / <b>{1}</b> (fixed)]<br>".format(cvc4_soundness, cvc4_fixed_soundness))

def extract_url(issue):
    body = issue.body
    for l in body.split("\n"):
        if "link:" in l or "Link:" in l:
            l = l.strip()
            l = l.split(":")[-2]+":"+l.split(":")[-1]
            l = l.strip()
            return l
    print(issue)
    assert(False)

def get_status(issue):
    if has_labels(issue,"Reported"): return "Reported"
    if has_labels(issue,"Confirmed"): return "Confirmed"
    if has_labels(issue,"Fixed"): return "Fixed"
    if has_labels(issue,"Duplicate"): return "Dup"
    if has_labels(issue,"Won't fix") or has_labels(issue,"no-repro"): return "Won't fix"
    print(issue.labels, issue.html_url,flush=True)
    assert(False)


"""
Print Semantic Fusion bug links
<h2>Bug findings with Semantic Fusion</h2>
<h2>CVC4</h2>
<a href=https://github.com/CVC4/CVC4/issues/3106>https://github.com/CVC4/CVC4/issues/3106</a> Confirmed<br>
...
<h2>Z3</h2>
<a href=https://github.com/Z3Prover/z3/issues/2366>https://github.com/Z3Prover/z3/issues/2366</a> Fixed<br>
"""
def print_html_sf(sf_stats):
    z3,cvc4 = sf_stats[0], sf_stats[1]
    print("<h2>Bug findings with Semantic Fusion</h2>")
    print("\n<h2>CVC4</h2>")
    for i in cvc4:
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))
    print("\n<h2>Z3</h2>")
    for i in z3:
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))

"""
Print Type-aware mutation bug links
<h2>Bug findings with Type-aware mutation</h2>
<h2>========= CVC4 =========</h2>
<h2>Soundness Bugs</h2>
<h4>Refutation Soundness</h4>
...
<h4>Solution Soundness</h4>
...
<h2>========= Z3 =========</h2>
<h2>Soundness Bugs</h2>
<h4>Refutation Soundness</h4>
"""
def print_html_ta(ta_stats):
    z3,cvc4 = ta_stats[0], ta_stats[1]
    z3_refutation, z3_solution = ta_stats[12], ta_stats[13]
    cvc4_refutation, cvc4_solution = ta_stats[14], ta_stats[15]
    print("<h2>Bug findings with Type-aware mutation</h2>")
    print("<h2>========= CVC4 =========</h2>")
    print("<h2>Soundness Bugs</h2>")
    print("<h4>Refutation Soundness</h4>")
    for i in cvc4_refutation:
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))
    print("\n<h4>Solution Soundness</h4>")
    for i in cvc4_solution:
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))
    print("<h2>Others</h2>")
    for i in cvc4:
        if has_labels(i,["Soundness"]):continue
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))

    print()
    print("<h2>========= Z3 =========</h2>")
    print("<h2>Soundness Bugs</h2>")
    print("<h4>Refutation Soundness</h4>")
    for i in z3_refutation:
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))
    print("\n<h4>Solution Soundness</h4>")
    for i in z3_solution:
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))
    print("<h2>Others</h2>")
    for i in z3:
        if has_labels(i,["Soundness"]):continue
        url, status = extract_url(i),get_status(i)
        print("<a href=\"{0}\">{0}</a> {1} <br />".format(url,status))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--summary', action='store_true')
    parser.add_argument('--sf-reports', action='store_true')
    parser.add_argument('--ta-reports', action='store_true')
    args = parser.parse_args()
    g = Github(privacy_key)
    if args.summary:
         ta_stats = get_stats(ta_bug_repo)
         sf_stats = get_stats(sf_bug_repo)
         print_counts(sf_stats, ta_stats)
    elif args.sf_reports:
        sf_stats = get_stats(sf_bug_repo)
        print_html_sf(sf_stats)
    elif args.ta_reports:
        ta_stats = get_stats(ta_bug_repo)
        print_html_ta(ta_stats)
