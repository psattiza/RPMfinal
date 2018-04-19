# RPMFinal
Robot Planning and Manipulation Project
by Tiffany Kalin, Jane Lockshin, and Paul Sattizahn

## Install
with apt-get or similar:
+ install swig and gmp (libgmp3-dev on ubuntu)
+ install python and pip (2 or 3 should work)
+ install pysmt with pip `$ pip install pysmt`
this also installs  pysmt-install utility

install yices:
+ `$ pysmt-install --yices`

+ `$ pysmt-install --env`
returns environment variable to add.
Add to bachrc or run export in current shell

+ `$ pysmt-install --check`
 verify install. Should see that yices is installed and in python path
 yices     True

To run:
+ `$ python plan.py`
       or
+ `$ python3 plan.py`



## Help

For help on options:
+ `python3 plan.py -h`

## Config files

### Curriculum 
Define required and elective courses `--curriculum`   
Each row contains a set of courses required in the form:  
  `#name, #number_required, #num_credits, #Course1, #Course2, ... `  
If number_required is -1, then all the courses in the row are required for
the curriculum. Otherwise at least that number of courses from this row must
be taken.
num_credits defines how many credits elements of this row constraints

### Courses
Define properties of a course `--courses`  
Each line defines a course in the form:  
`#name, #credit_hours, #numPreReqs, [#prereq1, #prereq2.1 #prereq2.2, ...], #numCoReqs, [#coreq1, #coreq2.1 #coreq2.2, ...]`  
if numPreReqs or numCoReqs is zero, no pre/coreqs follow
If a pre/coreq cell has multiple elements, one of the courses in that cell
must be taken to satisfy the pre/coreq

### Schedule
Define when courses are scheduled `--schedule`    
The first line is a list of semesters included in the schedule  
+ the semester names should be in chronological order
+ semesters that start with f are marked as fall
+ semesters that start with s are marked as spring   
 
All the following lines define the semesters a course is offered in form:  
`#name, #semester1 #semester2`  
If the second field matches:  
+ a: match for all semesters
+ f: match all semester beginning with a f as fall semesters
+ s: match all semesters beginning with a s as spring semesters

### Student
Define student information and prefrences `--student`  
Contain 3 lines:  
+ List of classes already taken separated by space  
+ #minCreditHours, #maxCreditHours  
+ #numSemesters  
