


-- SQL FINAL EXAM--


#1.A)Display all professors whose salary is greater than the average budget of all the departments (1
select name  from instructor where salary>(select avg(Budget) from department);
#1.B) Display the name of the department that has budget of more than 50000 (1 Mark)
select department from department where budget>50000;
#1.C) Display the ID of those instructors who have an ID length of 6 characters (1 Mark)
select instructorid from instructor where length(instructorid)>6;
#1.D) Display the name of all instructors with their respective department name and budget. (1Mark)
select name ,department,budget from instructor i join department d on i.department= d.department;
#Display all the details of instructors whose department name contains the word ‘science’ (1Mark)
select * from instructor where department like ('%science%');


#2.A) Display the name of students along with their respective score city of residence (1 Mark)
select s_name,m.score,d.address_city from student s join marks m join details d where m.s_id = s.s_id and d.school_id= m.school_id;
#2.B) Display the name of all the students and their corresponding email id. Fetch the names of those students as well who does not have an email address provided (1 Mark)
select s_name,d.email_ID from student s  
left join marks m on m.s_id = s.s_id
left join details d on d.school_id= m.school_id;
#2.C)Display the number students who have passed or failed respectively
select count(s_id) from marks group by status;
#2.D) Display name and email address of the student who is an 'IMO finalist' (1 Mark)
select s_name,d.email_ID  from 
student s join marks m on m.s_id = s.s_id 
join details d on d.school_id= m.school_id
where d.accomplishments like('%IMO%');
#Display the name of distinct cities where the students reside 
select distinct d.address_city  from 
student s join marks m on m.s_id = s.s_id 
join details d on d.school_id= m.school_id;


#3.A) Display the score of those students who have scored more marks than that of student with student_id 6. (1 Mark)
select score from marks where score>(select score from marks where s_id =6);
#3.B) Display the number of unique schools in the schema (1 Mark)
select count(distinct(school_id)) from marks;
#3.C) Display the number of students who reside in Bangalore (1 Mark)
select count(*) from marks where school_id in (select school_id from details where address_city like('%Banglore%'));
#3.D) Display the name of those students who has the character ‘s’ as the second lastcharacter in their name. (1 Mark)
select s_name from student where s_name like ('%s_');
#3 E)Display the first two letters of all the student names (1 Mark)
select substring(s_name,1,2) from student;


#Question 4

#Display the email address of those students who have the word ‘Geek’ mentioned in their accomplishments
select email_ID from DETAILS where accomplishments like('%Geek%');
#Display name and status of those students who has a school id in any of the following -1004, 1012 ,1016 (1Mark)
select name,m.status from student s join marks m on s.s_id = m.sid where s.s_id in ('1004','1002','1016');
#4.C) Display name and score of the students who have scored marks between 80 and 90 (1 Mark)
select name,m.Score from student s join marks m on s.s_id = m.sid where m.Score between 80 and 90;
#4.D) Write a query to display '1st Division' for students who have scored more than 90, '2nd Division' for those who have scored more than 70 and '3rd Division' for those who have scored more than 50 else display 'Fail'.
select s_id,
case 
 when score >90 then '1st Division'
 when score between 70 and 80 then '2nd Division'
when score between 50 and 70 then '3rd Division'
 else 'Fail'
 end as 'Divisions'
from marks ; 
#4.E) Write a query to fetch the average marks scored by all students (1 Mark)
select avg(score) from marks ;



-- Quest 5 : Display department wise headcount.
select department_id,count(employee_id) as 'head_count' from EMPLOYEE group by department_id;
#Display the department name along with department id and headcount
select department_name,e.department_id,count(employee_id) as 'head_count' from EMPLOYEE e left join  DEPARTMENT d on e.department_id=d.department_id group by e.department_id;
# Display the department whose headcount is greater than 3.
select department_name,e.department_id,count(employee_id) as 'head_count' from DEPARTMENT d left join EMPLOYEE e on d.department_id=e.department_id where count(employee_id)>3 group by e.department_id;
#Display the minimum, maximum, and average salary of employees in each department. (2Marks)
select min(salary) as 'Min Salary' ,max(salary) as 'Max Salary' ,avg(salary) as 'Avg Salary',e.department_id,department_name from EMPLOYEE e left join  DEPARTMENT d on e.department_id=d.department_id group by e.department_id;
#Display how many employees are getting same salary
select count(employee_id) as 'Same Salaried Count' from EMPLOYEE where salary in(select salary from  EMPLOYEE);
#Display department name, total employees, average salary, sum of salaries department wise where number of employees are greater than 2. Arrange the dataset by department name wise in ascending order.
select department_name,e.department_id,count(employee_id) as ' total employees' ,avg(salary) as 'Avg salary ' , sum(salary) as 'Sum of Salary' from EMPLOYEE e join  DEPARTMENT d on e.department_id=d.department_id where count(employee_id)>2 group by e.department_id order by department_name asc ;
#Display hiredate for all the employees in 'June 17,1999' format.
select date_format(hire_date,'%M%d','%Y') from EMPLOYEE;
#Display employees first_name, salary and their grade as per the below mentioned criteria
#<5000 'Grade 3',>5000 and <15000 'Grade 2'otherwise Grade3
select first_name,salary,
case 
 when salary <5000 then 'Grade3'
 when salary between 5000 and 1000 then 'Grade2'
 else 'Grade1'
 end as 'Grade'
from EMPLOYEE; 
#Display last_name and first_name of employees whose last name starts with J and arrange data in ascending order by last name in alphabetic series after J 
select last_name,first_name from EMPLOYEE where last_name like('J%') order by last_name asc;



-- Question 6: Use Employees and Department tables same as in previous section along with the below mentioned table
#A)Display all the employees who have their manager and department matching with the employee having an Employee ID of 121 or 200 but not 121 or 200 using subquery. 
select	*  from EMPLOYEE where manager_id in(select manager_id where employee_id in ('121','200')) and department_id in(select department_id where employee_id in ('121','200')) and employee_id not in ('120','121');
#B)Display 5th highest salary of employee using subquery 
select salary from EMPLOYEE where salary in (select salary from EMPLOYEE order by desc limit 4,1);
#C)Display name of employee, job and salary where salary greater than 100 and less than 10000 and department between 10 and 20 using subquery. 
select  concat(first_name,'  ', last_name)  as 'name' ,job_id,salary from EMPLOYEE where salary in (select salary from EMPLOYEE where salary between 100 and 10000) and department_id in (select department_id from EMPLOYEE where department_id between 10 and 20);
#D)Write a query to insert values in New_Employees which we have already created from employees table where employee id is whose salary >10000 using subquery
insert into New_Employees  ( select *  from EMPLOYEE where salary>10000 );
#E)Display the employee number, name (first name and last name) and job title for all employees whose salary is smaller than any salary of those employees whose job title is MK_MAN using subquery. 
select  employee_id,concat(first_name,'  ', last_name)  as 'name',job_id  from EMPLOYEE where salary <(select salary from EMPLOYEE where job_tiltle like('%MK_MAN%'));





