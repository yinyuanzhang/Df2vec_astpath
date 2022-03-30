#!/usr/bin/python
# develop: yinyuanzhang
# time: 2022/3/26 3:28 下午

import dockerfile
import logging
import os
from pathGenerate.astGenerate import *


# gain_Dockerfile_address 获取每个Dockerfile的文件地址并处理
def gain_dockerfile_address(intput_dir, max_path):
    files = os.listdir(intput_dir)
    for fi in files:
        fileAddress = os.path.join(intput_dir, fi)
        if os.path.isdir(fileAddress):
            gain_dockerfile_address(fileAddress)
    else:
        dockerfile_ast, expectionTime = gain_dockerfile_ast(fileAddress, 0)
        logging.warning("parser解析过程 expectionTime为{}次".format(expectionTime))









