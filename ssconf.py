#!/usr/bin/env python3
# coding=utf-8
#
# 感谢dalao
# https://www.logcg.com

import urllib3
import re
import datetime
import certifi
import codecs


def getList(listUrl):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',  # Force certificate check.
        ca_certs=certifi.where(),  # Path to the Certifi bundle.
    )

    data = http.request('GET', listUrl, timeout=10).data
    return data


def getGfwList():
    # the url of gfwlist
    baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'

    comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
    domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'

    tmpfile = './list/tmp'

    gfwListTxt = codecs.open('./list/gfwlist.txt', 'w', 'utf-8')
    gfwListTxt.write('# SS config file for surge with gfw list \n')
    gfwListTxt.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    gfwListTxt.write('\n')

    #add Surge RULESETFILE
    gfwSurgeRULESETFile = codecs.open('./configFileHere/Surge3_RULESET/surge3_ruleset_gfw.list', 'w', 'utf-8')
    gfwSurgeRULESETFile.write('# SS config file for surge with gfw list \n')
    gfwSurgeRULESETFile.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    gfwSurgeRULESETFile.write('\n')

    try:

        data = getList(baseurl)

        content = codecs.decode(data, 'base64_codec').decode('utf-8')

        # write the decoded content to file then read line by line
        tfs = codecs.open(tmpfile, 'w', 'utf-8')
        tfs.write(content)
        tfs.close()
        print('GFW list fetched, writing...')
    except:
        print('GFW list fetch failed, use tmp instead...')
    tfs = codecs.open(tmpfile, 'r', 'utf-8')

    # Store all domains, deduplicate records
    domainList = []

    # Write list
    for line in tfs.readlines():

        if re.findall(comment_pattern, line):
            continue
        else:
            domain = re.findall(domain_pattern, line)
            if domain:
                try:
                    found = domainList.index(domain[0])
                except ValueError:
                    if "spotify.com" in domain[0]:
                        continue
                    else:
                        domainList.append(domain[0])
                        gfwListTxt.write('DOMAIN-SUFFIX,%s,Proxy\n' % (domain[0]))
                        gfwSurgeRULESETFile.write('DOMAIN-SUFFIX,%s\n' % (domain[0]))
            else:
                continue

    tfs.close()
    gfwListTxt.close()


def getSurgeChinaIPList():
    # the url of chinaIP
    baseurl = 'https://raw.githubusercontent.com/17mon/china_ip_list/master/china_ip_list.txt'

    try:

        content = getList(baseurl)
        content = content.decode('utf-8')
        f = codecs.open('./list/chinaIPlist', 'w', 'utf-8')
        f.write(content)
        f.close()
    except:
        print('Get IPlist update failed,use cache to update instead.')

    ipList = codecs.open('./list/chinaIPlist', 'r', 'utf-8')
    ipListTxt = codecs.open('./list/suchinaIPlist.txt', 'w', 'utf-8')
    ipListTxt.write('# chinaIP list updated on ' + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S" + '\n'))

    #add Surge RULESETFILE
    ipsurgeRULESETFile = codecs.open('./configFileHere/Surge3_RULESET/surge3_ruleset_cnip.list', 'w', 'utf-8')
    ipsurgeRULESETFile.write('# chinaIP list updated on ' + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S" + '\n'))

    # Write list
    for line in ipList.readlines():

        ip = re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', line)
        if len(ip) > 0:
            ipListTxt.write('IP-CIDR,%s,CNProxy\n' % (ip[0]))
            ipsurgeRULESETFile.write('IP-CIDR,%s\n' % (ip[0]))

    ipListTxt.close()
    ipListTxt.close()


def getShadowrocketChinaIPList():
    # the url of chinaIP
    ipList = codecs.open('./list/chinaIPlist', 'r', 'utf-8')
    ipListTxt = codecs.open('./list/srchinaIPlist.txt', 'w', 'utf-8')
    ipListTxt.write('# chinaIP list updated on ' + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S" + '\n'))
    # Write list
    for line in ipList.readlines():

        ip = re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', line)
        if len(ip) > 0:
            ipListTxt.write('IP-CIDR,%s,DIRECT\n' % (ip[0]))

    ipListTxt.close()
    ipListTxt.close()

def getQuanChinaIPList():
    # the url of chinaIP
    ipList = codecs.open('./list/chinaIPlist', 'r', 'utf-8')
    ipListTxt = codecs.open('./list/sqchinaIPlist.txt', 'w', 'utf-8')
    ipListTxt.write('# chinaIP list updated on ' + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S" + '\n'))
    # Write list
    for line in ipList.readlines():

        ip = re.findall(r'\d+\.\d+\.\d+\.\d+/\d+', line)
        if len(ip) > 0:
            ipListTxt.write('IP-CIDR,%s,国内\n' % (ip[0]))

    ipListTxt.close()
    ipListTxt.close()


def genSurgeGFWAndChinaIPConf():
    f = codecs.open('template/surge_gfwlist&whiteIP_conf', 'r', 'utf-8')
    gfwlist = codecs.open('list/gfwlist.txt', 'r', 'utf-8')
    iplist = codecs.open('list/suchinaIPlist.txt', 'r', 'utf-8')
    file_content = f.read()
    iplist_buffer = iplist.read()
    gfwlist_buffer = gfwlist.read()
    gfwlist.close()
    iplist.close()
    f.close()

    GEOIPList = 'GEOIP,CN,CNProxy'

    file_content = file_content.replace('__GFWLIST__', gfwlist_buffer)
    file_content = file_content.replace('__CHINAIP__', GEOIPList)
    confs = codecs.open('configFileHere/surge_gfwlist&GEOIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

    file_content = file_content.replace(GEOIPList, iplist_buffer)
    confw = codecs.open('configFileHere/surge_gfwlist&whiteIP.conf', 'w', 'utf-8')
    confw.write(file_content)
    confw.close()


def genShadowrocketGFWAndChinaIPConf():
    f = codecs.open('template/shadowrocket_gfwlist&whiteIP_conf', 'r', 'utf-8')
    gfwlist = codecs.open('list/gfwlist.txt', 'r', 'utf-8')
    iplist = codecs.open('list/srchinaIPlist.txt', 'r', 'utf-8')
    file_content = f.read()
    iplist_buffer = iplist.read()
    gfwlist_buffer = gfwlist.read()
    gfwlist.close()
    iplist.close()
    f.close()

    GEOIPList = 'GEOIP,CN,DIRECT'

    file_content = file_content.replace('__GFWLIST__', gfwlist_buffer.replace('Proxy', 'PROXY'))
    file_content = file_content.replace('__CHINAIP__', GEOIPList)
    confs = codecs.open('configFileHere/shadowrocket_gfwlist&GEOIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

    file_content = file_content.replace(GEOIPList, iplist_buffer)
    confw = codecs.open('configFileHere/shadowrocket_gfwlist&whiteIP.conf', 'w', 'utf-8')
    confw.write(file_content)
    confw.close()

def genQuantumultGFWAndChinaIPConf():
    f = codecs.open('template/quan_gfwlist&whiteIP_conf', 'r', 'utf-8')
    gfwlist = codecs.open('list/gfwlist.txt', 'r', 'utf-8')
    iplist = codecs.open('list/sqchinaIPlist.txt', 'r', 'utf-8')
    file_content = f.read()
    iplist_buffer = iplist.read()
    gfwlist_buffer = gfwlist.read()
    gfwlist.close()
    iplist.close()
    f.close()

    GEOIPList = 'GEOIP,CN,国内'

    file_content = file_content.replace('__GFWLIST__', gfwlist_buffer.replace('DOMAIN-SUFFIX,', 'HOST-SUFFIX,')).replace('Proxy', 'PROXY')
    file_content = file_content.replace('__CHINAIP__', GEOIPList)
    confs = codecs.open('configFileHere/quan_gfwlist&GEOIP.conf', 'w', 'utf-8')
    confs.write(file_content)
    confs.close()

    file_content = file_content.replace(GEOIPList, iplist_buffer)
    confw = codecs.open('configFileHere/quan_gfwlist&whiteIP.conf', 'w', 'utf-8')
    confw.write(file_content)
    confw.close()

def main():
    print('Getting GFW list...')
    getGfwList()
    print('Getting chinaIP list...')
    getSurgeChinaIPList()
    getShadowrocketChinaIPList()
    getQuanChinaIPList()

    print('Generate config file:surge shadowrocket quantumult conf files success')
    genSurgeGFWAndChinaIPConf()
    genShadowrocketGFWAndChinaIPConf()
    genQuantumultGFWAndChinaIPConf()

    print('All done!')
    print('Now you need edit config file to add your server infomation.')


if __name__ == '__main__':
    main()
