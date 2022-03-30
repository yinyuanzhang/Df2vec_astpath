#!/usr/bin/python
# develop: yinyuanzhang
# time: 2022/3/30 9:59 上午





# parse_embedded_bash 解析Dockerfile的特殊的bash指令
def parse_embedded_bash(dockerfile_phase1):
    if dockerfile_phase1['type'] == 'MAYBE-BASH':
        return parse_within1(dockerfile_phase1)
    new_children = []
    for child in dockerfile_phase1['children']:
        new_children.append(parse_embedded_bash(child))
    dockerfile_phase1['children'] = new_children
    return dockerfile_phase1


# parse_within1 针对UNKNOWN指令执行具体解析
def parse_within1(bash_str):
    str_tokens = list(filter(not_empty,bash_str['value'].split(' ')))
    if "adduser" in str_tokens:  #1
        parsed = adduser_parser(str_tokens)
    elif "apk" in str_tokens and "update" in str_tokens:
        parsed = apk_update_parser(str_tokens)
    elif "apk" in str_tokens and "add" in str_tokens:
        parsed = apk_add_parser(str_tokens)
    elif "apt-add-repository" in str_tokens:
        parsed = aptaddrepository_parser(str_tokens)
    elif "apt-get" in str_tokens and "update" in str_tokens:
        parsed = apt_get_update_parser(str_tokens)
    elif "apt-get" in str_tokens and "install" in str_tokens:
        parsed = apt_get_install_parser(str_tokens)
    elif "apt-key" in str_tokens and "add" in str_tokens:
        parsed = apt_key_add_parser(str_tokens)
    elif "apt-key" in str_tokens and "del" in str_tokens:
        parsed = apt_key_del_parser(str_tokens)
    elif "apt-key" in str_tokens and "update" in str_tokens:
        parsed = apt_key_update_parser(str_tokens)
    elif "apt" in str_tokens and "update" in str_tokens:
        parsed = apt_update_parser(str_tokens)
    elif "apt" in str_tokens and "install" in str_tokens:
        parsed = apt_install_parser(str_tokens)
    elif "bash" in str_tokens:
        parsed = bash_parser(str_tokens)
    elif "cd" in str_tokens:
        parsed = cd_parser(str_tokens)
    elif "chmod" in str_tokens:
        parsed = chmod_parser(str_tokens)
    elif "chown" in str_tokens:
        parsed = chown_parser(str_tokens)
    elif "cmake" in str_tokens:
        parsed = cmake_parser(str_tokens)
    elif "'./configure'" in str_tokens:
        parsed = configure_parser(str_tokens)
    elif "cp" in str_tokens:
        parsed = cp_parser(str_tokens)
    elif "curl" in str_tokens:
        parsed = curl_parser(str_tokens)
    elif "dnf" in str_tokens and "update" in str_tokens:
        parsed = apk_add_parser(str_tokens)
    elif "dnf" in str_tokens and "install" in str_tokens:
        parsed = apk_update_parser(str_tokens)
    elif "docker-php-ext-install" in str_tokens:
        parsed = docker_php_ext_install_parser(str_tokens)
    elif "dpkg-architecture" in str_tokens:
        parsed = dpkg_architecture(str_tokens)
    elif "dpkg" in str_tokens:
        parsed = dpkg(str_tokens)
    elif "echo" in str_tokens:
        parsed = echo(str_tokens)
    elif "gem" in str_tokens and "update" in str_tokens:
        parsed = gem_update_parser(str_tokens)
    elif "gem" in str_tokens and "install" in str_tokens:
        parsed = gem_install_parser(str_tokens)
    elif "git" in str_tokens and "clone" in str_tokens:
        parsed = git_clone_parser(str_tokens)
    elif "go" in str_tokens:
        parsed = go_parser(str_tokens)
    elif "groupadd" in str_tokens:
        parsed = groupadd(str_tokens)
    elif "npm" in str_tokens and "update" in str_tokens:
        parsed = apk_update_parser(str_tokens)
    elif "npm" in str_tokens and "install" in str_tokens:
        parsed = apk_update_parser(str_tokens)
    elif "php" in str_tokens:
        parsed = php_parser(str_tokens)
    elif "python" in str_tokens:
        parsed = python_parser(str_tokens)
    elif "yum" in str_tokens and "update" in str_tokens:
        parsed = yum_update_parser(str_tokens)
    elif "yum" in str_tokens and "install" in str_tokens:
        parsed = yum_install_parser(str_tokens)
    elif "pip install" in str_tokens:
        parsed = pip_install_parser(str_tokens)
    elif "install_packages" in str_tokens:
        parsed = run_install_parser(str_tokens)
    elif "javac" in str_tokens:
        parsed = javac_parser(str_tokens)
    elif "rm" in str_tokens:
        parsed = rm_parser(str_tokens)
    else:
        parsed = unknown_parser(bash_str)
    return parsed





# def parse_within(bash_str):
#     #parsed = {'type': 'UNKNOWN', 'children': []}
#
#     parsed = { 'type': 'UNKNOWN', 'children': [] } # Start with nothing
#     phase = 0
#     # step1 = None
#     step2 = None
#     step3 = None
#     try:
#       print("try")
#       print(bash_str)
#       #Try and do real parse
#       step1 = subprocess.check_output(
#         'app.hs',
#         stderr=subprocess.DEVNULL,
#         input=bash_str.encode('utf-8')
#       )
#       phase = 1
#       print(json.dumps(json.loads(step1.decode('utf-8'))), flush=True)
#       step2 = subprocess.check_output(
#         ['jq-win64.exe', '-c', '--from-file', 'filter-1.jq'],
#         stderr=subprocess.DEVNULL,
#         input=step1
#       )
#       phase = 2
#       print(json.dumps(json.loads(step2.decode('utf-8'))), flush=True)
#       step3 = subprocess.check_output(
#         ['jq-win64.exe', '-c', '--from-file', 'filter-2.jq'],
#         stderr=subprocess.DEVNULL,
#         input=step2
#       )
#       phase = 3
#       parsed = json.loads(step3.decode('utf-8'))
#       print(parsed)
#     except Exception as ex:
#       return { 'type': 'UNKNOWN', 'children': [] }
#     return parsed
#


def adduser_parser(str_tokens):
    parsed = {
        'type': 'ADDUSER',
        'children': []
    }

    arg_count = 0
    user_count = 0
    for key in str_tokens:
        if key != "adduser":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'USER',
                    'value': key,
                    'children': []
                })
                user_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if user_count == 0:
        parsed['children'].append({
            'type': 'USER',
            'value': 'Null',
            'children': []
        })
    return parsed

def apk_update_parser(str_tokens):
    parsed = {
        'type': 'APK-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "apk" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def apk_add_parser(str_tokens):
    parsed = {
        'type': 'APK-ADD-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "apk" and key != "add":
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': '  Null',
            'children': []
        })
    return parsed

def aptaddrepository_parser(str_tokens):
    parsed = {
        'type': 'APTADDREPOSITORY',
        'children': []
    }

    arg_count = 0
    path_count = 0
    for key in str_tokens:
        if key != "apt-add-repository":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'DOCKER-PATH',
                    'value': key,
                    'children': []
                })
                path_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if path_count == 0:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })
    return parsed

def apt_get_update_parser(str_tokens):
    parsed = {
        'type': 'APT-GET-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "apt-get" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def apt_get_install_parser(str_tokens):
    parsed = {
        'type': 'APT-GET-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "apt-get" and key != "install":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': 'Null',
            'children': []
        })
    return parsed

def apt_key_add_parser(str_tokens):
    parsed = {
        'type': 'APT-KEY-ADD',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'KEY',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "apt-key" and key != "add":
                parsed['children'].append({
                    'type': 'KEY',
                    'value': key,
                    'children': []
                })
    return parsed

def apt_key_del_parser(str_tokens):
    parsed = {
        'type': 'APT-KEY-DEL',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'KEY',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "apt-key" and key != "del":
                parsed['children'].append({
                    'type': 'KEY',
                    'value': key,
                    'children': []
                })
    return parsed

def apt_key_update_parser(str_tokens):
    parsed = {
        'type': 'APT-KEY-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "apt-key" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def apt_update_parser(str_tokens):
    parsed = {
        'type': 'APT-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "apt" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def apt_install_parser(str_tokens):
    parsed = {
        'type': 'APT-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "apt" and key != "install":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': 'Null',
            'children': []
        })
    return parsed

def bash_parser(str_tokens):
    parsed = {
        'type': 'BASH',
        'children': []
    }

    if len(str_tokens) == 1:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "bash":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def cd_parser(str_tokens):
    parsed = {
        'type': 'CD',
        'children': []
    }

    if len(str_tokens) == 1:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "cd":
                parsed['children'].append({
                    'type': 'DOCKER-PATH',
                    'value': key,
                    'children': []
                })
    return parsed

def chmod_parser(str_tokens):
    parsed = {
        'type': 'CHMOD',
        'children': []
    }

    arg_count = 0
    path_count = 0
    for key in str_tokens:
        if key != "chmod":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'DOCKER-PATH',
                    'value': key,
                    'children': []
                })
                path_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if path_count == 0:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })
    return parsed

def chown_parser(str_tokens):
    parsed = {
        'type': 'CHOWN',
        'children': []
    }

    arg_count = 0
    path_count = 0

    for key in str_tokens:
        if key != "chown":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
        else:
            parsed['children'].append({
                'type': 'DOCKER-PATH',
                'value': key,
                'children': []
            })
            path_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if path_count == 0:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })
    return parsed

def cmake_parser(str_tokens):
    parsed = {
        'type': 'CMAKE',
        'children': []
    }

    arg_count = 0
    path_count = 0

    for key in str_tokens:
        if key != "cmake":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
        else:
            parsed['children'].append({
                'type': 'DOCKER-PATH',
                'value': key,
                'children': []
            })
            path_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if path_count == 0:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })
    return parsed

def configure_parser(str_tokens):
    parsed = {
        'type': 'CONFIGURE',
        'children': []
    }

    if len(str_tokens) == 1:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "'./configure'" and key.startswith('-'):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
            else:
                parsed['children'].append({
                    'type': 'ARG',
                    'value': 'Null',
                    'children': []
                })
    return parsed

def cp_parser(str_tokens):
    parsed = {
        'type': 'CP',
        'children': []
    }

    arg_count = 0
    path_count = 0

    for key in str_tokens:
        if key != "cp":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
        else:
            parsed['children'].append({
                'type': 'DOCKER-PATH',
                'value': key,
                'children': []
            })
            path_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if path_count == 0:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })
    return parsed

def curl_parser(str_tokens):
    parsed = {
        'type': 'CURL',
        'children': []
    }

    arg_count = 0
    link_count = 0

    for key in str_tokens:
        if key != "curl":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            elif "://" in key:
                parsed['children'].append({
                    'type': 'LINK',
                    'value': key,
                    'children': []
                })
                link_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if link_count == 0:
        parsed['children'].append({
            'type': 'LINK',
            'value': 'Null',
            'children': []
        })
    return parsed

def dnf_update_parser(str_tokens):
    parsed = {
        'type': 'DNF-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "dnf" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def dnf_install_parser(str_tokens):
    parsed = {
        'type': 'DNF-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "dnf" and key != "install":
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': '  Null',
            'children': []
        })
    return parsed

def docker_php_ext_install_parser(str_tokens):
    parsed = {
        'type': 'DOCKER-PHP-EXT-INSTALL',
        'children': []
    }

    arg_count = 0
    path_count = 0
    for key in str_tokens:
        if key != "docker-php-ext-install":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'DOCKER-PATH',
                    'value': key,
                    'children': []
                })
                path_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if path_count == 0:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })
    return parsed

def dpkg_architecture(str_tokens):
    parsed = {
        'type': 'DPKG_ARCHITECTURE',
        'children': []
    }

    arg_count = 0

    for key in str_tokens:
        if key != "dpkg-architecture":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1

    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    return parsed

def dpkg(str_tokens):
    parsed = {
        'type': 'DPKG',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "dpkg":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': 'Null',
            'children': []
        })
    return parsed

def echo(str_tokens):
    parsed = {
        'type': 'ECHO',
        'children': []
    }

    string_count = 0
    for key in str_tokens:
        if key != "echo":
            parsed['children'].append({
                'type': 'STRING',
                'value': key,
                'children': []
            })
            string_count = 1

    if string_count == 0:
        parsed['children'].append({
            'type': 'STRING',
            'value': 'Null',
            'children': []
        })
    return parsed

def export(str_tokens):
    pass

def find(str_tokens):
    pass

def gem_update_parser(str_tokens):
    parsed = {
        'type': 'GEM-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "gem" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def gem_install_parser(str_tokens):
    parsed = {
        'type': 'GEM-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "gem" and key != "install":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': 'Null',
            'children': []
        })
    return parsed

def git_clone_parser(str_tokens):
    parsed = {
        'type': 'GIT-CLONE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'LINK',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "git" and key != "clone":
                parsed['children'].append({
                    'type': 'LINK',
                    'value': key,
                    'children': []
                })
    return parsed

def go_parser(str_tokens):
    parsed = {
        'type': 'GO',
        'children': []
    }

    arg_count = 0
    string_count = 0
    if "install" in str_tokens:
        parsed = {
            'type': 'GO-INSTALL',
            'children': []
        }
    elif "get" in str_tokens:
        parsed = {
            'type': 'GO-GET',
            'children': []
        }
    elif "run" in str_tokens:
        parsed = {
            'type': 'GO-RUN',
            'children': []
        }
    elif "test" in str_tokens:
        parsed = {
            'type': 'GO-TEST',
            'children': []
        }
    elif "build" in str_tokens:
        parsed = {
            'type': 'GO-BUILD',
            'children': []
        }

    for key in str_tokens:
        if key != "go" and key != "get" and key != "run" and key != "test" and key != "build":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'STRING',
                    'value': key,
                    'children': []
                })
                string_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if string_count == 0:
        parsed['children'].append({
            'type': 'STRING',
            'value': 'Null',
            'children': []
        })
    return parsed

def gpg(str_tokens):
    pass

def grep(str_tokens):
    pass

def groupadd(str_tokens):
    parsed = {
        'type': 'GROUPADD',
        'children': []
    }

    arg_count = 0
    user_count = 0
    for key in str_tokens:
        if key != "groupadd":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'USER',
                    'value': key,
                    'children': []
                })
                user_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if user_count == 0:
        parsed['children'].append({
            'type': 'USER',
            'value': 'Null',
            'children': []
        })
    return parsed

def ldconfig(str_tokens):
    pass

def ln(str_tokens):
    pass

def make(str_tokens):
    pass

def npm_update_parser(str_tokens):
    parsed = {
        'type': 'NPM-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "npm" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def npm_install_parser(str_tokens):
    parsed = {
        'type': 'NPM-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "npm" and key != "install":
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': '  Null',
            'children': []
        })
    return parsed


def yum_update_parser(str_tokens):
    parsed = {
        'type': 'YUM-UPDATE',
        'children': []
    }

    if len(str_tokens) == 2:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })

    else:
        for key in str_tokens:
            if key != "yum" and key != "update":
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
    return parsed

def yum_install_parser(str_tokens):
    parsed = {
        'type': 'YUM-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "yum" and key != "install":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': 'Null',
            'children': []
        })
    return parsed


def php_parser(str_tokens):
    parsed = {
        'type': 'PHP',
        'children': []
    }

    arg_count = 0
    string_count = 0
    for key in str_tokens:
        if key != "php":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'STRING',
                    'value': key,
                    'children': []
                })
                string_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if string_count == 0:
        parsed['children'].append({
            'type': 'STRING',
            'value': 'Null',
            'children': []
        })
    return parsed

def pip_install_parser(str_tokens):
    parsed = {
        'type': 'PIP-INSTALL',
        'children': []
    }

    arg_count = 0
    pkg_count = 0
    for key in str_tokens:
        if key != "pip" and key != "install":
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': 'Null',
            'children': []
        })
    return parsed

def python_parser(str_tokens):
    parsed = {
        'type': 'PYTHON',
        'children': []
    }

    arg_count = 0
    path_count = 0
    for key in str_tokens:
        if key != "python":
            key = key.strip("\t\t")
            if key.startswith("-"):
                parsed['children'].append({
                    'type': 'ARG',
                    'value': key,
                    'children': []
                })
                arg_count = 1
            else:
                parsed['children'].append({
                    'type': 'DOCKER-PATH',
                    'value': key,
                    'children': []
                })
                path_count = 1
    if arg_count == 0:
        parsed['children'].append({
            'type': 'ARG',
            'value': 'Null',
            'children': []
        })
    if path_count == 0:
        parsed['children'].append({
            'type': 'DOCKER-PATH',
            'value': 'Null',
            'children': []
        })
    return parsed


def run_install_parser(str_tokens):
    parsed = {
        'type': 'RUN-INSTALL',
        'children': []
    }

    pkg_count = 0
    for key in str_tokens:
        if key != "apk" and key != "install":

                parsed['children'].append({
                    'type': 'PACKAGE',
                    'value': key,
                    'children': []
                })
                pkg_count = 1

    if pkg_count == 0:
        parsed['children'].append({
            'type': 'PACKAGE',
            'value': '  Null',
            'children': []
        })
    return parsed

def javac_parser(str_tokens):
    parsed = {
        'type': 'JAVAC',
        'children': []
    }
    return parsed

def rm_parser(str_tokens):
    parsed = {
        'type': 'RM',
        'children': []
    }
    return parsed

def unknown_parser(bash_str):
    parsed = {
        'type': 'UNKNOWN',
        'value': bash_str['value'],
        'children': []
    }
    return parsed

def not_empty(s):
    return s and s.strip()
