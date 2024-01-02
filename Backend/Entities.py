import psycopg2

class Account:
    def __init__(self,accountId,username,password,userType):
        self.accountId = accountId
        self.userName = username
        self.password = password
        self.userType = userType

        if(self.userName == ""):
            self.userName = None
        if(self.password == ""):
            self.password = None
        if(self.userType == ""): 
            self.userType = None
        

class Employee:
    def __init__(self,employeeId,employeeName,employeeSurname,employeePhone,employeeAddress):
        self.employeeId = employeeId
        self.employeeName = employeeName
        self.employeeSurname = employeeSurname
        self.employeePhone = employeePhone
        self.employeeAddress = employeeAddress
        
        if(employeeName == ""): 
            self.employeeName = None
        if(employeeSurname == ""):
            self.employeeSurname = None
        if(employeePhone == ""):
            self.employeePhone = None
        if(employeeAddress == ""):
            self.employeeAddress = None


class Employer:
    def __init__ (self,employerId,employerName,employerPhone,employerAdress):
        self.employerId = employerId
        self.employerName = employerName
        self.employerPhone = employerPhone
        self.employerAdress = employerAdress
        
        if(employerId == ""):
            self.employerId = None
        if(employerName == ""):
            self.employerName = None
        if(employerPhone == ""):
            self.employerPhone = None
        if(employerAdress == ""):
            self.employerAdress = None


class Education:
    def __init__(self,employeeId,schoolName,startDate,endDate,schoolType):
        self.employeeId = employeeId
        self.schoolName = schoolName
        self.startDate = startDate
        self.endDate = endDate
        self.schoolType = schoolType
        
        if(self.startDate == ""):
            self.startDate = None
        if(self.endDate == ""):
            self.endDate = None
        if(self.schoolName == ""):
            self.schoolName = None
        if(self.schoolType == ""):
            self.schoolType = None
    
class Experience:
    def __init__(self,employeeId,startDate,endDate,positionName,companyName):
        self.employeeId = employeeId
        self.startDate = startDate
        self.endDate = endDate
        self.positionName = positionName
        self.companyName = companyName
        
        if(self.startDate == ""):
            self.startDate = None
        if(self.endDate == ""):
            self.endDate = None
        if(self.positionName == ""):
            self.positionName = None
        if(self.companyName == ""):
            self.companyName = None
        
    def getExperience(self,employeeId):
        return self.employeeId
    
class Application:
    def __init__(self,employerId,applicationId,counter,applicationname,applciationdate,contracttype,positionname,description):
        self.employerId = employerId
        self.applicationId = applicationId
        self.counter = counter
        self.applicationname = applicationname
        self.applciationdate = applciationdate
        self.contracttype = contracttype
        self.positionname = positionname
        self.description = description
        if(self.counter == ""):
            self.counter = None
        if(self.applicationname == ""):
            self.applicationname = None
        if(self.applciationdate == ""):
            self.applciationdate = None
        if(self.contracttype == ""):
            self.contracttype = None
        if(self.positionname == ""):
            self.positionname = None
        if(self.description == ""):
            self.description = None
    