vals <- read.csv("out/mh17.csv", header=FALSE)

xdata = 1:nrow(vals)
ydata = unlist(vals)
fit = nls(ydata ~ a1*xdata^3 + a2*xdata^2 + a3*xdata + a4, start=list(a1=1, a2=1, a3=1, a4=1))

plot(xdata, predict(fit), col=1, type="l")
par(new=T)
plot(xdata, ydata, col=3)

