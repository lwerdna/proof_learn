Theorem my_first_proof : (forall A : Prop, A -> A).
Proof.
  intros A. (* let A be some arbitrary Prop *)
  intros proof_of_A.
  exact proof_of_A. (* when subgoal matches a hypothesis *)
Qed.

(* propositions should not be thought of as TRUE/FALSE
   but rather as PROVEN/UNPROVEN
   or HAS-A-PROOF/DOESNT-HAVE-A-PROOF *)

Theorem forward_small : (forall A B : Prop, A -> (A->B) -> B).
Proof.
 intros A.
 intros B.
 intros proof_of_A.
 intros A_implies_B.
 pose (proof_of_B := A_implies_B proof_of_A).
 exact proof_of_B.
 Show Proof.
Qed.
Print forward_small.

(* alternative: using apply *)
Theorem forward_small' : (forall A B : Prop, A -> (A->B) -> B).
Proof.
 intros A.
 intros B.
 intros proof_of_A.
 intros A_implies_B.
 apply A_implies_B in proof_of_A as B_holds.
 exact B_holds.
 Show Proof.
 Qed.

(* foward proofs build stuff in the context until the goal is reached *)
(* backwards proofs changes the subgoal *)
Theorem backward_small : (forall A B : Prop, A -> (A->B)->B).
Proof.
  intros A B. (* suppose A, B existed *)
  intros proof_of_A proof_of_A_implies_B.
  refine (proof_of_A_implies_B _).
    exact proof_of_A.
Qed.

Theorem backward_large : (forall A B C : Prop, A -> (A->B) -> (B->C) -> C).
Proof.
 intros A B C.
 intros proof_of_A A_implies_B B_implies_C.
 (* B_implies_C on SOMETHING would yield subgoal C
    that SOMETHING is B
    so new subgoal: B *)
 refine (B_implies_C _). (* generate subgoals for each hole '_' *)
   refine (A_implies_B _).
     exact proof_of_A.
Qed.

Theorem backward_huge : (forall A B C : Prop, A -> (A->B) -> (A->B->C) -> C).
Proof.
 intros A B C.
 intros proof_of_A A_implies_B A_imp_B_imp_C.
 refine (A_imp_B_imp_C _ _). (* if only we had A, B *)
   (* prove A *)
   exact proof_of_A.
   (* prove B *)
   refine (A_implies_B _). (* if only we had A *)
     exact proof_of_A.
Qed.

Theorem forward_huge : (forall A B C : Prop, A -> (A->B) -> (A->B->C) -> C).
Proof.
 intros A B C.
 intros proof_of_A A_implies_B A_imp_B_imp_C.
 pose (proof_of_B := A_implies_B proof_of_A).
 pose (proof_of_C := A_imp_B_imp_C proof_of_A proof_of_B).
 exact proof_of_C.
Show Proof.
Qed.

(* according to tutorial, most Coq proofs are backwards *)
(* Capital-F "False" is Prop with no proofs
 "False" should be read "Never Provable" *)
(* Capital-T "True" is Prop that has single proof called I
 "True" should be read "Always Provable" *)
(* lowercase "false", "true" are members of Set datatype named "bool" *)
Print I.

Theorem True_can_be_proven : True.
  exact I.
Qed.

(* we prove <something> is unprovable by proving
    (<something> -> False) *)

(* Definition <X> := <Y>. says that X and Y are interchangeable
*)
Locate "~". (* "~ x" := (not x) *)
Print not. (* fun A:Prop => A -> False *)
Theorem False_cannot_be_proven : ~False.
Proof.
  unfold not. (* goal ~False
                 not False       equivalent to above
                 False -> False  (not False => False) *)

  intros proof_of_False.
  exact proof_of_False.
Qed.


