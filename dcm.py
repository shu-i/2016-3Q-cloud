
import pika
import Dbaccessor
#2016.11.17 PM2035  Don't delete
class DataCenterManager():
    def __init__(self):
	pass
#---------------------------
# worker function
def callback(ch, method, properties, messagebody):
    print " [*] Received %r" % (messagebody,)

    ch.basic_ack(delivery_tag = method.delivery_tag)

    params = messagebody.split(',')
    machineId = params[2]

    # get task message
    taskMessage = getMessage(messagebody)

    # send message to agent
    sendMessage(machineId, taskMessage)
        
    # update table resourceinfo
    updateStatusOfResourceInfo(taskMessage)

# send message to agent
# @param machineId   : target machine id
# @param taskMessage : task info
def sendMessage(machineId, taskMessage):

    # create queue id
    queueId = 'task_queue_' + str(machineId)

    # send message 
    channel.queue_declare(queue=queueId, durable=True)
    channel.basic_publish(exchange='',
                              routing_key=queueId,
                              body=taskMessage,
                              properties=pika.BasicProperties(delivery_mode=2,))

# get message body to send to agent
def getMessage(request):
    
    # get instanceid from request message 
    params = request.split(',')

    # when creating a VM
    # message: 'c,instanceid, cpus, memo, disk, instancename, ip'
    if params[0] == 'c':
        
        mode = params[0]
        instanceId = params[1]
        cpus = params[3]
        memo = params[4]
        disk = params[5]
        ip = '192.168.122.' + params[1]
        instanceName = 'centos_' + params[1]
        message = mode + ',' + instanceId + ',' + cpus + ',' + memo + ',' + disk + ',' + instanceName + ',' + ip

    # when deleting a VM
    # message: 'd,instanceid, instancename, ip'
    elif params[0] == 'd':

        mode = params[0]
        instanceId = params[1]
        ip = '192.168.122.' + params[1]
        instanceName = 'centos_' + params[1]
        message = mode + ',' + instanceId + ',' + instanceName + ',' + ip

    # else
    else: 
        message = request

    print "send message to %s" % message
    return message
          
# update the status of table resourceinfo
# status :
# 0: request, 1: creating, 2: using, 3: deleting, 4: used 
def updateStatusOfResourceInfo(taskMessage):

    params = taskMessage.split(',')

    if params[0] == 'c':

        # status : inserting
        dba.updateResourceInfo(params[1], 1)

    elif params[0] == 'd':

        # status : deleting 
        dba.updateResourceInfo(params[1], 3)

    dba.commit()

def main():
    # get Dbaccessor instance
    global dba
    dba = Dbaccessor.Dbaccessor()

    # connect to the message queue server
    global connection
    global channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # confirm the target queue is existed. durable : message is saved for ever
    channel.queue_declare(queue='requestq', durable=True)

    print "[*] Waiting for messages. To exit press CTRL+C"

    # receive a message and treat with the massage received
    channel.basic_consume(callback, queue='requestq')

    channel.start_consuming()

    dba.closeConnection()

if __name__ == "__main__":
    main()

