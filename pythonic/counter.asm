push 0   ;; initialization
store x0  ; store the count in x0
push 0
store x1  ; store the loop index in x1
load x1   ;; counting loop starts here
push 5   ; add the numbers up to 5
cmp
beq 18
load x0
load x1
add
store x0
load x1
push 1
add
store x1
push 4
jmp      ;; counting loop ends here
load x0
print
halt