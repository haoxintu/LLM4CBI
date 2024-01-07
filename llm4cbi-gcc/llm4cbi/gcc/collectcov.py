import os
from RecBi.util import exccmd

def collect(compilersdir, infodir, bugIds, revisions, wrongoptions):

    for i in range(len(bugIds)):

        wrongoption = wrongoptions[i]
        bugId = bugIds[i]
        revision = revisions[i]

        testname = 'fail'

        covdir = compilersdir + revision + '/' + revision + '-build/gcc'
        srcdir = compilersdir + revision + '/' + revision + '/gcc'
        gccdir = compilersdir + revision + '/' + revision + '-build/bin'
        resdir = infodir + bugId

        os.chdir(resdir)

        # if os.path.exists(resdir + '/' + testname):
        #     exccmd('rm -rf ' + resdir + '/' + testname)


        exccmd('mkdir ' + resdir + '/' + testname)
        if os.path.exists(resdir + '/' + testname + '/method_info.txt') \
                and os.path.exists(resdir + '/' + testname + '/stmt_info.txt'):
            methodfile = open(resdir + '/' + testname + '/method_info.txt', 'r')
            methodlines = methodfile.readlines()
            methodfile.close()
            stmtfile = open(resdir + '/' + testname + '/stmt_info.txt', 'r')
            stmtlines = stmtfile.readlines()
            stmtfile.close()
            if len(stmtlines) > 0 and len(methodlines) > 0:
                continue
        # print("###THX gccdir : ", gccdir)
        # print("###THX resdir : ", resdir)
        methodfile = open(resdir + '/' + testname + '/method_info.txt', 'w')
        stmtfile = open(resdir + '/' + testname + '/stmt_info.txt', 'w')
        # delete all .gcda files
        # print("###THX covdir : ", covdir)
        exccmd('find ' + covdir + ' -name \"*.gcda\" | xargs rm -f')
        # compile test program
        wrongoption = wrongoption.replace("+", " ")  # THX
        print("wrongoption = ", wrongoption)
        exccmd(gccdir + '/gcc ' + wrongoption + ' ' + testname + '.c')  # change per bug

        if os.path.exists('gcdalist'):
            exccmd('rm gcdalist')
        # exccmd('find ' + srcdir + ' -name \"*.c\" > gcdalist')
        # exccmd('find ' + srcdir + ' -name \"*.h\" >> gcdalist')
        exccmd('find ' + covdir + ' -name \"*.gcda\" > gcdalist')

        # print("###THX srcdir : ", srcdir)
        f = open('gcdalist')
        lines = f.readlines()
        f.close()
        # print("###THX lines : ", lines)
        for i in range(len(lines)):
            gcdafile=lines[i].strip().replace(srcdir,covdir)
            # gcdafile=lines[i].strip().replace("-build","")

            if '/gcc/testsuite/' in gcdafile:
                continue
            # exccmd('cp ' + lines[i].strip() + ' ' + lines[i].strip().replace("-build", ""))
            # exccmd('cp ' + lines[i].strip() + ' ' + lines[i].strip().replace(srcdir, covdir))
            # print(lines[i].strip() + " --- " + lines[i].strip().replace("-build", ""))
            # print("### THX ?")
            # print("###THX gcdafile : ", gcdafile)
            os.chdir(covdir)
            # os.system('pwd')
            exccmd('rm *.gcov')
            if os.path.exists('gcovfile'):
                exccmd('rm gcovfile')
            #exccmd(gccdir + '/gcov -f '+gcdafile+' > gcovfile')
            exccmd('./gcov -f ' + gcdafile + ' > gcovfile')
            # os.chdir(resdir)
            # exccmd('gcov -f ' + gcdafile + ' > gcovfile')
            # print("gcdafile.strip : ", gcdafile.strip().split('/')[-1].replace('gcda', 'c'))
            file_temp = ""
            if os.path.exists('./' + gcdafile.strip().split('/')[-1].replace('gcda', 'c') + '.gcov'):
                # if not os.path.exists('./' + gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov'):
                file_temp = './' + gcdafile.strip().split('/')[-1].replace('gcda', 'c') + '.gcov'
            elif os.path.exists('./' + gcdafile.strip().split('/')[-1].replace('gcda', 'h') + '.gcov'):
                # if not os.path.exists('./' + gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov'):
                file_temp = './' + gcdafile.strip().split('/')[-1].replace('gcda', 'h') + '.gcov'
            else:
                continue
            # print("file_temp : ", file_temp)
            f = open('gcovfile')
            gcovlines = f.readlines()
            # print("### THX gcovlines : ", gcovlines)
            f.close()
            for j in range(len(gcovlines)):
                if 'Function \'' in gcovlines[j].strip():
                    if 'Lines executed:' in gcovlines[j + 1].strip() and float(
                            gcovlines[j + 1].strip().split('Lines executed:')[1].split('%')[0].strip()) != 0.0:
                        methodfile.write(gcdafile + ',' + gcovlines[j].strip().split('\'')[1] + ',' +
                                         gcovlines[j + 1].strip().split('Lines executed:')[1].split('%')[
                                             0].strip() + ',' + gcovlines[j + 1].strip().split('of')[-1].strip() + '\n')
            # os.chdir(resdir)
            # f = open(gcdafile.strip().split('/')[-1] + '.gcov')
            # print("file_temp : ", file_temp)
            f = open(file_temp)
            # print("###THX open?")
            stmtlines = f.readlines()
            # print("###THX stmtlines : ", stmtlines)
            f.close()

            tmp = []
            for j in range(len(stmtlines)):
                if stmtlines[j] == '------------------\n':
                    continue
                covcnt = stmtlines[j].strip().split(':')[0].strip()
                linenum = stmtlines[j].strip().split(':')[1].strip()
                if covcnt != '-' and covcnt != '#####':
                    tmp.append(linenum)
            if len(tmp) == 0:
                continue
            # print("###THX stmtfile : ", gcdafile+':'+','.join(tmp)+'\n')
            stmtfile.write(gcdafile+':'+','.join(tmp)+'\n')
        # print("at end?")
        stmtfile.close()
        methodfile.close()
