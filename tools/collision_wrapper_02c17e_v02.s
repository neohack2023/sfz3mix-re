/* CPU [02C17E,02C19A): prefix; leaf entry is immediately after this region.
 * Shared leaf source V01 remains unchanged. */
.text
.globl collision_wrapper_02c17e
collision_wrapper_02c17e:
 lea 0x400(%a5),%a6
 bsr.w .Lleaf
 lea 0x800(%a5),%a6
 bsr.w .Lleaf
 lea 0xc00(%a5),%a6
 bsr.w .Lleaf
 lea 0x1000(%a5),%a6
.Lleaf:
