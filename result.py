
import pika
import Dbaccessor

#---------------------------
# worker function
def callback(ch, method, properties, messagebody):
    print " [*] Received %r" % (messagebody,)

    ch.basic_ack(delivery_tag = method.delivery_tag)

    # get result message
    resultMessage = getMessage(messagebody)

    # save ssh key
    params = resultMessage.split(',')
    if params[0] == 'c':
        dba.insertSshKey(messagebody)
        
    # update table resourceinfo
    updateStatusOfResourceInfo(resultMessage)

# update the status of table resourceinfo
# status :
# 0: request, 1: creating, 2: using, 3: deleting, 4: used 
def updateStatusOfResourceInfo(resultMessage):

    params = resultMessage.split(',')

    instancename = params[1].replace("[","").replace("]","")
    if params[0] == 'c':

        # status : inserting
        dba.updateResourceInfo(instancename, 2)

    elif params[0] == 'd':

        # status : deleting 
        dba.updateResourceInfo(instancename, 4)

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
    channel.queue_declare(queue='resultq', durable=True)

    print "[*] Waiting for messages. To exit press CTRL+C"

    # receive a message and treat with the massage received
    channel.basic_consume(callback, queue='resultq')

    channel.start_consuming()

    dba.closeConnection()

if __name__ == "__main__":
    main()

