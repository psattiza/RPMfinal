; The 4-operator blocks world domain from the 2nd International
; Planning Competition.

(define (domain courses)
  (:constants CSM101 LAIS100)
  (:predicates (taken ?x))
  (:action take-CSM101
           :precondition (and (not (taken CSM101)))
           :effect (and (taken CSM101) ))
  (:action take-LAIS100
           :precondition (and (not (taken LAIS100)))
           :effect (and (taken LAIS100) ))
  (:action take-LAIS200
           :precondition (and (not (taken LAIS100) (t))
           :effect (and (taken LAIS100) ))

 )
