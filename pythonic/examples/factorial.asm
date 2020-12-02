input     ; take user input
push x0
store 0  ; store argument  (n) in x0
push 1    ; accumulator variable
push x1
store 0  ; stored in x1

factorial:
    push x0
    load 0   ;; factorial starts here (idx 4)
    push 0
    cmp
    beq end   ; if n == 0: return x1
    push 1
    push x0
    load 0
    sub
    push x2
    store 0   ; temporary storage
    push x0
    load 0
    push x1
    load 0
    mul
    push x1
    store 0
    push x2
    load 0
    push x0
    store 0   ; setup for next function call
    push factorial
    jmp       ;; end of factorial

end:
    push x1
    load 0   ;; end tag here
    print
    halt