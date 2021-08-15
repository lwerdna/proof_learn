(* some definitions *)

(* mynat is sort Set and is defined as... *)
Inductive mynat : Set :=
  | O : mynat
  | S : mynat -> mynat.

Check O.
Check (S O).
Check (S (S O)).

Definition pred: mynat -> mynat :=
  fun (x: mynat) =>
    match x with
      O => O
     |(S n) => n
     end.

Compute (pred O).
Compute (pred (S O)).
Compute (pred (S (S O))).

Fixpoint add (a b: mynat) : mynat :=
    match a, b with
     | O, b => b
     | (S l), b => (add l (S b))
     end.

Compute (add O O).
Compute (add O (S O)).
Compute (add (S O) (S O)).
Compute (add (S (S O)) (S (S O))).

Fixpoint mul (a b: mynat) : mynat :=
  match a, b with
    | O, b => O
    | (S O), O => O
    | (S O), b => b
    | (S x), b => mul x (add b b)
    end.
     
Compute mul O O.
Compute mul O (S O).
Compute mul O (S (S O)).
Compute mul (S O) (S O).
Compute mul (S (S O)) (S (S O)). (* 2 x 2 = 4 *)

Check eq.
Print eq.
Locate "<".
Print lt.
Inductive myeq {A: Type}: A -> A -> Prop := | myeq_refl: forall (x: A), myeq x x.
Print myeq.
Inductive myeq (A: Type): Prop := | myeq_constructor: forall (x: A), myeq x x.
Compute eq 0 1.

Check (eq O).

(* propositions as types, proofs as programs (proofs as TERMS) *)
Locate "=". (* '=' is calling eq *)

Check eq.
Print eq.

Check (eq_refl 3).
Check @eq_refl nat 3.


Inductive myeq (A : Type) (x : A) : A -> Prop :=
  myeq_constructor : x = x.


Definition foo:Prop := forall (x y z : nat), x*y + z = x*y + z.
Check foo.
Print foo.

Check eq_refl.
Print eq_refl.

Check eq.
Print eq.


Definition myeq (A : Type) (x : A) : nat := 5.
Print myeq.
Check (myeq nat 1).
(* Inductive myeq2 (A : Type) (x : A) : nat := 5. *)

Check ((eq nat 1) nat).

Definition foo:Prop := forall (x y z : mynat), (add (mul x y) z) = (add (mul x y) z).
Print foo.

Definition bar := fun (x y z : mynat) => eq_refl.


Check foo.
(*
Check pred pred.
Check (add (mul x y) z) = (add (mul x y) z).
Check eq (add (mul x y) z) (add (mul x y) z).
*)
(* level 1 *)
(* For all natural numbers x, y and z, we have xy+z=xy+z *)
Lemma example1:
  forall (x y z : mynat), (add (mul x y) z) = (add (mul x y) z).
  Show Proof.
  reflexivity.
  Show Proof.