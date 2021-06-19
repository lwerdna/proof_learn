Theorem obvious_fact : 1 + 1 = 2.
Proof.
Show Proof.
simpl.
Show Proof.
trivial.
Show Proof.
Qed.
Check obvious_fact.

Print obvious_fact.

(* think of how 42 is meaningful because it has type nat
  and 42+1 is meaningful because 42 has type nat, 1 has type nat
  and add has type nat -> nat
  
  now think of how 42 + true has no meaning, because while
  the respective meaning/type exists, add doesn't for these types*)

Compute Nat.add 42 1.

Definition x := 42.
Check x. (* x : nat   ...so what's a nat? *)
Check nat. (* nat : Set *)
Check Set. (* Set : Type *)
(* and Set is the type of "program specifications" which describe computations *)

(* thus 42 is a "program specification" or computation that returns 42 because 42:nat and nat:Set *)

Definition increment x:nat :=
  x+1.

Check increment 5.

(* thus increment is a "program specification" or a computation because it returns nat and nat:Set *)

Check 1 + 1 = 2. (* type Prop *)
Check eq. (* ?A, ?A -> Prop *)
Locate "=".
Check @eq.
Check @eq nat 5 5. (* explicit type given *)
Check eq 5 5. (* implicit type given *)
Check eq 5 6. (* notice no truth value! just returns prop is all it says, hmm *)

(* easy thought: x has type nat
   deep thought: there is evidence for type nat
                 a value 42 inhabits this type
                 typechecker allowing the assignment means 42 "proves" nat *)
                 
Print obvious_fact.
Print eq_refl.
Print eq.
Check eq.
Check eq 5 5.


Check and. (* Prop -> Prop -> Prop        or         : forall (_ : Prop) (_ : Prop), Prop *)
Check or.  (* Prop -> Prop                or         : forall (_ : Prop) (_ : Prop), Prop *)
Check not. (* Prop -> Prop                or         : forall _ : Prop, Prop *)
Check True. (* : Prop that always holds *)
Check true. (* : bool *)
Check False. (* : Prop that always holds *)
Check false. (* : bool *)

(* P -> Q has two roles:
   t1 -> t2 is type of functions that take input type t1 and return output t2 
   P -> Q is a proposition that asserts P implies Q 
   resolve this was thinking of them as a transformer
   function t1 -> t2 transforms values of type t1 into values of type t2
   implication P -> Q a function that transforms evidence for P into evidence for Q *)

Theorem p_implies_p : forall P:Prop, P -> P.
  intros P.
  intros H.
  assumption. (* goal is given by assumption *)
Qed.
