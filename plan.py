#pysmt needs to be installed
from pysmt.shortcuts import Symbol, LE, GE, And, Int, Or, Iff, Implies, ExactlyOne, FALSE, TRUE, Not, get_model, get_unsat_core, is_sat, is_unsat, Plus, Equals, Real, Times
from pysmt.typing import INT, REAL

#come with python
import argparse
import random

#local import
import read as r

def course (name, semester):
	return Symbol("taken_%s_%d" % (name, semester), REAL)


parser = argparse.ArgumentParser(description='Course planning with some help from pySMT')
parser.add_argument('--cirriculum', metavar='cir', type=str, default="cirriculum.csv",
                    help='specifies filepath to cirriculum csv file, default "cirriculum.csv"')
parser.add_argument('--courses', metavar='c', type=str, default="courses.csv",
                    help='specifies filepath to courses csv file, default "courses.csv"')
parser.add_argument('--schedule', metavar='s', type=str, default="schedule.csv",
                    help='specifies filepath to class shedule csv file, default "schedule.csv"')
parser.add_argument('--student', metavar='s', type=str, default="student.csv",
                    help='specifies filepath to student csv file, default student.csv')
args = parser.parse_args()

#print(args)

#Default values
min_credit_hours = 6.0
max_credit_hours = 10.5
semesters_remaining = 8


every_course, credit_hours, prereqs, coreqs = r.readPreCoReq(args.courses)
courses, electives = r.readCirriculum(args.cirriculum)

fall, valid_falls, spring, valid_springs, other, map_semester_to_number  = r.readSchedule(args.schedule)

already_taken, min_credit_hours, max_credit_hours, semesters_remaining = r.readStudent(args.student)

'''
already_taken = []
courses = ["epic151", "ebgn201", "math111", "csci101",
 "csm101", "math112", "phgn100", "csci261", "csci262", "math201",
 "math213", "csci341", "phgn200", "chgn121", "csci403",
 "csci400", "csci306"]
electives = [
  [1, 4, "chgn122", "cben110", "chgn125", "gegn101"],
  [2, 0.5, "pagn201", "pagn102", "pagn207", "pagn210"],
  [3, 3, "csci404", "csci440", "csci446", "csci445"]
]
credit_hours = {
	"epic151": 3,
	"ebgn201": 3,
	"math111": 4,
	"csci101": 3,
	"csm101": 0.5,
	"math112": 4,
	"phgn100": 4.5,
	"csci261": 3,
	"csci262": 3,
	"math201": 3,
	"math213": 4,
	"csci341": 3,
	"phgn200": 4.5,
	"chgn121": 4,
	"csci403": 3,
	"csci400": 3,
	"csci306": 3,
}
prereqs = {
   "math112": ["math111"],
   "phgn100": ["math111"],
   "math201": ["math112"],
   "csci262": ["csci261"],
   "math213": ["math112"],
   "csci404": ["csci262", "math201"],
   "csci341": ["csci261"],
   "phgn200": ["phgn100"],
   "chgn122": ["chgn121"],
   "chgn125": ["chgn125"],
   "csci440": ["csci341", "csci261"],
   "csci445": ["csci262"],
   "csci446": ["csci445"],
   "csci400": ["csci306"],
   "csci403": ["csci262"],
   "csci306": ["csci262"]
}

coreqs = {
    "phgn100": ["math112"],
	"csci341": ["csci262"],
	"phgn200": ["math213"],
	"csci445": ["csci403"],
	"csci446": ["csci400"]
}

fall = ["csci445"] #list of fall
spring = ["csci404", "pagn102"] #list of spring
other = { #hash table poRealing to array of right semester
	"csci440": ["f2", "f3", "s4"],
	"csci446": ["s1", "s4"]
}

valid_falls=[0, 2, 4, 6]
valid_springs=[1, 3, 5, 7]

map_semester_to_number = {
	"f1": 0,
	"s1": 1,
	"f2": 2,
	"s2": 3,
	"f3": 4,
	"s3": 5,
	"f4": 6,
	"s4": 7
}
'''



all_credit_hours = credit_hours
for arr in electives:
	for c in arr[2:]:
		if c not in all_credit_hours:
			all_credit_hours[c] = arr[1]

taken_credits = 0
for t in already_taken:
	if t in all_credit_hours.keys():
		taken_credits += all_credit_hours[t]

total_credit_hours = 0
for c in courses:
	total_credit_hours += credit_hours[c]
for e in electives:
	total_credit_hours += (e[0]*e[1])

credit_hours_remaining = total_credit_hours - taken_credits


if (semesters_remaining != 0):

        while ((credit_hours_remaining / semesters_remaining) > max_credit_hours):
                semesters_remaining += 1
        
        while ((credit_hours_remaining / semesters_remaining) < min_credit_hours):
                semesters_remaining -=1
else:
        print("No more semesters needed.");

all_courses = []
for c in courses:
	all_courses.append(c)
for co in electives:
	for c in co[2:]:
		all_courses.append(c)

facts = TRUE()

#Range for classes, only one class per schedule
num_semesters = list(range(-1, semesters_remaining))
always_range = And([Or(Equals(course(c, b), Real(0)), Equals(course(c, b), Real(1))) for c in all_courses for b in num_semesters])

#Required classes need at least one class
all_classes = And([Equals(Plus([course(c, b) for b in num_semesters]), Real(1)) for c in courses])

#credit hours things
#based on number of classes
all_semester = And([And(GE(Plus([course(c, b) for c in all_courses]), Real(2)), LE(Plus([course(c, b) for c in all_courses]), Real(3))) for b in num_semesters[1:]])

#based on credit hours
all_semester_hours = And([And(GE(Plus([Times(course(c, b), Real(all_credit_hours[c])) for c in all_courses]), Real(min_credit_hours)),
	LE(Plus([Times(course(c, b), Real(all_credit_hours[c])) for c in all_courses]), Real(max_credit_hours))) for b in num_semesters[1:]])

#prereqs
befores_keys = range(semesters_remaining)
befores_values = [[] for i in range(semesters_remaining)]

befores_start = 0
for s in range(len(befores_values)):
	befores_values[s] = range(-1, befores_start)
	befores_start += 1

befores = {}
for i in range(len(befores_keys)):
	befores[befores_keys[i]] = befores_values[i]
#Can't be on first step, each prereq and coreq created
prereqs_init = And([(Equals(course(c, 0), Real(0))) for c in prereqs])
prereqs_only = And([And([Equals(course(c, b), Real(1)).Implies(And([Equals(Plus([course(cp, be) for be in befores[b]]), Real(1)) for cp in prereqs[c]]))
 	for b in num_semesters[1:]]) for c in prereqs])

coreqs_only = And([And([Equals(course(c, b), Real(1)).Implies(
(And([Or(Equals(course(cc, b), Real(1)), (Equals(Plus([course(cc, bef) for bef in befores[b]]), Real(1)))) for cc in coreqs[c]])) )
for b in num_semesters[1:]]) for c in coreqs])

#already taken
already_taken_courses = And([Equals(course(c, -1), Real(1)) for c in already_taken])
not_yet_taken_courses = And([Equals(course(c, -1), Real(0)) for c in all_courses if c not in already_taken])

#electives
electives_courses = And([Equals(Plus([course(c, b) for c in electives[i][2:]
for b in num_semesters]), Real(a[0])) for i, a in enumerate(electives)])

#At most electives can have one class in the schedule
restrict_electives = And([And([LE(Plus([course(c, b) for b in num_semesters]), Real(1))
	for c in electives[i][2:]]) for i, a in enumerate(electives)])


#Scheduling constraints
csm101 = Or(Equals(course("CSM101", 0), Real(1)),  Equals(course("CSM101", -1), Real(1)))
fall_courses = And([And([Equals(course(c, b), Real(1)).Implies(Or([Equals(Real(b), Real(f))
	for f in valid_falls])) for b in num_semesters]) for c in fall])

spring_courses = And([And([Equals(course(c, b), Real(1)).Implies(Or([Equals(Real(b), Real(s))
	for s in valid_springs])) for b in num_semesters]) for c in spring])

other_courses = And([And([Equals(course(c, b), Real(1)).Implies(Or([Equals(Real(b), Real(map_semester_to_number[s]))
	for s in other[c]])) for b in num_semesters]) for c in other.keys()])

print("Creating domain")
facts_domain = And(facts,

		 always_range,

		 all_semester_hours,

		 all_classes,

		 prereqs_init,

		 prereqs_only,

		 coreqs_only,

		 already_taken_courses,

		 not_yet_taken_courses,

		 electives_courses,

		 restrict_electives,

		 csm101,

		 fall_courses,

		 spring_courses,

		 other_courses
)

print("Generate model")
model = get_model(facts_domain, solver_name="yices")

#print model
if model is None:
	print("UNSAT")
        print("Please verify that the student fields are correct.")
    # In isolation they are both fine, rules from both are probably
    # interacting.
    #
    # The problem is given by a nesting of And().
    # conjunctive_partition can be used to obtain a "flat"
    # structure, i.e., a list of conjuncts.
    #
	from pysmt.rewritings import conjunctive_partition
	conj = conjunctive_partition(facts_domain)
	ucore = get_unsat_core(conj)
	print("UNSAT-Core size '%d'" % len(ucore))
	for f in ucore:
		print(f.serialize())
else:
	f1_classes = []
	s1_classes = []
	f2_classes = []
	s2_classes = []
	f3_classes = []
	s3_classes = []
	f4_classes = []
	s4_classes = []
	for x in model:
		if x[1]._content.payload == 1:
			if x[0]._content.payload[0].endswith('0'):
				f1_classes.append(x[0])
			if x[0]._content.payload[0].endswith('_1'):
				s1_classes.append(x[0])
			if x[0]._content.payload[0].endswith('2'):
				f2_classes.append(x[0])
			if x[0]._content.payload[0].endswith('3'):
				s2_classes.append(x[0])
			if x[0]._content.payload[0].endswith('4'):
				f3_classes.append(x[0])
			if x[0]._content.payload[0].endswith('5'):
				s3_classes.append(x[0])
			if x[0]._content.payload[0].endswith('6'):
				f4_classes.append(x[0])
			if x[0]._content.payload[0].endswith('7'):
				s4_classes.append(x[0])

	print("Already taken: " + str(already_taken))
	print("Credits taken: " + str(taken_credits))
	print("Credit hours per semester: " + str(min_credit_hours) + " to " + str(max_credit_hours))
	print( "f1: " + str(f1_classes))
	print( "s1: " + str(s1_classes))
	print( "f2: " + str(f2_classes))
	print( "s2: " + str(s2_classes))
	print( "f3: " + str(f3_classes))
	print( "s3: " + str(s3_classes))
	print( "f4: " + str(f4_classes))
	print( "s4: " + str(s4_classes))
