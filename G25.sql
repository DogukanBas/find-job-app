create table account(
	accountId int primary key,
	username varchar unique not null,
	pass varchar not null,
	userType bool not null,
	CONSTRAINT check_pass_length CHECK (LENGTH(pass) > 5 and LENGTH(pass) < 13)
);

create table employer(
	employerId int primary key references account(accountId) on delete cascade,
	employerName varchar,
	employerPhone varchar,
	employerAddress varchar,
	CONSTRAINT check_numeric_characters CHECK (employerPhone  ~ '^[0-9]+$')
);

create table employee(
	employeeId int primary key references account(accountId) on delete cascade,
	employeeName varchar,
	employeeSurname varchar,
	employeePhone varchar,
	employeeAddress varchar,
	CONSTRAINT check_numeric_characters CHECK (employeePhone  ~ '^[0-9]+$')
);

create table employee_education(
	employeeId int references employee(employeeId),
	schoolName varchar,
	startDate date,
	endDate date,
	schoolType varchar CHECK (schoolType In ('High School','Bachelors','Masters'))
	);
	
create table employee_experience(
	employeeId int references employee(employeeId),
	startDate date,
	endDate date,
	positionName varchar,
	companyName varchar);
	
create table applications(
	employerId int references employer(employerId),
	applicationId int primary key,
	counter int,
	applicationName varchar,
	applicationDate date,
	contractType varchar CHECK (contractType In ('Part Time','Full Time','Intern')),
	positionName varchar,
	description varchar,
	isActive bool
	);

create table appliedApplications(
	employeeId int references employee(employeeId),
	applicationId int references applications(applicationId),
	status varchar CHECK (status In ('waiting','rejected','approved','canceled')),
	coverLetter varchar,
	applicationDate date 
);

CREATE VIEW applicationView AS
SELECT
	aa.employeeId,
    app.applicationId,
    employer.employerName,
    app.counter,
    app.applicationName,
    app.applicationDate,
    app.contractType,
    app.positionName,
    app.description,
    aa.status,
    aa.coverLetter,
    aa.applicationDate AS appliedApplicationDate
FROM
    applications app
JOIN
    appliedApplications aa ON app.applicationId = aa.applicationId
join employer on employer.employerId = app.employerId;

CREATE VIEW applicantsView AS
SELECT
	aa.employeeId,
	aa.applicationId,
	aa.status,
	aa.coverLetter,
	aa.applicationDate,
	emp.employeeName,
	emp.employeeSurname,
	emp.employeePhone,
	emp.employeeAddress
FROM
    employee emp
JOIN
    appliedApplications aa ON emp.employeeId = aa.employeeId;


	
CREATE OR REPLACE FUNCTION createAccountFunction()
RETURNS TRIGGER AS $$
BEGIN
	case new.userType 
	   when False then insert into employer values(new.accountId,null,null,null);
	   when True then insert into employee values(new.accountId,null,null,null,null);
	 
   	end case;

   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER createAccountTrigger
AFTER INSERT ON account
FOR EACH ROW
WHEN (NEW.accountId IS NOT NULL)
EXECUTE FUNCTION createAccountFunction();


CREATE OR REPLACE FUNCTION increaseAdvertisementCounterFunction()
RETURNS TRIGGER AS $$
BEGIN
	update applications as adv set counter = counter + 1 where new.applicationId = adv.applicationId;

   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER increaseAdvertisementCounterTrigger
AFTER INSERT ON appliedApplications
FOR EACH ROW
WHEN (NEW.applicationId IS NOT NULL)
EXECUTE FUNCTION increaseAdvertisementCounterFunction();

create sequence accountIdGenerator start with 1 increment by 1 no cycle;
create sequence advertisementIdGenerator start with 1 increment by 1 no cycle;

create  type loginCheckType as (userType varchar, accountidd int);

CREATE OR REPLACE FUNCTION loginCheck(funcUsername varchar, funcPassword varchar)
RETURNS loginCheckType as $$

DECLARE 
loginInfo loginCheckType;
counter int :=0;
accountCheck cursor for select username,pass,userType,accountid from account ;
begin
    loginInfo.userType:='No such user';
	loginInfo.accountidd := -1;
    FOR account_row in accountCheck LOOP
    if(account_row.username=funcUsername and account_row.pass=funcPassword) THEN
        loginInfo.accountidd=account_row.accountid ;
        IF(account_row.userType = true) then
            loginInfo.userType='Employee';
        ELSE 
            loginInfo.userType='Employer';
        END IF ;
    END IF;
    END LOOP;
    return loginInfo;
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION deleteApplication(funcApplicationId int) 
returns void as $$
BEGIN
	UPDATE applications
	SET isActive = false
	WHERE applicationId = funcApplicationId;

	UPDATE appliedApplications
	SET status = 'canceled'
	WHERE applicationId = funcApplicationId;
	
END;
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION checkExistanceEducation(employeeId int,schoolname varchar,startdate date,enddate date,schooltype varchar)
returns bool as $$
DECLARE 
isExist bool;
exist_cursor CURSOR FOR SELECT * from employee_education;
BEGIN 
	isExist := false;
	FOR row_cursor in exist_cursor LOOP
		IF(employeeId = row_cursor.employeeId and schoolname = row_cursor.schoolname and startdate = row_cursor.startdate and enddate = row_cursor.enddate and schooltype = row_cursor.schooltype) THEN
			isExist := true;
		END IF;	
	END LOOP;
	RETURN isExist;
END;
$$ LANGUAGE 'plpgsql';
	


CREATE OR REPLACE FUNCTION checkExistanceExperience(employeeId int, startdate date, enddate date, positionname varchar, companyname varchar)
returns bool as $$
DECLARE 
isExist bool;
exist_cursor CURSOR FOR SELECT * from employee_experience;
BEGIN 
	isExist := false;
	FOR row_cursor in exist_cursor LOOP
		IF(employeeId = row_cursor.employeeId  and startdate = row_cursor.startdate and enddate = row_cursor.enddate and positionname = row_cursor.positionname and row_cursor.companyname = companyname) THEN
			isExist := true;
		END IF;	
	END LOOP;
	RETURN isExist;
END;
$$ LANGUAGE 'plpgsql';

insert into account values(nextval('accountidgenerator'),'bilal','123456',True);
insert into account values(nextval('accountidgenerator'),'hüseyin','123123',True);
insert into account values(nextval('accountidgenerator'),'berkan','asd123',True);
insert into account values(nextval('accountidgenerator'),'doğukan','654321',True);
insert into account values(nextval('accountidgenerator'),'said','123asd',True);
insert into account values(nextval('accountidgenerator'),'ahmet','12345678',True);
insert into account values(nextval('accountidgenerator'),'mehmet','asdfasdf',True);
insert into account values(nextval('accountidgenerator'),'mustafa','987654321',True);
insert into account values(nextval('accountidgenerator'),'ömer','1234asdf',True);
insert into account values(nextval('accountidgenerator'),'talha','asdf1234',True);

update employee set employeename = 'Bilal' , employeesurname = 'Müftüoğlu', employeePhone = '05435434343', employeeAddress = 'Bağcılar/İstanbul' where employeeId = 1;
update employee set employeename = 'Hüseyin' , employeesurname = 'Arıcı', employeePhone = '05555555555', employeeAddress = 'Kayaşehir/İstanbul' where employeeId = 2;
update employee set employeename = 'Berkan' , employeesurname = 'Eti', employeePhone = '05134568745', employeeAddress = 'Gaziosmanpaşa/İstanbul' where employeeId = 3;
update employee set employeename = 'Doğukan' , employeesurname = 'Baş', employeePhone = '05324567890', employeeAddress = 'Beylikdüzü/İstanbul' where employeeId = 4;
update employee set employeename = 'Said' , employeesurname = 'Görmez', employeePhone = '05433456785', employeeAddress = 'Esenler/İstanbul' where employeeId = 5;
update employee set employeename = 'Ahmet' , employeesurname = 'Dursun', employeePhone = '05431235432', employeeAddress = 'Esenyurt/İstanbul' where employeeId = 6;
update employee set employeename = 'Mehmet' , employeesurname = 'Efe', employeePhone = '05324560987', employeeAddress = 'Levent/İstanbul' where employeeId = 7;
update employee set employeename = 'Mustafa' , employeesurname = 'Güzel', employeePhone = '05063219647', employeeAddress = 'Beşiktaş/İstanbul' where employeeId = 8;
update employee set employeename = 'Ömer' , employeesurname = 'Diner', employeePhone = '05057469364', employeeAddress = 'Üsküdar/İstanbul' where employeeId = 9;
update employee set employeename = 'Talha' , employeesurname = 'Çelik', employeePhone = '05339743578', employeeAddress = 'Bahçelievler/İstanbul' where employeeId = 10;

insert into account values(nextval('accountidgenerator'),'bosch','boschpass',False);
insert into account values(nextval('accountidgenerator'),'soft','softpass',False);
insert into account values(nextval('accountidgenerator'),'yapıkredi','ykpass',False);
insert into account values(nextval('accountidgenerator'),'aselsan','aselsanpass',False);
insert into account values(nextval('accountidgenerator'),'tusaş','tusaşpass',False);
insert into account values(nextval('accountidgenerator'),'baykar','baykarpass',False);
insert into account values(nextval('accountidgenerator'),'akbank','akbankpass',False);
insert into account values(nextval('accountidgenerator'),'arçelik','arçelikpass',False);
insert into account values(nextval('accountidgenerator'),'vodafone','vodafonepass',False);
insert into account values(nextval('accountidgenerator'),'roketsan','roketsanpass',False);

update employer set employername = 'Bosch' , employerphone = '02163456789', employeraddress = 'Maltepe/İstanbul' where employerId = 11;
update employer set employername = 'Softtech' , employerphone = '02126579867', employeraddress = 'Maslak/İstanbul' where employerId = 12;
update employer set employername = 'Yapıkredi' , employerphone = '02624569876', employeraddress = 'Gebze' where employerId = 13;
update employer set employername = 'Aselsan' , employerphone = '03123459546', employeraddress = 'Ankara' where employerId = 14;
update employer set employername = 'Tusaş' , employerphone = '02124568435', employeraddress = 'Teknopark/YTÜ' where employerId = 15;
update employer set employername = 'Baykar' , employerphone = '02129456794', employeraddress = 'Hadımköy' where employerId = 16;
update employer set employername = 'Akbank' , employerphone = '02168357648', employeraddress = 'Maltepe' where employerId = 17;
update employer set employername = 'Arçelik' , employerphone = '0212845737', employeraddress = 'İstanbul' where employerId = 18;
update employer set employername = 'Vodafone' , employerphone = '02126842578', employeraddress = 'Beşiktaş' where employerId = 19;
update employer set employername = 'Roketsan' , employerphone = '03123977364', employeraddress = 'Ankara' where employerId = 20;

insert into employee_education values(1,'Yıldız Teknik Üniversitesi','2020-08-10','2025-06-06','Bachelors');
insert into employee_education values(1,'Gelenbevi Anadolu Lisesi','2016-09-10','2020-05-04','High School');
insert into employee_education values(2,'İstanbul Üniversitesi','2020-08-10','2025-06-06','Bachelors');
insert into employee_education values(2,'Yaşar Acar Fen Lisesi','2016-09-10','2020-05-04','High School');
insert into employee_education values(3,'İstanbul Teknik Üniversitesi','2021-10-11','2025-06-07','Bachelors');
insert into employee_education values(3,'Çapa Fen Lisesi','2017-09-09','2021-05-06','High School');
insert into employee_education values(4,'Boğaziçi Üniversitesi','2020-08-10','2025-06-06','Bachelors');
insert into employee_education values(4,'Boğaziçi Üniversitesi','2026-09-07','2027-07-06','Masters');
insert into employee_education values(6,'Aydın Üniversitesi','2022-08-10','2026-05-04','Bachelors');
insert into employee_education values(8,'Marmara Üniversitesi','2019-03-04','2025-02-03','Bachelors');

insert into employee_experience values(1,'2019-01-01','2022-01-01','Software Developer','Google');
insert into employee_experience values(1,'2022-01-01','2022-08-08','Backend Developer','Microsoft');
insert into employee_experience values(2,'2023-05-08','2023-08-09','Frontend Developer','Meta');
insert into employee_experience values(2,'2020-02-03','2021-03-02','Project Manager','Amazon');
insert into employee_experience values(3,'2023-01-01','2024-01-01','Control Engineer','THY');
insert into employee_experience values(4,'2017-01-01','2020-02-02','RPA Developer','Twitter');
insert into employee_experience values(5,'2011-09-10','2013-01-06','Calibration Engineer','Vestel');
insert into employee_experience values(6,'2022-06-03','2022-06-06','AI Engineer','Tüpraş');
insert into employee_experience values(7,'2024-01-01','2024-02-03','Data Scientist','Turkcell');
insert into employee_experience values(8,'2021-01-03','2023-03-03','Software Developer','Aselsan');

insert into applications values(11,nextval('advertisementidgenerator'),0,'Bosch Software Developer','2023-01-01','Part Time','Software Developer','Bosch Software Developer',True);
insert into applications values(11,nextval('advertisementidgenerator'),0,'Bosch Hardware Specialist','2022-05-10','Part Time','Software Developer','Bosch Hardware Specialist',True);
insert into applications values(11,nextval('advertisementidgenerator'),0,'Bosch System Analyst','2023-04-02','Full Time','System Analyst','Bosch System Analyst',True);
insert into applications values(11,nextval('advertisementidgenerator'),0,'Bosch Software Intern','2022-10-01','Intern','Software Intern','Bosch Software Intern',True);
insert into applications values(12,nextval('advertisementidgenerator'),0,'Softtech Software Developer','2023-12-09','Full Time','Software Developer','Softtech Software Developer',True);
insert into applications values(12,nextval('advertisementidgenerator'),0,'Softtech ERP Developer','2024-01-01','Part Time','ERP Developer','Softtech ERP Developer',True);
insert into applications values(13,nextval('advertisementidgenerator'),0,'Yapıkredi Software Intern','2023-10-10','Intern','Software Intern','Yapıkredi Software Intern',True);
insert into applications values(13,nextval('advertisementidgenerator'),0,'Yapıkredi Software Developer','2023-11-01','Full Time','Software Developer','Yapıkredi Software Developer',True);
insert into applications values(14,nextval('advertisementidgenerator'),0,'Aselsan Embedded System Engineer','2023-10-10','Full Time','Embedded System Engineer','Aselsan Embedded System Engineer',True);
insert into applications values(14,nextval('advertisementidgenerator'),0,'Aselsan Software Developer','2023-09-08','Full Time','Software Developer','Aselsan Software Developer',True);

insert into appliedApplications values(1,1,'waiting','I am a software developer','2024-01-13');
insert into appliedApplications values(2,1,'waiting','I am a very good software developer','2023-10-11');
insert into appliedApplications values(3,1,'waiting','I am a master software developer','2023-09-12');
insert into appliedApplications values(1,4,'waiting','I want to attend internship program','2023-08-10');
insert into appliedApplications values(1,5,'waiting','I am a software developer','2023-07-11');
insert into appliedApplications values(2,5,'waiting','I am a very good software developer','2023-06-12');
insert into appliedApplications values(3,5,'waiting','I am a master software developer','2023-05-13');
insert into appliedApplications values(4,7,'waiting','I want to attend internship program','2023-04-14');
insert into appliedApplications values(4,8,'waiting','I am a software developer','2023-03-15');
insert into appliedApplications values(5,8,'waiting','I am a very good software developer','2023-02-16');
insert into appliedApplications values(5,9,'waiting','I am a embedded software engineer','2023-01-17');
