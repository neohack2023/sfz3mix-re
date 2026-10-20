/* CPU [029A42,029A66): bounded straight-line block, owner unresolved. */
.text
.globl collision_dual_records_029a42
collision_dual_records_029a42:
 movea.l 0x9c(%a6),%a0
 movea.l 0x9c(%a4),%a1
 lsl.w #3,%d0
 lsl.w #3,%d1
 lea 0(%a0,%d0.w),%a0
 lea 0(%a1,%d1.w),%a1
 move.w 2(%a0),%d0
 add.w 0x14(%a6),%d0
 move.w 2(%a1),%d1
 add.w 0x14(%a4),%d1
