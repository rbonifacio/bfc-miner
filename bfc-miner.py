import time
import re
import json
import git
import csv

import numpy as np

output = open("out.csv", "w")


csvFileName = raw_input('Path for the csv file: ')

with open(csvFileName) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        regex = '({}-[09\w]+)'.format(row[0])
        handle = open(row[1], "r")

        print("\n \n **** Processing project " + row[0] + " *** \n ")

        # --------------------------------
        # Loading the issues database
        # --------------------------------
        
        contents = handle.read()
        issues   = json.loads(contents)

        items    = {}
        total    = 0 
        dups     = 0

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

        # --------------------------------
        # finding the set of issues' BFCs 
        # --------------------------------

        start_time = time.time()

        repo = git.Repo(row[2])
        log  = repo.iter_commits()

        err1    = 0                        # commits that we didn't find an issue 
        err2    = 0                        # commits without issue reference

        matches = 0                        # number of commits we match!

        for info in log:    
            m = re.search(regex, info.message)
            if m and str(m.group(1)) in items:
                bfcs = items[str(m.group(1))]
                bfcs.append(str(info))
                items[m.group(1)] = bfcs
                output.write(row[0] + "," + m.group(1) + "," + str(info) + "\n")
                matches += 1
            elif m:
                err1 += 1
            else:
                err2 += 1

        print("Finished in %s seconds. \n" % (time.time() - start_time))
       
        print("(*) Total of matches: " + str(matches))
        print("(*) Total of commits that we did not find the issue: " + str(err1))
        print("(*) Total of commits without a reference to an issue: " + str(err2))

        # --------------------------------
        # computing basic statistics 
        # --------------------------------
        
        bfcs_per_issue = list()

        for issue in items:
            bfcs = items[issue]
            bfcs_per_issue.append(len(bfcs)) 

        print("Statistics about the number of BFCs of the issues")
        
        print("min number of bfcs:    " + str(np.min(bfcs_per_issue)))
        print("max number of bfcs:    " + str(np.max(bfcs_per_issue)))
        print("mean number of bfcs:   " + str(np.mean(bfcs_per_issue)))
        print("median number of bfcs: " + str(np.median(bfcs_per_issue)))
        print("hist:                  " + str(np.histogram(bfcs_per_issue)))

        print("\n \n **** Finishing processing project " + row[0] + " *** \n ")
        
        handle.close()

output.close()

#    dictionary  = eval('{{ "hash" : "{}", "author" : "{}", "date": "{}", "message": "{}" }}'.format(str(info), str(info.author), str(info.committed_date),info.message.replace("\n", "\\n"))
