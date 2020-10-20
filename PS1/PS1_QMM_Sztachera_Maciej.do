clear all

cd "D:\prywatne\Werkstatt\main\UAB QEM\Quantitative Macroeconomics\PS1"

* NOTE: You need to set the Stata working directory to the path
* where the data file is located.

set more off

clear
quietly infix                 ///
  int     year       1-4      ///
  long    serial     5-9      ///
  byte    month      10-11    ///
  double  hwtfinl    12-21    ///
  double  cpsid      22-35    ///
  byte    asecflag   36-36    ///
  double  asecwth    37-46    ///
  byte    pernum     47-48    ///
  double  wtfinl     49-62    ///
  double  cpsidp     63-76    ///
  double  asecwt     77-86    ///
  byte    age        87-88    ///
  byte    sex        89-89    ///
  int     race       90-92    ///
  byte    empstat    93-94    ///
  byte    labforce   95-95    ///
  int     occ        96-99    ///
  int     ind        100-103  ///
  int     uhrsworkt  104-106  ///
  int     ahrsworkt  107-109  ///
  byte    absent     110-110  ///
  int     educ       111-113  ///
  byte    workly     114-115  ///
  double  inctot     116-124  ///
  double  incwage    125-132  ///
  double  hourwage   133-137  ///
  double  earnweek   138-145  ///
  using `"cps_00010.dat"'

replace hwtfinl   = hwtfinl   / 10000
replace asecwth   = asecwth   / 10000
replace wtfinl    = wtfinl    / 10000
replace asecwt    = asecwt    / 10000
replace hourwage  = hourwage  / 100
replace earnweek  = earnweek  / 100

format hwtfinl   %10.4f
format cpsid     %14.0f
format asecwth   %10.4f
format wtfinl    %14.4f
format cpsidp    %14.0f
format asecwt    %10.4f
format inctot    %9.0f
format incwage   %8.0f
format hourwage  %5.2f
format earnweek  %8.2f

label var year      `"Survey year"'
label var serial    `"Household serial number"'
label var month     `"Month"'
label var hwtfinl   `"Household weight, Basic Monthly"'
label var cpsid     `"CPSID, household record"'
label var asecflag  `"Flag for ASEC"'
label var asecwth   `"Annual Social and Economic Supplement Household weight"'
label var pernum    `"Person number in sample unit"'
label var wtfinl    `"Final Basic Weight"'
label var cpsidp    `"CPSID, person record"'
label var asecwt    `"Annual Social and Economic Supplement Weight"'
label var age       `"Age"'
label var sex       `"Sex"'
label var race      `"Race"'
label var empstat   `"Employment status"'
label var labforce  `"Labor force status"'
label var occ       `"Occupation"'
label var ind       `"Industry"'
label var uhrsworkt `"Hours usually worked per week at all jobs"'
label var ahrsworkt `"Hours worked last week"'
label var absent    `"Absent from work last week"'
label var educ      `"Educational attainment recode"'
label var workly    `"Worked last year"'
label var inctot    `"Total personal income"'
label var incwage   `"Wage and salary income"'
label var hourwage  `"Hourly wage"'
label var earnweek  `"Weekly earnings"'

label define month_lbl 01 `"January"'
label define month_lbl 02 `"February"', add
label define month_lbl 03 `"March"', add
label define month_lbl 04 `"April"', add
label define month_lbl 05 `"May"', add
label define month_lbl 06 `"June"', add
label define month_lbl 07 `"July"', add
label define month_lbl 08 `"August"', add
label define month_lbl 09 `"September"', add
label define month_lbl 10 `"October"', add
label define month_lbl 11 `"November"', add
label define month_lbl 12 `"December"', add
label values month month_lbl

label define asecflag_lbl 1 `"ASEC"'
label define asecflag_lbl 2 `"March Basic"', add
label values asecflag asecflag_lbl

label define age_lbl 00 `"Under 1 year"'
label define age_lbl 01 `"1"', add
label define age_lbl 02 `"2"', add
label define age_lbl 03 `"3"', add
label define age_lbl 04 `"4"', add
label define age_lbl 05 `"5"', add
label define age_lbl 06 `"6"', add
label define age_lbl 07 `"7"', add
label define age_lbl 08 `"8"', add
label define age_lbl 09 `"9"', add
label define age_lbl 10 `"10"', add
label define age_lbl 11 `"11"', add
label define age_lbl 12 `"12"', add
label define age_lbl 13 `"13"', add
label define age_lbl 14 `"14"', add
label define age_lbl 15 `"15"', add
label define age_lbl 16 `"16"', add
label define age_lbl 17 `"17"', add
label define age_lbl 18 `"18"', add
label define age_lbl 19 `"19"', add
label define age_lbl 20 `"20"', add
label define age_lbl 21 `"21"', add
label define age_lbl 22 `"22"', add
label define age_lbl 23 `"23"', add
label define age_lbl 24 `"24"', add
label define age_lbl 25 `"25"', add
label define age_lbl 26 `"26"', add
label define age_lbl 27 `"27"', add
label define age_lbl 28 `"28"', add
label define age_lbl 29 `"29"', add
label define age_lbl 30 `"30"', add
label define age_lbl 31 `"31"', add
label define age_lbl 32 `"32"', add
label define age_lbl 33 `"33"', add
label define age_lbl 34 `"34"', add
label define age_lbl 35 `"35"', add
label define age_lbl 36 `"36"', add
label define age_lbl 37 `"37"', add
label define age_lbl 38 `"38"', add
label define age_lbl 39 `"39"', add
label define age_lbl 40 `"40"', add
label define age_lbl 41 `"41"', add
label define age_lbl 42 `"42"', add
label define age_lbl 43 `"43"', add
label define age_lbl 44 `"44"', add
label define age_lbl 45 `"45"', add
label define age_lbl 46 `"46"', add
label define age_lbl 47 `"47"', add
label define age_lbl 48 `"48"', add
label define age_lbl 49 `"49"', add
label define age_lbl 50 `"50"', add
label define age_lbl 51 `"51"', add
label define age_lbl 52 `"52"', add
label define age_lbl 53 `"53"', add
label define age_lbl 54 `"54"', add
label define age_lbl 55 `"55"', add
label define age_lbl 56 `"56"', add
label define age_lbl 57 `"57"', add
label define age_lbl 58 `"58"', add
label define age_lbl 59 `"59"', add
label define age_lbl 60 `"60"', add
label define age_lbl 61 `"61"', add
label define age_lbl 62 `"62"', add
label define age_lbl 63 `"63"', add
label define age_lbl 64 `"64"', add
label define age_lbl 65 `"65"', add
label define age_lbl 66 `"66"', add
label define age_lbl 67 `"67"', add
label define age_lbl 68 `"68"', add
label define age_lbl 69 `"69"', add
label define age_lbl 70 `"70"', add
label define age_lbl 71 `"71"', add
label define age_lbl 72 `"72"', add
label define age_lbl 73 `"73"', add
label define age_lbl 74 `"74"', add
label define age_lbl 75 `"75"', add
label define age_lbl 76 `"76"', add
label define age_lbl 77 `"77"', add
label define age_lbl 78 `"78"', add
label define age_lbl 79 `"79"', add
label define age_lbl 80 `"80"', add
label define age_lbl 81 `"81"', add
label define age_lbl 82 `"82"', add
label define age_lbl 83 `"83"', add
label define age_lbl 84 `"84"', add
label define age_lbl 85 `"85"', add
label define age_lbl 86 `"86"', add
label define age_lbl 87 `"87"', add
label define age_lbl 88 `"88"', add
label define age_lbl 89 `"89"', add
label define age_lbl 90 `"90 (90+, 1988-2002)"', add
label define age_lbl 91 `"91"', add
label define age_lbl 92 `"92"', add
label define age_lbl 93 `"93"', add
label define age_lbl 94 `"94"', add
label define age_lbl 95 `"95"', add
label define age_lbl 96 `"96"', add
label define age_lbl 97 `"97"', add
label define age_lbl 98 `"98"', add
label define age_lbl 99 `"99+"', add
label values age age_lbl

label define sex_lbl 1 `"Male"'
label define sex_lbl 2 `"Female"', add
label define sex_lbl 9 `"NIU"', add
label values sex sex_lbl

label define race_lbl 100 `"White"'
label define race_lbl 200 `"Black/Negro"', add
label define race_lbl 300 `"American Indian/Aleut/Eskimo"', add
label define race_lbl 650 `"Asian or Pacific Islander"', add
label define race_lbl 651 `"Asian only"', add
label define race_lbl 652 `"Hawaiian/Pacific Islander only"', add
label define race_lbl 700 `"Other (single) race, n.e.c."', add
label define race_lbl 801 `"White-Black"', add
label define race_lbl 802 `"White-American Indian"', add
label define race_lbl 803 `"White-Asian"', add
label define race_lbl 804 `"White-Hawaiian/Pacific Islander"', add
label define race_lbl 805 `"Black-American Indian"', add
label define race_lbl 806 `"Black-Asian"', add
label define race_lbl 807 `"Black-Hawaiian/Pacific Islander"', add
label define race_lbl 808 `"American Indian-Asian"', add
label define race_lbl 809 `"Asian-Hawaiian/Pacific Islander"', add
label define race_lbl 810 `"White-Black-American Indian"', add
label define race_lbl 811 `"White-Black-Asian"', add
label define race_lbl 812 `"White-American Indian-Asian"', add
label define race_lbl 813 `"White-Asian-Hawaiian/Pacific Islander"', add
label define race_lbl 814 `"White-Black-American Indian-Asian"', add
label define race_lbl 815 `"American Indian-Hawaiian/Pacific Islander"', add
label define race_lbl 816 `"White-Black--Hawaiian/Pacific Islander"', add
label define race_lbl 817 `"White-American Indian-Hawaiian/Pacific Islander"', add
label define race_lbl 818 `"Black-American Indian-Asian"', add
label define race_lbl 819 `"White-American Indian-Asian-Hawaiian/Pacific Islander"', add
label define race_lbl 820 `"Two or three races, unspecified"', add
label define race_lbl 830 `"Four or five races, unspecified"', add
label define race_lbl 999 `"Blank"', add
label values race race_lbl

label define empstat_lbl 00 `"NIU"'
label define empstat_lbl 01 `"Armed Forces"', add
label define empstat_lbl 10 `"At work"', add
label define empstat_lbl 12 `"Has job, not at work last week"', add
label define empstat_lbl 20 `"Unemployed"', add
label define empstat_lbl 21 `"Unemployed, experienced worker"', add
label define empstat_lbl 22 `"Unemployed, new worker"', add
label define empstat_lbl 30 `"Not in labor force"', add
label define empstat_lbl 31 `"NILF, housework"', add
label define empstat_lbl 32 `"NILF, unable to work"', add
label define empstat_lbl 33 `"NILF, school"', add
label define empstat_lbl 34 `"NILF, other"', add
label define empstat_lbl 35 `"NILF, unpaid, lt 15 hours"', add
label define empstat_lbl 36 `"NILF, retired"', add
label values empstat empstat_lbl

label define labforce_lbl 0 `"NIU"'
label define labforce_lbl 1 `"No, not in the labor force"', add
label define labforce_lbl 2 `"Yes, in the labor force"', add
label values labforce labforce_lbl

label define uhrsworkt_lbl 997 `"Hours vary"'
label define uhrsworkt_lbl 999 `"NIU"', add
label values uhrsworkt uhrsworkt_lbl

label define absent_lbl 0 `"NIU"'
label define absent_lbl 1 `"No"', add
label define absent_lbl 2 `"Yes, laid off"', add
label define absent_lbl 3 `"Yes, other reason (vacation, illness, labor dispute)"', add
label values absent absent_lbl

label define educ_lbl 000 `"NIU or no schooling"'
label define educ_lbl 001 `"NIU or blank"', add
label define educ_lbl 002 `"None or preschool"', add
label define educ_lbl 010 `"Grades 1, 2, 3, or 4"', add
label define educ_lbl 011 `"Grade 1"', add
label define educ_lbl 012 `"Grade 2"', add
label define educ_lbl 013 `"Grade 3"', add
label define educ_lbl 014 `"Grade 4"', add
label define educ_lbl 020 `"Grades 5 or 6"', add
label define educ_lbl 021 `"Grade 5"', add
label define educ_lbl 022 `"Grade 6"', add
label define educ_lbl 030 `"Grades 7 or 8"', add
label define educ_lbl 031 `"Grade 7"', add
label define educ_lbl 032 `"Grade 8"', add
label define educ_lbl 040 `"Grade 9"', add
label define educ_lbl 050 `"Grade 10"', add
label define educ_lbl 060 `"Grade 11"', add
label define educ_lbl 070 `"Grade 12"', add
label define educ_lbl 071 `"12th grade, no diploma"', add
label define educ_lbl 072 `"12th grade, diploma unclear"', add
label define educ_lbl 073 `"High school diploma or equivalent"', add
label define educ_lbl 080 `"1 year of college"', add
label define educ_lbl 081 `"Some college but no degree"', add
label define educ_lbl 090 `"2 years of college"', add
label define educ_lbl 091 `"Associate's degree, occupational/vocational program"', add
label define educ_lbl 092 `"Associate's degree, academic program"', add
label define educ_lbl 100 `"3 years of college"', add
label define educ_lbl 110 `"4 years of college"', add
label define educ_lbl 111 `"Bachelor's degree"', add
label define educ_lbl 120 `"5+ years of college"', add
label define educ_lbl 121 `"5 years of college"', add
label define educ_lbl 122 `"6+ years of college"', add
label define educ_lbl 123 `"Master's degree"', add
label define educ_lbl 124 `"Professional school degree"', add
label define educ_lbl 125 `"Doctorate degree"', add
label define educ_lbl 999 `"Missing/Unknown"', add
label values educ educ_lbl

label define workly_lbl 00 `"NIU"'
label define workly_lbl 01 `"No"', add
label define workly_lbl 02 `"Yes"', add
label values workly workly_lbl


drop if asecflag==1

replace sex=0 if sex~=1

* 1. Employment rate
*PREPARE UNEMPLOYMENT PANEL

tostring year, replace
tostring month, generate(mo)
gen date=year+"."+mo
destring year, replace

* Remove non-working age population

drop if age>64 & ~inlist(empstat,01,10,12) | age<15 & ~inlist(empstat,01,10,12)

* To calculate the employment rate we drop all individuals who are not in the labour force

gen emprate=0

replace emprate = 1 if empstat==01 | empstat==10 | empstat ==12 

count if emprate == 1 & uhrsworkt == 999

* Unemployment by education

replace educ = 125 if educ==125 | educ==124
replace educ = 100 if educ<124 & educ>73
replace educ = 75 if 73==educ
replace educ = 50 if educ<73
decode educ, generate(edu)
replace edu = ">college" if educ==125
replace edu = "college" if educ==100
replace edu = "HS" if educ==75
replace edu = "<HS" if educ==50
drop educ
encode date, generate(t)
encode edu, generate(educ)
format t %tm
replace t=t+56*12+8


gen tele=1 if inlist(ind,2670,6090,8090,4090,8670,6080,1990,4770,7190,1070,3190,6470,6070,9480,7590,8180,1280,2770,7180,9380,2680,4585,7880,8560,3070,4370,4870,8370,1090,4560,8380,2170,7580,4265,1890,9590,7780,4890,570,6570,2270,270,4195,8080,9370,1680,1370,4795,5680,3095,9180,2070,4580,4270,7890,2290,6690,7570,490,6670,5295,3380,4080,2470,6590,3470,3690,8880,9490,5690,3670,2790,2690,6870,3960,9570,4380,6680,9190,7270,9080,8390,7070,9170,4680,3580,7870,6890,4170,3390,5590,7670,690,9160,8970,4490,2380,3780,3180,7460,7290,6970,6695,6990,7390,7280,2190,7470,7490,3365,190,370,6672,6480,7380,3370,7370,1390,4590,6780,3590,4570,6490,480,1770)

replace tele=0 if tele~=1

preserve 

collapse sex, by(occ)
* Create an index of the high covid hazard participation
sort sex

restore
preserve

* Check if dropping unidentified working hours causes to underestimate employment drop
drop if emprate==0 | (emprate==1 & ~inlist(uhrsworkt, 997, 999))
collapse (sum) agg_emp=emprate, by(t)
twoway (line agg_emp t)

restore

gen sex_group = 1
* Occupation with at least 80% male employment
replace sex_group = 2 if inlist(occ,7700,1400,8220,2920,2040,8920,1020,9141,9140,1500,9150,1007,1340,1555,1550,8025,7730,160,1545,9142,9610,1450,1310,9040,9840,8330,1750,9350,3870,8000,8720,1350,9360,7920,9760,9410,2805,600,3850,8650,3710,7610,1360,7430,2900,4930,4255,9365,7510,1530,8100,7950,7010,9750,6005,1520,8810,4252,4750,6660,8640,9260,1320,9720,1410,1510,9420,9265,300,8040,8200,5530,1106,6420,1560,9600,6410,2905,7020,1460,8500,8550,9570,3750,7900,9560,220,8555,6100,7640,4210,4251,4250,4240,9200,6600,7905,7550,6850,7030,8530,9130,8010,9030,7000,7630,7040,9240,6500,6765,7300,8630,7160,6700,8620,8465,8030,9300,8140,9210,1551,6520,7120,6400,3740,7420,7100,7925,8600,8130,6730,6300,7540,6460,7320,9310,7340,6825,8610,6950,9510,6540,7140,6260,3720,6940,7330,6115,7110,6200,6305,6710,7240,7360,6130,6840,6355,6240,6820,6360,6230,6320,9650,6440,1440,7260,7560,8940,7740,6830,6330,7150,7200,6530,7130,6750,6515,7350,9520,6210,7220,7315,7410,6250,6442,6800,7210,6220,6920,6441,2755,6740,8210,6835)
* Occupations with at lest 70% female employment
replace sex_group = 0 if inlist(occ,2300,3310,4525,3230,3640,5700,4600,3515,5740,1822,4510,5710,3270,3510,3030,3645,5730,4522,3500,3603,5400,3258,5820,2540,3255,5120,3600,4230,5140,3210,3601,5110,3424,2862,3150,2013,3140,2145,2011,2330,3610,5160,3630,4610,3648,2435,2012,5720,5860,3646,5840,4520,4150,3649,4521,5310,4830,2545,3245,2014,3602,2430,2635,5320,2010,3420,5330,8350,5360,2310,5010,5340,3421,5250,3946,5260,725,2016,5130,9050,5220,2740,5910,3430,2004,3261,5420,2002,5810,1825,2440,4350,3520,2003,8320,4160,5940,2001,135,2632,4900,1820,136,3647,640,2160,3300,3422,2000,4720,630,3423,2633,4330,2025,5100,5020,4110,8300,2555,4320,726,2550,3320,4621,5300,2861,5000,350,3620,4120,420,2006,3220,4655,2860)

label value tele
label value sex_group

preserve

collapse emprate month, by(educ t)
xtset educ t
gen detrend_educ = .
gen detrend_educ_p = .

forvalues i=1(1)4{
	reg emprate t i.month if t<tm(2019m8) & educ==`i'
	predict nocovid`i' if t>=tm(2019m8)
	replace detrend_educ = emprate - nocovid`i' if educ==`i'
	replace detrend_educ_p = (emprate - nocovid`i')/nocovid`i' if educ==`i'
}

forvalues i=1(1)4{
	xtline emprate if educ==`i', overlay i(educ) t(t) ytitle("Employment rate by educ") ttitle("Time") addplot(tsline nocovid`i' if educ==`i') name(gra`i')
	xtline detrend_educ if educ==`i', overlay i(educ) t(t) ytitle("Employment rate dev by educ") ttitle("Time") addplot(tsline detrend_educ_p if educ==`i')  name(grad`i')
}

graph combine gra1 gra2 gra3 gra4
graph export edu_emp.png

graph combine grad1 grad2 grad3 grad4
graph export edu_empD.png

* Unemployment by industry groups

restore
preserve

collapse emprate month, by(tele t)
xtset tele t

gen detrend_tele = .
gen detrend_tele_p = .

forvalues i=0(1)1{
	reg emprate t i.month if t<tm(2019m9) & tele==`i'
	predict ncovid`i' if t>=tm(2019m9)
	replace detrend_tele = emprate - ncovid`i' if tele==`i'
	replace detrend_tele_p = (emprate - ncovid`i')/ncovid`i' if tele==`i'
	}

forvalues i=0(1)1{
	xtline emprate if tele==`i', overlay i(tele) t(t) ytitle("Employment rate by industry") ttitle("Time") addplot(tsline ncovid`i' if tel==`i') name(grf`i')
	xtline detrend_tele if tele==`i', overlay i(tele) t(t) ytitle("Employment rate by industry") ttitle("Time") addplot(tsline detrend_tele_p if tel==`i') name(grfd`i')
}

graph combine grf0 grf1
graph export tele_emp.png

graph combine grfd0 grfd1
graph export tele_empD.png

* Unemployment by occupations

restore
preserve

collapse emprate month, by(sex_group t)

xtset sex_group t

gen detrend_occ = .
gen detrend_occ_p = .

forvalues i=0(1)2{
	reg emprate t i.month if t<tm(2019m9) & sex_group==`i'
	predict ncvid`i' if t>=tm(2019m9)
	replace detrend_occ = emprate - ncvid`i' if sex_group==`i' 
	replace detrend_occ_p = (emprate - ncvid`i')/ncvid`i' if sex_group==`i'
	}

forvalues i=0(1)2{
	xtline emprate if sex_group==`i', overlay i(sex_group) t(t) ytitle("Employment rate by occupations sex participation") ttitle("Time") addplot(tsline ncvid`i' if sex_group==`i') name(gf`i')
	xtline detrend_occ if sex_group==`i', overlay i(sex_group) t(t) ytitle("Employment rate by occupations sex participation") ttitle("Time") addplot(tsline detrend_occ_p if sex_group==`i') name(gfd`i')
}

graph combine gf0 gf1 gf2
graph export occ_emp.png

graph combine gfd0 gfd1 gfd2
graph export occ_empD.png

* 2. Average weekly hours

restore 
preserve

drop if uhrsworkt == 999 | uhrsworkt == 997

* AWH by education

collapse uhrsworkt month, by(educ t)

xtset educ t

gen detrend_educ_2 = .
gen detrend_educ_2_p = .

forvalues i=1(1)4{
	reg uhrsworkt t i.month if t<tm(2019m8) & educ==`i'
	predict nocovid_2`i' if t>=tm(2019m8)
	replace detrend_educ_2 = uhrsworkt - nocovid_2`i' if educ==`i'
	replace detrend_educ_2_p = (uhrsworkt - nocovid_2`i')/nocovid_2`i' if educ==`i'
}


forvalues i=1(1)4{
	xtline uhrsworkt if educ==`i', overlay i(educ) t(t) ytitle("Avg working hours by educ") ttitle("Time") addplot(tsline nocovid_2`i' if educ==`i') name(gra_2`i')
	xtline detrend_educ_2 if educ==`i', overlay i(educ) t(t) ytitle("Avg working hours deviation by educ") ttitle("Time") addplot(tsline detrend_educ_2_p if educ==`i') name(grad_2`i')
}

graph combine gra_21 gra_22 gra_23 gra_24
graph export edu_ahc.png

graph combine grad_21 grad_22 grad_23 grad_24
graph export edu_ahcD.png

* AWH by industry

restore
preserve

drop if uhrsworkt == 999 | uhrsworkt == 997

collapse uhrsworkt month, by(tele t)

xtset tel t

gen detrend_tele2 = .
gen detrend_tele2_p = .


forvalues i=0(1)1{
	reg uhrsworkt t i.month if t<tm(2019m9) & tel==`i'
	predict ncovid2`i' if t>=tm(2019m9)
	replace detrend_tele2 = uhrsworkt - ncovid2`i' if tel==`i'
	replace detrend_tele2_p = (uhrsworkt - ncovid2`i')/ncovid2`i' if tel==`i'
	}

forvalues i=0(1)1{
	xtline uhrsworkt if tel==`i', overlay i(tele) t(t) ytitle("Avg working hours by industry") ttitle("Time") addplot(tsline ncovid2`i' if tel==`i') name(grf2`i')
	xtline detrend_tele2 if tel==`i', overlay i(tele) t(t) ytitle("Avg working hours by industry") ttitle("Time") addplot(tsline detrend_tele2_p if tel==`i') name(grfd2`i')
}

graph combine grf20 grf21
graph export tele_ahc.png

graph combine grfd20 grfd21
graph export tele_ahcD.png

* AWH by occupation

restore
preserve

drop if uhrsworkt == 999 | uhrsworkt == 997

collapse uhrsworkt month, by(sex_group t)

xtset sex_group t

gen detrend_occ2 = .
gen detrend_occ2_p = .

forvalues i=0(1)2{
	reg uhrsworkt t i.month if t<tm(2019m9) & sex_group==`i'
	predict ncvid2`i' if t>=tm(2019m9)
	replace detrend_occ2 = uhrsworkt - ncvid2`i' if sex_group==`i' 
	replace detrend_occ2_p = (uhrsworkt - ncvid2`i')/ncvid2`i' if sex_group==`i'
}

forvalues i=0(1)2{
	xtline uhrsworkt if sex_group==`i', overlay i(sex_group) t(t) ytitle("Avg working hours by occupations sex participation") ttitle("Time") addplot(tsline ncvid2`i' if sex_group==`i') name(gf2`i')
	xtline detrend_occ2 if sex_group==`i', overlay i(sex_group) t(t) ytitle("Avg working hours by occupations sex participation") ttitle("Time") addplot(tsline detrend_occ2_p if sex_group==`i') name(gfd2`i')
}

graph combine gf20 gf21 gf22
graph export occ_ahc.png

graph combine gfd20 gfd21 gfd22,
graph export occ_ahcD.png

* 3. Decomposition of aggregate hours

* Predict employment and uhrsworkt
restore
preserve

drop if uhrsworkt == 997
drop if uhrsworkt == 999 & emprate~=0
replace uhrsworkt = 0 if uhrsworkt==999 & emprate == 0

gen agg = uhrsworkt*emprate

collapse (sum) agg_hours=agg (mean) emprate uhrsworkt month, by(t)

reg agg_hours i.month t if t<tm(2019m9)
predict noc_agg if t>=tm(2019m9)
gen dev_agg = (agg_hours-noc_agg)/noc_agg

reg emprate i.month t if t<tm(2019m9)
predict noc_emp if t>=tm(2019m9)
gen dev_emp = (emprate-noc_emp)/noc_emp if t>=tm(2019m9)

reg uhrsworkt i.month t if t<tm(2019m9)
predict noc_uhr if t>=tm(2019m9)
gen dev_uhr = (uhrsworkt-noc_uhr)/noc_uhr if t>=tm(2019m9)

twoway (line dev_emp t) (line dev_uhr t) (line dev_agg t)
graph export decomp_emp.png

* 4. Decomposition of wages

restore 
preserve

collapse (sum) agg_wag=earnweek (mean) earnweek emprate month, by(t)

reg agg_wag i.month t if t<tm(2019m9)
predict noc_agg if t>=tm(2019m9)
gen dev_wag = (agg_wag - noc_agg)/noc_agg

reg earnweek i.month t if t<tm(2019m9)
predict noc_wag if t>=tm(2019m9)
gen dev_inc = (earnweek-noc_wag)/noc_wag

reg emprate i.month t if t<tm(2019m9)
predict noc_emp if t>=tm(2019m9)
gen dev_emp = (emprate-noc_emp)/noc_emp

twoway (line dev_wag t) (line dev_inc t) (line dev_emp t) 
graph export decomp_wag.png

twoway (line earnweek t)
