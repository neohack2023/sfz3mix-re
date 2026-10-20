.text
.global sfz_buffer_writer
sfz_buffer_writer:
    move.l %d1,0(%a4,%d0.w)
    move.l %d2,4(%a4,%d0.w)
    move.l %d3,8(%a4,%d0.w)
    addi.w #16,%d0
    andi.w #0xff0,%d0
    move.w %d0,0x6e80(%a5)
    rts
