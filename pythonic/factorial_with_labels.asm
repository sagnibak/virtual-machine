input     ; take user input
store x0  ; store argument  (n) in x0
push 1    ; accumulator variable
store x1  ; stored in x1

factorial:
    load x0   ;; factorial starts here (idx 4)
    push 0
    cmp
    beq end   ; if n == 0: return x1
    push 1
    load x0
    sub
    store x2  ; temporary storage
    load x0
    load x1
    mul
    store x1
    load x2
    store x0  ; setup for next function call
    push factorial
    jmp       ;; end of factorial

end:
    load x1   ;; end tag here
    print
    halt