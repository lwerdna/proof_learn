(* theorems are types with sort Prop,
  and a proof of a theorem is a term with that type *)
 
Inductive MyClaim: Prop :=
  Evidence1: MyClaim |
  Evidence2: MyClaim.
  
Theorem easy_proof : MyClaim.
  exact Evidence1.
  Show Proof.
Qed.

(* seems like cheating doesn't it? but look at how
 True is made: *)
Print True.

Theorem easy_proof2 : True.
  exact I.
  Show Proof.
Qed.


