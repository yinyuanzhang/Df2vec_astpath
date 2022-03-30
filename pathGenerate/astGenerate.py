import logging
import dockerfile
from pathGenerate.astGenerateFromBash import *
from pathGenerate.stringGenerate import *


# VALID_DIRECTIVES 指有效的dockerfile指令   p：后面几个指令不太熟悉    p:列表类型
VALID_DIRECTIVES = [
    'From',
    'run',
    'cmd',
    'label',
    'maintainer',
    'expose',
    'env',
    'add',
    'copy',
    'entrypoint',
    'volume',
    'user',
    'workdir',
    'arg',
    'onbuild',
    'stopsignal',
    'healthcheck',
    'shell'
]




# gain_dockerfile_ast 解析获取每个Dockerfile对应的AST
def gain_dockerfile_ast(fileAddress, expectionTime):
    logging.debug('init fileAddress success')
    dockerfile_string = gain_dockerfile_string(fileAddress)
    dockerfile_ast = ""
    try:
        # 解析成常见指令型string
        dockerfile_structural_string = dockerfile.parse_string(dockerfile_string)
        logging.debug("dockerfile_structural_string 解析为%s", dockerfile_structural_string)
        # 常见指令解析
        dockerfile_ast_middle = parse_instruction(dockerfile_structural_string)
        logging.debug("dockerfile_ast_middle 解析为%s", dockerfile_ast_middle)
        # 特殊bash解析
        dockerfile_ast = parse_embedded_bash(dockerfile_ast_middle)
    except Exception as ex:
        expectionTime = expectionTime + 1
    return dockerfile_ast, expectionTime



# parse_instruction 解析Dockerfile的常用指令
def parse_instruction(dockerfile_structural_string):
    # dockerfile_ast 指定dockerfile AST 结构   p:doct类型
    dockerfile_ast = {
        'type': 'DOCKER-FILE',
        'children': []
    }

    for instruction in dockerfile_structural_string:
        logging.debug(instruction.cmd)
        logging.debug(VALID_DIRECTIVES)
        if instruction.cmd == 'FROM':
            logging.debug(instruction.cmd)
        if instruction.cmd not in VALID_DIRECTIVES:
            continue

        # 1.children 节点是list[] 加 dict{}
        if instruction.cmd == 'run':
            instructions = instruction.value[0].split("&&")
            for i in range(len(instructions)):
                dockerfile_ast['children'].append({
                    'type': 'DOCKER-RUN',
                    'children': [{
                        'type': 'MAYBE-BASH',
                        'value':instructions[i],
                        'children':[]
                    }]
                })

        # 2. cmd
        elif instruction.cmd == 'cmd':
            cmd_node = {
                'type':'DOCKER-CMD',
                'children':[]
            }

            for value in instruction.value:
                cmd_node['children'].append({
                  'type': 'DOCKER-CMD-ARG',
                  'value': value,
                  'children': []
                })

            dockerfile_ast['children'].append(cmd_node)

        # 3. expose
        elif instruction.cmd == 'expose':
            expose_node = {
                'type':'DOCKER-EXPOSE',
                'children':[]
            }

            expose_node['children'].append({
                'type': 'DOCKER-PORT',
                'value': instruction.value[0],
                'children': []
            })

            dockerfile_ast['children'].append(expose_node)

        # 4.  env
        elif instruction.cmd == 'env':
            env_node = {
                'type':'DOCKER-ENV',
                'children':[]
            }

            for name, value in zip(instruction.value[::2], instruction.value[1::2]):
                env_node['children'].append({
                    'type': 'ENV-NAME',
                    'value': name,
                    'children': []
                })

                env_node['children'].append({
                    'type': 'DOCKER-LITERAL',
                    'value': value,
                    'children': []
                })

                dockerfile_ast['children'].append(env_node)

        # 5. add
        elif instruction.cmd == 'add':
            add_node = {
                'type': 'DOCKER-ADD',
                'children': []
            }

            add_node['children'].append({
                'type': 'DOCKER-ADD-TARGET',
                'children': [{
                    'type': 'DOCKER-PATH',
                    'value': instruction.value[-1],
                    'children': []
                }]
            })

            for arg in instruction.value[:-1]:
                add_node['children'].append({
                    'type': 'DOCKER-ADD-SOURCE',
                    'children': [{
                        'type': 'DOCKER-PATH',
                        'value': arg,
                        'children': []
                    }]
                })

            dockerfile_ast['children'].append(add_node)

        # 6. copy
        elif instruction.cmd == 'copy':
            copy_node = {
                'type': 'DOCKER-COPY',
                'children': []
            }

            copy_node['children'].append({
                'type': 'DOCKER-COPY-TARGET',
                'children': [{
                    'type': 'DOCKER-PATH',
                    'value': instruction.value[-1],
                    'children': []
                }]
            })

            for arg in instruction.value[:-1]:
                if (arg != None):
                    copy_node['children'].append({
                        'type': 'DOCKER-COPY-SOURCE',
                        'children': [{
                            'type': 'DOCKER-PATH',
                            'value': arg,
                            'children': []
                        }]
                })

            dockerfile_ast['children'].append(copy_node)

        # 7. entrypoint
        elif instruction.cmd == 'entrypoint':
            first = instruction.value[0]

            entrypoint_node = {
                'type': 'DOCKER-ENTRYPOINT',
                'children': []
            }

            entrypoint_node['children'].append({
                    'type': 'DOCKER-ENTRYPOINT-EXECUTABLE',
                    'value': first,
                    'children': []
            })

            for value in instruction.value[1:]:
                entrypoint_node['children'].append({
                    'type': 'DOCKER-ENTRYPOINT-ARG',
                    'value': value,
                    'children': []
                })

            dockerfile_ast['children'].append(entrypoint_node)

        # 8. volume
        elif instruction.cmd == 'volume':
            volume_node = {
                'type': 'DOCKER-VOLUME',
                'children': []
            }

            for arg in instruction.value:
                volume_node['children'].append({
                    'type': 'DOCKER-PATH',
                    'value': arg,
                    'children': []
                })

            dockerfile_ast['children'].append(volume_node)

        # 9. user
        elif instruction.cmd == 'user':
            user_node = {
                'type': 'DOCKER-USER',
                'children': []
            }

            user_node['children'].append({
              'type': 'DOCKER-LITERAL',
              'value': instruction.value[0],
              'children': []
            })

            dockerfile_ast['children'].append(user_node)

        # 10. workdir
        elif instruction.cmd == 'workdir':
            workdir_node = {
            'type': 'DOCKER-WORKDIR',
            'children': []
            }

            workdir_node['children'].append({
                'type': 'DOCKER-PATH',
                'value': instruction.value[0],
                'children': []
            })

        # 11. arg
        elif instruction.cmd == 'arg':
          arg_node = {
            'type': 'DOCKER-ARG',
            'children': []
          }

          arg_node['children'].append({
              'type': 'DOCKER-NAME',
              'value': instruction.value[0] if '=' not in instruction.value[0] else instruction.value[0].split('=')[
                  0].strip(),
              'children': []
          })

          if '=' in instruction.value[0]:
            arg_node['children'].append({
              'type': 'DOCKER-LITERAL',
              'value': instruction.value[0].split('=')[-1].strip(),
              'children': []
            })

          dockerfile_ast['children'].append(arg_node)

        # 12. shell
        elif instruction.cmd == 'shell':
          first = instruction.value[0]

          shell_node = {
            'type': 'DOCKER-SHELL',
            'children': []
          }

          shell_node['children'].append({
              'type': 'DOCKER-SHELL-EXECUTABLE',
              'value': first,
              'children': []
             })

    return dockerfile_ast
