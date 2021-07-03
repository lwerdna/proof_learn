Inductive human:Set := John | Jack | Jeff.

Theorem human_exists : human.
  exact John.
Qed.

Inductive human2:Prop := John2 | Jack2 | Jill2.

Theorem human_exists2 : human2.
  exact John2.
Qed.

Print True.
Theorem True_is_provable: True.
  exact I.
Qed.

Print False.