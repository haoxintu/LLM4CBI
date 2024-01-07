#experimental environment
#torch version 1.4.0
#python version 3.7.3
import os, time, sys, math
from random import choice
# from RecBi.llvm import checkIsPass_wrongcodeOneline,checkIsPass_zeroandsegmentoneline,checkIsPass_multilineswrongcode,checkIsPass_zeroandonenumber
from RecBi.util import *
from configparser import ConfigParser
import torch
import numpy as np

# @THX
import openai
import re
import os
import random
import subprocess

mutation_rules = ['inserting a branch (i.e., if) statement',
                  'inserting a loop (i.e., while or for) statement',
                  'inserting a function call',
                  'inserting a goto statement',
                  'inserting or removing a qualifier (i.e., volatile, const, and restrict)',
                  'inserting or removing a modifier (i.e., long, short, signed, and unsigned)',
                  'replacing a variable with another valid existing one',
                  'replacing a constant with another valid one',
                  'replacing or removing an unary operator',
                  'replacing a binary operator with another valid one']

def checkIsPass_wrongcodeOneline(configFile, revisionNumber,compilationOptionsRight,compilationOptionsWrong): # change per bug

    print("here in checkIsPass?")
    cfg = ConfigParser()
    cfg.read(configFile)
    compilersdir = cfg.get('llvm-locations', 'compilersdir')
    prefixpath = compilersdir + revisionNumber + '/' + revisionNumber

    llvmPath=prefixpath+'-build/bin/clang'
    covdir=prefixpath+'-build'

    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
    # os.system(llvmPath+' '+compilationOptionsRight+' mainvar.c')
    # print("start compiling right version : ", llvmPath+' '+compilationOptionsRight+' mainvar.c')
    err_set = set()
    os.system('{ ' + llvmPath + ' ' + compilationOptionsRight + ' mainvar.c' + ' ;}' + ' >comp_output.txt 2>&1')
    print('\033[1;35m --------------------compiler log begin' '\033[0m')
    os.system("cat comp_output.txt")
    print('\033[1;35m --------------------compiler log end' '\033[0m')
    lines = ''
    with open('comp_output.txt', 'r') as file:
        for line in file:
            lines += line
    regex = re.compile(r'^.*\berror\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    regex = re.compile(r'^.*\bundefined\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    if not os.path.exists('a.out'):
        return 0, err_set # compilation error
    if os.path.exists('rightfile'):
        os.system('rm rightfile')
    start=time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee rightfile')
    os.system('{ timeout 10 ./a.out ; } >rightfile 2>&1')
    end=time.time()
    if (end-start)>=10:
        return 0, err_set
    # print("rightfile : ")
    # os.system("cat rightfile")
    f=open('rightfile')
    lines=f.readlines()
    print("lines in rightfile : ", lines)
    f.close()
    if len(lines)!=1:
        print("lines != 1 in wrongOneline?, this means the oracle is removed")
        # os.system("cat rightfile")
        return 0, err_set
    else:
        if 'core dumped' in lines[0] or 'dumped core' in lines[0]:
            return 0, err_set
    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
    # print("start compiling wrong version : ", llvmPath+' '+compilationOptionsWrong+' mainvar.c')
    os.system(llvmPath+' '+compilationOptionsWrong+' mainvar.c')
    if not os.path.exists('a.out'):
        return 0, err_set

    if os.path.exists('wrongfile'):
        os.system('rm wrongfile')
    start=time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee wrongfile')
    os.system('{ timeout 10 ./a.out ; } >wrongfile 2>&1')
    end=time.time()
    if (end-start)>=10:
        return 0, err_set
    # print("wrongfile : ")
    # os.system("cat wrongfile")
    f=open('wrongfile')
    lines=f.readlines()
    print("lines in wrongfile : ", lines)
    f.close()
    if len(lines)!=1:
        return 0, err_set
    else:
        if 'core dumped' in lines[0] or 'dumped core' in lines[0]:
            return 0, err_set
    if os.path.exists('diffwr'):
        os.system('rm diffwr')
    os.system('diff wrongfile rightfile > diffwr')
    f=open('diffwr')
    lines=f.readlines()
    f.close()
    print("diffwr :")
    os.system("cat diffwr")
    if len(lines)==0:
        return 1, err_set # pass
    else:
        return 2, err_set # still fail

def checkIsPass_zeroandsegmentoneline(configFile, revisionNumber,compilationOptionsRight,compilationOptionsWrong): # change per bug

    cfg = ConfigParser()
    cfg.read(configFile)
    compilersdir = cfg.get('llvm-locations', 'compilersdir')
    prefixpath = compilersdir + revisionNumber + '/' + revisionNumber
    llvmPath=prefixpath+'-build/bin/clang'
    covdir=prefixpath+'-build'

    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
    # os.system(llvmPath+' '+compilationOptionsRight+' mainvar.c')
    err_set = set()
    os.system( '{ ' + llvmPath+' '+compilationOptionsRight+' mainvar.c' + ' ;}' + ' >comp_output.txt 2>&1')
    print('\033[1;35m --------------------compiler log begin' '\033[0m')
    os.system("cat comp_output.txt")
    print('\033[1;35m --------------------compiler log end' '\033[0m')
    lines = ''
    with open('comp_output.txt', 'r') as file:
        for line in file:
            lines += line
    regex = re.compile(r'^.*\berror\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    regex = re.compile(r'^.*\bundefined\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    if not os.path.exists('a.out'):
        return 0, err_set

    if os.path.exists('rightfile'):
        os.system('rm rightfile')

    start=time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee rightfile')
    os.system('{ timeout 10 ./a.out ; } >rightfile 2>&1')
    end=time.time()
    if (end-start)>=10:
        return 0, err_set

    f=open('rightfile')
    lines=f.readlines()
    f.close()
    if len(lines)!=0:
        os.system("cat rightfile")
        print('\033[1;35m --------------------right != 0?' '\033[0m')
        return 0, err_set

    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
    os.system(llvmPath+' '+compilationOptionsWrong+' mainvar.c')
    if not os.path.exists('a.out'):
        return 0, err_set

    if os.path.exists('wrongfile'):
        os.system('rm wrongfile')
    start=time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee wrongfile')
    os.system('{ timeout 10 ./a.out ; } >wrongfile 2>&1')
    end=time.time()
    if (end-start)>=10:
        return 0, err_set

    f=open('wrongfile')
    lines=f.readlines()
    f.close()
    # if len(lines)!=1:
    #     os.system("cat wrongfile")
    #     print('\033[1;35m --------------------wrongfile != 1?' '\033[0m')
    #     return 0,err_set

    if os.path.exists('diffwr'):
        os.system('rm diffwr')
    os.system('diff wrongfile rightfile > diffwr')
    f=open('diffwr')
    diffmesslines=f.readlines()
    f.close()
    print("**************")
    print("rightfile : ")
    os.system("cat rightfile")
    print("wrongfile : ")
    os.system("cat wrongfile")
    print("oriwrongfile : ")
    os.system("cat oriwrongfile")
    print("**************")
    if os.path.exists('diffow'):
        os.system('rm diffow')
    os.system('diff wrongfile oriwrongfile > diffow')
    f=open('diffow')
    diffowlines=f.readlines()
    print("diffowlines : ", diffowlines)
    f.close()

    print("len of diffmesslines : ", diffmesslines)
    if len(diffmesslines)==0:
        return 1, err_set # pass
    else:
        if len(diffowlines)==0: # 'core dumped' in lines[0]:
            return 2, err_set # still fail
        else:
            return 0, err_set


def checkIsPass_multilineswrongcode(configFile, revisionNumber,compilationOptionsRight,compilationOptionsWrong): # change per bug

    cfg = ConfigParser()
    cfg.read(configFile)
    compilersdir = cfg.get('llvm-locations', 'compilersdir')
    prefixpath = compilersdir + revisionNumber + '/' + revisionNumber
    llvmPath=prefixpath+'-build/bin/clang'
    covdir=prefixpath+'-build'

    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
    # os.system(llvmPath+' '+compilationOptionsRight+' mainvar.c')
    err_set = set()
    os.system('{ ' + llvmPath + ' ' + compilationOptionsRight + ' mainvar.c' + ' ;}' + ' >comp_output.txt 2>&1')
    print('\033[1;35m --------------------compiler log begin' '\033[0m')
    os.system("cat comp_output.txt")
    print('\033[1;35m --------------------compiler log end' '\033[0m')
    lines = ''
    with open('comp_output.txt', 'r') as file:
        for line in file:
            lines += line
    regex = re.compile(r'^.*\berror\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    regex = re.compile(r'^.*\bundefined\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    if not os.path.exists('a.out'):
        return 0, err_set

    if os.path.exists('rightfile'):
        os.system('rm rightfile')

    start=time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee rightfile')
    os.system('{ timeout 10 ./a.out ; } >rightfile 2>&1')
    end=time.time()
    if (end-start)>=10:
        return 0, err_set

    f=open('rightfile')
    lines=f.readlines()
    f.close()
    if len(lines)<=1:
        return 0, err_set
    if 'core dumped' in lines[0] or 'dumped core' in lines[0] or 'exception' in lines[0] or 'Abort' in lines[
        0] or 'Segmentation' in lines[0]:
        return 0, err_set

    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find ' + covdir + ' -name \"*.gcda\" | xargs rm -f')
    os.system(llvmPath + ' ' + compilationOptionsWrong + ' mainvar.c')
    if not os.path.exists('a.out'):
        return 0, err_set

    if os.path.exists('wrongfile'):
        os.system('rm wrongfile')
    start = time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee wrongfile')
    os.system('{ timeout 10 ./a.out ; } >wrongfile 2>&1')
    end = time.time()
    if (end - start) >= 10:
        return 0, err_set

    f = open('wrongfile')
    lines = f.readlines()
    f.close()
    if len(lines) <= 1:
        return 0, err_set
    if 'core dumped' in lines[0] or 'dumped core' in lines[0] or 'exception' in lines[0] or 'Abort' in lines[
        0] or 'Segmentation' in lines[0]:
        return 0, err_set

    if os.path.exists('diffwr'):
        os.system('rm diffwr')
    os.system('diff wrongfile rightfile > diffwr')
    f = open('diffwr')
    diffmesslines = f.readlines()
    f.close()
    if len(diffmesslines) == 0:
        return 1, err_set  # pass
    else:
        return 2, err_set  # still fail

def checkIsPass_zeroandonenumber(configFile, revisionNumber,compilationOptionsRight,compilationOptionsWrong): # change per bug

    cfg = ConfigParser()
    cfg.read(configFile)
    compilersdir = cfg.get('llvm-locations', 'compilersdir')
    prefixpath = compilersdir + revisionNumber + '/' + revisionNumber
    print("***********THX: goes here??????????")
    llvmPath=prefixpath+'-build/bin/clang'
    covdir=prefixpath+'-build'

    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
    # os.system(gccpath+' '+compilationOptionsRight+' mainvar.c')
    err_set = set()
    os.system('{ ' + llvmPath + ' ' + compilationOptionsRight + ' mainvar.c' + ' ;}' + ' >comp_output.txt 2>&1')
    print('\033[1;35m --------------------compiler log begin' '\033[0m')
    os.system("cat comp_output.txt")
    print('\033[1;35m --------------------compiler log end' '\033[0m')
    lines = ''
    with open('comp_output.txt', 'r') as file:
        for line in file:
            lines += line
    regex = re.compile(r'^.*\berror\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    regex = re.compile(r'^.*\bundefined\w*\b.*$', re.MULTILINE)
    # Find all the matches in the string and add them to a set
    matches = {match.strip() for match in regex.findall(lines)}
    err_set.update(matches)
    if not os.path.exists('a.out'):
        # failed compiliation
        return 0, err_set

    if os.path.exists('rightfile'):
        os.system('rm rightfile')

    start=time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee rightfile')
    os.system('{ timeout 10 ./a.out ; } >rightfile 2>&1')
    end=time.time()
    if (end-start)>=10:
        return 0, err_set

    f=open('rightfile')
    lines=f.readlines()
    f.close()
    if len(lines)!=0:
        os.system("cat rightfile")
        print('\033[1;35m --------------------rightfile != 0?' '\033[0m')
        return 0, err_set

    if os.path.exists('a.out'):
        os.system('rm a.out')
    os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
    os.system(gccpath+' '+compilationOptionsWrong+' mainvar.c')
    if not os.path.exists('a.out'):
        return 0, err_set

    if os.path.exists('wrongfile'):
        os.system('rm wrongfile')
    start=time.time()
    # os.system('timeout 10 ./a.out 2>&1 | tee wrongfile')
    os.system('{ timeout 10 ./a.out ; } >wrongfile 2>&1')
    end=time.time()
    if (end-start)>=10:
        return 0, err_set

    f=open('wrongfile')
    lines=f.readlines()
    f.close()
    # if len(lines)!=1:
    #      os.system("cat wrongfile")
    #    print('\033[1;35m --------------------wrongfile != 1?' '\033[0m')
    #     return 0, err_set

    if os.path.exists('diffwr'):
        os.system('rm diffwr')
    os.system('diff wrongfile rightfile > diffwr')
    f=open('diffwr')
    diffmesslines=f.readlines()
    f.close()
    if len(diffmesslines)==0:
        return 1, err_set # pass
    else:
        if len(lines)==1 and 'core dumped' not in lines[0] and 'dumped core' not in lines[0]:
            return 2, err_set # still fail
        else:
            return 0, err_set


def remove_unused_printf(file1, file2):
    # Open the first file for reading
    with open(file1, 'r') as f1:
        # Read the entire file and split it into lines
        lines1 = f1.read().splitlines()

    # Define a regular expression to match lines containing printf function
    printf_pattern = re.compile(r'\bprintf\b')

    # Initialize an empty set to store the lines containing printf in the first file
    printf_lines = set()

    # Loop through each line in the first file
    for i, line in enumerate(lines1):
        # If the line contains printf function, add it to the set
        if printf_pattern.search(line):
            printf_lines.add(line.strip())

    # Open the second file for reading
    with open(file2, 'r') as f2:
        # Read the entire file and split it into lines
        lines2 = f2.read().splitlines()

    # Loop through each line in the second file
    new_lines = []
    for line in lines2:
        # If the line does not contain printf function or it is in the set of lines to keep, add it to the new_lines list
        if not printf_pattern.search(line) or line.strip() in printf_lines:
            new_lines.append(line)

    # Write the modified second file back to disk
    with open(file2, 'w') as f3:
        f3.write('\n'.join(new_lines))


def collectCov(testname):
    os.system('mkdir -p ' + passdir + '/passcov/' + testname)
    methodfile = open(passdir + '/passcov/' + testname + '/method_info.txt', 'w')
    stmtfile = open(passdir + '/passcov/' + testname + '/stmt_info.txt', 'w')

    if os.path.exists('gcdalist'):  # all files to be collected
        os.system('rm gcdalist')
    os.system('find ' + covdir + ' -name \"*.gcda\" > gcdalist')

    f = open('gcdalist')
    lines = f.readlines()
    # print("THX lens : ", lines)
    f.close()

    for i in range(len(lines)):
        gcdafile = lines[i].strip()
        if '/clang/test/' in gcdafile:
            continue
        os.system('rm *.gcov')
        if os.path.exists('gcovfile'):
            os.system('rm gcovfile')
        os.system(gcovpath + ' -f ' + gcdafile + ' > gcovfile')
        if not os.path.exists('./' + gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov'):
            continue

        f = open('gcovfile')
        gcovlines = f.readlines()
        # print("THX: gcovlines : ", gcovlines)
        f.close()

        for j in range(len(gcovlines)):
            if 'Function \'' in gcovlines[j].strip():
                if 'Lines executed:' in gcovlines[j + 1].strip() and float(
                        gcovlines[j + 1].strip().split('Lines executed:')[1].split('%')[0].strip()) != 0.0:
                    methodfile.write(
                        gcdafile.split(covdir + '/')[-1] + ',' + gcovlines[j].strip().split('\'')[1] + ',' +
                        gcovlines[j + 1].strip().split('Lines executed:')[1].split('%')[0].strip() + ',' +
                        gcovlines[j + 1].strip().split('of')[-1].strip() + '\n')
        f = open(gcdafile.strip().split('/')[-1].split('.gcda')[0] + '.gcov')
        stmtlines = f.readlines()
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
        stmtfile.write(gcdafile.split(covdir + '/')[-1] + ':' + ','.join(tmp) + '\n')
    stmtfile.close()
    methodfile.close()

def diffWithExistingCov(testname):
    if len(os.listdir(passdir + '/passcov')) == 1:
        thisfile = open(passdir + '/passcov/' + testname + '/stmt_info.txt')
        thislines = thisfile.readlines()
        thisfile.close()

        thisset = set()
        for i in range(len(thislines)):
            filenameitem = thislines[i].strip().split(':')[0]
            lineitems = thislines[i].strip().split(':')[1].split(',')
            for j in range(len(lineitems)):
                thisset.add(filenameitem + ':' + lineitems[j])
        existingcovset[testname] = thisset & failset
        unionCovwithFail[testname] = thisset | failset
        passCov[testname] = thisset
        return 0  # different

    thisfile = open(passdir + '/passcov/' + testname + '/stmt_info.txt')
    # print("this line: ", passdir + '/passcov/' + testname + '/stmt_info.txt')
    thislines = thisfile.readlines()
    thisfile.close()

    # print("thislines = ", thislines)
    thisset = set()
    for i in range(len(thislines)):
        filenameitem = thislines[i].strip().split(':')[0]
        lineitems = thislines[i].strip().split(':')[1].split(',')
        for j in range(len(lineitems)):
            thisset.add(filenameitem + ':' + lineitems[j])

    for key in existingcovset.keys():
        # print("###THX: " + existingcovset[key] + str(thisset & failset))
        #if  len( existingcovset[key] | (thisset & failset)) == 0:  #THX changed a bit
        #    similarity = 0
        #else:
        similarity = float(len(existingcovset[key] & (thisset & failset))) / len(
            existingcovset[key] | (thisset & failset))
        if similarity == 1:
            return 1  # same
    existingcovset[testname] = thisset & failset
    unionCovwithFail[testname] = thisset | failset
    passCov[testname] = thisset
    return 0  # different

def data_flow_analysis(src_file):
    # Create an empty dictionary to store the data
    data_dict = {}

    # get the dict from srcSlice
    os.system("cp {} example.c".format(src_file))
    # os.system("pwd")
    # os.system("cat example.c")
    os.system("srcml ./example.c --position -o example.c.xml")
    # os.system ("cat example.c")
    os.system("srcslice example.c.xml > example.c.dict")

    # Open the text file for reading
    with open('example.c.dict', 'r') as f:
        # Initialize variables to store the data for each item
        name = ''
        dvars = set()
        aliases = set()
        use = set()
        definition = set()
        edges = set()

        # Iterate over each line in the file
        for line in f:
            # Strip whitespace from the line
            line = line.strip()

            # Check if the line contains the name of an item
            if line.startswith('Name: '):
                # If it does, store the name in the name variable
                name = line.split('Name: ')[1].strip()

            # Check if the line contains the set of defined variables for an item
            elif line.startswith('Dvars: '):
                # If it does, store the set of variables in the dvars variable
                dvars = set(line.split('Dvars: ')[1].strip("{}").split(','))
                dvars.discard('')
                # print("dvar : ", dvars)

            # Check if the line contains the set of aliases for an item
            elif line.startswith('Aliases: '):
                # If it does, store the set of aliases in the aliases variable
                aliases = set(line.split('Aliases: ')[1].strip("{}").split(','))
                aliases.discard('')

            # Check if the line contains the set of used variables for an item
            elif line.startswith('Use: '):
                # If it does, store the set of variables in the use variable
                use = set(line.split('Use: ')[1].strip("{}").split(','))
                use.discard('')

            # Check if the line contains the set of defined variables for an item
            elif line.startswith('Def: '):
                # If it does, store the set of variables in the definition variable
                definition = set(line.split('Def: ')[1].strip("{}").split(','))
                definition.discard('')

            # Check if the line contains the set of edges for an item
            elif line.startswith('Edges: '):
                # If it does, store the set of edges in the edges variable
                edges = set(line.split('Edges: ')[1].strip("{}").split('),'))
                edges.discard('')

                # Create a dictionary to store the data for this item
                item_dict = {
                    'Dvars': dvars,
                    'Aliases': aliases,
                    'Use': use,
                    'Def': definition,
                    'Edges': edges
                }

                # Store the dictionary in the data_dict with the name as the key
                data_dict[name] = item_dict

                # Reset the variables for the next item
                name = ''
                dvars = set()
                aliases = set()
                use = set()
                definition = set()
                edges = set()

    # Print the resulting dictionary
    # print(data_dict)

    names_less_than_10 = set()
    for name, values in data_dict.items():
        first_def = min(map(int, values['Def']))
        if first_def < 10:
            names_less_than_10.add(name)

    # print(names_less_than_15)

    all_dict = {}

    # Loop through the dictionary created earlier
    for name, info_dict in data_dict.items():
        # Get the counts of elements in "Dvars," "Use," and "Edges"
        # dvars_count = len(info_dict["Dvars"])
        use_count = len(info_dict["Use"])
        # edges_count = len(info_dict["Edges"])
        define_count = len(info_dict["Def"])

        # Create a new dictionary to store the counts
        counts = define_count + use_count;
        # Add the counts dictionary to the count_dict with the name as the key
        all_dict[name] = counts


    global_dict = {}

    # Loop through the dictionary created earlier
    for name, info_dict in data_dict.items():
        if name in names_less_than_10:
            # Get the counts of elements in "Dvars," "Use," and "Edges"
            dvars_count = len(info_dict["Dvars"])
            use_count = len(info_dict["Use"])
            edges_count = len(info_dict["Edges"])

            # Create a new dictionary to store the counts
            counts = dvars_count + use_count + edges_count;
            # Add the counts dictionary to the count_dict with the name as the key
            global_dict[name] = counts

    # Print the count_dict
    # print("global_dict: ", global_dict)


    # get the top-n
    topn= 3

    # for all_dict
    keys_set = set(all_dict.keys())
    top_keys_all = set()
    sorted_all_dict = sorted(all_dict.items(), key=lambda x: x[1], reverse=True)
    if len(keys_set) < topn:
        top_keys_all = keys_set
    else:
        top_keys_all = set(dict(sorted_all_dict[:topn]).keys())
    # print("top_keys_all : ", top_keys_all)

    # for global_dict
    keys_set = set(global_dict.keys())
    top_keys_global = set()
    sorted_global_dict = sorted(global_dict.items(), key=lambda x: x[1], reverse=True)
    if len(keys_set) < topn:
        top_keys_global = keys_set
    else:
        top_keys_global = set(dict(sorted_global_dict[:topn]).keys())
    # print("top_keys_global : ", top_keys_global)

    # find the variable in the printf
    # define a regular expression pattern to match printf statements
    printf_pattern = re.compile(r'printf\s*\(\s*"[^"]*"\s*(?:,\s*(.+)\s*)?\)')

    # open the C source code file
    with open('example.c', 'r') as f:
        code = f.read()

    # find all printf statements in the code
    for match in printf_pattern.finditer(code):
        # extract the variable being printed (if any)
        var = match.group(1)
        # print("len of top_key_all : ", len(top_keys_all))
        if var and len(top_keys_all) >= 2 and len(top_keys_global) >= 2 :
            # print the variable name
            print('Variable to be printed:', var.strip())
            top_keys_all.discard(var)
            top_keys_global.discard(var)
        # else:
        #     print('No variable to be printed')
    # print("top_keys_all : ", top_keys_all)
     #print("top_keys_global : ", top_keys_global)
    top_keys_global.discard('')
    top_keys_all.discard('')
    return top_keys_all, top_keys_global

def write_dict_to_file(filename, my_dict):
    with open(filename, 'w') as f:
        for key, value in my_dict.items():
            # f.write(str(key) + '\n')
            if isinstance(value, list):
                for item in value:
                    f.write(str(item) + ' ')
            else:
                f.write(str(value) + '\n')
            f.write('\n')

def control_flow_analysis(src_file):
    ret = set()
    topn = 1
    # os.system("cp {} example.c".format(src_file))
    os.system("rm cyclo*.txt")
    os.system("cp {} example.c".format(src_file))
    os.system("cp /media/haoxin/sam-disk/fl-compiler/chatIso/clint-test/Makefile .")
    os.system("make clean > /dev/null && bear make > /dev/null")
    os.system("oclint-json-compilation-database -- --enable-global-analysis -report-type=html -o test.html -rc CYCLOMATIC_COMPLEXITY=0 > cyclo-temp.txt")
    # os.system("cat cyclo.txt")
    # get the out from oclint (cyclomatic complexity for each block)
    # read the file and extract the last three columns
    # preprocessing
    # os.system("cat cyclo-temp.txt")
    with open('cyclo-temp.txt', 'r') as file:
        lines = file.readlines()
    d = {}
    for line in lines:
        columns = line.split()
        if len(columns) == 2:
            continue
        key = columns[0]
        if len(columns) == 3:
            d[key][1] = columns[2]
        else:
            d[key] = columns[1:]
    write_dict_to_file("cyclo.txt", d)
    # print("-----------")
    # os.system("cat cyclo.txt")
    with open('cyclo.txt', 'r') as f:
        data = []
        for line in f:
            parts = line.split()
            if parts == None:
                return ret
            data.append((int(parts[1]), int(parts[2]), int(parts[3])))
    # create a set of the last three columns and order it by the second column
    line_numbers = []
    keywords = ['printf', 'abort']
    try:
        with open(src_file, 'r') as file:
            lines = file.readlines()
            for line_number, line in enumerate(lines, start=1):
                if any(keyword in line for keyword in keywords):
                    line_numbers.append(line_number)
    except FileNotFoundError:
        print(f'File "{file_path}" not found.')
    print("line_number : ", line_numbers)

    # remove the range includes the oracle
    print("before data: ", data)
    set_data_copy = data.copy()  # Create a copy of the set to avoid modifying it during iteration
    for number in line_numbers:
        for element in set_data_copy:
            # print("data: ", data)
            # print("element :", element)
            if element not in data:
                return ret
            if element[1] <= number <= element[2]:
                data.remove(element)
    print("after data: ", data)
    if len(data) == 0:
        return ret
    set_data = set(data)
    ordered_set_data = sorted(set_data, key=lambda x: -x[0])
    # print("ordered_set_data : ", ordered_set_data)
    if len(ordered_set_data) < topn:
        ret = ordered_set_data
    else:
        ret = set(ordered_set_data[:topn])
    print("ret from control flow analysis : ", ret)
    return ret




def write_to_mutation_file_all(all_variable_list, global_variable_list, ret_location_list, file):
    length = ' 1 - 5 '
    with open(file, 'w') as f:  # for clear the contents in the file
        pass
    if len(ret_location_list) != 0:
        for loc in ret_location_list[:1]:
            begin_line = loc[1]
            end_line = loc[2]
            # print("loc[0]: ", loc[1])
            # print("loc[1]: ", loc[2])
            # print("begin_line : ", begin_line)
            # print("end_line : ", end_line)
            loc_prompt = 'only between line {} and line {} in the original given program'.format(begin_line, end_line)
            #loc_prompt = "at the most complex place"
            #global_variable_list = "the most complex variable"
            #all_variable_list "the most complex variable"
            with open(file, 'a') as f:
                f.write(
                    'addQualifier;inserting a qualifier (i.e., volatile, const, and restrict) of the variable in the list {}'.format(
                        all_variable_list) + '\n')
                f.write(
                    'remQualifier;removing a qualifier (i.e., volatile, const, and restrict) of the variable in the list {}'.format(
                        all_variable_list) + '\n')
                f.write(
                    'addModifier;inserting a modifier (i.e., long, short, signed, and unsigned) of the variable in the list {}'.format(
                        all_variable_list) + '\n')
                f.write(
                    'remModifier;removing a modifier (i.e., long, short, signed, and unsigned) of the variable in the list {}'.format(
                        all_variable_list) + '\n')
                f.write(
                    'repContant;replacing a constant with another valid one of a variable in the list {} '.format(
                        all_variable_list) + '\n')
                f.write(
                    'repBinary;replacing a binary operator with another valid one on the variables in the list {}'.format(
                        all_variable_list) + '\n')
                f.write(
                    'repRemUnary;replacing or removing an unary operator on the variables in the list {}'.format(
                        all_variable_list) + '\n')
                f.write('repUnary;removing an unary operator on the variables in the list {} {} (if any)'.format(
                     all_variable_list, loc_prompt) + '\n')
                f.write(
                    'repVar;replacing a variable in the list {} with another valid existing one in the list {}  '.format(
                        all_variable_list, global_variable_list) + '\n')
                f.write('addIf;inserting a branch (i.e., if) statement with length {} lines in the statement body {} and reusing the variables in the list {} '.format(
                    length, loc_prompt, global_variable_list) + '\n')
                f.write(
                    'addWhile;inserting a loop (i.e., while or for) statement with length {} lines in the statement body {} and reusing the variables in the list {} '.format(
                        length, loc_prompt, global_variable_list) + '\n')
                f.write('addFunction;inserting a function call with length {} lines in the statement body {} and reusing the variables in the list {} '.format(length, loc_prompt,
                                                                                                         global_variable_list) + '\n')
                f.write('addGoto;inserting a goto statement with length {} lines in the statement body {} and reusing the variables in the list {} '.format(length, loc_prompt,
                                                                                                         global_variable_list) + '\n')
                # print("prot: ", mutate)
    else:
        loc_prompt = 'at the beginning of the main function'
        with open(file, 'a') as f:
            f.write(
                'addQualifier;inserting a qualifier (i.e., volatile, const, and restrict) of the variable in the list {}'.format(
                    all_variable_list) + '\n')
            f.write(
                'remQualifier;removing a qualifier (i.e., volatile, const, and restrict) of the variable in the list {}'.format(
                    all_variable_list) + '\n')
            f.write(
                'addModifier;inserting a modifier (i.e., long, short, signed, and unsigned) of the variable in the list {}'.format(
                    all_variable_list) + '\n')
            f.write(
                'remModifier;removing a modifier (i.e., long, short, signed, and unsigned) of the variable in the list {}'.format(
                    all_variable_list) + '\n')
            f.write(
                'repContant;replacing a constant with another valid one of a variable in the list {}'.format(
                    all_variable_list) + '\n')
            f.write(
                'repBinary;replacing a binary operator with another valid one on the variables in the list {}'.format(
                    all_variable_list) + '\n')
            f.write(
                'repRemUnary;replacing or removing an unary operator on the variables in the list {} '.format(
                    all_variable_list) + '\n')
            f.write('repUnary;removing an unary operator on the variables in the list {} {} (if any)'.format(
                    all_variable_list, loc_prompt) + '\n')
            f.write(
                'repVar;replacing a variable in the list {} with another valid existing one in the list {}'.format(
                    all_variable_list, global_variable_list) + '\n')
            f.write(
                'addIf;inserting a branch (i.e., if) statement with length {} lines in the statement body {}  and reusing the variables in the list {} '.format(
                        length, loc_prompt, global_variable_list) + '\n')
            f.write(
                'addWhile;inserting a loop (i.e., while or for) statement with length {} lines in the statement body {} and reusing the variables in the list {} '.format(
                        length, loc_prompt, global_variable_list) + '\n')
            f.write('addFunction;inserting a function call with length {} lines in the statement body {} and reusing the variables in the list {} '.format(
                length, loc_prompt,global_variable_list) + '\n')
            f.write(
                    'addGoto;inserting a goto statement with length {} lines in the statement body {} and reusing the variables in the list {} '.format(length,loc_prompt,
                                                                                                             global_variable_list) + '\n')
            # print("prot: ", mutate)
    f.close()
    with open(file, 'r') as f:
        num_lines = len(f.readlines())
    f.close()
    return num_lines


def is_passing_test_program_validation(src_file):
    '''
    given the program and use frama-c to detect it;
    return 1 if no assertion error in the results
    '''
    os.system("cp /media/haoxin/sam-disk/fl-compiler/chatIso/clint-test/ub_test.sh .")
    os.system("./ub_test.sh {} > validation_result.txt".format(src_file))
    try:
        with open("validation_results.txt", 'r') as file:
            for line in file:
                if 'assertion' in line or 'error' in line:
                    return 0
        return 1
    except FileNotFoundError:
        print(f"File '{src_file}' not found.")
        return 0

def extract_error_message(file_path):
    # for test validation
    os.system("cp /media/haoxin/sam-disk/fl-compiler/chatIso/clint-test/ub_test.sh .")
    os.system("./ub_test.sh {} > validation_result.txt".format(file_path))
    try:
        with open("validation_result.txt", 'r') as file:
            for line in file:
                if 'error' in line or 'assertion' in line:
                    error_index = line.find("'") # find the index of the first quote character
                    if error_index != -1:
                        # find the index of the second quote character starting from the first quote index
                        error_index2 = line.find("'", error_index+1)
                        if error_index2 != -1:
                            # extract the error message between the first and second quote characters
                            error_message = line[error_index+1:error_index2]
                            return error_message
        return None
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None


def insert_lines(file1, file2):
    # remove the comments in the first 10 lines
    with open(file2, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        new_line = line.split("//")[0]  # get the substring before the first occurrence of "//"
        new_lines.append(new_line)

    with open(file2, "w") as f:
        f.write("".join(new_lines))

    # read the contents of the first file
    with open(file1, 'r') as f1:
        lines1 = f1.readlines()[:10]

    # read the contents of the second file
    with open(file2, 'r') as f2:
        lines2 = f2.readlines()

    # create a dictionary to store the lines in the second file by key
    lines2_dict = {}
    for line in lines2:
        key = ' '.join(line.strip().split()[-2:])
        lines2_dict[key] = line

    # insert the missing lines from the first file to the beginning of the second file
    with open(file2, 'w') as f2:
        for line in lines1:
            key = ' '.join(line.strip().split()[-2:])
            if key not in lines2_dict:
                f2.write(line)
        f2.writelines(lines2)


def insert_printf_for_wrong_code(file1, file2):
    # Open file A and find the printf function and location indicator
    # printf_line = ''
    with open(file1, 'r') as fileA:
        lines = fileA.readlines()
        for i, line in enumerate(lines):
            if 'printf' in line:
                printf_line = line.strip()
                location = lines[i + 1].strip()  # Get the location indicator from the next line
                break
    if printf_line is None:
        return

    # Check if printf function is already in file B
    with open(file2, 'r') as fileB:
        b_lines = fileB.readlines()
        printf_found = False
        for line in b_lines:
            if printf_line in line:
                printf_found = True
                break

    # Insert the printf line into file B before the location indicator if it's not already present
    if not printf_found:
        with open(file2, 'w') as new_fileB:
            i = 0
            while i < len(b_lines):
                if location in b_lines[i]:
                    # Insert the printf line before the line with the location indicator
                    new_fileB.write(printf_line + '\n')
                    new_fileB.write(b_lines[i])
                    i += 1
                else:
                    new_fileB.write(b_lines[i])
                    i += 1
    else:
        print('Printf function is already present in file B')


def insert_printf_for_wrong_code_multi(fileA, fileB):
    # Read the contents of file A and file B
    with open(fileA, 'r') as f:
        a_lines = f.readlines()
    with open(fileB, 'r') as f:
        b_lines = f.readlines()

    # Find the line numbers of printf functions in file A
    printf_lines = []
    for i, line in enumerate(a_lines):
        if 'printf' in line:
            printf_lines.append(i)

    # If there are no printf functions in file A, return
    if len(printf_lines) == 0:
        return

    # Check if file B contains the same printf functions
    for line_num in printf_lines:
        found = False
        for b_line in b_lines:
            if 'printf' in b_line and a_lines[line_num].strip() in b_line:
                found = True
                break
        if found:
            continue  # Do not insert if printf already exists in file B

        # Find the location indicator for the printf function
        loc_indicator = a_lines[line_num+1].strip()

        # Find the line number of the location indicator in file B
        b_line_num = -1
        for i, line in enumerate(b_lines):
            if loc_indicator in line:
                b_line_num = i
                break

        # If the location indicator is not found in file B, skip the printf function
        if b_line_num == -1:
            continue

        # Insert the printf function in file B
        b_lines.insert(b_line_num, a_lines[line_num])

    # Write the modified contents of file B back to the file
    with open(fileB, 'w') as f:
        f.writelines(b_lines)


def  insert_abort_for_seg(fileA, fileB):
    # Read the contents of file A and file B
    with open(fileA, 'r') as f:
        a_lines = f.readlines()
    with open(fileB, 'r') as f:
        b_lines = f.readlines()

    # Find the line numbers of printf functions in file A
    printf_lines = []
    for i, line in enumerate(a_lines):
        if 'abort' in line:
            printf_lines.append(i)

    # If there are no printf functions in file A, return
    if len(printf_lines) == 0:
        return

    # Check if file B contains the same printf functions
    for line_num in printf_lines:
        found = False
        for b_line in b_lines:
            if 'abort' in b_line and a_lines[line_num].strip() in b_line:
                found = True
                break
        if found:
            continue  # Do not insert if printf already exists in file B

        # Find the location indicator for the printf function
        loc_indicator = a_lines[line_num+1].strip()

        # Find the line number of the location indicator in file B
        b_line_num = -1
        for i, line in enumerate(b_lines):
            if loc_indicator in line:
                b_line_num = i
                break

        # If the location indicator is not found in file B, skip the printf function
        if b_line_num == -1:
            continue

        # Insert the printf function in file B
        b_lines.insert(b_line_num, a_lines[line_num])

    # Write the modified contents of file B back to the file
    with open(fileB, 'w') as f:
        f.writelines(b_lines)

    # remove potiential return -1;
    with open(fileB, 'r') as f:
        content = f.read()
    modified_content = content.replace("return -1;", "")
    with open(fileB, 'w') as f:
        f.write(modified_content)


def check_oracles(file_a, file_b):
    '''
    # Define the strings to search for
    strings_to_search = ["printf", "abort"]

    # Count the number of occurrences of the strings in file A
    count_a = 0
    with open(file_a, 'r') as f:
        file_a_content = f.read()
        for s in strings_to_search:
            count_a += file_a_content.count(s)

    # Count the number of occurrences of the strings in file B
    count_b = 0
    with open(file_b, 'r') as f:
        file_b_content = f.read()
        for s in strings_to_search:
            count_b += file_b_content.count(s)
    print("+++ count_a : ", count_a)
    print("+++ count_b : ", count_b)
    # Return true if the number of occurrences of the strings in file B matches file A
    print("\n")
    print("+++ count_a : ", count_a)
    print("+++ count_b : ", count_b)
    return count_a == count_b
    '''
    with open(file_a, "r") as f_a:
        count_a = sum(1 for line in f_a if "printf" in line.split("//")[0] or "abort" in line.split("//")[0])
    with open(file_b, "r") as f_b:
        count_b = sum(1 for line in f_b if "printf" in line.split("//")[0] or "abort" in line.split("//")[0])
    print("\n")
    print("+++ count_a : ", count_a)
    print("+++ count_b : ", count_b)
    return count_a == count_b


def add_comment_before_string(file_path):
    """
    Given a file path, add '//' before each occurrence of a pattern in each line of the file.
    """
    pattern = "###@@@###"
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if pattern in line:
            idx = line.index(pattern)
            lines[i] = line[:idx] + "//" + line[idx:]

    with open(file_path, 'w') as f:
        f.writelines(lines)


def replace_void_with_int(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    modified_content = content.replace("void", "int")

    with open(file_path, 'w') as file:
        file.write(modified_content)



# --------------------------------------- main process begin---------------------------------------

os.environ["OMP_NUM_THREADS"] = "1"
revisionnumber = sys.argv[1]
compilationOptionsRight = sys.argv[2].replace('+', ' ')
compilationOptionsWrong = sys.argv[3].replace('+', ' ')
checkpass = sys.argv[4]
roundcount = sys.argv[5]
configFile = sys.argv[6]
bugId = sys.argv[7]
cfg = ConfigParser()
cfg.read(configFile)


# password = cfg.get('password', 'password')
# autosudo = 'echo ' + password + ' | sudo -S '
GAMMA = cfg.getfloat('params', 'gamma')
compilersdir = cfg.get('llvm-locations', 'compilersdir') + revisionnumber + '/' + revisionnumber
passdir = cfg.get('llvm-locations', 'passdir') + roundcount + '/' + bugId
infodir = cfg.get('llvm-locations', 'infodir') + bugId

if os.path.exists(passdir):
    os.system('rm -rf ' + passdir)
os.system('mkdir -p ' + passdir)
os.chdir(passdir)
print("@@@@@@@ THX passdir : ", passdir)
gccpath = compilersdir + '-build/bin/clang'
gcovpath = 'gcov'
covdir = compilersdir + '-build'
mutatedir = cfg.get('llvm-locations', 'mutatedir')
# os.system('cp -r ' + mutatedir + '* .') # do not copy muators here

if os.path.exists(passdir + '/failtest'):
    os.system('rm -rf ' + passdir + '/failtest')
os.system('mkdir -p ' + passdir + '/failtest')
os.system('cp ' + infodir + '/fail.c ' + passdir + '/failtest')
os.system('mkdir -p ' + passdir + '/passcov')
failtestdir = './failtest'
firstfailtestdir = './firstfailtest'
os.system('mkdir -p ' + firstfailtestdir)
passtestdir = './passtest'
os.system('mkdir -p ' + passtestdir)

mutateRecord = open('mutateRecode', 'w')
successRecord = open('successRecord', 'w')

os.system('cp ' + failtestdir + '/fail.c ' + './')
if os.path.exists('a.out'):
    os.system('rm a.out')
os.system(gccpath + ' ' + compilationOptionsWrong + ' fail.c')
if os.path.exists('oriwrongfile'):
    os.system('rm oriwrongfile')
if not os.path.exists('a.out'):
    sys.exit(1)
# os.system('./a.out 2>&1 | tee oriwrongfile')
os.system('{ timeout 10 ./a.out; echo $? ; } >oriwrongfile 2>&1')
# print 'start'
failcovpath = cfg.get('llvm-locations', 'infodir')
if os.path.exists(failcovpath + bugId + '/failcov/stmt_info.txt'):
    tarpath = failcovpath + bugId + '/failcov/stmt_info.txt'
elif os.path.exists(failcovpath + bugId + '/fail/stmt_info.txt'):
    tarpath = failcovpath + bugId + '/fail/stmt_info.txt'
else:
    print ("Error!!")
    sys.exit(1)
failfile = open(tarpath)
faillines = failfile.readlines()
failfile.close()
failset = set()
for i in range(len(faillines)):
    filename = faillines[i].strip().split(':')[0]
    stmtlist = faillines[i].strip().split(':')[1].split(',')
    for j in range(len(stmtlist)):
        failset.add(filename + ':' + stmtlist[j])


#initialization

# @THX starts : prepare the mutation rules
src_file = infodir + '/fail.c'
# print("src_file : ", src_file)
ret_locations = control_flow_analysis(src_file)
ret_location_list = sorted(list(ret_locations))
# print("ret_location_list : ", ret_location_list)
top_keys_all, top_keys_global = data_flow_analysis(src_file)

'''
loc_prompt = ''
if len(ret_location_list) != 0:
    random_loc = random.randint(0, len(ret_location_list) - 1)
    begin_line = ret_location_list[random_loc][1]
    end_line = ret_location_list[random_loc][2]
    # print("begin_line : ", begin_line)
    # print("end_line : ", end_line)
    loc_prompt = 'only between line {} and line {} in the original given program'.format(begin_line, end_line)
else:
    loc_prompt = 'at the most complex block of the existing statement'
print("loc_prompt : ", loc_prompt)
'''

all_variable_list = sorted(list(top_keys_all))

if len(top_keys_global) != 0:
    global_variable_list = sorted(list(top_keys_global))
else:
    global_variable_list = all_variable_list

print("all_variable_list : ", all_variable_list)
print("global_variable_list : ", global_variable_list)

stepForward = cfg.getint('params', 'miu') # how many future steps we analyze
cntStepForward = 0 # cntOneBatch is the number of step in one batch, used for recording and quiting one batch
action_file_path = cfg.get('llvm-locations', 'actionFile')
num_lines = write_to_mutation_file_all(all_variable_list, global_variable_list, ret_location_list, action_file_path)
# num_lines = 13
N_S = num_lines
N_A = num_lines
averageSimilarity = 0
averageDiversity = 0
print("numlines : ", num_lines)
ini_stat = np.ones(num_lines)
print("ini_stat: ", ini_stat)
actions = []
# TODO replace action file here

action_file = open(action_file_path)
lines = action_file.readlines()
for i in range(len(lines)):
    line = lines[i].strip()
    actions.append(line)
addLine = [dict()]
for i in range(1, 15 + 1):
    addLine.append(dict())
print("addLine : ", addLine)
# print("actions : ", actions)
passingcnt = 0 # passingcnt is the number of generated witness test program.
firstfailcnt = 0
# existingcovset is used for record the pair(passing test program, the intersection of the statement coverage of this program and that of failing test program)
existingcovset = dict()
# unionCovwithFail is used for record the pair(passing test program, the union of the statement coverage of this program and that of failing test program)
unionCovwithFail = dict()
# passCov is used for record the coverage of each passing test program. The form of each element is (testname, pair(filename, statement))
passCov = dict()
failtype = 'fail'
os.system('mkdir -p ' + failtestdir + 'ori')

# averageTimesForLoopToGenerateOnePass and recordAverageTimes[] are used to detect the average steps we need to generate
# one passing test program. They are mainly used to tune hyperparameters: stepForward
# averageTimesForLoopToGenerateOnePass = 0
# recordAverageTimes = []
#buffer_s, buffer_a, buffer_r are used to record the states, actions and rewards during one 'stepForward'
buffer_s = []
buffer_a = []
buffer_r = []

alpha = cfg.getfloat('params', 'alpha')

net = Net(N_S, N_A)
optim = torch.optim.Adam(net.parameters(), lr = cfg.getfloat('params', 'beta'))

preInstantScore = 0 # used to store the instant score in the last round

recordfile = open('recordfile', 'w')

historyscore = []
for i in range(num_lines):
    # the first element is the times we have selected this mutation class, the second one is the score
    historyscore.append([0,0])

ub_set = set()
syn_err_set = set()
fail_prog_set = set()

countfile = open('countfile', 'w')
totoal_prog = 0
syn_error_prog = 0
compiled_prog = 0
ub_prog = 0
failing_prog = 0
passing_interesting = 0
passing_not_interesting = 0
same_prog = 0
repeative_prog = 0
remove_oracle_prog = 0
gaptime = 0

### @ THX ends

# openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # can be anything
# openai.api_base = "http://127.0.0.1:8000/v1"

# from llama_cpp import Llama
# llm = Llama(model_path="/media/haoxin/sam-disk/fl-compiler/other-llms/llama.cpp/models/wizardlm/ggml-wizardlm-7b-q8_0.bin", n_ctx=4096, n_threads=12)

# set the maximum number of witness test programs to 499(of course, it is impossible to
# produce so many programs in only one hour)
starttime = time.time()
cnt = 0;
while (passingcnt < 499):
# while cnt != 1:
    cnt = 1
    endtime = time.time()
    gaptime = endtime - starttime
    print("$$$$$$$$$$$$ gap time : ", gaptime)
    print('\033[1;35m --------$$$ passing test program : ', passingcnt, '\033[0m')
    if gaptime > 3600: # set the time limit to one hour
        if len(os.listdir(passtestdir)) > 0:
            break
        else:
            starttime = time.time()
            os.system('mv ' + failtestdir + '/* ' + failtestdir + 'ori')
            if len(os.listdir(firstfailtestdir)) == 0:
                break
            os.system('mv ' + firstfailtestdir + '/* ' + failtestdir)
            failtype = 'firstfail'

    doesGeneratePassingTestProgram = False
    ############## select seed program
    # averageTimesForLoopToGenerateOnePass += 1
    mutatefile = ''
    # failtype=choice(passorfail)
    if failtype == 'fail':
        mutatefile = failtestdir + '/fail.c'
    elif failtype == 'firstfail':
        if len(os.listdir(passtestdir)) > 0:
            break
        # if len(os.listdir(failtestdir))==0:
        #     continue
        tmpfile = choice(os.listdir(failtestdir))
        mutatefile = failtestdir + '/' + tmpfile
    # else:
    #     if len(os.listdir(passtestdir))==0:
    #         continue
    #     tmpfile=choice(os.listdir(passtestdir))
    #     mutatefile=passtestdir+'/'+tmpfile
    print("mutatefile : ", mutatefile)


    print("len of actions : ", len(actions))

    # actionNo = calActionNo(classNo) # changed by THX: no need to calcuate the Action No

    optim.zero_grad()
    classNo = net.choose_action(v_wrap(ini_stat[None, :]))
    classNo = classNo.numpy()[0]
    print("classNo : ", classNo)
    actionNo = classNo  # original deep learning alg
    # actionNo = random.randint(0, 11)
    print("actionNo : ", actionNo)
    mutationNo = actionNo
    print("mutationNo : ", mutationNo)
    commandMutate = actions[actionNo]

    # print("commandMutate : ", commandMutate)

    # print('\033[1;35m --------------------commandMutate = ', commandMutate, '\033[0m')
    # time.sleep(2)

    classfile = commandMutate.strip().split(';')[0]
    testname = 'pass_' + classfile + str(mutationNo) + '_' + str(passingcnt+1)
    inputslist = commandMutate.strip().split(';')[1].split(',')
    for i in range(len(inputslist)):
        inputslist[i] = '\"' + inputslist[i] + '\"'
    inputsstr = ' '.join(inputslist)
    ############## mutate program
    os.system('rm *.c')
    os.system('cp ' + mutatefile + ' ./main.c')
    mutateRecord.write(mutatefile + ';' + commandMutate + ';' + str(mutationNo) + '\n')
    mutateRecord.flush()
    #print("mutateRecord : ", mutateRecord)

    if os.path.exists('mainvar.c'):
        os.system('rm mainvar.c')

    print("### Start generating program using GPT !")
    os.system("pwd")

    selected = commandMutate.strip().split(';')[1]
    print("selected mutation_rule : ", selected)
    # exit(1)
    prog = ""
    with open('./main.c', 'r') as file:
        file_contents = file.read()
        prog = file_contents

    # print("org prog: ", prog)

    messages = [
    # system message first, it helps set the behavior of the assistant
    { "role": "system",
      "content": "You are an effective program mutator and your job is to generate a semantic in-equivalent variant the input code based on the specified instructions in the following."},
]
    mutation_instruction = "(*) clear up your memory from now and do not generate repeated programs. Please generate only one semantic in-equivalent variant of the input test program ```{}``` (make sure the variant program can be compiled and valid without any undefined behavior) by {} and \
                                       keep other code the same as the input program (comment in the code what you have changed). Please also do the following (1) surround the generated C code with three backticks (i.e., ```); (2) avoid any syntax error (i.e.,\"use of undeclared identifier\") or semantic errors \
                               and (3) (hard restriction) keep existing definition of global or local variables and function definitions of the input program in new generated program in the generated code; \
                               (4) try your best to generate the variant with different semantics compared with the input program;  (5) please do not directly assign to the variable in printf function (if any)\
                                (6) In the solution code, please do not remove or modify any lines that include the comment `###@@@### KEEP THIS LINE`. For example, giving you the code `printf(\"%d\n\", c); // ###@@@### KEEP THIS LINE` or ` __builtin_abort (); // ###@@@### KEEP THIS LINE` in the original program, you should not remove such lines in your solution \
                                  (7) please modify the lines before the first comment that includes string `###@@@### KEEP THIS LINE`".format(
    prog, selected) + " and (8) please save the new program into `gpt-test.c` and (9) do not generate loop initial declarations for for-loop statement"

    messages.append( {"role": "user", "content": mutation_instruction},)

    # UB checking
    if len(ub_set) != 0:
        ub_string = ''
        for ret in ub_set: # add the validation feedback to LLMs
            ub_string += ret + ', '
        ub_back_to_llm = "The program you generated is bad, and I got the error \" {} \" from Frama-c. Please do not generate such program again".format(ub_string)
        messages.append({"role": "user", "content": ub_back_to_llm})
    syn_string = ''
    if len(syn_err_set) != 0:
        # syn_string = ''
        for syn in syn_err_set:
            syn_string += syn + ', '
        # print("error in the set : ", syn_string)
        syn_back_to_llm = "The program you generated has a syntax error, and I got the error \"{} \" after compiling. Please fix them and do not generate such program again".format(syn_string)
        messages.append({"role": "user", "content": syn_back_to_llm})
    if len(fail_prog_set) != 0:
        fprog_string = ''
        for f in fail_prog_set:
            fprog_string += '```' + f + '```, '
        # print("error in the set : ", syn_string)
        fail_back_to_llm = "The following programs you generated {} still CAN reproduce the compiler bug or the `printf` function in the given program was removed in the new program, where you should NOT remove it, please do not generate such programs again".format(
            fprog_string)
        # messages.append({"role": "user", "content": fail_back_to_llm})
    # print("@@@@ messages : ", messages)
    # exit(1)

    try:
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages,
            temperature=1.0,
        )
    except openai.error.APIError as e:
        # Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        continue
    except openai.error.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        continue
    except openai.error.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        continue
    except openai.error.ServiceUnavailableError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        continue

    #output = llm("Q: {} A: ".format(mutation_instruction), max_tokens=2000, echo=True)
    # print("chat_completion: ", chat_completion)
    # print("### GPT usage : ", chat_completion['usage'])
    # print("***************** model used : ", model)

    pattern = r"\`\`\`([\s\S]*?)\`\`\`"
    reply = chat_completion.choices[0].message.content
    # messages.append({"role": "assistant", "content": reply})
    # print("reply from GPT (before filtering) : ", reply)
    reply = re.findall(pattern, reply)
    # print("reply from GPT : ", reply)
    new_reply = []
    for r in reply:
        if r.find('main') != -1:
            new_reply.append(r)
    reply = new_reply
    if len(reply) == 0: # in case the reply is not
        continue
    if reply[-1].startswith('c') or reply[-1].startswith('C'):
        reply[-1] = reply[-1][1:]
    # print("Reply: ", reply)
    totoal_prog += 1
    with open("mainvar.c", "w") as f:
        for line in reply[-1]:
            f.write(line)
    remove_unused_printf("./main.c", "./mainvar.c")

    # perform test validation process
    ret = extract_error_message('./mainvar.c')
    rad_nu = random.randint(1, 100000)
    if ret == None:
        print("COOL!!! the generated program is passed by the validation process!")
        pass
    else:
        print("this file contains undefined behavior")
        ub_prog  += 1
        os.system("cp mainvar.c ub_{}.c".format(rad_nu))
        if ret not in ub_set:
            ub_set.add(ret)
        os.system("cat validation_result.txt")
        # exit(1)
        continue
    
    print("original code is: ------------------")
    os.system("cat main.c")
    print("generated code is: ------------------")
    os.system("cat mainvar.c")
    f_mainvar = open('mainvar.c')
    temp = f_mainvar.readlines()
    f_mainvar.close()
    if len(temp) == 0: # if there are no difference between the new test program and old program
        print("None program is generated :(")
        continue
    
    if check_oracles("./main.c", "mainvar.c") == False:
        print("Checking oracle failed, now try to fix this, ....")
        # print("during oralce checking ------")
        # os.system("cat mainvar.c")
        insert_printf_for_wrong_code_multi('./main.c', './mainvar.c')
        # insert_abort_for_seg('./main.c', './mainvar.c')
        remove_oracle_prog += 1
        if check_oracles("./main.c", "mainvar.c") == False:
            print("Checking oracle still failed, continue to generate a new program ....")
            continue
        else:
            print("Great, the oracle checking is passed!!!")
    print("after oracle checking +++++ ")
    # replace_void_with_int("mainvar.c")
    os.system("cat mainvar.c")
    add_comment_before_string('./mainvar.c')
    print("### End generating program using GPT !")
    
    if os.path.exists('difftmp'):
        os.system('rm difftmp')
    os.system('diff main.c mainvar.c > difftmp')
    f = open('difftmp')
    difflines = f.readlines()
    f.close()
    if len(difflines) == 0: # if there are no difference between the new test program and old program
        same_prog += 1
        print("same_prog : ", same_prog)
        continue
    else:
        if os.path.exists('bugmessage'):
            os.system('rm bugmessage')
        # os.system('find '+covdir+' -name \"*.gcda\" | xargs rm -f')
        # os.system(gccpath+' '+compilationOptions+' mainvar.c 2>&1 | tee bugmessage')
        flagIsPass = -1
        err_set = set()
        if checkpass == 'checkIsPass_wrongcodeOneline':
            flagIsPass, err_set = checkIsPass_wrongcodeOneline(configFile, revisionnumber, compilationOptionsRight,
                                                                             compilationOptionsWrong)  # 1:pass; 2:still fail
            if len(err_set) != 0:
                syn_err_set.update(err_set)
                syn_error_prog += 1
        elif checkpass == 'checkIsPass_zeroandsegmentoneline':
            flagIsPass, err_set = checkIsPass_zeroandsegmentoneline(configFile, revisionnumber, compilationOptionsRight,
                                                                                  compilationOptionsWrong)  # 1:pass; 2:still fail
            if len(err_set) != 0:
                syn_err_set.update(err_set)
                syn_error_prog += 1
        elif checkpass == 'checkIsPass_multilineswrongcode':
            flagIsPass, err_set = checkIsPass_multilineswrongcode(configFile, revisionnumber, compilationOptionsRight,
                                                                                compilationOptionsWrong)  # 1:pass; 2:still fail
            if len(err_set) != 0:
                syn_err_set.update(err_set)
                syn_error_prog += 1
        elif checkpass == 'checkIsPass_zeroandonenumber':
            flagIsPass, err_set = checkIsPass_zeroandonenumber(configFile, revisionnumber, compilationOptionsRight,
                                                                                compilationOptionsWrong)
            if len(err_set) != 0:
                syn_err_set.update(err_set)
                syn_error_prog += 1
        else:
            raise Exception('unkown checkpass')

        if flagIsPass == 0:
            if len(err_set) == 0:
                compiled_prog += 1 # minus the syntax error should be the actual number of compiled programs
            print("syn_error_prog : ", syn_error_prog)
            continue
        elif flagIsPass == 2:
            firstfailcnt += 1
            failing_prog += 1
            compiled_prog += 1
            print("failing_prog : ", failing_prog)
            # THX: we add the feedback to LLMs here as well
            fprog = ""
            with open('./mainvar.c', 'r') as file:
                file_contents = file.read()
                fprog = file_contents
            # print("still failed program: ", fprog)
            fail_prog_set.add(fprog)
            # if len(os.listdir(firstfailtestdir))==5000:
            #     os.system('rm -rf '+firstfailtestdir+'/'+choice(os.listdir(firstfailtestdir)))
            os.system('mv mainvar.c ' + firstfailtestdir + '/firstfail_' + classfile + str(mutationNo) + '_' + str(
                firstfailcnt) + '.c')
            continue
        else:
            compiled_prog += 1
            print("compiled_prog : ", compiled_prog)
            print("the flagIsPass : ", flagIsPass)
            print("passtestdir : ", passtestdir)
            print("failtestdir : ", failtestdir)
            flagIsExist = diffWithExistingPass(passtestdir, failtestdir)
            if flagIsExist == 0:
                passing_not_interesting += 1
                print("#### No interesting coverage, generating again")
                continue
            else:
                print("the flagIsExist : " + str(flagIsExist) + "  testname : " + str(testname))
                passing_interesting += 1
                print('\033[1;35m --------$$$ passing test program : ', passing_interesting, '\033[0m')
                passingcnt += 1
                collectCov(testname)
                flagCovIsRepetitive = diffWithExistingCov(testname)
                if flagCovIsRepetitive == 1:
                    print("Repetitive?")
                    os.system('rm -rf ' + passdir + '/passcov/' + testname)
                    passingcnt -= 1
                    repeative_prog += 1
                    continue
                else:
                    f = open('difffilefail')
                    lines = f.readlines()
                    ju = True
                    
                    if ju:
                        doesGeneratePassingTestProgram = True
                        # recordAverageTimes.append(averageTimesForLoopToGenerateOnePass)
                        # averageTimesForLoopToGenerateOnePass = 0
                        os.system('mv mainvar.c ' + passtestdir + '/pass_' + classfile + str(mutationNo) + '_' + str(
                            passingcnt) + '.c')
                        successRecord.write(mutatefile + ';' + commandMutate + ';' + str(mutationNo) + '\n')
                        successRecord.flush()
                    else:
                        os.system('rm -rf ' + passdir + '/passcov/' + testname)
                        passingcnt -= 1
                        print("return???")
                        continue
    
    # start of memorized prompt search

    buffer_s.append(ini_stat)
    if doesGeneratePassingTestProgram:
        ini_stat[classNo] += 1
    buffer_a.append(classNo)
    averageSimilarity, averageDiversity = calSimilarityandDiversity(testname,passingcnt, existingcovset,
                                                                    unionCovwithFail, averageSimilarity, passCov, averageDiversity)
    instantScore = math.sqrt(passingcnt) * (alpha * averageDiversity + (1 - alpha) * averageSimilarity)
    instantReward = instantScore - preInstantScore

    # New
    recordfile.write('----------\n')

    # @THX
    recordfile.write("averageSimilarity: " + str(averageSimilarity) + '\n')
    recordfile.write("averageDiversity: " +  str(averageDiversity) + '\n')

    recordfile.write('mutation rule: ' + commandMutate + '\n')
    recordfile.write('succeed? ' + str(doesGeneratePassingTestProgram) + '\n')
    recordfile.write('instantScore: ' + str(instantScore) + '\n')
    recordfile.write('instantScore ingoring n: ' + str(instantScore / passingcnt) + '\n')
    recordfile.write('instantReward: ' + str(instantReward) + '\n')
    recordfile.flush()

    print("buffer_a : ", buffer_a)
    print("buffer_r : ", buffer_r)
    print("buffer_s : ", buffer_s)

    # New
    if doesGeneratePassingTestProgram:
        if instantReward < 0:
            os.system('rm -rf ' + passtestdir + '/pass_' + classfile + str(mutationNo) + '_' + str(passingcnt) + '.c')
            os.system('rm -rf ' + passdir + '/passcov/' + testname)

    preInstantScore = instantScore
    historyscore[classNo][1] = (instantReward + historyscore[classNo][1] * historyscore[classNo][0]) \
                               / (historyscore[classNo][0] + 1)
    historyscore[classNo][0] += 1
    buffer_r.append(historyscore[classNo][1])
    cntStepForward += 1
    if(cntStepForward == stepForward): # one batch is over
        #calculate the loss function and backpropagate
        v_s_ = net((v_wrap(ini_stat[None, :])))[-1].data.numpy()[0, 0]
        buffer_v_target = []
        for r in buffer_r[::-1]:  # reverse buffer r
            v_s_ = r + GAMMA * v_s_
            buffer_v_target.append(v_s_)
        buffer_v_target.reverse()

        loss = net.loss_func(
            v_wrap(np.vstack(buffer_s)),
            v_wrap(np.array(buffer_a)),
            v_wrap(np.array(buffer_v_target)[:, None]))
        loss.backward()
        optim.step()
        cntOneBatch = 0
        print("buffer_a : ", buffer_a)
        print("buffer_r : ", buffer_r)
        print("buffer_s : ", buffer_s)
        buffer_a = []
        buffer_r = []
        buffer_s = []

    # end of memorized search


countfile.write('total_prog: ' + str(totoal_prog) + '\n')
countfile.write('syn_error_prog: ' + str(syn_error_prog) + '\n')
countfile.write('same_prog: ' + str(same_prog) + '\n')
countfile.write('compiled_prog: ' + str(compiled_prog) + '\n')
countfile.write('ub_prog: ' + str(ub_prog) + '\n')
countfile.write('failing_prog: ' + str(failing_prog) + '\n')
countfile.write('passing interesting: ' + str(passing_interesting) + '\n')
countfile.write('passing not interesting: ' + str(passing_not_interesting) + '\n')
countfile.write('repeative_prog: ' + str(repeative_prog) + '\n')
countfile.write('remove_oracle_prog: ' + str(remove_oracle_prog) + '\n')
countfile.write('gaptime: ' + str(gaptime) + '\n')
countfile.write('select prompt: ' + selected + '\n')
countfile.flush()
countfile.close()

recordfile.close()
successRecord.close()
mutateRecord.close()


