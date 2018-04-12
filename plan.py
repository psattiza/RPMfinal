from pysmt.shortcuts import Symbol, LE, GE, And, Int, Or, Iff, Implies, ExactlyOne, FALSE, TRUE, Not, get_model, get_unsat_core, is_sat, is_unsat, Plus, Ite
from pysmt.typing import INT
import random

def course (name, semester):
	return Symbol("taken_%s_%s" % (name, semester)) 

#Choose first semester courses out of those without prereqs
courses = ["math112", "phgn100", "epic151"]

no_prereqs = [course("math111", "f1"), course("csm101", "f1"), course("chgn121", "f1"), course("csci101","f1"), course("pagn102", "f1")]

before_courses = random.sample(no_prereqs, 2)
before_non_courses = [Not(item) for item in no_prereqs if item not in before_courses]


#Spring 2015
before = "f1"
#Or with all befores when comes to that
print "f1: " + str(before_courses )
taken = []
for c in before_courses:
	taken.append(c)
print taken

for current in ["s1", "f2", "s2"]:
	facts = TRUE()
	facts_courses_before = (And([c for c in taken]))
	facts_courses_not_done = (And([c for c in before_non_courses]))

	facts_domain = (facts & 
		facts_courses_before

#DO ONLY SEMESTERS THAT HAPPENED BEFORE. BEFORE MATRIX TO KEEP TRACK, CREATE OR FOR BOTH PREREQS AND COURSE ITSELF

		& course("math112", current).Implies(And(course("math111", before), Not(course("math112", before))))

		& course("phgn100", current).Implies(And(course("math111", before), Not(course("phgn100", before))))

		& course("epic151", current).Implies(And(Not(course("epic151", before))))


		& course("pagn103", current).Implies(And(Not(course("pagn103", before))))

		& course("ebgn201", current).Implies(And(Not(course("ebgn201", before))))

		& course("math111", current).Implies(And(Not(course("math111", before))))

		& course("csm101", current).Implies(And(Not(course("csm101", before))))

		& course("chgn121", current).Implies(And(Not(course("chgn121", before))))

		& course("csci101", current).Implies(And(Not(course("csci101", before))))

		& course("pagn102", current).Implies(And(Not(course("pagn102", before))))
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
		before_courses = random.sample(current_only_curr, 2)
		for c in before_courses:
			taken.append(c)
		before_non_courses = [Not(item) for item in current_all_courses if item not in taken]
		print current + ": " + str(before_courses )
		before = current
