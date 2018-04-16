from pysmt.shortcuts import Symbol, LE, GE, And, Int, Or, Iff, Implies, ExactlyOne, FALSE, TRUE, Not, get_model, get_unsat_core, is_sat, is_unsat, Plus, Equals
from pysmt.typing import INT
import random

def course (name, semester):
	return Symbol("taken_%s_%d" % (name, semester), INT)
courses = ["epic151", "ebgn201", "math111", "csci101",
 "csm101", "math112", "phgn100", "csci261", "csci262", "math201",
 "math213", "csci341", "csci404", "phgn200", "chgn121", "csci403",
 "csci400", "csci306"]

electives_1 = [
  [1, "chgn122", "cben110", "chgn125", "gegn101"],
  [2, "pagn101", "pagn102", "pagn103", "pagn104"],
  [3, "csci404", "csci440", "csci446", "csci445"]
]


all_courses = []
for c in courses:
	all_courses.append(c)
for co in electives_1:
	for c in co[1:]:
		all_courses.append(c)

#Need this in this format
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

facts = TRUE()

#Range for classes, only one class per schedule
num_semesters = [0, 1, 2, 3, 4, 5, 6, 7]
always_range = And([Or(Equals(course(c, b), Int(0)), Equals(course(c, b), Int(1))) for c in all_courses for b in num_semesters])

all_classes = And([Equals(Plus([course(c, b) for b in num_semesters]), Int(1)) for c in courses])

#credit hours things
all_semester = And([And(GE(Plus([course(c, b) for c in courses]), Int(2)), LE(Plus([course(c, b) for c in all_courses]), Int(3))) for b in num_semesters])
#

#print electives_1_courses
#prereqs
befores = {
	1: [0],
	2: [0, 1],
	3: [0, 1, 2],
	4: [0, 1, 2, 3],
	5: [0, 1, 2, 3, 4],
	6: [0, 1, 2, 3, 4, 5],
	7: [0, 1, 2, 3, 4, 5, 6]
}

prereqs_init = And([(Equals(course(c, 0), Int(0))) for c in prereqs])
prereqs_only = And([And([Equals(course(c, b), Int(1)).Implies(And([Equals(Plus([course(cp, be) for be in befores[b]]), Int(1)) for cp in prereqs[c]]))
 	for b in num_semesters[1:]]) for c in prereqs])

coreqs_only = And([And([Equals(course(c, b), Int(1)).Implies(
(And([Or(Equals(course(cc, b), Int(1)), (Equals(Plus([course(cc, bef) for bef in befores[b]]), Int(1)))) for cc in coreqs[c]])) )
for b in num_semesters[1:]]) for c in coreqs])

coreqs_only = TRUE()
both = TRUE()

#electives
electives_courses = And([Equals(Plus([course(c, b) for c in electives_1[i][1:]
for b in num_semesters]), Int(a[0])) for i, a in enumerate(electives_1)])

restrict_electives = And([And([LE(Plus([course(c, b) for b in num_semesters]), Int(1))
	for c in electives_1[i][1:]]) for i, a in enumerate(electives_1)])


#Scheduling constraint
csm101 = Equals(course("csm101", 0), Int(1))


facts_domain = (facts


		& always_range

		& all_semester

		& all_classes

		& prereqs_init

		& prereqs_only

		& coreqs_only

		& electives_courses

		& restrict_electives

		& csm101


)

model = get_model(facts_domain)

#print model
if model is None:
	print("UNSAT")
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
			if x[0]._content.payload[0].endswith('1'):
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

	print "f1: " + str(f1_classes)
	print "s1: " + str(s1_classes)
	print "f2: " + str(f2_classes)
	print "s2: " + str(s2_classes)
	print "f3: " + str(f3_classes)
	print "s3: " + str(s3_classes)
	print "f4: " + str(f4_classes)
	print "s4: " + str(s4_classes)
