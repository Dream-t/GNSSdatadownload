## coding:utf-8

##   python scripts for downloading obs/nav/sp3/clk/dcb/erp/snx，需要stations.py和timeCov.py
## usage: python <pyfile> <YYYY> <MM> <DD> <type> <ndays>
##
#####################################################################################################
import os,sys,re
import calendar
from StationsList import *
from timeCov import *
import pandas as pd


# -k 不进行SSL安全检查 -n 使用_netrc中用户名和密码进行登录 --progress-bar 显示进度条 -L重定向，跟随网址自动跳转 -o 输出到指定文件
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
MGXOBS="%SSSS*.crx.gz"
GOBS="%SSSS%DDD0.%yyo.Z"
ION ="codg%DDD0.%yyi.Z"
gbmclk ="gbm%WWWW%N.clk.Z"
gbmsp3 ="gbm%WWWW%N.sp3.Z"

#   --data url ---
#mobsurl=r"ftp://igs.ign.fr/pub/igs/data/campaign/mgex/daily/rinex3/%YYYY/%DDD/"
mobsurl ="https://cddis.nasa.gov/archive/gnss/data/daily/%YYYY/%DDD/%yyd/"
gobsurl=r'https://cddis.nasa.gov/archive/gps/data/daily/%YYYY/%DDD/%yyo/'
#gobsurl=r'ftp://igs.gnsswhu.cn/pub/gps/data/daily/%YYYY/%DDD/%yyo/'

brdmurl= r"https://cddis.nasa.gov/archive/gnss/data/campaign/mgex/daily/rinex3/%YYYY/%DDD/%YYp/" #brdm
#navurl=r"ftp://gdc.cddis.eosdis.nasa.gov/gnss/data/campaign/mgex/daily/rinex3/%YYYY/%DDD/%YYp/" #brdm

sp3url=r"https://cddis.nasa.gov/archive/gnss/products/mgex/%WWWW/" #COD GFZ GRG SHA的MGEX sp3 clk ,其中COD和GFZ还提供ERP产品
clkurl=r"https://cddis.nasa.gov/archive/gnss/products/mgex/%WWWW/"
erpurl=r"https://cddis.nasa.gov/archive/gnss/products/%WWWW/" #igsyyPwwww.erp.Z 和上一个ERP没啥区别 #erpurl=r"ftp://igs.ign.fr/pub/igs/products/" #igsyyPwwww.erp.Z 一周的
dcburl=r"https://cddis.nasa.gov/archive/gnss/products/mgex/dcb/%YYYY/"  #CAS megx dcb
snxurl=r"https://cddis.nasa.gov/archive/gnss/products/%WWWW/"  #igsyyPwwww.snx.Z 一周的周解文件，weekly combiantion of IGS daily combines solutions;每个分析中心也有自己的SNX
ionurl=r"https://cddis.nasa.gov/archive/gps/products/ionex/%YYYY/%DDD/"
gbmurl =r'ftp://ftp.gfz-potsdam.de/pub/GNSS/products/mgex/%WWWW/'


def mkdir(dirpath):         #创建文件夹
    isExists = os.path.exists(dirpath)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(dirpath)
        print(dirpath + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(dirpath + ' 目录已存在')

def Download_gbm(savedir,year,mon,day,ndays):   #下载gbm的sp3和clk
    mjd = ymd2mjd(year, mon, day)
    FailedDocument = []
    obspath = savedir + '/'
    mkdir(obspath)
    while (ndays > 0):
        Y,M,D = mjd2ymd(mjd)
        gweek,dow = ymd2wkdow(Y,M,D)
        urltemp = gbmurl.replace("%WWWW", str(gweek))
        url = urltemp.replace("%N", str(dow))
        for f in [gbmclk,gbmsp3]:
            ftemp= f.replace("%WWWW", str(gweek))
            file = ftemp.replace("%N", str(dow))
            furl = url + file
            sfile = obspath + '/' + file
            cmd_exe = cmd + ' ' + sfile + ' ' + furl
            # print(cmd_exe)
            if os.path.exists(os.path.splitext(sfile)[0]):
                print("---%s exist in %s" % (file, savedir))
            else:
                print("---%s download..." % file)
                ret = os.system(cmd_exe)
                if ret != 0:
                    print("download fail %s" % file)
                    FailedDocument.append(file)
                else:
                    os.system(decompress + ' ' + sfile)
        ndays -= 1
        mjd += 1
        if (ndays <= 0):
            print(' Download failed filelist:/n')
            print(FailedDocument)

def Download_dcb(savedir,year,doy,ndays):
    dcbdir = savedir+'/'
    mkdir(dcbdir)
    yy = year-2000
    FailedDocument = []
    while (ndays > 0):
        url = dcburl.replace("%YYYY", str(year))
        file = MGXDCB.replace("%YYYY", str(year))
        file = file.replace("%DDD", "%03d" % doy)
        furl = url + file
        sfile = dcbdir + file
        cmd_exe = cmd + ' ' + sfile + ' ' + furl
        if os.path.exists(os.path.splitext(sfile)[0]):
            print("---%s exist in %s" % (os.path.splitext(file)[0], savedir))
        else:
            print("---%s download... " % file)
            ret = os.system(cmd_exe)
            if ret != 0:
                print("download fail %s" % (file))
                FailedDocument.append(file)
            else:
                os.system(decompress + ' ' + sfile)
        ndays -= 1
        doy += 1
        if doy > 365:
            if calendar.isleap(year):
                if doy == 367:
                    year += 1
                    yy += 1
                    doy = 1
            else:
                year += 1
                yy += 1
                doy = 1
        if (ndays <= 0):
            print(' Download failed filelist:')
            print(FailedDocument)


def Download_ionex(savedir, year, doy, ndays):  #下载电离层数据
    FailedDocument = []
    url = ionurl.replace("%YYYY", str(year))
    yy =year -2000
    ionex =ION.replace("%yy", str(yy))
    gbmpath = savedir + '/'
    mkdir(gbmpath)
    while (ndays > 0):
        url_doy = url.replace("%DDD", str(doy))
        file = ionex.replace("%DDD", str(doy))
        furl = url_doy + file
        sfile = gbmpath + '/'+file
        cmd_exe = cmd + ' ' + sfile + ' ' + furl
        # print(cmd_exe)
        if os.path.exists(os.path.splitext(sfile)[0]):
            print("---%s exist in %s" % (file, savedir))
        else:
            print("---%s download..." % file)
            ret = os.system(cmd_exe)
            if ret != 0:
                print("download fail %s" % file)
                FailedDocument.append(file)
            else:
                os.system(decompress + ' ' + sfile)
        ndays -= 1
        doy += 1
        if doy > 365:
            if calendar.isleap(year):
                if doy == 367:
                    year += 1
                    doy = 1
            else:
                year += 1
                doy = 1
        if (ndays <= 0):
            print(' Download failed filelist:')
            print(FailedDocument)

def Download_mobs(savedir,year,doy,ndays):          #下载多系统观测文件(crx,包含BeiDou)
    msitelist =[station.upper() for station in StationsList ]
    FailedDocument = []
    yy = year - 2000
    while (ndays > 0):
        url = mobsurl.replace("%YYYY", str(year))
        url = url.replace("%DDD", "%03d" % doy)
        url = url.replace('%yy', str(yy))
        cmd_getlist = "curl -c .urs_cookies -b .urs_cookies -n -L " +url +"*.crx.gz?list"
        ret = os.popen(cmd_getlist,'r').read()
        mobspath = savedir + '/' + str(doy)
        mkdir(mobspath)
        for site in msitelist:
            regex = site+r".*\.crx\.gz"
            partern = re.compile(regex)
            match = partern.findall(ret)
            if len(match) ==0:
                if site in msitelist:
                        msitelist.remove(site)
                print("------station %s is not exsit----" %site) 
                continue
            sname = match[0]
            furl = url +sname
            sfile = mobspath + '/' + sname
            oname = sname[0:-6]+str(yy)+'o'
            ofile = mobspath + '/' + oname
            cmd_exe = cmd + ' ' + sfile + ' ' + furl 
            if os.path.exists(ofile):
                print("---%s exist in %s" % (oname, savedir))
            else:
                print("---%s download..." % sname)
                ret1 = os.system(cmd_exe)
                ret2 = os.system(decompress + ' ' + sfile)
                if ret1 != 0 or ret2 != 0:
                    print("download fail %s" %sname)
                    if site in msitelist:
                        msitelist.remove(site)
                    FailedDocument.append(sname)
                else:
                    # 格式转换
                    new_file0=sname[0:-3]
                    new_file=sname[0:-6]+str(year-2000)+'d'
                    if os.path.exists(mobspath + '/' + new_file):
                        os.remove(sfile)
                    else:
                        os.rename(mobspath + '/' + new_file0,mobspath + '/' + new_file)
                    crx2rnx_cmd = 'crx2rnx '+mobspath + '/' +new_file
                    print("%s......."%crx2rnx_cmd)
                    os.system(crx2rnx_cmd)
                    os.remove(mobspath + '/' +new_file)
        ndays -= 1
        if (ndays <= 0):
            sitelist =[station.upper() for station in msitelist ]
            Qualist = pd.DataFrame(sitelist, index=None)
            Qualist.to_csv('MgexQualifiedStationList.csv')
            print(' MgexQualifiedStationList.csv has saved! ')
            print(' Download failed filelist: ')
            print(FailedDocument)
        doy += 1
        if doy > 365:
            if calendar.isleap(year):
                if doy == 367:
                    year += 1
                    doy = 1
            else:
                year += 1
                doy = 1

def Download_gobs(savedir,year,doy,ndays):          #观测文件下载GREJ
    gsitelist = StationsList
    sitelist1 = []
    for site in gsitelist:
        temp = GOBS.replace('%SSSS', site.lower())
        sitelist1.append(temp)
    # print(sitelist1)
    FailedDocument = []
    while (ndays > 0):
        yy = year - 2000
        url = gobsurl.replace("%YYYY", str(year))
        url = url.replace("%yy", str(yy))
        url = url.replace("%DDD", str(doy))
        obspath = savedir + '/' + str(doy)
        mkdir(obspath)
        for site in sitelist1:
            # file = site.replace("%YYYY", str(year))
            file = site.replace("%DDD", str(doy))
            file = file.replace('%yy', str(yy))
            furl = url + file
            sfile = obspath + '/' + file
            cmd_exe = cmd + ' ' + sfile + ' ' + furl
            if os.path.exists(os.path.splitext(sfile)[0]):
                print("---%s exist in %s" % (file, savedir))
            else:
                print("---%s download..." % file)
                retDownload = os.system(cmd_exe)
                retDecompress = os.system(decompress + ' ' + sfile)
                if retDecompress != 0 or retDownload != 0:
                    print("download fail %s" % file)
                    if  os.path.exists(os.path.splitext(sfile)[0]):
                        os.remove(sfile)
                    regex = r"[a-z]{2}[a-z\d]{2}"
                    FailedSite = re.match(regex,file).group(0)
                    if FailedSite in gsitelist:
                        gsitelist.remove(FailedSite)
                    
        ndays -= 1

        doy += 1
        if doy > 365:
            if calendar.isleap(year):
                if doy == 367:
                    year += 1
                    doy = 1
            else:
                year += 1
                doy = 1
        if (ndays <= 0):
            Qualist = pd.DataFrame(gsitelist,index=None)
            Qualist.to_csv('QualifiedStationList.csv')
            print(' QualifiedStationList.csv has saved! ')
            print(' Download failed filelist: ')
            print(FailedDocument)

def Download_brdm(savedir,year,doy,ndays):              #下载多系统广播文件
    yy = year-2000
    FailedDocument = []
    while (ndays > 0):
        url = brdmurl.replace("%YYYY", str(year))
        url = url.replace("%DDD", "%03d" % doy)
        url = url.replace("%YY", "%02d" % yy)
        file = MGXNAV.replace("%DDD", "%03d" % doy)
        file = file.replace("%YY", "%02d" % yy)
        furl = url + file
        sfile = savedir + '/'+file
        cmd_exe = cmd + ' ' + sfile + ' ' + furl
        # print(cmd_exe)
        if os.path.exists(os.path.splitext(sfile)[0]):
            print("---%s exist in %s" % (file, savedir))
        else:
            print("---%s download... " % file)
            ret = os.system(cmd_exe)
            if ret != 0:
                print("download fail %s" % (file))
                FailedDocument.append(file)
            else:
                os.system(decompress + ' ' + sfile)
        ndays -= 1
        doy += 1
        if doy > 365:
            if calendar.isleap(year):
                if doy == 367:
                    year += 1
                    yy += 1
                    doy = 1
            else:
                year += 1
                yy += 1
                doy = 1
        if (ndays <= 0):
            print(' Download failed filelist:/n')
            print(FailedDocument)

def NavSelecet(ac):
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
    return acsp3,acclk

def main():
    if len(sys.argv)<6:
        print("usage: python <pyfile> <YYYY> <MM> <DD> <type> <ndays>")
        sys.exit()
    year=int(sys.argv[1]);mon=int(sys.argv[2]);day=int(sys.argv[3])
    type=sys.argv[4];     ndays=int(sys.argv[5])
    # year = 2020;
    # mon = 4;
    # day = 30
    # type = 'nav';
    # ndays = 1
    #
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
    savedir = input('Please input the savepath:')+'/'
# COD GFZ GRG IAC JAX SHA WUM

    
    for case in switch(type.lower()):
        if case('mobs'):
            Download_mobs(savedir, year, doy, ndays)
            break
        if case('gobs'):
            Download_gobs(savedir, year, doy, ndays)
            break
        if case('brdm'):
            Download_brdm(savedir, year, doy, ndays)
            break
        if case('ion'):
            Download_ionex(savedir, year, doy, ndays)
            break
        if case('gbm'):
            Download_gbm(savedir,year,mon,day,ndays)
            break
        if case('dcb'):
            Download_dcb(savedir, year, doy, ndays);
            break
        if case('sp3'):
            ac = input("Input the sp3 data source(SHA WUM JAX COD GFZ GRG IAC):")
            acsp3,acclk= NavSelecet(ac)
            FailedDocument = []
            sp3dir = savedir + '/'
            mkdir(sp3dir)
            yy = year - 2000
            while(ndays>0):
                url= sp3url.replace("%WWWW",str(week))
                file=acsp3.replace("%YYYY",str(year))
                file=file.replace("%DDD","%03d"%doy)
                furl=url+file
                sfile=sp3dir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                #print(cmd_exe)
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print("---%s  exist in %s"%(os.path.splitext(file)[0],savedir))
                else:
                    print("---%s download... "%file)
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                        FailedDocument.append(file)
                    else:
                        os.system(decompress+' '+sfile)
                ndays-=1
                if (ndays <= 0):
                    print(' Download failed filelist: ')
                    print(FailedDocument)
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
            ac = input("Input the CLK data source(SHA WUM JAX COD GFZ GRG IAC):")
            acsp3,acclk = NavSelecet(ac)
            FailedDocument = []
            clkdir = savedir + '/'
            mkdir(clkdir)
            yy = year - 2000
            while(ndays>0):
                url=clkurl.replace("%WWWW",str(week))
                file=acclk.replace("%YYYY",str(year))
                file=file.replace("%DDD","%03d"%doy)
                furl=url+file
                sfile=clkdir+file
                cmd_exe=cmd+' '+sfile+' '+furl
                #print(cmd_exe)
                if os.path.exists(os.path.splitext(sfile)[0]):
                    print("---%s  exist in %s"%(os.path.splitext(file)[0],savedir))
                else:
                    print("---%s download... "%file)
                    ret=os.system(cmd_exe)
                    if ret !=0:
                        print("download fail %s"%(file))
                        FailedDocument.append(file)
                    else:
                        os.system(decompress+' '+sfile)

                ndays-=1
                if (ndays <= 0):
                    print(' Download failed filelist:/n')
                    print(FailedDocument)
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


 
if __name__ == '__main__':
    main()