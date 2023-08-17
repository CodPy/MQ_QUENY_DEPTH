import pymqi
import datetime
from flask import Flask,render_template
app = Flask('queue')

def is_part_in_list(check_str, words):
    if words in check_str:
            return True
    return False

def qinfo():
    queue_manager = 'RGSMGR_PROD'
     # channel = 'SYSTEM.DEF.SVRCONN'
    channel = 'RSU.DEF.SVRCONN'
    host = 'esb-prod-mq-01.rgs.ru'
    port = '1414'
    conn_info = '{}({})'.format(host, port)
    user = 'mq_adm'
    password = 'shuTh8ooyohk'
    bytes_encoding = 'utf-8'
    default_ccsid = 819
    qmgr = pymqi.connect(queue_manager, channel, conn_info, user, password,bytes_encoding=bytes_encoding, default_ccsid=default_ccsid)
    pcf = pymqi.PCFExecute(qmgr,response_wait_interval=90000)
    c = 0
    attrs = {
        pymqi.CMQC.MQCA_Q_NAME :'*'
    }
    result = pcf.MQCMD_INQUIRE_Q(attrs)


    dict_queue={}
    for queue_info in result:
        try:

            if int(queue_info[3])>0:


                qname=str(queue_info[2016].decode(('utf-8').replace(" ",""))).strip()
            #print(str(queue_info[2016].decode(('utf-8').replace(" ","")))+': '+str(queue_info[3]))
                dict_queue.update({qname:int(str(queue_info[3]).strip())})

        except:
            a=1

    keys_bad=[]
    for key in dict_queue:
        if    is_part_in_list   (key,'DEAD')==True \
           or is_part_in_list(key,'SPLUNK')==True or is_part_in_list(key,'SYSTEM')==True \
                or is_part_in_list(key,'PYMQPCF')==True or is_part_in_list(key,'AMQ.MQEXPLORER'): \

           #or is_part_in_list(key,'DIASREINS')==True: # ставим очереди которые хотим исключить например сейчасисключаем все очереди со словом DEAD в названии
            keys_bad.append(key)

    for key in keys_bad:
        del dict_queue[key]


    sorted_dict = {}
    sorted_keys = sorted(dict_queue, key=dict_queue.get,reverse=True)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = dict_queue[w]
    str_obj=''

    for key,val in sorted_dict.items():
        #print (key,': ', val)
        print  (key)
        v_str=str(val)
        str_obj = str_obj+'&#128504'+key+': '+v_str+'<br>'+'<br>'
        #str_obj =  str_obj + ' ' + key + '<br>'
    qmgr.disconnect()
    current_datetime = datetime.datetime.now()
    current_datetime = datetime.datetime.strftime(current_datetime, "%d.%m.%Y %H:%M:%S")
    current_datetime = str(current_datetime)
    return  '<b>'+'&#8986'+' '+current_datetime+'<br>'+'<br>'+ '&#10031'  +'Очереди больше ноля сообщений: промышленная среда IBM MQ. Cервер: esb-prod-mq-01.rgs.ru'+'&#10031'+'</b>'+'<br>'+'<br>' +str_obj
    #return '<b>'+'не удалось считать список очередей IBM MQ.'+'</b>'

@app.route('/')
def webprint():
    qinfo()
    return qinfo()

if __name__=="__main__":
    app.run(host='0.0.0.0', port = 7778)