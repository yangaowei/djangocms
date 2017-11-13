#encoding=utf-8

from consumer.models import Consumer,Service,VirtualServer,Job
from cms.constant import ircsId

def generate_userinfo_xml(consumer,operType):    
    result = '''<?xml version="1.0" encoding="UTF-8" ?>
<userInfo xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ircsId>%s</ircsId>
    <operType>%s</operType>
    <nature>%s</nature>
    <unitNature>%s</unitNature>
    <name>%s</name>
    <idType>%s</idType>
    <id>%s</id>
    <addr>%s</addr>
    <zipCode>%s</zipCode>
    <tel>%s</tel>
    <mobile>%s</mobile>
    <email>%s</email>''' %(ircsId,operType,consumer.nature,consumer.unitNature,consumer.name,consumer.idType,consumer._id,consumer.addr,consumer.zipCode,consumer.tel,consumer.phone,consumer.email)
    for service in consumer.service_set.all():
        tmp = '''
    <service>
        <serviceContent>%s</serviceContent>
        <appServiceType>%s</appServiceType>
        <regType>%s</regType>
        <regId>%s</regId>
        <setMode>%s</setMode>
        <domains>%s</domains>
    </service>''' %(service.serviceContent,service.appServiceType,service.regType,service.regId,service.setMode,service.domains)

        result += tmp

    result += '''
</userInfo>
    '''
    return result

def generate_dynamicResource_xml(vs,operType):
    result = '''
<?xml version="1.0" encoding="UTF-8" ?>
<dynamicResource xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ircsId>%s</ircsId>
    <operType>%s</operType>
    <domain>%s</domain>
    <ip>%s</ip>
    <virtualId>%s</virtualId>
    <virtualType>%s</virtualType>
    <ownerTime>%s</ownerTime>
    <name>%s</name>
    <idType>%s</idType>
    <id>%s</id>
</dynamicResource>
    ''' %(ircsId,operType,vs.domains,vs.ip,vs.name,vs.virtualType,str(vs.ownerTime)[:19],vs.consumer.name,vs.idType,vs._id)

    return result