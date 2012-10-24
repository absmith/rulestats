import re

import os
import sys
import base64
import csv
import hashlib

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now
from rulestats.core.models import *

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-f','--file',dest='file',help='Get ACLs from a file'),
    )
    
    def handle(self, *args, **options):

        if options['file']:
            try:
                with open(options['file']) as f: 
                    firewall = Firewall.objects.get(pk=1)
                    self.process_access_list(f.readlines(), firewall)
            except IOError as e:
                print 'Error: %s' % e.value

        
    def process_access_list(self, access_list, firewall):

        reobj = re.compile(r"\s*access-list\s(\S+)\sline\s\d+\sextended\s(permit|deny)\s(\w+)\s(.+)\s\(hitcnt=(\d+)\)\s(\w+)")

        stored_rules = list(firewall.rules.values('hash', 'hash1', 'access_list'))
        live_rules = []
        
        for line in access_list:
            # create our own hash just in cause the asa ends up with a duplicate hash
            # had it happen in the past
            hash1 = hashlib.sha256(line.split('(')[0]).hexdigest()
            match = reobj.search(line)
            rule = {}
            if match:
                if match.group(1).find("_nat_static") != -1:
                    continue

                if match.group(4).find("object") != -1:
                    continue

                rule['firewall'] = firewall
                rule['access_list'] = match.group(1)
                rule['type'] = match.group(2)
                rule['protocol'] = match.group(3)
                rule['details'] =  match.group(4)
                rule['hit_count'] = match.group(5)
                rule['hash'] =  match.group(6)
                rule['hash1'] = hash1
                live_rules.append(rule)


        # Proccess rules
        for rule in live_rules:
            rule_index = {'hash': rule['hash'],
                          'access_list': rule['access_list'],
                          'hash1': rule['hash1']}
            if rule_index in stored_rules:
                object = firewall.rules.get(hash=rule['hash'],
                                            access_list=rule['access_list'],
                                            hash1=rule['hash1'])
                object.access_list = rule['access_list']
                object.type = rule['type']
                object.protocol = rule['protocol']
                object.details = rule['details']
                object.current_hit_count = rule['hit_count']
                object.hash = rule['hash']
                object.hash1 = rule['hash1']
                object.save()
  
                stored_rules.remove(rule_index)
            else:
                firewall.rules.create(
                      access_list=rule['access_list'],
                      type=rule['type'],
                      protocol=rule['protocol'],
                      details=rule['details'],
                      current_hit_count=rule['hit_count'],
                      max_hit_count=rule['hit_count'],
                      max_hit_count_timestamp=now(),
                      hash=rule['hash'],
                      hash1=rule['hash1']
                      )
                      
        # at this port anything left in stored_rules should 
        # be a stale rule and should be removed
        for rule in stored_rules:
            firewall.rules.filter(hash=rule['hash'],
                                  access_list=rule['access_list'],
                                  hash1=rule['hash1']).delete()