#encoding=utf-8
# load django evnironment
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

import sys
import base64
import hashlib
import logging
import time
import traceback
import requests
reload(sys)
sys.setdefaultencoding('utf-8')
from consumer.models import *
from cms.constant import key,ircsId

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger('jobdaemon')
logger.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] [%(process)d] [%(filename)s:%(lineno)s] %(message)s','%Y-%m-%dT%H:%M:%S')
stdout = logging.StreamHandler(stream=sys.stdout)
stdout.setFormatter(log_format)
stdout.setLevel(logging.DEBUG)
logger.addHandler(stdout)

def gen_sign(s):
    #base64_s = base64.b64encode(s)
    md5_s = "%s%s%s" %(ircsId,s,key)
    print md5_s
    return hashlib.md5(md5_s).hexdigest()


UserInfoAPI = 'http://221.4.253.229:8080/ucenter_ircs/userInfo'
ynamicResourceAPI = 'http://221.4.253.229:8080/ucenter_ircs/dynamicResource'

def sync(url,parameters):
    from urllib import quote
    try:
        logger.info("sync url %s" %url)
        print parameters.strip()
        contentXml = base64.b64encode(parameters.strip())
        contentXml = quote(contentXml)
        ticket = gen_sign(contentXml)
        print ticket
        data = {'contentXml':contentXml,'ticket':ticket}
        r = requests.post(url,data=data,timeout=15)
        return r.content
    except:
        traceback.print_exc()

def run():
    while True:
        unfinish = Job.list_unfinished()
        for item in unfinish:
            result = None
            if item.jobType == 1:
                result = sync(UserInfoAPI,item.parameters)
            elif item.jobType == 2:
                result = sync(ynamicResourceAPI,item.parameters)
            if result:
                logger.info('sycn result %s' %str(result))

            break
        time.sleep(10)

if __name__ == '__main__':
    logger.info("nothing")
    run()