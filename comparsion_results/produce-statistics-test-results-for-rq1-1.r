library(readxl)

rq1_1_diwi <- read_xls("./tse-llm4cbi/rq1-1-diwi.xls")
print("############ data from table rq1_diwi ###########")
print(rq1_1_diwi)

rq1_1_recbi <- read_xls("./tse-llm4cbi/rq1-1-recbi.xls")
print("############ data from table rq1_diwi ###########")
print(rq1_1_recbi)

rq1_1_llm4cbi <- read_xls("./tse-llm4cbi/rq1-1-llm4cbi.xls")
print("############ data from table rq1_llm4cbi ###########")
print(rq1_1_llm4cbi)


tem_table <- rq1_1_recbi
tem_llm4cbi <- rq1_1_llm4cbi
## TOP-1
X <- c(as.numeric(unlist(tem_table[2:11, 2])), as.numeric(unlist((tem_table[14:23, 2]))))
Y <- c(as.numeric(unlist(tem_llm4cbi[2:11, 2])),as.numeric(unlist(tem_llm4cbi[14:23, 2])))

print("X:")
print(X)

print("Y:")
print(Y)

print("========= top-1 ========")
p1 <- wilcox.test(X, Y)
print("P1 : ")
print(p1)
R1<-sum(rank(c(Y,X))[seq_along(Y)])
#R1<-sum(rank(c(X,Y))[seq_along(X)]) # MFR/MAF
#print(R1)
a12 <- (R1/20 - (20+1)/2)/20
print("a12 : ")
print(a12)


## TOP-5
X <- c(as.numeric(unlist(tem_table[2:11, 3])), as.numeric(unlist((tem_table[14:23, 3]))))
Y <- c(as.numeric(unlist(tem_llm4cbi[2:11, 3])),as.numeric(unlist(tem_llm4cbi[14:23, 3])))

print("X:")
print(X)

print("Y:")
print(Y)

print("========= top-5 ========")
p1 <- wilcox.test(X, Y)
print("P1 : ")
print(p1)
R1<-sum(rank(c(Y,X))[seq_along(Y)])
#R1<-sum(rank(c(X,Y))[seq_along(X)]) # MFR/MAF
#print(R1)
a12 <- (R1/20 - (20+1)/2)/20
print("a12 : ")
print(a12)

## TOP-10
X <- c(as.numeric(unlist(tem_table[2:11, 4])), as.numeric(unlist((tem_table[14:23, 4]))))
Y <- c(as.numeric(unlist(tem_llm4cbi[2:11, 4])),as.numeric(unlist(tem_llm4cbi[14:23, 4])))

print("X:")
print(X)

print("Y:")
print(Y)

print("========= top-10 ========")
p1 <- wilcox.test(X, Y)
print("P1 : ")
print(p1)
R1<-sum(rank(c(Y,X))[seq_along(Y)])
#R1<-sum(rank(c(X,Y))[seq_along(X)]) # MFR/MAF
#print(R1)
a12 <- (R1/20 - (20+1)/2)/20
print("a12 : ")
print(a12)


## TOP-20
X <- c(as.numeric(unlist(tem_table[2:11, 5])), as.numeric(unlist((tem_table[14:23, 5]))))
Y <- c(as.numeric(unlist(tem_llm4cbi[2:11, 5])),as.numeric(unlist(tem_llm4cbi[14:23, 5])))

print("X:")
print(X)

print("Y:")
print(Y)

print("========= top-20 ========")
p1 <- wilcox.test(X, Y)
print("P1 : ")
print(p1)
R1<-sum(rank(c(Y,X))[seq_along(Y)])
#R1<-sum(rank(c(X,Y))[seq_along(X)]) # MFR/MAF
#print(R1)
a12 <- (R1/20 - (20+1)/2)/20
print("a12 : ")
print(a12)

## MFR
X <- c(as.numeric(unlist(tem_table[2:11, 6])), as.numeric(unlist((tem_table[14:23, 6]))))
Y <- c(as.numeric(unlist(tem_llm4cbi[2:11, 6])),as.numeric(unlist(tem_llm4cbi[14:23, 6])))

print("X:")
print(X)

print("Y:")
print(Y)

print("========= MFR ========")
p1 <- wilcox.test(X, Y)
print("P1 : ")
print(p1)
#R1<-sum(rank(c(Y,X))[seq_along(Y)])
R1<-sum(rank(c(X,Y))[seq_along(X)]) # MFR/MAF
#print(R1)
a12 <- (R1/20 - (20+1)/2)/20
print("a12 : ")
print(a12)

## MFR
X <- c(as.numeric(unlist(tem_table[2:11, 7])), as.numeric(unlist((tem_table[14:23, 7]))))
Y <- c(as.numeric(unlist(tem_llm4cbi[2:11, 7])),as.numeric(unlist(tem_llm4cbi[14:23, 7])))

print("X:")
print(X)

print("Y:")
print(Y)

print("========= MAR ========")
p1 <- wilcox.test(X, Y)
print("P1 : ")
print(p1)
#R1<-sum(rank(c(Y,X))[seq_along(Y)])
R1<-sum(rank(c(X,Y))[seq_along(X)]) # MFR/MAF
#print(R1)
a12 <- (R1/20 - (20+1)/2)/20
print("a12 : ")
print(a12)


