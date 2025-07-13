# Script to simulate ARMA processes and examine their true and sampled ACF, PACF
armod<-c(0.373, 0.114) # AR(2) for lag 1 diff of DJ Utilities Index

mamod<-c(0.2279, -0.2488)
# mamod<-NULL # no moving average component.
sdmod<-sqrt(0.1796)
nsamples<-100
abs(polyroot(c(1,-armod)))# check causality
abs(polyroot(c(1,mamod))) # check invertability

acfmod<-ARMAacf(ar=armod,ma=mamod,lag.max=15)
pacfmod<-ARMAacf(ar=armod,ma=mamod,lag.max=15,pacf=TRUE)
# Compare against ACF, PACF for some samples....
for(i in 1:10){
par(mfrow=c(3,2))
plot(acfmod, type="h",xlab="lag",ylim=c(-1,1))
abline(h=0)
title("Theoretical ACF")
plot(pacfmod, type="h",xlab="lag",ylim=c(-1,1))
abline(h=0)
title("Theoretical PACF")

x<-arima.sim(n = nsamples, list(ar = armod, ma = mamod),
          sd = sdmod)

acf(x,lag.max=15, main=paste("Sample Path ",as.character(i)))
pacf(x,lag.max=15, main=paste("Sample Path ",as.character(i)))
ts.plot(x, main=paste("Sample Path ",as.character(i)))
}

