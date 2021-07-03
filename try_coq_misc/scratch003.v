Check true.
Check bool.
Locate "+".

Locate "~".
Print not. (* fun A:Prop => A->False
              given any proposition P, return the implication:
              P -> False *)

Inductive MyClaim : Prop.

Check not MyClaim.
Compute not MyClaim.

Print not.

(* ~False just says:
   False -> False *)
Theorem False_cannot_be_proven : ~False.
Proof.
  unfold not. (* not x => x -> False *)
  intros proof_of_False.
  exact proof_of_False.
Qed.

Theorem False_cannot_be_proven__again : ~False.
Proof.
  intros proof_of_False.
  case proof_of_False. (* goal per construction of argument (hypothesis)
                          but there is no way to construct false, done! *)
Qed.

Theorem thm_true_imp_true : True -> True.
Proof.
intros proof_of_True.
exact proof_of_True. (* or exact I *)
Qed.

(* ??? -> True is provable because the implication
  is only violated when consequent is untrue *)
Theorem thm_false_imp_true : False -> True.
Proof.
  (* False is the proposition with no constructors *)
  intros proof_of_False.
  case proof_of_False.
  (* exact I. (* true is always true *) *)
Qed.

Theorem thm_false_imp_false : False -> False.
Proof.
  intros proof_of_False.
  case proof_of_False.
Qed.

Inductive Human := John | Jack | Jill.

Definition is_man : Human -> Prop :=
  fun (x: Human) =>
    match x with
      John => True |
      Jack => True |
      _ => False
  end.

Theorem false_implies_anything : forall P : Prop,
  0 = 1 -> P.
Proof.
  intros P zero_equals_one.
  discriminate.
Qed.

Print false_implies_anything.

Theorem false_implies_anything2 : forall P : Prop,
  False -> P.
Proof.
  intros P zero_equals_one.
  contradiction.
Qed.

Theorem False_implies_all: False -> 1=2.
Proof.
intros H.
contradiction.
Qed.

Theorem funny :
  forall x:Human, (~(x = Jill)) -> (is_man x).
    intros x.
    intros H.
    destruct x.
    simpl. exact I.
    simpl. exact I.
    contradiction.
  Qed.

