import psycopg2
import Backend.Helper as Helper
from Backend.Entities import *

Helper.DataBaseConnector.singleton=Helper.DataBaseConnector()
conn2 = Helper.DataBaseConnector.singleton.connection

def registerEmployer(employer,account):
    conn2 = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        insertQuery="INSERT INTO account(accountId,username,pass,userType) VALUES(%s,%s,%s,%s)"
        cur.execute("SELECT nextval('accountIdGenerator')")
        accountID= cur.fetchone()[0]
        values=(accountID,account.userName,account.password,account.userType)
        cur.execute(insertQuery,values)
        insertQuery = "UPDATE employer SET employerName = %s, employerPhone = %s, employerAddress = %s WHERE employerId = %s"
        values = (employer.employerName, employer.employerPhone,employer.employerAdress, accountID)
        cur.execute(insertQuery,values)
        conn2.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)



def registerEmployee(employee,account):
    conn2 = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        insertQuery="INSERT INTO account(accountId,username,pass,userType) VALUES(%s,%s,%s,%s)"
        cur.execute("SELECT nextval('accountIdGenerator')")
        accountID= cur.fetchone()[0]
        values=(accountID,account.userName,account.password,account.userType)
        cur.execute(insertQuery,values)
        insertQuery = "UPDATE employee SET employeeName = %s, employeeSurname = %s, employeePhone = %s, employeeAddress = %s where employeeId = %s"
        values = (employee.employeeName, employee.employeeSurname,employee.employeePhone,employee.employeeAddress, accountID)
        cur.execute(insertQuery,values)
        conn2.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def login(account):
    conn2 = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    try:
        print(account.userName) 
        print(account.password)
        query = "SELECT * FROM account"
        values = (account.userName, account.password)
        cur.execute(query,values) 
        print("assa")
        userType = cur.fetchone()
        print(userType)
        
        

        # print("all")
        # if(len(userType) == 0):
        #     print("Kullanici adi veya şifre yanlis")
        #     return False
        # else:
        #     if(userType[0][0] == "True"):
        #         print("Employee")
        #     else:
        #         print("Employer")
                

    except(Exception, psycopg2.DatabaseError) as error:
        print("za")
        print(error)
        print("xd")

# login(Account(0,"usernaeme","1234","false"))
# registerEmployer(Employer(0,"aktif","1234","bakirkoy"),Account(0,"usernaeme","1234","False"))