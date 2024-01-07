from multiprocessing import Pool
from ..util import *
from configparser import ConfigParser

def run(bugId, revision, right, wrong, checkpass, k, configFile):
    print("THX run?")
    # print("run the following", 'python /home/haoxin/disk-dut/research/RecBi-GCC/RecBi/RecBi/gcc/search-A2C.py '+revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)
    # os.system('python /home/haoxin/disk-dut/research/RecBi-GCC/RecBi/RecBi/gcc/search-A2C.py '+revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)
    # os.system('python /home/haoxin/disk-dut/research/RecBi-GCC/RecBi-gpt/RecBi/gcc/search-A2C-gpt.py '+revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)
    os.system('python /home/haoxin/disk-dut/research/RecBi-GCC/RecBi-gpt/RecBi/gcc/search-A2C-gpt.py '+revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)

def batchrun(bugIds, revisions, rights, wrongs, checkpasses, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    batch_num = cfg.getint('params', 'batch_num')
    loops = cfg.getint('params', 'loops')
    # print("THX in batch run?")
    # p = Pool(processes = batch_num)
    for k in range(1, loops+1):
        # for i in range(len(bugIds)):
        if 1:
            bugId = bugIds
            revision = revisions
            right = rights
            wrong = wrongs
            checkpass = checkpasses
            # p.apply_async(run, args=(bugId, revision, right, wrong, checkpass, k, configFile))
            run (bugId, revision, right, wrong, checkpass, k, configFile)
    # p.close()
    # p.join()

def run_llama(bugId, revision, right, wrong, checkpass, k, configFile):
    print("THX run?")
    # print("run the following", 'python /home/haoxin/disk-dut/research/RecBi-GCC/RecBi/RecBi/gcc/search-A2C.py '+revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)
    # os.system('python /home/haoxin/disk-dut/research/RecBi-GCC/RecBi/RecBi/gcc/search-A2C.py '+revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)
    os.system('python /home/haoxin/disk-dut/research/RecBi-GCC/RecBi-gpt/RecBi/gcc/search-A2C-llama.py '+revision+' '+right+' '+wrong+' '+checkpass+' '+str(k) + ' ' + configFile + ' ' + bugId)

def batchrun_llama(bugIds, revisions, rights, wrongs, checkpasses, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    batch_num = cfg.getint('params', 'batch_num')
    loops = cfg.getint('params', 'loops')
    # print("THX in batch run?")
    # p = Pool(processes = batch_num)
    for k in range(1, loops+1):
        # for i in range(len(bugIds)):
        if 1:
            bugId = bugIds
            revision = revisions
            right = rights
            wrong = wrongs
            checkpass = checkpasses
            # p.apply_async(run, args=(bugId, revision, right, wrong, checkpass, k, configFile))
            run_llama(bugId, revision, right, wrong, checkpass, k, configFile)
    # p.close()
