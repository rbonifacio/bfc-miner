import time
import re
import json
import git

import numpy as np

name = raw_input("Project name (same as the issue number prefix): ")
f = raw_input("JSON file with the issues repository: ")
repo_url  = raw_input("path to the local git repository: ")


regex = '({}-[09\w]+)'.format(name)

print(regex)

h = open(f, "r")
contents = h.read()

issues = json.loads(contents)

max = 0

items = {}

total = 0 
dups = 0

print('Parsing issues ...')
start_time = time.time()
for issue in issues:
    if issue in items:
        dups += 1
    else:
        items[issue] = list()
        total += 1

print("Finished in %s seconds. \n" % (time.time() - start_time))

print('(*) Total issues     : ' + str(total))
print('(*) Duplicated issues: ' + str(dups))

print('\n') 
print('Loading repository data ...')

repo = git.Repo(repo_url)

log = repo.iter_commits()

max = 0

matches = 0
err1 = 0
err2 = 0

for info in log:    
    m = re.search(regex, info.message)
    if m and str(m.group(1)) in items:
        bfcs = items[str(m.group(1))]
        bfcs.append(str(info))
        items[m.group(1)] = bfcs
        matches += 1
    elif m:
        err1 += 1
    else:
        err2 += 1

print("Total of matches: " + str(matches))
print("Total of commits that we did not find the issue: " + str(err1))
print("Total of commits without a reference to an issue: " + str(err2))

info1 = 0
info2 = 0
info3 = 0
l = list()
for issue in items:
    bfcs = items[issue]
    l.append(len(bfcs)) 
    if(len(bfcs) == 0):
        info1 += 1
    elif len(bfcs) == 1:
        info2 += 1
    else:
        info3 += 1

print("Total of issues without bfc " + str(info1))
print("Total of issues with exactly one bfc: " + str(info2))
print("Total of issues with more than one bfc: " + str(info3))

print(np.min(l))
print(np.max(l))
print(np.mean(l))
print(np.median(l))

h.close()


#    dictionary  = eval('{{ "hash" : "{}", "author" : "{}", "date": "{}", "message": "{}" }}'.format(str(info), str(info.author), str(info.committed_date),info.message.replace("\n", "\\n"))
