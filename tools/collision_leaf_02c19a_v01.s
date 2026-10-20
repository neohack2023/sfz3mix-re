/* SFZ3 Mix v0.32: candidate leaf at CPU 0x02C19A..0x02C1E1.
 * Authored instructions, no incbin/raw-byte directives.
 * A6: receiver object. A4: sign-extended opponent word at A6+0x38.
 * Name describes observed math; collision-contact/visual semantics unproven.
 */
.text
.balign 2
.globl sfz_push_edge_distance_02c19a
sfz_push_edge_distance_02c19a:
    moveq #0,%d1
    tst.b (%a6)
    beq.s .Lstore
    movea.w 0x38(%a6),%a4
    moveq #0,%d0
    move.b 0xcb(%a4),%d0
    beq.s .Lposition
.Lbox:
    movea.l 0x9c(%a4),%a0
    lsl.w #3,%d0
    lea 0(%a0,%d0.w),%a0
    move.w 4(%a0),%d1
    neg.w %d1
    move.w (%a0),%d0
    move.b 0x2c9(%a6),%d2
    eori.b #1,%d2
    beq.s .Lposition
    neg.w %d0
    neg.w %d1
.Lposition:
    add.w %d1,%d0
    add.w 0x10(%a4),%d0
    move.w 0x10(%a6),%d1
    sub.w %d0,%d1
    bpl.s .Lstore
    neg.w %d1
.Lstore:
    move.w %d1,0x21c(%a6)
    rts
.size sfz_push_edge_distance_02c19a,.-sfz_push_edge_distance_02c19a
