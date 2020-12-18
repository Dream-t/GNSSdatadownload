
## function for time convert and class switch
##
##
## verification by http://www.gnsscalendar.com/index.html?year=2019
## written by tmx 2020/11/17 10:01
##############################################
##-------------------------------------------
## 年月日转为约化儒略日，没有考虑小时和分钟
##
## input:
##      year    4-digit        
##      mon     2-digit
##      day     2-digit
##
## return:
##      mjd     (int)
## ref:
#       李征航.GPS测量数据处理 P29 公式2    
##--------------------------------------------
def ymd2mjd(year,mon,day):
    if mon<=2:
        mon=mon+12
        year=year-1
    mjd=int(365.25*year)+int(30.6001*(mon+1))+day+1720981.5-2400000.5
    return int(mjd)

##-------------------------------------------
## 年月日转为GPS周和周内天，没有考虑小时和分钟
##
## input:
##      year    4-digit        
##      mon     2-digit
##      day     2-digit
##
## return:
##      week     (int)
##      dow      (int)
## ref:
#       none     
##--------------------------------------------
def ymd2wkdow(year,mon,day):
    GPS_year=1980
    GPS_mon=1
    GPS_day=6
    GPS_mjd=ymd2mjd(GPS_year,GPS_mon,GPS_day)
    cur_mjd=ymd2mjd(year,mon,day)
    dmjd=cur_mjd-GPS_mjd
    week=int(dmjd/7)
    dow=dmjd%7
    return week,dow

##-------------------------------------------
## 约化儒略日转换为年、年积日，没有考虑小时和分钟
##
## input:
##      mjd      (int)        

##
## return:
##      year     (int)
##      doy      (int)
## ref:
#       李征航.GPS测量数据处理 P29     
##--------------------------------------------
def mjd2ydoy(mjd):
    jd=mjd+2400000.5
    a=int(jd+0.5)
    b=a+1537
    c=int((b-122.1)/365.25)
    d=int(365.25*c)
    e=int((b-d)/30.600)
    M=e-1-12*int(e/14)
    Y=c-4715-int((7+M)/10)
    mjd0=ymd2mjd(Y,1,1)
    doy=mjd-mjd0+1
    return Y,doy

##-------------------------------------------
## 约化儒略日转换为年、月、日，没有考虑小时和分钟
##
## input:
##      mjd      (int)        

##
## return:
##      year     (int)
##      mon      (int)
##      day      (int)
## ref:
#       李征航.GPS测量数据处理 P29     
##--------------------------------------------
def mjd2ymd(mjd):
    jd=mjd+2400000.5
    a=int(jd+0.5)
    b=a+1537
    c=int((b-122.1)/365.25)
    d=int(365.25*c)
    e=int((b-d)/30.600)
    D=b-d-int(30.6001*e)+0
    M=e-1-12*int(e/14)
    Y=c-4715-int((7+M)/10)
    
    return Y,M,D


# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False