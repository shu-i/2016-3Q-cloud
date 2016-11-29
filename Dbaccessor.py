# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import errorcode

# DB accessor
class Dbaccessor:

    def __init__(self):
        try:
            # get database connection
            self.connector = mysql.connector.connect(host="localhost", db="ssxz", user="s_user1", passwd="Qwer1234@", charset="utf8") 
        except mysql.connector.Error as e:
            print "can't get db connection: {}".format(e)
      
    # insert a record into resourceinfo
    def insertResourceInfo(self, request):
        try:
            params = request.split(',')
            cursor = self.connector.cursor() 
            cursor.execute("insert into resourceinfo (instanceid, machineid, cpus, memocapacity, diskcapacity) \
                            values (%s, %s, %s, %s, %s)",
                          (params[1], params[2], params[3], params[4], params[5]))
            cursor.close()
        except mysql.connector.Error as e:
            print "insert error: %s : %s" % (e.errno, e.msg)

    # insert a record into sshkey
    def insertSshKey(self, result):
        try:
            params = result.split(',')
            instancename = params[1].replace("[","").replace("]","")
            cursor = self.connector.cursor() 
            cursor.execute("insert into sshkey (instancename, sshkey) \
                            values (%s, %s)",
                          (instancename, params[2]))
            cursor.close()
        except mysql.connector.Error as e:
            print "insert error: %s : %s" % (e.errno, e.msg)
 
    # get resource info
    def getStatus(self, instanceid):
        try:
            status = 0
            cursor = self.connector.cursor() 
            cursor.execute("select status from resourceinfo where instanceid=%s" % instanceId)
            result = cursor.fetchall()
            for record in result:
                status = record[0]
            cursor.close()
        except mysql.connector.Error as e:
            print "select error: %s : %s" % (e.errno, e.msg)
            
        return status

    # get machine id
    def getMachineId(self, instanceId):
        try:
            machineId = 0
            cursor = self.connector.cursor() 
            cursor.execute("select machineid from resourceinfo where instanceid=%s" % instanceId)
            result = cursor.fetchall()
            for record in result:
                machineId = record[0]
            cursor.close()
        except mysql.connector.Error as e:
            print "select error: %s : %s" % (e.errno, e.msg)
            
        return machineId


    # get idle machine id
    def getIdleMachineId(self, message):
        try:
            idleMachine = 0
            params = message.split(',')
            cursor = self.connector.cursor() 
            cursor.execute("select a.machineid, a.cpus, a.memocapacity as totalmemo, \
            a.diskcapacity as totaldisk, ifnull(b.memocapacity,'0'), \
            ifnull(b.diskcapacity, '0') from totalinfo a left join \
            (select machineid, sum(memocapacity) as memocapacity, \
            sum(diskcapacity) as diskcapacity from resourceinfo \
            where status <> 4 group by machineid order by machineid) b \
            on a.machineid = b.machineid")

            result = cursor.fetchall()
            maxRemainder = 0
            remainder = 0
            for record in result:

                # find the idle machine
                # if cpus >= requestedcpus and
                # totalmemory - usedmemory >= requestedmemory and
                # totaldisk - useddisk >= requesteddisk
                remainder = int(record[3]) - int(record[5])
                print 'remainder,maxRemainder:%s, %s' % (remainder, maxRemainder)
                if (int(record[1]) >= int(params[0])) and \
                (int(record[2]) - int(record[4]) >= int(params[1])) and \
                (remainder >= int(params[2])):

                    # find the machine with max space
                    if maxRemainder < remainder:
                        idleMachine = record[0]
                        maxRemainder = remainder

            cursor.close()

        except mysql.connector.Error as e:
            print "select error: %s : %s" % (e.errno, e.msg)

        return idleMachine

    # update resource info
    def updateResourceInfo(self, instanceid, status):
        try:
            cursor = self.connector.cursor() 
            cursor.execute("update resourceinfo set status=%s where instanceid=%s", (status, instanceid)) 
            cursor.close()
        except mysql.connector.Error as e:
            print "update error: %s : %s" % (e.errno, e.msg)

    # get instance id from sequence 
    def getInstanceId(self):
        try:
            instanceid = 0
            cursor = self.connector.cursor() 
            cursor.execute("select nextval('imageid')")
            result = cursor.fetchall()
            for record in result:
                instanceid = record[0]
            cursor.close()

        except mysql.connector.Error as e:
            print "update error: %s : %s" % (e.errno, e.msg)

        return instanceid

    # commit
    def commit(self):
        self.connector.commit()

    # close connection
    def closeConnection(self):
        self.connector.close()

if __name__ == "__main__":
    test=Dbaccessor()
    a=test.selectResourceInfo(1)
    print("--status--")
    print(a)
    test.closeConnection()

