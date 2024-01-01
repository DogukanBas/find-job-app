import psycopg2
import Backend.Helper as Helper
from Backend.Entities import *
from psycopg2.errors import *

yeni 

Helper.DataBaseConnector.singleton = Helper.DataBaseConnector()
def registerEmployer(employer,account):
    if(employer.employerName == None) :
        return "Name cannot be empty."
    conn = Helper.DataBaseConnector.singleton.connection
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
        conn.commit()

    except( psycopg2.errors.UniqueViolation) as error:
        print("UniqueViolation" + employer.employerName + " " + employer.employerPhone + " " + employer.employerAdress)
        conn.rollback()
        return "The username already taken. Please try another one."
    
    except( psycopg2.errors.NotNullViolation) as error2:
        print("NotNullViolation")
        conn.rollback()
        return "Username and password cannot be empty."    
    
    except( psycopg2.DatabaseError) as error:
        print("Transaction")
        print(error)
        conn.rollback()
        return ("Unvalid Phone Number. Please try again.")
    except(Exception) as error:
        print(error)
        conn.rollback()
        return "Unknown error"
    
    return True


def registerEmployee(employee,account):
    if (employee.employeeName == None or employee.employeeSurname == None):
        return "Name and Surname cannot be empty."
     
        
    ##check password in sql

    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    # set save point
    try:
        insertQuery="INSERT INTO account(accountId,username,pass,userType) VALUES(%s,%s,%s,%s)"
        cur.execute("SELECT nextval('accountIdGenerator')")
        accountID= cur.fetchone()[0]
        values=(accountID,account.userName,account.password,account.userType)
        cur.execute(insertQuery,values)
        insertQuery = "UPDATE employee SET employeeName = %s, employeeSurname = %s, employeePhone = %s, employeeAddress = %s where employeeId = %s"
        values = (employee.employeeName, employee.employeeSurname,employee.employeePhone,employee.employeeAddress, accountID)
        cur.execute(insertQuery,values)
        conn.commit()
    except(psycopg2.errors.UniqueViolation) as error:
        print("UniqueViolation")
        conn.rollback()
        return "The username already taken. Please try another one."
    
    except( psycopg2.errors.NotNullViolation) as error2:
        print("NotNullViolation")
        conn.rollback()
        return "Username and password cannot be empty."   
    
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("Transaction")
        conn.rollback()
        return ("Unvalid Phone Number. Please try again.")
    
    return True


def loginCheck(account):
    if(account.userName is None or account.password is None):
        print("returned")
        return "Username and password cannot be empty."
    conn = Helper.DataBaseConnector.singleton.connection
    cur = Helper.DataBaseConnector.singleton.cursor
    
    try:
        print(account.userName) 
        print(account.password)
        query = "SELECT userType FROM account where username = %s and pass = %s"
        values = (account.userName, account.password)
        cur.execute(query,values) 
        userType = cur.fetchone()
        
        if(userType == None):
            print("No such user")
            return "No such user"
        
        else:
            if(userType[0] == "True"):
                return "Employee"
            else:
                return "Employer"
                
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return error


        

# login(Account(0,"usernaeme","1234","false"))
# registerEmployer(Employer(0,"aktif","1234","bakirkoy"),Account(0,"usernaeme","1234","False"))