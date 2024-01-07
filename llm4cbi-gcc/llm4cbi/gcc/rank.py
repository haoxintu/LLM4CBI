import os,sys,math
from configparser import ConfigParser

def rank(revisions, bugIds, configFile):

    cfg = ConfigParser()
    cfg.read(configFile)
    loops = cfg.getint('params', 'loops')
    infodir = cfg.get('gcc-locations', 'infodir')
    passdir = cfg.get('gcc-locations', 'passdir')
    bugList = cfg.get('gcc-locations', 'bugList')
    resultFile = cfg.get('gcc-locations', 'resultFile')

    for loop in range(1, loops+1):

        # revisions = []
        # bugIds = []
        # revfile = open(bugList)
        # revlines = revfile.readlines()
        # revfile.close()
        #
        # for i in range(len(revlines)):
        #     revisions.append(revlines[i].strip().split(',')[1])
        #     bugIds.append(revlines[i].strip().split(',')[0])

        passdir2 = passdir + str(loop)
        # print("passdir2 : ", passdir2)

        # remove mutators
        os.system("rm " + passdir2 + '/' + bugIds + '/add*')
        os.system("rm " + passdir2 + '/' + bugIds + '/remModifierQualifier')
        os.system("rm " + passdir2 + '/' + bugIds + '/rep*')
        os.system("rm -rf " + passdir2 + '/' + bugIds + '/testFile')

        resultFile2 = resultFile.split('.csv')[0] + str(loop) + '.csv'
        result = open(resultFile2,'w')

        # for i in range(len(revisions)):
        if 1:
            # print("len of revisions : ", len(revisions))
            # print("i = ", i)
            rev = revisions
            bugId = bugIds
            result.write(rev+ '  bug' + bugId + ':\n')
            locationfile = open(infodir+'/'+bugId+'/locations')
            locationlines = locationfile.readlines()
            locationfile.close()
            buggyfiles = set()

            for i in range(len(locationlines)):
                if 'file' in locationlines[i].strip() and 'method' in locationlines[i].strip():
                    buggyfile = locationlines[i].strip().split(';')[0].strip().split(':')[1].strip().split('trunk/')[-1]
                    # print("bugfile : ", buggyfile)
                    # buggyfile = "gcc/gimple.c" # TODO FOR TESTING ONLY
                    buggyfiles.add(buggyfile)

            if os.path.exists(infodir+'/'+bugId+'/failcov/stmt_info.txt'):
                tarpath=infodir+'/'+bugId+'/failcov/stmt_info.txt'
            elif os.path.exists(infodir+'/'+bugId+'/fail/stmt_info.txt'):
                tarpath=infodir+'/'+bugId+'/fail/stmt_info.txt'
            else:
                print ("Error!!")
                sys.exit(1)

            failfile = open(tarpath)
            faillines = failfile.readlines()
            failfile.close()

            failstmt = dict()
            passstmt = dict()
            failfileset = set()
            failfilemapstmt = dict()
            # get fail names
            for i in range(len(faillines)):
                # print faillines[i]
                file_str_fail = faillines[i].strip().split(':')[0].split('-build/')[0] + '/' + faillines[i].strip().split(':')[0].split('-build/')[1]
                # filename = faillines[i].strip().split(':')[0].split('-build/')[1].replace("gcda", "c")  # THX TODO should be ok only keep .c?
                # print("file_str_fail : ", file_str_fail)
                file_temp = ""
                # os.system("pwd")
                # if os.path.exists(file_str_fail.replace("gcda", "c")):
                # print("yes?")
                    # if not os.path.exists('./' + gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov'):
                file_temp = faillines[i].strip().split(':')[0].split('-build/')[1].replace("gcda", "c")
                # print("fail file_temp : ", file_temp)
                # elif os.path.exists(file_str_fail.replace("gcda", "h")):
                    # print("no?")
                    # if not os.path.exists('./' + gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov'):
                    # file_temp = faillines[i].strip().split(':')[0].split('-build/')[1].replace("gcda", "h")
                #else:
                #     continue
                # print("file_temp fail : ", file_temp)
                # filename = faillines[i].strip().split(':')[0].split('-build/')[1]
                # filename = faillinesplit[0].strip().split('.gcda')[0].strip()
                # print("filename in faillines : ", faillines[i].strip().split(':')[0].split('-build/')[1])
                filename = file_temp
                # print("filename in faillines : ", filename)
                # if not filename.endswith('.c'):
                #     continue
                failfileset.add(filename)
                stmtlist = faillines[i].strip().split(':')[1].split(',')
                # print("stmtlist fail : ", stmtlist)
                failfilemapstmt[filename] = set(stmtlist)
                for stmt in stmtlist:
                    failstmt[filename + ',' + stmt] = 1
                    passstmt[filename + ',' + stmt] = 0
            # print("failstmt : ", failstmt)
            # print("passstmt : ", passstmt)
            # get passing file names
            for i in os.listdir(passdir2 + '/' + bugId + '/passcov'):
                # print("??? i = ", i, " path : ", passdir2 + '/' + bugId + '/passcov')
                passfile = open(passdir2 + '/' + bugId + '/passcov/' + i + '/stmt_info.txt')
                passlines = passfile.readlines()
                passfile.close()
                #print("passlines : ", passlines)
                for j in range(len(passlines)):
                    # filename = passlines[j].strip().split(':')[0].split('-build/')[0]
                    file_str1 = passlines[j].strip().split(':')[0].split('-build/')[0] + '/' + passlines[j].strip().split(':')[0].split('-build/')[1]
                    #print("file_str1 :", file_str1)
                    # print("filename----- : ", file_str1.replace("gcda", "c"))

                    #filename = passlines[j].strip().split(':')[0].split('-build/')[1].replace("gcda", "c")
                    file_temp = ""
                    # TODO only rank .c files
                    # if os.path.exists(file_str1.replace("gcda", "c")):
                        # print("yes?")
                        # if not os.path.exists('./' + gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov'):
                    file_temp = passlines[j].strip().split(':')[0].split('-build/')[1].replace("gcda", "c")
                    # print("file_temp:", file_temp)
                    #elif os.path.exists(file_str1.replace("gcda", "h")):
                    #     print("no?")
                        # if not os.path.exists('./' + gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov'):
                    #    file_temp = passlines[j].strip().split(':')[0].split('-build/')[1].replace("gcda", "h")
                    #else:
                    #    continue
                    # print("file_temp pass: ", file_temp)
                    # print("filename : ", filename)
                    # if not filename.endswith('.c'):  # consider c and h files
                    #     continue
                    # if not filename.endswith('.h'):  # consider c and h files
                    #     continue
                    filename = file_temp
                    # print("filename : ", filename)
                    # print("failfileset: ", failfileset)
                    if filename not in failfileset:
                        continue
                    # print("filename 1111: ", filename)
                    stmtlist = passlines[j].strip().split(':')[1].split(',')
                    # print("stmtlist pass : ", stmtlist)
                    # print("failfilemapstmt[filename] : ", failfilemapstmt[filename])
                    # print("set(stmtlist) & failfilemapstmt[filename]: ", set(stmtlist) & failfilemapstmt[filename])
                    for stmt in set(stmtlist) & failfilemapstmt[filename]:
                        if filename+','+stmt in failstmt.keys():
                            # print("never executed here?")
                            # exit(1)
                            # print("key in increment : ",filename + ',' + stmt )
                            passstmt[filename + ',' + stmt] += 1
            # print("failstmt : ", failstmt)
            # print("passstmt : ", passstmt)
            score = dict()
            filescore = dict()
            for key in failstmt.keys():
                # print("key : ", key)
                # print("failstmt[key] : ", failstmt[key])
                # print("passstmt[key] : ", passstmt[key])
                score[key] = float(failstmt[key]) / math.sqrt(
                    float(failstmt[key]) * (failstmt[key] + passstmt[key]))
                # if passstmt[key]==0:
                #   score[key]=1.0
                # else:
                #   score[key]=float(failstmt[key])/passstmt[key]

                keyfile = key.split(',')[0]
                if keyfile not in filescore.keys():
                    filescore[keyfile] = []
                    filescore[keyfile].append(score[key])
                else:
                    filescore[keyfile].append(score[key])
            # print("socre : ", score)
            # print("filesocre : ", filescore)
            fileaggstmtscore = dict()
            for key in filescore.keys():
                fileaggstmtscore[key] = float(sum(filescore[key])) / len(filescore[key])
            scorelist = sorted(fileaggstmtscore.items(), key=lambda d: d[1], reverse=True)
            # print("scrorelist : ", scorelist, "len : ", len(scorelist))
            # print("fileaggstmtscore : ", fileaggstmtscore)
            print("buggyfiles : ", buggyfiles)
            for bf in buggyfiles:
                tmp = []
                for i in range(len(scorelist)):
                    # if bf not in fileaggstmtscore:
                    #     print('\033[1;35m The buggy file is not located in the finalist\033[0m')
                    #     exit(1)
                    if fileaggstmtscore[bf] == scorelist[i][1]:
                        tmp.append(i)
                result.write(
                    bf + ',' + str(min(tmp) + 1) + ',' + str(max(tmp) + 1) + ',' + str(fileaggstmtscore[bf]) + '\n')
            result.write('\n')
            result.flush()
        result.close()

def rank_(revisions, bugIds, configFile):
    cfg = ConfigParser()
    cfg.read(configFile)
    loops = cfg.getint('params', 'loops')
    infodir = cfg.get('gcc-locations', 'infodir')
    passdir = cfg.get('gcc-locations', 'passdir')
    rankFile = cfg.get('gcc-locations', 'rankFile')
    finalrank = {}

    for loop in range(1, loops + 1):

        # revisions = []
        # bugIds = []
        # revfile = open(bugList)
        # revlines = revfile.readlines()
        # revfile.close()
        #
        # for i in range(len(revlines)):
        #     revisions.append(revlines[i].strip().split(',')[1])
        #     bugIds.append(revlines[i].strip().split(',')[0])

        passdir2 = passdir + str(loop)


        for i in range(len(revisions)):
            rev = revisions[i]
            bugId = bugIds[i]
            locationfile = open(infodir + '/' + bugId + '/locations')
            locationlines = locationfile.readlines()
            locationfile.close()
            buggyfiles = set()

            for i in range(len(locationlines)):
                if 'file' in locationlines[i].strip() and 'method' in locationlines[i].strip():
                    buggyfile = locationlines[i].strip().split(';')[0].strip().split(':')[1].strip().split('trunk/')[-1]
                    buggyfiles.add(buggyfile)

            if os.path.exists(infodir + '/' + bugId + '/failcov/stmt_info.txt'):
                tarpath = infodir + '/' + bugId + '/failcov/stmt_info.txt'
            elif os.path.exists(infodir + '/' + bugId + '/fail/stmt_info.txt'):
                tarpath = infodir + '/' + bugId + '/fail/stmt_info.txt'
            else:
                print("Error!!")
                sys.exit(1)

            failfile = open(tarpath)
            faillines = failfile.readlines()
            failfile.close()

            failstmt = dict()
            passstmt = dict()
            failfileset = set()
            failfilemapstmt = dict()
            for i in range(len(faillines)):
                # print faillines[i]
                filename = faillines[i].strip().split(':')[0].split('-build/')[1]
                if not filename.endswith('.c'):
                    continue
                failfileset.add(filename)
                stmtlist = faillines[i].strip().split(':')[1].split(',')
                failfilemapstmt[filename] = set(stmtlist)
                for stmt in stmtlist:
                    failstmt[filename + ',' + stmt] = 1
                    passstmt[filename + ',' + stmt] = 0

            for i in os.listdir(passdir2 + '/' + bugId + '/passcov'):
                passfile = open(passdir2 + '/' + bugId + '/passcov/' + i + '/stmt_info.txt')
                passlines = passfile.readlines()
                passfile.close()
                for j in range(len(passlines)):
                    filename = passlines[j].strip().split(':')[0].split('-build/')[1]
                    if not filename.endswith('.c'):  # consider c and h files
                        continue
                    if filename not in failfileset:
                        continue
                    stmtlist = passlines[j].strip().split(':')[1].split(',')
                    for stmt in set(stmtlist) & failfilemapstmt[filename]:
                        # if filename+','+stmt in failstmt.keys():
                        passstmt[filename + ',' + stmt] += 1

            score = dict()
            filescore = dict()
            for key in failstmt.keys():
                score[key] = float(failstmt[key]) / math.sqrt(
                    float(failstmt[key]) * (failstmt[key] + passstmt[key]))
                # if passstmt[key]==0:
                #   score[key]=1.0
                # else:
                #   score[key]=float(failstmt[key])/passstmt[key]

                keyfile = key.split(',')[0]
                if keyfile not in filescore.keys():
                    filescore[keyfile] = []
                    filescore[keyfile].append(score[key])
                else:
                    filescore[keyfile].append(score[key])

            fileaggstmtscore = dict()
            for key in filescore.keys():
                fileaggstmtscore[key] = float(sum(filescore[key])) / len(filescore[key])

            if finalrank == {}:
                finalrank = fileaggstmtscore
            else:
                for key in fileaggstmtscore.keys():
                    finalrank[key] += fileaggstmtscore[key]

    scorelist = sorted(finalrank.items(), key=lambda d: d[1], reverse=True)

    f = open(rankFile, 'w')
    for score in scorelist:
        file = score[0]
        value = score[1]
        if 'CMakeFiles' in file:
            files = file.split('/')
            files2 = '/'
            for i in range(len(files)):
                if files[i] != 'CMakeFiles' and not '.dir' in files[i] and files[i] != '':
                    files2 += files[i]
                    files2 += '/'
            file = files2[:-1]
        f.write(file + ',' + str(value) + '\n')
    f.close()
