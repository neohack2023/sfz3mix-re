.text
.globl decision_apply_037ad2
decision_apply_037ad2:
 .set .Ldispatch,decision_apply_037ad2+(0x35a50-0x37ad2)
 move.b #6,0x204(%a6)
 clr.l 0x200(%a6)
 bra.w .Ldispatch
