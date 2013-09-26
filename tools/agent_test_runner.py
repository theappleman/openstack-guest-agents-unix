#!/usr/bin/env python

import time
import os
from ConfigParser import RawConfigParser
import fabric
from fabric.api import env, run
from fabric.operations import put


def install_python_and_curl():
    #Redhat Releases
    run("if [ -f /etc/redhat-release ]; "
        "then IF_PYTHON=`which python > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then apt-get -y install python; fi;"
        "IF_PYTHON=`which curl > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then apt-get -y install curl; fi fi")

    #Open-SuSE image
    run("if [ -f /etc/SuSE-release ]; "
        "then IF_PYTHON=`which python > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then zypper install -y python; fi;"
        "IF_PYTHON=`which curl > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then zypper install -y curl; fi fi")

    #Debian images
    run("if [ -f /etc/debian_version ]; "
        "then IF_PYTHON=`which python > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then apt-get install -y python; fi;"
        "IF_PYTHON=`which curl > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then apt-get install -y curl; fi fi")

    #FreeBSD images
    run("if [ `uname -s` == 'FreeBSD' ]; "
        "then IF_PYTHON=`which python > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then pkg_add -r python; fi;"
        "then IF_BASH=`which bash > /dev/null ; echo $?` ; if [[ $IF_BASH == '1' ]]; "
        "then pkg_add -r bash; fi;"
        "IF_PYTHON=`which curl > /dev/null ; echo $?` ; if [[ $IF_PYTHON == '1' ]]; "
        "then pkg_add -r curl; fi fi")


def install_agent():
    run("curl -OkL https://raw.github.com/rackerlabs/openstack-guest-agents-unix/master/tests/functional/install_agent.py")
    run("python install_agent.py")
    run("rm -rf install_agent.py")


def run_tests():
    run("curl -OkL https://raw.github.com/rackerlabs/openstack-guest-agents-unix/master/tests/functional/agent_tester.py")
    run("python agent_tester.py")
    run("rm -rf agent_tester.py")


def install_agent_and_run_tests():
    install_python_and_curl()
    install_agent()
    print("Going for reboot")
    time.sleep(5)
    fabric.operations.reboot(120)
    run_tests()


def load_config():
    config = RawConfigParser()
    config.read(os.path.join(os.getcwd(), "fabfile.cfg"))
    env.hosts = [config.get('testnode', 'host_ipv4')]
    env.user = config.get('testnode', 'username')
    env.password = config.get('testnode', 'password')


load_config()
