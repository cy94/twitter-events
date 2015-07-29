# classify.R
# 
# chandan yeshwanth
# chandan.yeshwanth@gmail.com
# 
# 14 July 2015

# Used to classify points obtained from curve fitting
# (see: sigmoid_fit.R)
# Points are 4 tuples of sigmoid function parameters with 
# the associated word
# Clustering separates Sigmoid-curves from straight-line
# curves

classify <- function(vals, eventname) {
  words = unlist(vals["word"])
  
  a1 = as.numeric(unlist(vals["a1"]))
  a2 = as.numeric(unlist(vals["a2"]))
  a3 = as.numeric(unlist(vals["a3"]))
  a4 = as.numeric(unlist(vals["a4"]))
  
  # plot and save as SVG
  dirname = "classified/"
  outfilename = paste(dirname, eventname, ".svg", sep="")
  
  svg(outfilename, height = 15, width = 30)
  plot(jitter(a2), jitter(a3), xlim=c(-5, 0.1))
  text(jitter(a2), jitter(a3), labels=words, cex=0.7, pos=3)
  dev.off()
}