#!/usr/bin/python
# develop: yinyuanzhang
# time: 2022/3/30 11:00 上午


# 将Dockerfile文件转化成String类型
def gain_dockerfile_string(fileAddress):
    file_inside = open(fileAddress, encoding='gb18030', errors='ignore')
    dockerfile_string = ''
    for line in file_inside:
        dockerfile_string += line
    return dockerfile_string