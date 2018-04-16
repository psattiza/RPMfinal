from pysmt.shortcuts import Symbol, LE, GE, And, Int, Or, Iff, Implies, ExactlyOne, FALSE, TRUE, Not, get_model, get_unsat_core, is_sat, is_unsat, Plus, Equals
from pysmt.typing import INT
import random

def course (name, semester):
	return Symbol("taken_%s_%d" % (name, semester))

def course_2(name):
	return Symbol("taken_%s" % (name))

#Choose first semester courses out of those without prereqs
courses = ["math112", "phgn100", "epic151", "pagn103", "ebgn201", "math111", "chgn121", "csci101", "pagn102"]

#Need this in this format
prereqs = {
   "math112": ["math111"],
   "phgn100": ["math111"]
}

coreqs = {
    "phgn100": ["math112"]
}

#Electives: randomize which are chosen, then append onto courses

no_prereqs_names = []
both_names = []
only_coreq = []
only_prereq = []
for c in courses:
	if c not in prereqs and c not in coreqs:
		no_prereqs_names.append(c)
	if c in prereqs.keys() and c in coreqs:
		both_names.append(c)
	if c in prereqs.keys() and c not in coreqs.keys():
		only_prereq.append(c)
	if c not in prereqs.keys() and c in coreqs.keys():
		only_coreq.append(c)

before_courses_not_csm101 = random.sample(no_prereqs_names, 2)
before_courses = [course("csm101", 1)]
taken = []
taken_no_time = []
for b in before_courses_not_csm101:
	before_courses.append(course(b, 1))
	taken.append(course(b, 1))
	taken_no_time.append(course_2(b))
taken.append(course("csm101", 1))

before_non_courses = [Not(course(item, 1)) for item in no_prereqs_names if course(item, 1) not in before_courses]
n_taken_no_time = [Not(course_2(item)) for item in courses if course_2(item) not in taken_no_time]

before = [1]
print "1: " + str(before_courses )

#Generalize iffs
iffs = []

for current in [2, 3, 4]:
	facts = TRUE()
	facts_courses_before = (And([c for c in taken]))
	facts_courses_non_before = (And([c for c in before_non_courses]))

	#no prereqs/coreqs
	#print no_prereqs_names
	bare_iffs = (facts & (And([course(c, current).Iff(And([Not(course(c, b)) for b in before])) for c in no_prereqs_names])))
	prereq_iffs = (facts & (And([course(c, current).Iff(And((And([Not(course(c, b)) for b in before])), (And([Or([course(cp, be) for be in before]) for cp in prereqs[c]]))    )) for c in only_prereq])))
	both_iffs = (facts & (And([course(c, current).Iff(And((And([Not(course(c, b)) for b in before])), (And([Or([course(cp, be) for be in before]) for cp in prereqs[c]])),  (And([Or(course(cc, current), (Or([course(cc, bef) for bef in before]))) for cc in coreqs[c]]))    )) for c in both_names])))
	coreq_iffs = (facts & (And([course(c, current).Iff(And((And([Not(course(c, b)) for b in before])), (And([Or(course(cc, current), (Or([course(cc, bef) for bef in before]))) for cc in coreqs[c]]))    )) for c in only_coreq])))
	#Scheduling constraints: add in Equals(current, Int(1)) for all valid semesters. Have to handle for first semester and handle classes that are variable (not all, fall, or spring). Hash each class to each time they are available, add that into generalized
	facts_domain = (facts &
		facts_courses_before

		& facts_courses_non_before

	#	& course("math112", current).Iff(And((Or([course("math111", b) for b in before])), (And([Not(course("math112", b)) for b in before]))))

	#	& course("phgn100", current).Iff(And((Or([course("math111", b) for b in before])), (Or(course("math112", current), (Or([course("math112", b) for b in before])))),(And([Not(course("phgn100", b)) for b in before]))))

	#	& course("epic151", current).Iff(And((And([Not(course("epic151", b)) for b in before]))))


	#	& course("pagn103", current).Iff(And((And([Not(course("pagn103", b)) for b in before]))))


	#	& course("ebgn201", current).Iff(And((And([Not(course("ebgn201", b)) for b in before]))))


	#	& course("math111", current).Iff(And((And([Not(course("math111", b)) for b in before]))))


	#	& course("csm101", current).Iff(And((And([Not(course("csm101", b)) for b in before]))))


	#	& course("chgn121", current).Iff(And((And([Not(course("chgn121", b)) for b in before]))))


	#	& course("csci101", current).Iff(And((And([Not(course("csci101", b)) for b in before]))))


	#	& course("pagn102", current).Iff(And((And([Not(course("pagn102", b)) for b in before])) ))


	& bare_iffs

	& prereq_iffs

	& both_iffs

	& coreq_iffs
	)


	model = get_model(facts_domain)
	current_all_courses = []
	if model is None:
		print("UNSAT")
	else:
		for x in model:
			if x[1]._content.payload is True:
				current_all_courses.append(x[0])
		current_only_curr = []
		for c in current_all_courses:
			if c not in taken:
				current_only_curr.append(c)
		if len(current_only_curr) < 3:
			before_courses = current_only_curr
		else:
			#Credit hours and coreqs
			#Credit hours: when add class, add to credit hour limit, then check. Coreqs: will have to handle but should be fine. Extra function to compute it? Hash for each class to credit hour length
			num_classes = 0
			before_courses = []
			max_semester_length = 3
			while num_classes < max_semester_length:
				before_course = random.sample(current_only_curr, 1)[0]
				course_name = before_course._content.payload[0].split("_")[1]
				#Handle coreqs
				if course_name in coreqs:
					coreqs_courses = []
					all_cos = coreqs[course_name]
					#Collect all coreqs in this semester
					for cos in all_cos:
						if course(cos, current) in current_only_curr:
							coreqs_courses.append(course(cos, current))
					#Add them to before_courses if not already added
					if len(coreqs_courses) > 0:
						for c in coreqs_courses:
							if c not in before_courses:
								before_courses.append(c)
								current_only_curr.remove(c)
					#Pop out extra before_courses
					length_now = len(before_courses) + 1 #include new course
					if length_now == max_semester_length:
						num_classes = max_semester_length
					elif length_now > max_semester_length:
						num_to_pop = length_now - max_semester_length
						while num_to_pop > 0:
							before_courses.pop(0)
							num_to_pop -= 1
				current_only_curr.remove(before_course)
				before_courses.append(before_course)
				num_classes = len(before_courses)
			#before_courses = random.sample(current_only_curr, 3)
		for c in before_courses:
			taken.append(c)
		before_non_courses = [Not(item) for item in current_all_courses if item not in taken]
		print str(current) + ": " + str(before_courses )
		before.append(current)
