.text
.globl opponent_near_predicate_037a46
opponent_near_predicate_037a46:
 bsr.w .Lhelper
 beq.s .Lfalse
 movea.w 0x38(%a6),%a4
 tst.b 0x31(%a4)
 bne.s .Lfalse
/* Reuse the unchanged V03 reader region and its common return blocks. */
.include "tools/collision_consumer_037a56_v03.s"
.Lhelper:
