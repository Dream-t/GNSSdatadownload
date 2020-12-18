

# python脚本实现GNSS数据自动下载

本文代码思路参考了博文[https://blog.csdn.net/weixin_39672353/article/details/109852755] 在此基础上做了些优化

# 文章目录

- ##### 脚本功能介绍

- ##### 使用前的准备

- ##### 脚本的使用方法

- ##### 总结

# 功能简介

   GNSS数据的下载工作繁琐重复，本文通过python实现了数据的自动下载，可以支持MGEX观测文件（.crx 和.o文件）、广播星历（brdm），精密轨道与钟差（.sp3,.clk）、电离层数据（.i文件）、DCB。所有类型文件均可自动解压，其中.crx文件将自动转换为o文件，自动按年积日进行分类存放。由于CDDIS分析中心从2020年10月31日不再支持匿名的FTP下载，目前的数据下载只能通过HTTPS or ftp-ssl，并需要事先注册EARTHDATA的账号。

开发环境python 3（除了pandas,其他均为python自带标准库，使用前需要提前安装pandas），通过curl方式下载，需要提前配置好，下文中给出了配置方法。

# 1.使用前的准备

------

- ## python环境的搭建：

​	可以直接到官网下载python安装包，不过更推荐直接安装Anaconda，Anaconda指的是一个开源的Python发行版本，其包含了conda、Python等180多个科学包及其依赖项。 因为包含了大量的科学包，Anaconda 的下载文件比较大（约 531 MB），如果只需要某些包，或者需要节省带宽或存储空间，也可以使用Miniconda这个较小的发行版（仅包含conda和 Python）。

​	建议通过清华镜像站下载，速度较快，镜像站地址:https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/。Anaconda 安装教程可以参考博文：[(1条消息) Anaconda 的安装教程（图文）_艺术艺术的博客-CSDN博客_anaconda安装教程](https://blog.csdn.net/weixin_43715458/article/details/100096496) 安装时建议添加环境变量，如下图所示，由于本脚本使用了pandas库，需要自行安装，python环境安装完成后，可以直接在命令行中使用以下命令安装（安装时添加了环境变量才可这样使用）

```
pip install pandas
```

​	![第五步2](https://img-blog.csdnimg.cn/20190827094614915.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcxNTQ1OA==,size_16,color_FFFFFF,t_70)

- ## curl的下载和配置：

  ​	关于curl以及如何使用curl下载CDDIS的数据可以参考以下两篇文章，讲的非常详细：

  1. [CURL版IGS-CDDIS下载GNSS数据-山东大学空间科学研究院卫星导航与遥感研究中心](https://navrs.wh.sdu.edu.cn/info/1621/1487.htm)
  2. CDDIS官方的[CDDIS | | About | CDDIS File Download Documentation](https://cddis.nasa.gov/About/CDDIS_File_Download_Documentation.html)

# 2.脚本的使用

------

一共有三个python脚本，main.py、StationList.py和timeCov.py，main.py调用其他两个，station.py储存测站列表，可以在其中输入自己需要下载的站点名称，一列表格式存放，用于下载观测值文件，timeCov.py包含一些时间转换函数。QualifiedStaiontlist为gobs下载命令时的输出文件，MgexQualifiedStaiontlist为mobs命令下的输出文件，输出的站点为指定的日期范围内所有历元数据都成功下载的站点列表。除了python脚本时，还有两个exe文件，gzip用于文件解压，crx2rnx用于将.crx文件转换为.yyo文件。

![image-20201218095817123](C:%5CUsers%5Chyisoe%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201218095817123.png)

- #### 脚本通过命令行启动，使用方法如下：

```python
python [pyfile] [YYYY] [MM] [DD] [type]  [ndays]
pyfile: python file name(main.py)
YYYY：  4-digit year
MM:     2-digit month
DD:     2-digit day of month
type:   gobs/mobs/gbm/nav/ion/sp3/clk/dcb/
ndays:  number of days
```



- #### 下表给出了各个type命令的下载的文件类型：

| type |                             含义                             |
| :--: | :----------------------------------------------------------: |
| gobs |           观测文件（gps/data/daily/year/doyyyo/）            |
| mobs |         多系统观测文件（mgex/daily/rinex3/year/doy/)         |
| ion  | COD i文件 电离层数据（"https://cddis.nasa.gov/archive/gps/products/ionex/year/doy/"） |
| gbm  | GFZ机构的精密卫星轨道和钟差改正，包含.clk和.sp3文件        [ftp://ftp.gfz-potsdam.de/pub/GNSS/products/mgex/gpsweek/](ftp://ftp.gfz-potsdam.de/pub/GNSS/products/mgex/) |
| dcb  | CAS的DCB产品https://cddis.nasa.gov/archive/gnss/products/mgex/dcb/year/ |
| brdm |                    多系统广播星历，p文件                     |
| sp3  | SP3文件，需要输入第二参数，可选择产品机构（COD GFZ GRG IAC JAX SHA WUM） |
| clk  | CLK文件，需要输入第二参数，可选择产品机构（COD GFZ GRG IAC JAX SHA WUM） |

- ####  脚本使用示例：需要输入路径，若目标文件夹不存在会自动创建一个同名文件夹，观测值文件会自动创建文件夹并按doy命名存放

![](C:%5CUsers%5Chyisoe%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201215231734215.png)

<img src="C:%5CUsers%5Chyisoe%5CAppData%5CRoaming%5CTypora%5Ctypora-user-images%5Cimage-20201211134309723.png" alt="image-20201211134309723" style="zoom: 80%;" />



# 3.总结

   该python脚本实现了自动下载GNSS数据，可以自动下载GNSS obs/sp3/clk/brdm/dcb/ion数据，并且扩展起来也十分方便，同时解压分类文件转换等功能也能自动完成，避免了很多重复性的工作。





参考文档：

------

- https://blog.csdn.net/weixin_43715458/article/details/100096496

- https://navrs.wh.sdu.edu.cn/info/1621/1487.html
- https://cddis.nasa.gov/About/CDDIS_File_Download_Documentation.html
- https://blog.csdn.net/weixin_39672353/article/details/109852755

