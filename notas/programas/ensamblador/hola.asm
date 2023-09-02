section .data
	hello:     db 'Hola, mundo!',10    ; Saludo más un salto de línea
	helloLen:  equ $-hello             ; Longitud del saludo

section .text
	global _start

_start:
	mov eax,4            ; Llamada al sistema para escribir (sys_write)
	mov ebx,1            ; Descriptor de archivo 1: salida estándar
	mov ecx,hello        ; Poner la dirección de hello en ecx
	mov edx,helloLen     ; Pon la longitud de hello en edx
	int 80h              ; Llamada al sistema

	mov eax,1            ; Llamada al sistema para terminar (sys_exit)
	mov ebx,0            ; Salir con código de error 0 (éxito)
	int 80h