#!/bin/sh
echo "-----------配置开始--------------"
cat /proc/version
python3 --version
pip3 --version
if [ $? -ne 0 ];then
  echo -e "未检测到python3/pip3指令，请检环境配置"
  exit 201
fi
#获取工作目录
WORK_DIR=$1
if [ ! -n "${WORK_DIR}" ];then
  echo "缺少参数WORK_DIR，请输入程序根目录，例如:/home/workspace"
  exit 1
fi
echo "获取程序根目录：${WORK_DIR}"
source ${WORK_DIR}/conf/config.properties
user=`whoami`
echo "当前用户：${user}"
echo "安装依赖包"
#判断并安装Python虚拟运行环境
if [ ${enable_virtualenv} == "true" ];then
  echo "配置python虚拟运行环境:${WORK_DIR}/virtualenv"
  pip3 install --no-index --find-links=${WORK_DIR}/lib/engine virtualenv && \
  mkdir -p ${WORK_DIR}/virtualenv && \
  virtualenv ${WORK_DIR}/virtualenv && \
  source ${WORK_DIR}/virtualenv/bin/activate
fi
if [ $? -ne 0 ];then
  echo -e "虚拟运行环境配置失败，请检查python运行环境是否配置正确!"
  exit 203
fi
#如上述配置了虚拟运行环境，则后续安装运行在虚拟环境中
pip3 install --no-index --find-links=${WORK_DIR}/lib/ -r ${WORK_DIR}/requirements.txt
pip3 install --no-index --find-links=${WORK_DIR}/lib/engine/ ams_engine
if [ $? -ne 0 ];then
  echo -e "依赖包安装失败!"
  exit 204
fi
echo "-----------配置结束--------------"
exit 0