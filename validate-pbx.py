#!/usr/bin/env python3

############################################################################
# Script para Validação de push de forma a evitar quebras do projeto de    #
# testes do calabash.                                                      #
############################################################################
# Desenvolvido por : Alexandre Garrefa                                     #
# alexandre.garrefa@concretesolutions.com.br                               #
# Criado em  : 14/01/2015                                                  #
############################################################################

import re
import sys
from os import path, listdir
#from colorama import init, Fore, Back, Style

def print_banner():
  print ('#'*76)
  print ('# Safe Push Script')
  print ('#'*76)

def pbxfile_path():
  # get this file path
  fpath = path.abspath(__file__) 
  # cd ../../
  proj_path = path.split(fpath)[0]
  proj_path = path.split(proj_path)[0]
  # list directories in repo directory
  dir_list = listdir(proj_path)
  rx = re.compile('^.*\.xcodeproj$')
  # find project folder
  proj_dir = ''
  for dir_name in dir_list:
    if re.match(rx,dir_name) : 
      proj_dir = dir_name
      break
  pbxfile = "{0}/{1}/project.pbxproj".format(proj_path,proj_dir)
  return pbxfile

def read_file(fname):
  f = open(fname)
  content = f.read().splitlines()
  f.close()
  return content

def get_targets_ref(pbxfile):
  refs_dic = {}
  rx_beg = re.compile('^/\* Begin PBXNativeTarget section \*/$')
  rx_end = re.compile('^/\* End PBXNativeTarget section \*/$')
  content = lines_between(rx_beg,rx_end,pbxfile)
  rx_beg = re.compile('^.*= {$')
  rx_end = re.compile('^.*};$')
  beg_found = False
  end_found = False
  parts = []
  temp = []
  for line in content:
    if beg_found :
      end_found = re.match(rx_end,line)
      if end_found : 
        end_found = False
        beg_found = False
        parts.append(temp)
        temp = []
        continue
      else : temp.append(line)
    else : beg_found = re.match(rx_beg,line)
  rx_ref = re.compile('^\s*productReference = (\w+) /\*\s+(.+\.app)\s+\*/;$')
  rx_res = re.compile('^.*(\w{24})\s.*/\* Resources \*/,.*$')
  rx_sou = re.compile('^.*(\w{24})\s.*/\* Sources \*/,.*$')
  for part in parts :
    source    = ''
    resource  = ''
    reference = ''
    for line in part :
      match = re.search(rx_sou,line)
      if match : source = match.group(1)
      else : 
        match = re.search(rx_res,line)
        if match : resource = match.group(1)
        else : 
          match = re.search(rx_ref,line)
          if match : reference = match.group(2)
    if len(reference) and len(source) and len (resource):
      refs_dic[reference] = [source,resource]
  return refs_dic

def get_target_resources_from_file(target_ref,section,pbxfile):
  content = []
  rx_beg = re.compile('^/\* Begin %s section \*/$'%section)
  rx_end = re.compile('^/\* End %s section \*/$'%section)
  rx_ref = re.compile('.*%s.* /\* (Sources|Resources) \*/ = {'%target_ref)
  content = lines_between(rx_beg,rx_end,pbxfile)
  content = lines_between(rx_ref,re.compile('^\s*};$'),content)
  content = lines_between(re.compile('^.*files = \(.*$'),re.compile('^.*\);$'),content)
  resources = []
  for line in content:
    rx = re.compile('^.*/(\* .*) \*/.*$')
    search = re.search(rx,line)
    if search : resources.append(search.group(1))
  return sorted(resources)

def lines_between(rx_beg,rx_end,content):
  lines = []
  beg_found = False
  end_found = False
  for line in content:
    if end_found : break
    if not beg_found : beg_found = re.match(rx_beg,line)
    if beg_found :
      lines.append(line)
      end_found = re.match(rx_end,line)
  return lines

def number_of_missing_file():
  file_content = read_file(pbxfile_path())
  targets_ref  = get_targets_ref(file_content)

  dic_resources = {}
  for key in sorted(targets_ref.keys()):
    sources = get_target_resources_from_file( targets_ref[key][0],\
                                              'PBXSourcesBuildPhase',\
                                              file_content)
    resources = get_target_resources_from_file( targets_ref[key][1],\
                                                'PBXResourcesBuildPhase',\
                                                file_content)
    allfiles = sources + resources
    dic_resources[key] = allfiles
  allfiles = []
  for key in sorted(dic_resources.keys()):
    obj = dic_resources[key]
    allfiles += obj
  allfiles = set(allfiles)
  missing_files = 0
  for key in sorted(dic_resources.keys()):
    obj = dic_resources[key]
    diff = allfiles.difference(obj)
    missing_files += len(diff)
    if(len(diff)) : print ('\n[{0}] files in {1}'.format(len(diff),key))
    for line in diff : print ('\033[1;41m[Missing]\033[0m : {0}'.format(line))
  return missing_files

if __name__ == '__main__':
  #init()
  missing_files = number_of_missing_file()
  sys.exit(missing_files)
