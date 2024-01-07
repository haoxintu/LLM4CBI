#!/bin/bash

if
   clang -pedantic -Wall -O \
  -I/home/tuhaoxin/dut-research/gitee/lpm-csmith/src-csmith/runtime $1 >out_clang.txt 2>&1 &&\
  ! grep 'conversions than data arguments' out_clang.txt &&\
  ! grep 'incompatible redeclaration' out_clang.txt &&\
  ! grep 'ordered comparison between pointer' out_clang.txt &&\
  ! grep 'eliding middle term' out_clang.txt &&\
  ! grep 'end of non-void function' out_clang.txt &&\
  ! grep 'invalid in C99' out_clang.txt &&\
  ! grep 'specifies type' out_clang.txt &&\
  ! grep 'should return a value' out_clang.txt &&\
  ! grep 'uninitialized' out_clang.txt &&\
  ! grep 'incompatible pointer to' out_clang.txt &&\
  ! grep 'incompatible integer to' out_clang.txt &&\
  ! grep 'type specifier missing' out_clang.txt &&\
  frama-c -cpp-command 'gcc  -C -Dvolatile= -E -I. -I/home/tuhaoxin/dut-research/gitee/lpm-csmith/src-csmith/runtime' \
  -val -no-val-show-progress -machdep x86_64 -cpp-frama-c-compliant $1 > out_framac.txt 2>&1
then
  ubs=$(egrep -i '(user error|assert)' out_framac.txt)
  tmp=$(printf '%s\n' "${ubs//"assert \\valid_read(argv + 1)"/}")
  echo $tmp
  flag=`echo $tmp|awk '{print match($0,"assert")}'`;
  if [ $flag -gt 0 ];then
    exit 1
  else
    echo "This program is heathy!"
    exit 0
  fi
else
  exit 1
fi
