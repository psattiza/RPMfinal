; The 4-operator blocks world domain from the 2nd International
; Planning Competition.

(define (domain courses)
  (:constants MATH111 CSM101 CHGN121 LAIS100 PHGN100 CSCI261 CSCI262 CSCI101)
  (:predicates (taken ?x))
  (:action take-LAIS100
           :precondition (and (not (taken LAIS100)))
           :effect (and (taken LAIS100) ))
  (:action take-CSM101
           :precondition (and (not (taken CSM101)))
           :effect (and (taken CSM101)))
  (:action take-CHGN121
           :precondition (and (not (taken CHGN121)))
           :effect (and (taken CHGN121)))
  (:action take-MATH111
           :precondition (and (not (taken MATH111)))
           :effect (and (taken MATH111)))
  (:action take-PHGN100
           :precondition (and (not (taken PHGN100)) (taken MATH111))
           :effect (and (taken PHGN100)))
  (:action take-CSCI261
           :precondition (and (not (taken CSCI261)))
           :effect (and (taken CSCI261)))
  (:action take-CSCI262
           :precondition (and (not (taken CSCI262)) (taken CSCI261))
           :effect (and (taken CSCI262)))
  (:action take-CSCI101 
           :precondition (and (not (taken CSCI101)))
	   :effect (and (taken CSCI101)))
 
 )
