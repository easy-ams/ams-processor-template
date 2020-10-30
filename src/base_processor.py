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
