from RecBi.llvm import *
from RecBi.util import metrics
from configparser import ConfigParser
import sys
import json


run = sys.argv[1]

cfg = ConfigParser()
cfg.read('config-{}/config.ini'.format(run))
configFile = cfg.get('llvm-locations', 'configFile')
bugList = cfg.get('llvm-locations', 'bugList')
compilersdir = cfg.get('llvm-locations', 'compilersdir')
infodir = cfg.get('llvm-locations', 'infodir')

revisions = []
bugIds = []
rights = []
wrongs = []
checkpasses = []

revfile = open(bugList)
revlines = revfile.readlines()
revfile.close()

os.system("rm final_results-{}.txt ; touch final_results-{}.txt".format(run, run))

for i in range(len(revlines)):
    
    bugIds = revlines[i].strip().split(',')[0]
    revisions = revlines[i].strip().split(',')[1]
    rights = revlines[i].strip().split(',')[2]
    wrongs = revlines[i].strip().split(',')[3]
    checkpasses = revlines[i].strip().split(',')[4]
    # reduced = cfg.get('llvm-rev', 'reduced').split(',')
    #print(reduced)

    # bugIds = list(set(bugIds) - set(reduced))

    mode = cfg.get('mode', 'mode')
    if mode != 'verification' and mode != 'utilization':
        raise Exception('Unknown mode... Please check config.ini and correct it.')

    print('\033[1;35m Begin batchrun\033[0m')
    # batch run to get the configureFile
    print("input of batch run")
    print("bugIds: ", bugIds)
    print("revisions: ", revisions)
    print("rights: ", rights)
    print("wrongs: ", wrongs)
    print("checkpasses: ", checkpasses)
    print("configFile: ", configFile)
    batchrun(bugIds, revisions, rights, wrongs, checkpasses, configFile)
    # batchrun_llama(bugIds, revisions, rights, wrongs, checkpasses, configFile)
    print('\033[1;35m Begin delete\033[0m')
    #delete(configFile)
   

    print('\033[1;35m mode::verification\033[0m')

    print('\033[1;35m Begin rank\033[0m')
    rank(revisions, bugIds, configFile)
    print('\033[1;35m Begin analyze\033[0m')
    finallist = analyze(configFile)
    result = metrics(finallist)

    # @THX
    os.system("pwd")
    with open('final_results-{}.txt'.format(run), 'a') as convert_file:
        convert_file.write(str(bugIds) + " : ")
        convert_file.write(json.dumps(finallist) + " \t ")
        convert_file.write(json.dumps(result))
        convert_file.write("\n")

    print('\033[1;35m finallist = ', finallist,'\033[0m')
    print('\033[1;35m result = ', result,'\033[0m')
    
