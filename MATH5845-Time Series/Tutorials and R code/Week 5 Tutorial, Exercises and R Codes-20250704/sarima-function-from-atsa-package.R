
# Function 'sarima' in the 'astsa' package:
# type 'sarima' in the command window to see the code....

function (xdata, p, d, q, P = 0, D = 0, Q = 0, S = -1, details = TRUE, 
          xreg = NULL, tol = sqrt(.Machine$double.eps), no.constant = FALSE) 
{
  trc = ifelse(details == TRUE, 1, 0)
  n = length(xdata)
  if (is.null(xreg)) {
    constant = 1:n
    xmean = rep(1, n)
    if (no.constant == TRUE) 
      xmean = NULL
    if (d == 0 & D == 0) {
      fitit = stats::arima(xdata, order = c(p, d, q), seasonal = list(order = c(P, 
                                                                                D, Q), period = S), xreg = xmean, include.mean = FALSE, 
                           optim.control = list(trace = trc, REPORT = 1, 
                                                reltol = tol))
    }
    else if (xor(d == 1, D == 1) & no.constant == FALSE) {
      fitit = stats::arima(xdata, order = c(p, d, q), seasonal = list(order = c(P, 
                                                                                D, Q), period = S), xreg = constant, optim.control = list(trace = trc, 
                                                                                                                                          REPORT = 1, reltol = tol))
    }
    else fitit = stats::arima(xdata, order = c(p, d, q), 
                              seasonal = list(order = c(P, D, Q), period = S), 
                              include.mean = !no.constant, optim.control = list(trace = trc, 
                                                                                REPORT = 1, reltol = tol))
  }
  if (!is.null(xreg)) {
    fitit = stats::arima(xdata, order = c(p, d, q), seasonal = list(order = c(P, 
                                                                              D, Q), period = S), xreg = xreg, optim.control = list(trace = trc, 
                                                                                                                                    REPORT = 1, reltol = tol))
  }
  old.par <- par(no.readonly = TRUE)
  layout(matrix(c(1, 2, 4, 1, 3, 4), ncol = 2))
  rs <- fitit$residuals
  stdres <- rs/sqrt(fitit$sigma2)
  num <- sum(!is.na(rs))
  plot.ts(stdres, main = "Standardized Residuals", ylab = "")
  alag <- 10 + sqrt(num)
  ACF = stats::acf(rs, alag, plot = FALSE, na.action = na.pass)$acf[-1]
  LAG = 1:alag/frequency(xdata)
  L = 2/sqrt(num)
  plot(LAG, ACF, type = "h", ylim = c(min(ACF) - 0.1, min(1, 
                                                          max(ACF + 0.4))), main = "ACF of Residuals")
  abline(h = c(0, -L, L), lty = c(1, 2, 2), col = c(1, 4, 4))
  stats::qqnorm(stdres, main = "Normal Q-Q Plot of Std Residuals")
  stats::qqline(stdres, col = 4)
  nlag <- ifelse(S < 4, 20, 3 * S)
  ppq <- p + q + P + Q
  pval <- numeric(nlag)
  for (i in (ppq + 1):nlag) {
    u <- stats::Box.test(rs, i, type = "Ljung-Box")$statistic
    pval[i] <- stats::pchisq(u, i - ppq, lower.tail = FALSE)
  }
  plot((ppq + 1):nlag, pval[(ppq + 1):nlag], xlab = "lag", 
       ylab = "p value", ylim = c(0, 1), main = "p values for Ljung-Box statistic")
  abline(h = 0.05, lty = 2, col = "blue")
  on.exit(par(old.par))
  k = length(fitit$coef)
  BIC = log(fitit$sigma2) + (k * log(n)/n)
  AICc = log(fitit$sigma2) + ((n + k)/(n - k - 2))
  AIC = log(fitit$sigma2) + ((n + 2 * k)/n)
  list(fit = fitit, AIC = AIC, AICc = AICc, BIC = BIC)
}
