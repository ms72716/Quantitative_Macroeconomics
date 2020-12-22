clear all

set fredkey "put your fredkey here", permanently
* GDPC1 GDPPOT

// Import data from the Federal Reserve Economic Database
import fred GDPC1 GPDIC1 FEDFUNDS MICH CPALTT01USM657N PRS85006173 PAYEMS AHETPI, daterange("01jan1980" "01jan2020") aggregate(quarterly)

// Generate a monthly time format variable
gen dateq = qofd(daten)

// set data as time series
tsset dateq, quarterly

// rename variables for convenience
rename GDPC1 Y
rename FEDFUNDS ffr
rename MICH ie
rename CPALTT01USM657N i
rename PRS85006173 LS
rename GPDIC1 investment
rename PAYEMS employment
rename AHETPI wages