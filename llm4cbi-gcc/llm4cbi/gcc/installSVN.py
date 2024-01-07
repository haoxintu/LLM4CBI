import os, sys
from ..util import exccmd
from configparser import ConfigParser

def rewrite_installs(new_installs, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    bugList = cfg.get('gcc-locations', 'bugList')
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
                lines[j] = lines[j].split('\n')[0][:-10] + 'install_no\n' # TODO change this to yes after building
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
    compilersdir = cfg.get('gcc-locations', 'compilersdir')
    # password = cfg.get('password', 'password')
    # autosudo = 'echo ' + password + ' | sudo -S '
    new_installs = []

    if revisions == []:
        raise Exception('No compiler trunk is ready to be installed...')

    for i in range(len(revisions)):

        whether_install = whether_installs[i]
        if whether_install == 'install_yes':
            continue
        bugId = bugIds[i]
        rev = revisions[i]
        revpath = compilersdir+'/'+rev
        print("###THX revpath : ", revpath)
        # if os.path.exists(revpath):
        #    exccmd('rm -rf '+revpath)
        try:
            # os.system('mkdir '+revpath)
            # print('\033[1;35m svn downloading..\033[0m')
            os.system('svn co svn://gcc.gnu.org/svn/gcc/trunk -' + rev + ' ' + revpath + '/' + rev)
            # os.system('rm -rf ' + revpath + '/' + rev + '-build')
            os.system('mkdir ' + revpath + '/' + rev + '-build')
            os.chdir(revpath + '/' + rev + '-build')
            os.system('cd ../' + rev + '; ./contrib/download_prerequisites; cd ../' + rev + '-build')

            # os.system(
            #  '../' + rev + '/configure --enable-languages=c,c++ --disable-werror --enable-checking=release --with-gmp=/home/haoxin/disk-dut/research/compilers/gcc-11/gmp --with-mpfr=/home/haoxin/disk-dut/research/compilers/gcc-11/mpfr --with-mpc=/home/haoxin/disk-dut/research/compilers/gcc-11/mpc --prefix=' + revpath + '/' + rev + '-build' + ' --enable-coverage')

            os.system(
                'CC=gcc-4.8 CXX=g++-4.8 ../' + rev + '/configure --enable-languages=c,c++ --disable-werror --enable-checking=release  MAKEINFO=missing --prefix=' + revpath + '/' + rev + '-build' + ' --enable-coverage')
            print('\033[1;35m make..\033[0m')
            os.system('make -j ' + str(install_thread))
            os.system('make install')
            # os.chdir(compilersdir)
        except:
            print('\033[1;35m Failed to install GCC revision ', str(rev),'\033[0m')

        new_installs.append(bugId)
    rewrite_installs(new_installs, configFile)
