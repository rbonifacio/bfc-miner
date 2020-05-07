# BFC-MINER

Mine the bug fix commits from a project.

### Execution

Just run `python bfc-miner.py` and then inform the csv file with the list
of projects that should be processed. Each row in the csv file
must have three columns:

   * the project name
   * the path to the json file with the list of project's issues
   * the path to the local git repository of the project

