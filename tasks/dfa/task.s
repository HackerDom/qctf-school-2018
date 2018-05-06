SECTION .data
    dfa         db 0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh
                db 0bh,05h,05h,05h,05h,0eh,0eh,06h,05h,07h,05h,05h,05h,05h,0eh
                db 0dh,0dh,09h,0dh,0dh,0dh,03h,0dh,0dh,0dh,0dh,0dh,0dh,0dh,01h
                db 0dh,0ch,08h,0ch,0dh,0dh,0dh,0dh,0ah,0dh,0dh,0ah,0dh,0dh,0dh
                db 0bh,0dh,0dh,00h,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,02h,0dh,0dh
                db 00h,0dh,0dh,04h,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh,0dh
    state       db 0dh
	alpha       db placeholder
    
    tma_msg     db "Use like `./task <FLAG>`", 0xa, 0
    tma_len     equ $ - tma_msg
    
    ok_msg      db "You're right!", 0xa, 0
    ok_len      equ $ - ok_msg

    wrong_msg   db "Wrong flag!", 0xa, 0
    wrong_len   equ $ - wrong_msg

SECTION .text
global _start

too_many_args:
    mov     rdx, tma_len
    mov     rsi, tma_msg
    mov     rax, 1
    mov     rdi, rax
    syscall
    jmp     exit

final:
    mov     al, [state]
    cmp     al, 04h
    jz      write_ok
    jmp     write_wrong

write_ok:
    mov     rdx, ok_len
    mov     rsi, ok_msg
    mov     rax, 1
    mov     rdi, rax
    syscall
    jmp     exit

write_wrong:
    mov     rdx, wrong_len
    mov     rsi, wrong_msg
    mov     rax, 1
    mov     rdi, rax
    syscall
    jmp     exit

_start:
    mov     rax, [rsp]
    cmp     rax, 2
    jne     too_many_args
    mov     r8, [rsp + 0x10]

iter:
    xor     rax, rax
    mov     al, byte [r8]
    test    al, al
    jz      final

    mov     rbx, alpha
    xlat
    
    mov     bx, 15
    mul     bx
    add     al, [state]
    mov     rbx, dfa
    xlat

    mov     [state], al
    inc     r8
    jmp     iter

exit:
    mov     rax, 0x3c
    syscall
