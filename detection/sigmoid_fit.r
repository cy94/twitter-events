# sigmoid_fit.r

# Chandan Yeshwanth
# chandan.yeshwanth@gmail.com
# 13 July 2015

# This script is part of a an event detection procedure for twitter data
# (See github.com/cy94)
# The script uses as input a time series of IDF values for words in this format - 
#   input.csv
# 
#   word,1,2,3 ... 180 (header)
#   mh17,a,b,c ... d
#   .
#   .
#   .
#   
#   where a, b, c are the IDF values for the word "mh17" in the corresponding minutes
#   1, 2, 3 of the input Twitter data

# The IDF plot is modelled as a sigmoid function (see: http://www.wikiwand.com/en/Sigmoid_function)
# and curve parameters are obtained using the nls function in R
# Curves are expected to be one of two types - 
#   * sigmoid - the word frequency increases rapidly at a point in time, possibly corresponds to 
#               an event
#   * straight line - "baseline" words with nearly constant IDF (also includes stray occurrences 
#                                                                of words)

# four parameter sigmoid function

# import files
source("classify.R")

sigmoid = function(params, t){
  a1 = params[1]
  a2 = params[2]
  a3 = params[3]
  a4 = params[4]
  sigmoid = a1 + a2/(1 + exp(-a3 * (t - a4)))
}

PRINTDETAILS = TRUE

eventname <- "mh17"
dirname <- "out/"
fullfilename <- paste(dirname, eventname, ".csv", sep="")

idfs <- read.csv(fullfilename)

results <- data.frame(word = character(),
                      a1 = double(),
                      a2 = double(),
                      a3 = double(),
                      a4 = double(),
                      stringsAsFactors = FALSE
                      )

for (row in 2 : nrow(idfs)) {
# for (row in 17 : 17) {
  idf_vals <- na.omit(unlist(idfs[row, 2:ncol(idfs)]))
  
  # the time series, one point for each minute
  time <- 1:(length(idf_vals))
  
  word <- paste(rownames(idfs)[row], as.character(idfs[row, 1]))
  
  plot(idf_vals, xlab="Minutes from start", ylab="IDF", ylim=c(0, 6))
  title(word)
  
  # fit data tos sigmoid curve
  fitmodel = nls(idf_vals ~ a1 + a2/(1 + exp(-a3 * (time - a4))),
               start = list(a1 = mean(idf_vals), 
                            a2 = -sd(idf_vals),
                            a3 = 1,
                            a4 = 100),
               algorithm = "port",
               lower = c(-1,-Inf,1,20),
               upper = c(10,0,Inf,200),
               control = nls.control(warnOnly = TRUE)
            )
  
  # plot the fitted curve
  params = coef(fitmodel)
  # print(word)
  # print(c(word, unlist(params)))
  
  print(unlist(params))
 
  # lines(time, sigmoid(params, time))
  
  # store in a data frame
  results[nrow(results) + 1, ] = c(word, unlist(params))
  
  # wait for user input, then go to next word
  line <- readline()
}  

# print(results)
classify(results, eventname)