
import psycopg2
class Account:
    def __init__(self,accountId,username,password,userType):
        self.accountId = accountId
        self.userName = username
        self.password = password
        self.userType = userType


class Employee:
    def __init__(self,employeeId,employeeName,employeeSurname,employeePhone,employeeAddress):
        self.employeeId = employeeId
        self.employeeName = employeeName
        self.employeeSurname = employeeSurname
        self.employeePhone = employeePhone
        self.employeeAddress = employeeAddress

class Employer:
   
    def __init__ (self,employerId,employerName,employerPhone,employerAdress):
        self.employerId = employerId
        self.employerName = employerName
        self.employerPhone = employerPhone
        self.employerAdress = employerAdress
class Experience:
    def __init__(self,employeeId,startDate,endDate,positionName,companyName):
        self.employeeId = employeeId
        self.startDate = startDate
        self.endDate = endDate
        self.positionName = positionName
        self.companyName = companyName

    def getExperience(self,employeeId):
        
        return self.employeeId
    
