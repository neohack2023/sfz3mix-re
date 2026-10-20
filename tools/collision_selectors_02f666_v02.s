/* CPU [02F666,02F68C): bounded block; owning function unresolved. */
.text
.globl collision_selectors_02f666
collision_selectors_02f666:
 move.l (%a0),0xc8(%a6)
 moveq #0,%d0
 movea.l 0x1c(%a6),%a0
 move.b 0xa(%a0),%d0
 lsl.w #2,%d0
 movea.l 0xc0(%a6),%a0
 move.l 0(%a0,%d0.w),0xc4(%a6)
 move.b 0xc6(%a6),0x3d(%a6)
 moveq #0,%d0
 move.b 0xc6(%a6),%d0
