#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

os.environ['PROCESSOR_PATH'] = 'D:/coding park/processor-customized/'
os.environ['default_model_path'] = 'D:/coding park/processor-customized/model'

import ams_engine.app as ams
if __name__ == '__main__':
    ams.app.run('0.0.0.0', 8088, debug=True, threaded=True)
