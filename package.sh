#!/bin/bash
# CreateBy:CodeHerry

#可根据实际环境修改如下命令
#环境变量
source conf/config.properties
#下载离线包至lib文件夹
pip3 download -r requirements.txt -d ./lib
#将工程打包压缩生成tar.gz文件存放在当前工程根目录下
tar -zcvf ${project_name}.tar.gz *