********************************************************************************
************* Quantitative Macroeconomics. The Final Project. ************************************
********************************************************************************
*Author: SZTACHERA, Maciej Jan

clear all

// working directory is where you put this do-file. Put it together with dataset.
cd "`c(pwd)'"

//load dataset
use VAR.dta

// set data as time series
tsset dateq, quarterly

// Generate variables
gen lnY = log(Y)
gen gY =  lnY[_n] - lnY[_n-1]
gen LLS = log(LS)
gen gLS = LLS[_n] - LLS[_n-1]
gen demployment = employment[_n] - employment[_n-1]

// STATIONARITY TESTING

gen dgLS =d.gLS
reg dgLS l.gLS
estat bgodfrey
eststo: dfuller gLS

gen dlnY = d.lnY
reg dlnY L.lnY L(3).lnY L(9).lnY
estat bgodfrey
eststo: dfuller lnY, lags(9)

gen dinfl = d.i
reg dinfl l.i l(4).i
estat bgodfrey
eststo: dfuller i, lags(4)

gen die = d.ie
reg die l.ie
estat bgodfrey
eststo: dfuller ie

gen dffr = d.ffr
reg dffr l(1/9).ffr
estat bgodfrey
eststo: dfuller ffr, lags(9)

gen ddffr = d.dffr
reg ddffr l(1).dffr l(8).dffr
estat bgodfrey
eststo: dfuller dffr, lags(8)

esttab using dfuller1.tex, title(ADF stationarity testing table\label{tab1}) alignment(D{.}{.}{-1}) width(0.4\hsize) compress replace
eststo clear

gen dwages = d.wages
reg dwages l.wages l(3).wages l(8/9).wages dateq
estat bgodfrey
eststo: dfuller wages, trend lags(9)

gen wage_growth = (wages[_n]-wages[_n-1])/wages[_n-1]
gen dwgrowth = d.wage_growth
reg dwgrowth l(1/2).wage_growth l(7/8).wage_growth
estat bgodfrey
eststo: dfuller wage_growth, lags(8)

gen employment_growth = (employment[_n]-employment[_n-1])/employment[_n-1]
gen dwemployment = d.employment_growth
reg dwemployment l(1).employment_growth l(5/6).employment_growth 
estat bgodfrey
eststo: dfuller employment_growth, lags(6)

gen investment_growth = (investment[_n]-investment[_n-1])/investment[_n-1]
gen digrowth = d.investment_growth
reg digrowth l.investment_growth
estat bgodfrey
eststo: dfuller investment_growth

esttab using dfuller2.tex, title(ADF stationarity testing table\label{tab1}) alignment(D{.}{.}{-1}) width(0.4\hsize) compress replace

// Prepare variables for VAR
gen lffr = ffr[_n-1]
gen dlffr = d.lffr
gen lffr2 = ffr[_n-2]
gen dlffr2 = d.lffr2
gen lffr3 = ffr[_n-3]
gen dlffr3 = d.lffr3
gen lie3 = ie[_n-3]
gen lgLS3 = gLS[_n-3]
gen lffr5 = ffr[_n-5]
gen lie5 = ie[_n-5]
gen dlffr5 = d.lffr5
gen lgLS5 = gLS[_n-5]
gen fgLS = f.gLS

// BASELINE VAR ANALYSIS

* Set up a structural VAR with standard NK monetary policy transmission mechanism without lags
* The theory implies that an increase in the interest rate should decrease the marginal cost, which 
* in the NK model is the reciprocal of the LS, and this should in turn decrease inflation:

// checking VAR lag order
varsoc dffr gLS, maxlag(8)
matrix A2 = (1,0\.,1)
matrix B2 = (.,0\0,.)
svar dffr gLS, lags(1) aeq(A2) beq(B2)
eststo: vargranger
esttab using vargranger_ffr_gLS.tex, title(Granger results ffr_gLS table\label{tab1}) alignment(D{.}{.}{-1}) width(0.4\hsize) replace
eststo clear

varsoc dffr gLS i,maxlag(8)
matrix A3 = (1,0,0\.,1,0\.,.,1)
matrix B3 = (.,0,0\0,.,0\0,0,.)
svar dffr gLS i, lags(1/4) aeq(A3) beq(B3)
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(dffr)
irf graph oirf, impulse(dffr) response(gLS)

varsoc dffr i gLS, maxlag(8)
svar dffr i gLS, lags(1) aeq(A3) beq(B3)
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(dffr)
irf graph oirf, impulse(dffr) response(gLS)

varsoc dffr i ie gLS, maxlag(8)
matrix A4 = (1,0,0,0\.,1,0,0\.,.,1,0\.,.,.,1)
matrix B4 = (.,0,0,0\0,.,0,0\0,0,.,0\0,0,0,.)
svar dffr i ie gLS, lags(1) aeq(A4) beq(B4)
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(dffr)
irf graph oirf, impulse(dffr) response(gLS)

varsoc dffr gY i ie gLS, maxlag(8)
matrix A5 = (1,0,0,0,0\.,1,0,0,0\.,.,1,0,0\.,.,.,1,0\.,.,.,.,1)
matrix B5 = (.,0,0,0,0\0,.,0,0,0\0,0,.,0,0\0,0,0,.,0\0,0,0,0,.)
svar dffr gY i ie gLS, lags(1) aeq(A5) beq(B5)
varstable
eststo: vargranger
esttab using vargranger_ffr_fgLS.tex, title(Granger results ffr_gLS table\label{tab1}) alignment(D{.}{.}{-1}) width(0.4\hsize) replace
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(gLS)

eststo clear

* Use investment growth instead of output growth
varsoc dffr investment_growth i ie gLS, maxlag(8)
svar dffr investment_growth i ie gLS, lags(1) aeq(A5) beq(B5)

* Use wage growth instead of inflation
varsoc dffr wage_growth gLS, maxlag(8)
svar dffr wage_growth gLS, lags(1) aeq(A3) beq(B3)
varstable

varsoc dffr gLS wage_growth, maxlag(8)
svar dffr gLS wage_growth, lags(1) aeq(A3) beq(B3)
varstable

varsoc dffr wage_growth ie gLS, maxlag(8)
svar dffr wage_growth ie gLS, lags(1) aeq(A4) beq(B4)
varstable

// Checking stability condition of (S)VAR run command "varstable" after estimation of VAR
varstable

// MONETARY POLICY LAG HYPOTHESIS

* 1 quarter lagged interest rate

varsoc dlffr ie gLS, maxlag(8)
svar dlffr ie gLS, lags(1) aeq(A3) beq(B3)
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dlffr) response(gLS) 

// Standard NK VAR with LS, inflation expectations and lagged interest rate

* 1 QUARTER LAG
// imposing restrictions
varsoc dlffr gY i ie gLS, maxlag(8)
svar dlffr gY i ie gLS, lags(1) aeq(A5) beq(B5)
vargranger

* 2-QUARTER LAG

// imposing restrictions
varsoc dlffr2 gY i ie gLS, maxlag(8)
svar dlffr2 gY i ie gLS, lags(1) aeq(A5) beq(B5)
vargranger

* 3-QUARTER LAG - THE MOST PROMISING RESULTS ARE HERE

// imposing restrictions
varsoc dlffr3 gY i ie gLS, maxlag(8)
svar dlffr3 gY i ie gLS, lags(1) aeq(A5) beq(B5)
eststo: vargranger
esttab using vargranger_dlffr3_gLS.tex, title(Granger results dlffr3_gLS table\label{tab1}) alignment(D{.}{.}{-1}) width(0.4\hsize) replace
irf create var, set(var) replace
irf graph oirf, impulse(dlffr3) response(gLS)
irf create var, set(var) replace
irf graph oirf, impulse(dlffr3) response(gY)
irf graph oirf, impulse(dlffr3) response(i)

* With stationary lagged inflation expectations
varsoc dlffr3 gY i lie3 gLS, maxlag(8)
svar dlffr3 gY i lie3 gLS, lags(1) aeq(A5) beq(B5)
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dlffr3) response(gLS)

* Change order
varsoc dlffr3 lie3 gLS gY i, maxlag(8)
svar dlffr3 lie3 gLS gY i, lags(1) aeq(A5) beq(B5)
vargranger

// Try without inflation expectations
varsoc dlffr3 gY i gLS, maxlag(8)
eststo: svar dlffr3 gY i gLS, lags(1) aeq(A4) beq(B4)
vargranger

* 5-QUARTER LAG

// imposing restrictions
varsoc dlffr5 gY i ie gLS, maxlag(8) 
svar dlffr5 gY i ie gLS, lags(1) aeq(A5) beq(B5)
vargranger

varsoc dlffr5 gY i lie5 gLS, maxlag(8)
svar dlffr5 gY i lie5 gLS, lags(1) aeq(A5) beq(B5)
vargranger
irf create var, set(var) replace
irf graph sirf, impulse(dlffr5) response(gLS)

* with lagged labor share
// imposing restrictions
varsoc dlffr5 gY i lie5 lgLS5, maxlag(8)
svar dlffr5 gY i lie5 lgLS5, lags(1) aeq(A5) beq(B5)
vargranger

// Try without inflation expectations
varsoc dlffr5 gY i gLS, maxlag(8)
eststo: svar dlffr5 gY i gLS, lags(1) aeq(A4) beq(B4)
vargranger

// AGNOSTIC APPROACH

// Agnostic approach based on factor remunerations and assumption that the interest rate impacts investment first.
* contrary to the NK assumption that the main channel is the Euler equation
varsoc dffr investment_growth wage_growth employment_growth gLS, maxlag(8)
svar dffr investment_growth wage_growth employment_growth gLS, lags(1) aeq(A5) beq(B5)
varstable
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(gLS)

* Test different ordering
varsoc employment_growth dffr investment_growth wage_growth gLS, maxlag(8)
svar employment_growth dffr investment_growth wage_growth gLS, lags(1) aeq(A5) beq(B5)
varstable
eststo: vargranger
esttab using vargranger_dffr_gLS_definition.tex, title(Granger results dlffr3_gLS table\label{tab1}) alignment(D{.}{.}{-1}) width(0.4\hsize) replace
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(gLS)
irf graph oirf, response(gLS)

* Test different structure
matrix A6 = (1,0,0,0,0,0\.,1,0,0,0,0\.,.,1,0,0,0\.,.,.,1,0,0\.,.,.,.,1,0\.,.,.,.,.,1)
matrix B6 = (.,0,0,0,0,0\0,.,0,0,0,0\0,0,.,0,0,0\0,0,0,.,0,0\0,0,0,0,.,0\0,0,0,0,0,.)
varsoc i employment_growth dffr investment_growth wage_growth gLS, maxlag(8)
svar i employment_growth dffr investment_growth wage_growth gLS, lags(1) aeq(A6) beq(B6)
varstable
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(gLS)

* Reduce the number of parameters (wages not needed)
varsoc employment_growth dffr investment_growth gLS, maxlag(8)
svar employment_growth dffr investment_growth gLS, lags(1) aeq(A4) beq(B4)
varstable
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(dffr) response(gLS)

* Combine with monetary policy lag
* 1 lag
svar dlffr investment_growth wage_growth employment_growth gLS, lags(1) aeq(A5) beq(B5)
varstable
vargranger
* 2 lags
svar dlffr2 investment_growth wage_growth employment_growth gLS, lags(1) aeq(A5) beq(B5)
varstable
varstable
vargranger
* 3 lags
svar dlffr3 investment_growth wage_growth employment_growth gLS, lags(1) aeq(A5) beq(B5)
varstable
varstable
vargranger
* 5 lags
svar dlffr5 investment_growth wage_growth employment_growth gLS, lags(1)  aeq(A5) beq(B5)
varstable
varstable
vargranger

* With inflation

* 2 lags 
svar dlffr2 investment_growth wage_growth employment_growth gLS i, lags(1/8) aeq(A6) beq(B6)
varstable
vargranger
* 3 lags
svar dlffr3 investment_growth wage_growth employment_growth gLS i, lags(1/8) aeq(A6) beq(B6)
varstable
vargranger
* 5 lags
svar dlffr5 investment_growth wage_growth employment_growth gLS i, lags(1/8) aeq(A6) beq(B6)
varstable
vargranger

//// THE PREVIOUS RESULTS NOT VERY ROBUST - problem with non-stationary federal funds rate and labor share
// Now I will try to detrend the federal funds rate and check if it is stationary

gen t = dateq
gen t_squared = t^2
gen t_cubed = t^3
gen t_fourth = t^4

reg ffr t*
predict trend

gen ffr_detrended = ffr - trend

// Check stationarity
gen dffr_d = d.ffr_detrended
reg dffr_d l(1/4).ffr_detrended
estat bgodfrey
dfuller ffr_detrended, lags(4)

// Apply the same procedure to the labor share\III
reg LS t*
predict trend2

gen LS_det = LS - trend2

// Check stationarity
gen dLS_d = d.LS_det
reg dLS_d l(1/4).LS_det
estat bgodfrey
dfuller LS_det, lags(4)

// The detrended series is stationary with 4 lags (robust result)
varsoc ffr_detrended gY i ie LS_det, maxlag(8)
svar ffr_detrended gY i ie LS_det, lags(1) aeq(A5) beq(B5)
vargranger
irf create var, set(var) replace
irf graph oirf, impulse(ffr_detrended) response(LS_det)