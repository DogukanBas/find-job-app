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
    def __init__(self,employerId,applicationId,counter,applicationName,applicationDate,contractType,positionName,description):
        self.employerId = employerId
        self.applicationId = applicationId
        self.counter = counter
        self.applicationName = applicationName
        self.applicationDate = applicationDate
        self.contractType = contractType
        self.positionName = positionName
        self.description = description
        
        if(self.counter == ""):
            self.counter = None
        if(self.applicationName == ""):
            self.applicationName = None
        if(self.applicationDate == ""):
            self.applicationDate = None
        if(self.contractType == ""):
            self.contractType = None
        if(self.positionName == ""):
            self.positionName = None
        if(self.description == ""):
            self.description = None


class Filter:
    def __init__(self,dateFilter,applicationNameFilter,companyNameFilter,positionNameFilter,contractTypeFilter):
        self.dateFilter = dateFilter # 1 : ascending, 2 : descending
        self.applicationNameFilter = applicationNameFilter 
        self.companyNameFilter = companyNameFilter
        self.positionNameFilter = positionNameFilter
        self.contractTypeFilter = contractTypeFilter
        
        if(self.dateFilter == ""):
            self.dateFilter = None
        if(self.applicationNameFilter == ""):
            self.applicationNameFilter = None
        if(self.companyNameFilter == ""):
            self.companyNameFilter = None
        if(self.positionNameFilter == ""):
            self.positionNameFilter = None
        if(self.contractTypeFilter == ""):
            self.contractTypeFilter = None