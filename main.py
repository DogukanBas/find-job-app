import psycopg2
from sql_servis import *
import Helper
from Entities import *

#

# #connect to the database
Helper.DataBaseConnector.singleton=Helper.DataBaseConnector()
# registerEmployer(Employer(0,"BOSCH","1234","bakirkoy"),Account(0,"usernaeme","1234","False"))
# registerEmployee(Employee(0,"ahmet","yilmaz","1234","bakirkoyadrsi"),Account(0,"usernaeme11","1234","True"))
# registerEmployee(Employee(0,"ahmet","yilmaz","1234","bakirkoyadrsi"),Account(0,"usernaemee1121","1234","True"))
registerEmployer(Employer(0,"aktif","1234","bakirkoy"),Account(0,"usernaeme","1234","False"))
login(Account(0,"usernaeme","1234","false"))