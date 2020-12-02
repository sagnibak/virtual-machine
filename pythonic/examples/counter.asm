push 0    ;; initialization
push x0
store 0  ; store the count in x0
push 0
push x1
store 0   ; store the loop index in x1

loop:
    push x1   ;; counting loop starts here
    load 0
    push 5    ; add the numbers up to 5
    cmp
    beq end
    push x0
    load 0
    push x1
    load 0
    add
    push x0
    store 0
    push x1
    load 0
    push 1
    add
    push x1
    store 0
    push loop
    jmp       ;; counting loop ends here

end:
    push x0
    load 0
    print
    halt