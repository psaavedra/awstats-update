# This file is aa very simple script. Your primarly tasks is search "sites
# enables" files in the nginx conf directory and for each of them, create
# a awstats conffile based in _awstats.TEMPLATE.conf file.
#
# This script has not available parameters.

import os
  
awstats_dir="/etc/awstats/"
awstats_file_prefix="awstats."
awstats_file_sufix=".conf"

sites_enable_dir="/etc/nginx/sites-enabled/"

conf_file_sufix=".conf"
conf_file_sep="-"
conf_files=[]


def generate_awstats_file (conf_file, conf_name):
  global awstats_dir
  global sites_enable_dir

  global awstats_dir
  global awstats_file_prefix
  global awstats_file_sufix

  server_name=""
  access_log=""

  f = file (sites_enable_dir + conf_file)
  for l in f.readlines():
    # Removing first black spaces 
    l = l.strip()
    
    if len(l) == 0 or l[0] == '#':
      continue

    if l.find("server_name") == 0:
      l = l.replace("server_name", "")
      l = l.replace(";", "")
      server_name = l.strip()

    if l.find("access_log") == 0:
      l = l.replace("access_log", "")
      l = l.replace(";", "")
      access_log = l

  # Generate awstats conf file from the template ...
  template_file = open (awstats_dir + "scripts/_" + awstats_file_prefix + "TEMPLATE" + awstats_file_sufix)
  generate_file = open (awstats_dir + awstats_file_prefix + conf_name
          + awstats_file_sufix, "w")
  
  for l in template_file.readlines():
 
    if l.find("__SITEDOMAIN__") != -1:
      l = l.replace("__SITEDOMAIN__", server_name.split(" ")[0])

    if l.find("__HOSTALIASES__") != -1:
      l = l.replace("__HOSTALIASES__", server_name)

    if l.find("__LOGFILE__") != -1:
      l = l.replace("__LOGFILE__", access_log)
   
    generate_file.write(l)
  
  template_file.flush()
  template_file.close()
  generate_file.flush()
  generate_file.close()

# Main ...

for f in os.listdir(awstats_dir):
  # Removing previous configurations
  if (f.find(awstats_file_prefix) != -1 ) and (f.endswith(awstats_file_sufix)):
    os.remove(awstats_dir + f)


for f in os.listdir(sites_enable_dir):
  if ( (f.find(conf_file_sufix) != -1) and (len (f)) == f.find(conf_file_sufix) + len (conf_file_sufix)):
    # get the code name of the site conf file
    conf_name = (f.split(conf_file_sep)[-1]).split(conf_file_sufix)[0]
    # print conf_name
    generate_awstats_file (f,conf_name)

