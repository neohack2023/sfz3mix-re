/* [037A56,037A82): first runtime-proven +21C consumer region.
 * A6 receiver, A4 opponent on entry. Containing function entry unresolved.
 * D0=0 when unsigned edge-distance >=48, otherwise test opponent state/animation.
 */
.text
.globl proximity_predicate_037a56
proximity_predicate_037a56:
 cmpi.w #0x30,0x21c(%a6)
 bcc.s .Lfalse
 tst.b 0xa9(%a4)
 beq.s .Lfalse
 cmpi.w #0x200,4(%a4)
 bne.s .Lfalse
 movea.w 0x38(%a6),%a4
 movea.l 0x1c(%a4),%a4
 move.l 8(%a4),%d0
 bne.s .Ltrue
.Lfalse:
 moveq #0,%d0
 rts
.Ltrue:
 moveq #1,%d0
 rts
