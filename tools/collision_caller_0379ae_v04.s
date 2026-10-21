.text
.globl decision_bit0_0379ae
decision_bit0_0379ae:
 .set .Lpredicate,decision_bit0_0379ae+(0x37a46-0x379ae)
 .set .Lsuccess,decision_bit0_0379ae+(0x37a3e-0x379ae)
 moveq #0,%d6
 btst %d6,%d5
 beq.s .Lnext
 bsr.w .Lpredicate
 bne.w .Lsuccess
.Lnext:
