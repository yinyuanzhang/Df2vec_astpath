#!/usr/bin/python
# develop: yinyuanzhang
# time: 2022/3/26 4:10 下午
import logging


# init_logging 自定义项目日志
def init_logging():
    log_format = '%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)

# %(levelname)s ，日志等级
# %(asctime)s ，时间
# %(filename)s ，文件名
# %(lineno)d ，行号
# %(message)s，日志信息
# python日志配置 https://github.com/HuiDBK/LogSetupDemo