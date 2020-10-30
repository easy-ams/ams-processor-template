###AMS Processor Template  

#### 介绍
推理代码开发模版，需搭配[ams-engine](https://gitee.com/easy-ams/ams-engine.git )使用.提供推理服务开发标准,简化推理服务研发及工程部署过程,让研发人员专注于核心工作. 

#### 框架说明

>工程结构  

```shell script
ams-processor-template|
                    --|src -->代码:预置推理脚本,自定义脚本
                    --|bin -->自动化脚本:固定,一般不需修改
                    --|conf -->配置文件:可编辑修改
                    --|model -->模型文件:存放模型文件
                    --|lib|  -->依赖包:python包安装文件
                        --|engine  -->ams_engine安装包及其它依赖文件
```

>文件说明  

src/base_processor.py:抽象基类,定义基础方法.详见源码
```python
import six
import time
import logging as logger
from abc import ABCMeta, abstractmethod


@six.add_metaclass(ABCMeta)
class BaseProcessor(object):
    """
    推理主类，须要继承BaseProcessor，作为推理调用的主方法入口，支持文本字符串、JSON、二进制参数类型(文件、图片)

    方法介绍：
           inference: preprocess-->process->postprocess执行方法(非必须)

           preprocess:前置预处理方法 （必须）

           process:推理方法 （必须）

           postprocess:后处理方法 （必须）
    重写方式：按需选择复写上述三个方法
    """

    def __init__(self, model_path='model'):
        """
        :param model_path: 模型路径，通过default.properties配置获取，默认为相对路径model_store
        """
        self.model_path = model_path
        return

    def inference(self, data):
        """
        Wrapper function to run preprocess, process and postprocess functions.
        Parameters
        ----------
        data : map of object
            Raw input from request.

        Returns
        -------
        list of outputs to be sent back to client.
            data to be sent back
        """
        pre_start_time = time.time()
        data = self.preprocess(data)
        infer_start_time = time.time()

        # Update preprocess latency metric
        pre_time_in_ms = (infer_start_time - pre_start_time) * 1000
        logger.info('preprocess time: ' + str(pre_time_in_ms) + 'ms')

        data = self.process(data)
        infer_end_time = time.time()
        infer_in_ms = (infer_end_time - infer_start_time) * 1000

        logger.info('process time: ' + str(infer_in_ms) + 'ms')
        data = self.postprocess(data)

        # Update inference latency metric
        post_time_in_ms = (time.time() - infer_end_time) * 1000
        logger.info('postprocess time: ' + str(post_time_in_ms) + 'ms')

        logger.info('latency: ' + str(pre_time_in_ms + infer_in_ms + post_time_in_ms) + 'ms')
        return data

    @abstractmethod
    def preprocess(self, data):
        """
        前置预处理方法，返回结果作为process的输入
        """
        return data

    @abstractmethod
    def process(self, data):
        """
        推理方法，返回结果作为postprocess的输入
        """
        return data

    @abstractmethod
    def postprocess(self, data):
        """
        后处理方法
        """
        return data

```

src/customized_processor.py:base_processor的实现类,必须提供,详见源码
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging as logger
from base_processor import BaseProcessor


class Inference(BaseProcessor):
    """
    推理主类，须要继承BaseProcessor，作为推理调用的主方法入口，支持文本字符串、JSON、二进制参数类型(文件、图片)

    方法介绍：
           preprocess:前置预处理方法 （非必须）

           process:推理方法 （必须）

           postprocess:后处理方法 （非必须）
    重写方式：按需选择复写上述方法
    """
    def preprocess(self, data):

        return data

    def process(self, data):
        """
        :param data: 输入预测数据
        :return: 返回预测结果
        """
        logger.info('test')
        return data

    def postprocess(self, data):
        return data
```
src/test.py:本地测试示例
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

os.environ['PROCESSOR_PATH'] = 'D:/coding park/processor-customized/'
os.environ['default_model_path'] = 'D:/coding park/processor-customized/model'

import ams_engine.app as ams
if __name__ == '__main__':
    ams.app.run('0.0.0.0', 8088, debug=True, threaded=True)

```
conf/config.properties:基础配置,可增加自定义参数
```properties
#项目名称名称，可编辑修改
project_name=customized_processor
#模型存放目录，可自定义
default_model_path=model
#是否开启python虚拟环境
enable_virtualenv=true
```

conf/endpoint.json:接口配置,与推理脚本对应,支持多个推理脚本,提供多个服务接口  
```json
[
  {
    "processor_script_name": "customized_processor",
    "processor_class_name": "Inference"
  }
]
```

bin/setup.sh:自动配置环境脚本,一般不需修改,详细介绍见源码  

/package.sh:自动打包脚本,可自定义打包过程,目的是将工程代码文件及依赖软件打包为离线文件,可迁移部署.  

/.gitlab-ci.yml:gitlab ci配置,可自定义,如不使用可忽略  
/requirements.txt:Python依赖配置,可自定义  
```properties
numpy
tensorflow==1.13.1
```

#### 使用思路
*自行根据实际需求调整使用方式*  
1.  背景  
用户需要将模型部署到生产内网环境,对外提供推理接口.  
2.  开发  
基于此工程提供的代码模版进行二次开发,按照上述要求修改配置文件.  
3.  打包  
自动打包:如公司内部有CI工具可考虑集成使用,实现自动化打包.  
手动打包:本地开发环境下,将依赖文件下载至lib目录,然后将工程压缩打包  
4.  部署  
自动部署:如公司内部有CD工具可考虑集成使用,实现自动部署  
手动部署:将部署包拷贝至服务器进行解压,执行部署脚本  
5.  启动  
Python虚拟运行环境,需激活环境后运行启动命令  
```shell script
#激活环境
source virtualenv/bin/activate
#执行启动命令
sh ams-start.sh <工程目录绝对路径> <port> <workers> <timeout>
```
标准环境,直接执行启动命令
```shell script
#执行启动命令
sh ams-start.sh <工程目录绝对路径> <port> <workers> <timeout>
```
|6.  测试  
提供HTTP接口,支持多种数据格式  

#### 特性
1.  预置ams_engine引擎，无需开发Web部分代码，只需关注推理函数代码开发  
2.  将通用流程标准化，可变部分配置化，灵活适用多种场景  

####参考  
[gitlab CI/CD](https://zhuanlan.zhihu.com/p/159709306)  
[gitlab-ci.yml](https://docs.gitlab.com/ee/ci/yaml/includes.)  
[阿里云PAI平台](https://help.aliyun.com/document_detail/113696.html?spm=a2c4g.11186623.6.745.58006125dhhphT)  
[华为ModelArts](https://www.huaweicloud.com/product/modelarts.html)  