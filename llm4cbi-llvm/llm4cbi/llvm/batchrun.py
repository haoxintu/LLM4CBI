from multiprocessing import Pool
from llm4cbi.util import *
from configparser import ConfigParser

def run(bugId, revision, right, wrong, checkpass, k, configFile):
    import os
    # path = os.getcwd() + '/llm4cbi/llvm/search-A2C-gpt-sim-div.py'
    path = os.getcwd() + '/llm4cbi/llvm/search-A2C-gpt.py'
    os.system('python '+ path + ' ' + revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)

def run_llama(bugId, revision, right, wrong, checkpass, k, configFile):
    import os
    path = os.getcwd() + '/llm4cbi/llvm/search-A2C-llama.py'
    # path = os.getcwd() + '/llm4cbi/llvm/search-A2C.py'
    os.system('python '+ path + ' ' + revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)


def batchrun(bugIds, revisions, rights, wrongs, checkpasses, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    batch_num = cfg.getint('params', 'batch_num')
    loops = cfg.getint('params', 'loops')

    # p = Pool(processes = batch_num)
    # for k in range(1, loops+1):
    if 1:
        # for i in range(len(bugIds)):
        if 1:
            bugId = bugIds
            revision = revisions
            right = rights
            wrong = wrongs
            checkpass = checkpasses
            # p.apply_async(run, args=(bugId, revision, right, wrong, checkpass, k, configFile))
            run (bugId, revision, right, wrong, checkpass, 1, configFile)
    # p.close()
    # p.join()

def batchrun_llama(bugIds, revisions, rights, wrongs, checkpasses, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    batch_num = cfg.getint('params', 'batch_num')
    loops = cfg.getint('params', 'loops')

    # p = Pool(processes = batch_num)
    # for k in range(1, loops+1):
    if 1:
        # for i in range(len(bugIds)):
        if 1:
            bugId = bugIds
            revision = revisions
            right = rights
            wrong = wrongs
            checkpass = checkpasses
            # p.apply_async(run, args=(bugId, revision, right, wrong, checkpass, k, configFile))
            run_llama(bugId, revision, right, wrong, checkpass, 1, configFile)
    # p.close()
    # p.join()

if __name__ == '__main__':
    bugIds = ['15920']
    revisions = ['r181189']
    rights = ['-O2']
    wrongs = ['-O3']
    checkpasses = 'checkIsPass_wrongcodeOneline'
    cfg = ConfigParser()
    cfg.read('config/config.ini')
    configFile = cfg.get('llvm-locations', 'configFile')
    batchrun(bugIds, revisions, rights, wrongs, checkpasses, configFile)
