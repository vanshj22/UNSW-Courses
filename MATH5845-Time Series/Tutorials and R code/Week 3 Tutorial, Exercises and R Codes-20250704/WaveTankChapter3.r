# Analysis of Wave Tank Data from Cowpertwait and Metcalfe.

# Read in Data from file

wave.dat<-read.table("wave.dat",header=T)
attach(wave.dat)

# plot full time series and check acf, pacf
#pdf("FigWaveHtTSplot.pdf")
par(mfrow=c(1,1))
plot(ts(waveht))
title("Wave Height over 39.7 seconds")
#dev.off()

par(mfrow=c(1,2))
acf(waveht)
pacf(waveht)


# Task 1
# Now look at 6 segments of 66 time points to check for stationarity:
par(mfrow=c(3,2))
for (blocknum in 1:6){
  blocktimes<-(blocknum-1)*66+1:66
  ts.plot(waveht[blocktimes]) 
  abline(v=0)
}
par(mfrow=c(3,2))
for (blocknum in 1:6){
  blocktimes<-(blocknum-1)*66+1:66
  acf(waveht[blocktimes])
}

# Task 2
# Automatically select best AR model using minimum AIC and Yule-Walker fit:

waveht.armod<-ar.yw(waveht)
waveht.armod.summary<-cbind(waveht.armod$ar,diag(waveht.armod$asy.var.coef)^0.5)
colnames(waveht.armod.summary)<-c("phi","s.e.")
round(waveht.armod.summary,3)

abs(polyroot(c(1,-waveht.armod$ar))) # check stationarity of fit!

# Fitting the AR(13) with MLE:
waveht.ar13MLEfit<-arima(waveht,order=c(13,0,0), method="ML")
waveht.ar13MLEfit

# Task 3
# Check if residuals from best AR model are white noise, Gaussian.
par(mfrow=c(2,2))

ts.plot(waveht.armod$resid,type="h")

acf(waveht.armod$resid,na.action=na.pass)
pacf(waveht.armod$resid,na.action=na.pass)
qqnorm(waveht.armod$resid)

# Task 4 
# Fit some mixed ARMA(p,q) models and compare

# Example to start you off...

waveht.arma<-arima(waveht,order=c(2,0,1), method="ML")
waveht.arma

# compare variance of 1-step prediction with best AR model:

waveht.arma$sigma2  # variance of innovations for ARMA model
waveht.armod$var.pred # variance of innovations for AR model

# which is the winner?

# Check if residuals from ARMA model are white noise, Gaussian.
par(mfrow=c(2,2))

ts.plot(waveht.arma$resid,type="h")

acf(waveht.arma$resid,na.action=na.pass)
pacf(waveht.arma$resid,na.action=na.pass)
qqnorm(waveht.arma$resid)



