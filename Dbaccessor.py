# -*- coding: utf-8 -*-
# author: shu
import mysql.connector

# DB accessor
class Dbaccessor:

  def __init__(self):
      # get database connection
      self.connector = mysql.connector.connect(host="localhost", db="ssxz", user="s_user1", passwd="s_user1", charset="utf8") 
      
  # insert record into resourceinfo
  def insertResourceInfo(self, machineid, aeraid, capacity, status):
      cursor = self.connector.cursor() 
      cursor.execute("insert into resourceinfo values(%s, %s, %s, %s)", (machineid, aeraid, capacity, status))
      cursor.close()
      
  # get resource info
  def selectResourceInfo(self, machineid, aeraid):
      cursor = self.connector.cursor() 
      cursor.execute("select status from resourceinfo where machineid=%s and aeraid=%s", (machineid, aeraid))
      result = cursor.fetchall()
      status = result[0][0]
      cursor.close()
      return status

  # update resource info
  def updateResourceInfo(self, machineid, aeraid, status):
      cursor = self.connector.cursor() 
      cursor.execute("update resourceinfo set status=%s where machineid=%s and aeraid=%s", (status, machineid, aeraid)) 
      cursor.close()

  # delete resource info
  def deleteResourceInfo(self, machineid, aeraid):
      cursor = self.connector.cursor() 
      cursor.execute("delete from resourceinfo where machineid=%s and aeraid=%s", (machineid, aeraid))
      cursor.close()

  # commit
  def commit(self):
      self.connector.commit()

  # close connection
  def closeConnection(self):
      self.connector.close()

#test=Dbaccessor()
#a=test.selectResourceInfo(1,1)
#print("--status--")
#print(a)
#test.insertResourceInfo(2,1,1000,1)
#test.updateResourceInfo(2,1,2)
#test.deleteResourceInfo(2,1)
#test.commit()
#test.closeConnection()

