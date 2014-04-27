#!/usr/bin/env python
import os
import sys
topdir = os.path.dirname(os.path.realpath(__file__)) + "../.."
topdir = os.path.realpath(topdir)
sys.path.insert(0, topdir)
""" this method have to be added to utils module"""
from subprocess import check_output,CalledProcessError
from vyos_session.utils import logger
import os

class PathError(Exception): pass
class AddressError(Exception): pass
class IpformatError(Exception): pass
class InterfaceError(Exception): pass
class ActionError(Exception): pass

class validation():

    """check if a given ip address is into a valid format"""
    @staticmethod
    def testip(ipaddr):
        addr_portions = ipaddr.split('.')
        if len(addr_portions) != 4:
            logger.error("provided ip address %s is not in the correct format!"%ipaddr)
            return False
        for portion in addr_portions:
            if not portion.isdigit():
                logger.error("provided ip address %s is not in the correct format!"%ipaddr)
                return False
            elem = int(portion)
            if elem < 0 or elem > 255:
                logger.error("provided ip address %s is not in the correct format!"%ipaddr)
                return False
        return True

    """check if a given interface already exist"""
    @staticmethod
    def testiface(iface):
        try:
            interfaces=check_output("ls /sys/class/net",shell=True)
        except CalledProcessError as e:
            logger.error("problem happened when extracting interfaces ! execution fails with return code %s" % e.returncode)
            return False
        mounted_ifaces = interfaces.split('\n')
        del mounted_ifaces[-1]
        if iface not in mounted_ifaces:
            logger.error("%s: the mentioned interfaces doesn't match with any existing one!"%iface)
            return False
        return True

    """verify if a given path is valid"""
    @staticmethod
    def testpath(path):
        if not os.path.exists(path):
            logger.error("%s: this path doesn't exist !"%path)
            return False
        return True
       
    """this method check if the inputed address match with one existing address"""
    @staticmethod
    def addrvalidation(addr):
        try:
            addresses = check_output("/sbin/ifconfig |grep 'inet addr'|awk '{print $2}'|sed 's/addr://g'",shell=True)
        except CalledProcessError as e:
            logger.error("problem happened when extracting existing addresses ! execution fails with return code %s" % e.returncode)
            return False
        activeaddr=addresses.split('\n')
        del activeaddr[-1]
        if addr not in activeaddr:
            logger.error("%s: the inputed address doesn't match with any existing one!"%addr)
            return False
        return True
