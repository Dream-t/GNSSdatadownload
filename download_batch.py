##!/usr/bin/env python
## coding:utf-8

##   python scripts for downloading obs/nav/sp3/clk/dcb/erp/snx，需要stations.py和timeCov.py
##   (MGEX)观测值文件下载MGEX观测网的测站(RINEX3),部分测站信息见stations.py，后期可进行扩展，在当前文件的sitelist设置要下载的测站
##   (MGEX)精密轨道和钟差，可以下载COD GFZ GRG IAC JAX SHA WUM，WUM可能部分时间只有SP3
##   (MGEX)导航星历，下载MGEX的混合星历
##   (MGEX)DCB文件下载是MGEX混合DCB
##   (IGS)erp和snx下载的是IGS（组合多个分析中心），默认一周下一个文件
## usage: python <pyfile> <YYYY> <MM> <DDD> <type> <AC> <ndays>
##  
##  written by tmx 2020/11/15 23:15
#####################################################################################################
import os,sys
import calendar
from stations import *
from timeCov import *

# 下载文件保存路径
savedir="E:\\Chromedownload\\GREAT-UPD_1.0\\util\\downloaddata\\"

# -k 不进行SSL安全检查 -n 使用.netrc中用户名和密码进行登录 --progress-bar 显示进度条 -L重定向，跟随网址自动跳转 -o 输出到指定文件
cmd=r"curl -k  -n -c cookiefile  --progress-bar -L  -o "  
# 解压文件
decompress="gzip -d "

#   ---file format---- 
MGXNAV="brdm%DDD0.%YYp.Z"
CODSP3="COD0MGXFIN_%YYYY%DDD0000_01D_05M_ORB.SP3.gz"
CODCLK="COD0MGXFIN_%YYYY%DDD0000_01D_30S_CLK.CLK.gz"

GFZSP3="GFZ0MGXRAP_%YYYY%DDD0000_01D_05M_ORB.SP3.gz"
GFZCLK="GFZ0MGXRAP_%YYYY%DDD0000_01D_30S_CLK.CLK.gz"

GRGSP3="GRG0MGXFIN_%YYYY%DDD0000_01D_15M_ORB.SP3.gz"
GRGCLK="GRG0MGXFIN_%YYYY%DDD0000_01D_30S_CLK.CLK.gz"

IACSP3="IAC0MGXFIN_%YYYY%DDD0000_01D_05M_ORB.SP3.gz"
IACCLK="IAC0MGXFIN_%YYYY%DDD0000_01D_30S_CLK.CLK.gz"

JAXSP3="JAX0MGXFIN_%YYYY%DDD0000_01D_05M_ORB.SP3.gz"
JAXCLK="JAX0MGXFIN_%YYYY%DDD0000_01D_30S_CLK.CLK.gz"

SHASP3="SHA0MGXRAP_%YYYY%DDD0000_01D_05M_ORB.SP3.gz"
SHACLK="SHA0MGXRAP_%YYYY%DDD0000_01D_05M_CLK.CLK.gz"

WUMSP3="WUM0MGXFIN_%YYYY%DDD0000_01D_15M_ORB.SP3.gz"
WUMCLK="WUM0MGXFIN_%YYYY%DDD0000_01D_30S_CLK.CLK.gz"

IGSERP="igs%YYP%WWWW.erp.Z"
IGSSNX="igs%YYP%WWWW.snx.Z"

MGXDCB="CAS0MGXRAP_%YYYY%DDD0000_01D_01D_DCB.BSX.gz"
MGXOBS="%SSSS00%CCC_R_%YYYY%DDD0000_01D_30S_MO.crx.gz"

#   --data url ---
obsurl=r"ftp://igs.ign.fr/pub/igs/data/campaign/mgex/daily/rinex3/%YYYY/%DDD/"
navurl=r"https://cddis.nasa.gov/archive/gnss/data/campaign/mgex/daily/rinex3/%YYYY/%DDD/%YYp/" #brdm
sp3url=r"https://cddis.nasa.gov/archive/gnss/products/mgex/%WWWW/" #COD GFZ GRG SHA的MGEX sp3 clk ,其中COD和GFZ还提供ERP产品
clkurl=r"https://cddis.nasa.gov/archive/gnss/products/mgex/%WWWW/"
erpurl=r"https://cddis.nasa.gov/archive/gnss/products/%WWWW/" #igsyyPwwww.erp.Z 和上一个ERP没啥区别 #erpurl=r"ftp://igs.ign.fr/pub/igs/products/" #igsyyPwwww.erp.Z 一周的
dcburl=r"https://cddis.nasa.gov/archive/gnss/products/mgex/dcb/%YYYY/"  #CAS megx dcb
snxurl=r"https://cddis.nasa.gov/archive/gnss/products/%WWWW/"  #igsyyPwwww.snx.Z 一周的周解文件，weekly combiantion of IGS daily combines solutions;每个分析中心也有自己的SNX

sitelist=['ABMF','CUT0','JFNG']
sitelist1=[]


def main():
    if len(sys.argv)<7:
        print("usage: python <pyfile> <YYYY> <MM> <DDD> <type> <AC> <ndays>")
        sys.exit()
    year=int(sys.argv[1]);mon=int(sys.argv[2]);day=int(sys.argv[3])
    type=sys.argv[4];      ac=sys.argv[5];   ndays=int(sys.argv[6])
    
#   start time
    mjd=ymd2mjd(year,mon,day)
    y,doy=mjd2ydoy(mjd)
    week,dow=ymd2wkdow(year,mon,day)
    yy=year-2000
#   end   time
    mjd_end=mjd+ndays-1
    Y,M,D=mjd2ymd(mjd_end)
    Y1,doy_end=mjd2ydoy(mjd_end)
    week_end,dow_end=ymd2wkdow(Y,M,D)
    
    print('---start time: year:%s mon:%02d day:%02d doy:%03d week:%s dow:%s'%(year,mon,day,doy,week,dow))
    print('---end   time: year:%s mon:%02d day:%02d doy:%03d week:%s dow:%s'%(Y,M,D,doy_end,week_end,dow_end))

# COD GFZ GRG IAC JAX SHA WUM
    for case in switch(ac.upper()):
        if case('COD'):
            acsp3=CODSP3
            acclk=CODCLK
            break
        if case('GFZ'):
            acsp3=GFZSP3
            acclk=GFZCLK
            break
        if case('GRG'):
            acsp3=GRGSP3
            acclk=GRGCLK
            break
        if case('IAC'):
            acsp3=IACSP3
            acclk=IACCLK
            break
        if case('JAX'):
            acsp3=JAXSP3
            acclk=JAXCLK
            break
        if case('SHA'):
            acsp3=SHASP3
            acclk=SHACLK
            break
        if case('WUM'):
            acsp3=WUMSP3
            acclk=WUMCLK
            break
    
    for case in switch(type.lower()):
        if case('obs'):
            for site in sitelist:
                temp=MGXOBS.replace('%SSSS',site)
                temp=temp.replace('%CCC',dict_stations[site][2])
                sitelist1.append(temp)
            print(sitelist1)
            while(ndays>0):
                url=obsurl.replace("%YYYY",str(year))
                url=url.replace("%DDD","%03d"%doy)
                for site in sitelist1:
                    file=site.replace("%YYYY",str(year))
                    file=file.replace("%DDD","%03d"%doy)
                    furl=url+file
                    sfile=savedir+file
                    cmd_exe=cmd+' '+sfile+' '+furl
                    print(cmd_exe)
                    if os.path.exists(os.path.splitext(sfile)[0]):
                        print("---%s exist in %s"%(file,savedir))
                    else:
                        print("---%s download..."%file)
                        ret=os.system(cmd_exe)
                        if ret!=0:
                            print("download fail %s"%file)
                        else:
                            os.system(decompress+' '+sfile)
                ndays-=1
                doy+=1
                if doy>365:
                    if calendar.isleap(year):
                        if doy==367:
                            year+=1
                            doy=1
                    else:
                        year+=1
                        doy=1
            break
        if case('nav'):
            while (ndays>0):
                url=navurl.replace("%YYYY",str(year))
                url=url.replace("%DDD","%03d"%doy)
                url=url.replace("%YY","%02d"%yy)
                file=MGXNAV.replace("%DDD","%03d"%doy)
                file=file.replace("%YY","%02d"%yy)
                furl=url+file
                sfile=savedir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                #print(cmd_exe)
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print("---%s exist in %s"%(file,savedir))
                else:
                    print("---%s download... "%file)
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                    else:
                        os.system(decompress+' '+sfile)           
                ndays-=1
                doy+=1
                if doy>365:
                    if calendar.isleap(year):
                        if doy==367:
                            year+=1
                            yy+=1
                            doy=1
                    else:
                        year+=1
                        yy+=1
                        doy=1
            break
        if case('sp3'):
            while(ndays>0):
                url=sp3url.replace("%WWWW",str(week))
                file=acsp3.replace("%YYYY",str(year))
                file=file.replace("%DDD","%03d"%doy)
                furl=url+file
                sfile=savedir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                #print(cmd_exe)
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print("---%s  exist in %s"%(os.path.splitext(file)[0],savedir))
                else:
                    print("---%s download... "%file)
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                    else:
                        os.system(decompress+' '+sfile)

                ndays-=1
                dow+=1
                if dow>6:
                    week+=1
                    dow=0
                doy+=1
                if doy>365:
                    if calendar.isleap(year):
                        if doy==367:
                            year+=1
                            doy=1
                    else:
                        year+=1
                        doy=1
                
            break
        if case('clk'):
            while(ndays>0):
                url=clkurl.replace("%WWWW",str(week))
                file=acclk.replace("%YYYY",str(year))
                file=file.replace("%DDD","%03d"%doy)
                furl=url+file
                sfile=savedir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                #print(cmd_exe)
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print("---%s  exist in %s"%(os.path.splitext(file)[0],savedir))
                else:
                    print("---%s download... "%file)
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                    else:
                        os.system(decompress+' '+sfile)

                ndays-=1
                dow+=1
                if dow>6:
                    week+=1
                    dow=0
                doy+=1
                if doy>365:
                    if calendar.isleap(year): #闰年
                        if doy==367:
                            year+=1
                            doy=1
                    else: #非闰年
                        year+=1
                        doy=1
            break
        if case('erp'):
            while(ndays>0):
                url=erpurl.replace("%WWWW",str(week))
                file=IGSERP.replace("%YY","%02d"%yy)
                file=file.replace("%WWWW",str(week))
                furl=url+file
                sfile=savedir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print('---%s exist in %s'%(os.path.splitext(sfile)[0],savedir))
                else:
                    print('---%s download...'%(file))
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                    else:
                        os.system(decompress+' '+sfile)
                while((6-dow)>=0):
                    ndays-=1
                    dow+=1
                    doy+=1
                    if doy>365:
                        if calendar.isleap(year):
                            if doy==367:
                                year+=1
                                yy+=1
                                doy=1
                                
                        else:
                            year+=1
                            yy+=1
                            doy=1
                dow=0
                week+=1


            break
        if case('snx'):
            while(ndays>0):
                url=snxurl.replace("%WWWW",str(week))
                file=IGSSNX.replace("%YY","%02d"%yy)
                file=file.replace("%WWWW",str(week))
                furl=url+file
                sfile=savedir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print('---%s exist in %s'%(os.path.splitext(sfile)[0]),savedir)
                else:
                    print('---%s download...'%(file))
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                    else:
                        os.system(decompress+' '+sfile)
                while((6-dow)>=0):
                    ndays-=1
                    dow+=1
                    doy+=1
                    if doy>365:
                        if calendar.isleap(year):
                            if doy==367:
                                year+=1
                                yy+=1
                                doy=1                              
                        else:
                            year+=1
                            yy+=1
                            doy=1
                dow=0
                week+=1
            break
        if case('dcb'):
            while(ndays>0):
                url=dcburl.replace("%YYYY",str(year))
                file=MGXDCB.replace("%YYYY",str(year))
                file=file.replace("%DDD","%03d"%doy)
                furl=url+file
                sfile=savedir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print("---%s exist in %s"%(os.path.splitext(file)[0],savedir))
                else:
                    print("---%s download... "%file)
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                    else:
                        os.system(decompress+' '+sfile)
                ndays-=1
                doy+=1
                if doy>365:
                    if calendar.isleap(year):
                        if doy==367:
                            year+=1
                            yy+=1
                            doy=1
                    else:
                        year+=1
                        yy+=1
                        doy=1
            break



 
if __name__ == '__main__':
    main()