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