import os, sys
from configparser import ConfigParser

def rewrite_installs(new_installs, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    bugList = cfg.get('llvm-locations', 'bugList')
    f = open(bugList)
    lines = f.readlines()
    f.close()
    downi = 0
    downj = 0
    for i in range(downi, len(new_installs)):
        bugId1 = new_installs[i]
        for j in range(downj, len(lines)):
            bugId2 = lines[j].strip().split(',')[0]
            if bugId1 == bugId2:
                # lines[j] = lines[j].split('\n')[0][:-10] + 'install_yes\n'
                lines[j] = lines[j].split('\n')[0][:-10] + 'install_yes\n'  # TODO do not modify for now
                downi = i + 1
                downj = j + 1
                break
    f = open(bugList, 'w')
    for line in lines:
        f.write(line)
    f.close()

def installSVN(revisions, configFile, whether_installs, bugIds):

    cfg = ConfigParser()
    cfg.read(configFile)
    install_thread = cfg.get('params', 'install_thread')
    compilersdir = cfg.get('llvm-locations', 'compilersdir')
    # password = cfg.get('password', 'password')
    # autosudo = 'echo ' + password + ' | sudo -S '
    print("###THX : params in installSVN: ", revisions, configFile, whether_installs, bugIds)
    new_installs = []

    if revisions == []:
        print('\033[1;35m No LLVM trunk is ready to be installed...\033[0m')

    for i in range(len(revisions)):

        whether_install = whether_installs[i]
        if whether_install == 'install_yes':
            continue

        rev = revisions[i]
        revpath = compilersdir+'/'+rev

        bugId = bugIds[i]

        try:
            # os.system('mkdir '+revpath)
            # print('\033[1;35m svn downloading..\033[0m')
            # print("###THX rev revpath : ", rev, revpath)
            # print('downloading llvm ... ')
            # os.system('git clone https://github.com/llvm-mirror/llvm.git')
            # print("checkout to the faulty version")
            # os.system("cd llvm; git checkout 5d042c63741bc5ccec8ad18bfebf9f621fcde640; cd ..")
            # os.system('rm -rf ' + revpath + '/' + rev)
            # os.system('mv llvm ' + revpath + '/' + rev)
            # print('downloading clang ... ')
            # os.system('git clone https://github.com/llvm-mirror/clang.git')
            # print("checkout to the faulty version")
            # os.system("cd clang; git checkout 5d042c63741bc5ccec8ad18bfebf9f621fcde640; cd ..")
            # os.system('mv clang ' + revpath + '/' + rev + '/tools/clang')
            # os.system('mv clang ' + revpath + '/')
            # os.system('svn co http://llvm.org/svn/llvm-project/cfe/trunk -'+rev+' '+revpath+'/'+rev+'/tools/clang')
            # os.system('svn co http://llvm.org/svn/llvm-project/llvm/trunk -'+rev+' '+revpath+'/'+rev)
            # os.system('svn co http://llvm.org/svn/llvm-project/cfe/trunk -'+rev+' '+revpath+'/'+rev+'/tools/clang')
            print("start build llvm compiler")
            os.system('rm -rf '+revpath+'/'+rev+'-build')
            os.system('mkdir '+revpath+'/'+rev+'-build')
            os.chdir(revpath+'/'+rev+'-build')
            print('\033[1;35m cmake...\033[0m')
            os.system('cmake -DCMAKE_EXPORT_COMPILER_COMMANDS=ON -DLLVM_TARGETS_TO_BUILD="X86" -DCMAKE_INSTALL_PREFIX='+compilersdir+'/'+rev+'/'+rev+'-build -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=gcc-7 -DCMAKE_CXX_COMPILER=g++-7 -DCMAKE_C_FLAGS=\"-g -O0 -fprofile-arcs -ftest-coverage\" -DCMAKE_CXX_FLAGS=\"-g -O0 -fprofile-arcs -ftest-coverage\" -DCMAKE_EXE_LINKER_FLAGS=\"-g -fprofile-arcs -ftest-coverage -lgcov\" -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python2 ../'+rev)
            print('\033[1;35m make..\033[0m')
            os.system('make -j ' + str(install_thread))
            os.system('make install')
        except:
            print('\033[1;35m Failed to install LLVM revision ', str(rev),'\033[0m')

        new_installs.append(bugId)


    rewrite_installs(new_installs, configFile)
