
import pika
import Dbaccessor

class request():
    def __init__(self, mode, params):
        self.mode = mode
        self.params = params
        self.instanceId = 0
        self.dba = Dbaccessor.Dbaccessor()

    # send message to request queue
    def sendMessage(self):

        # connect to message queue server
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # confirm the target message queue is existed
        channel.queue_declare(queue='requestq', durable=True)
        
        # when creating a VM
        if self.mode == 'c':

            # search the idle machine
            idleMachineId = self.dba.getIdleMachineId(self.params)
            if idleMachineId != 0:
                
                # get instance id
                self.instanceId = self.dba.getInstanceId()   
                # get messagebody
                messagebody = self.mode + ',' + str(self.instanceId) + ',' + str(idleMachineId) +  ',' + self.params
                # insert a record into resourceinfo
                self.dba.insertResourceInfo(messagebody) 
                self.dba.commit()
                self.dba.closeConnection()

                ret = self.instanceId

            else:
                print "sorry, not enough resources!"
                return -1

        # when deleting a VM
        elif self.mode == 'd':

            # search the target machine
            delMachineId = self.dba.getMachineId(self.params)
            if delMachineId != 0:
                
                # if target instanceid is existed
                messagebody = self.mode + ',' + self.params + ',' + str(delMachineId)
                ret = 0

            else:

                print "sorry, no such instanceid !"
                return -1
 
        # send message
        channel.basic_publish(exchange='',
                          routing_key='requestq',
                          body=messagebody,
                          properties=pika.BasicProperties(delivery_mode=2,))

        print "[x] Sent message %s" % messagebody

        connection.close()
        
        return ret

if __name__ == '__main__':

    obj = request('c', '2,1000,4096')
    # obj = request('d', '2')

    print "return code: %s " % obj.sendMessage()
