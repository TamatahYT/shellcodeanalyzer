# Created By Mahmoud NourEldin https://www.linkedin.com/in/tamatahyt @Engacker, my own writing/analyzing shellcode
# replace your shellcode in the CODE, and your shellcodeloader.exe path
# compile shellcodeloader.c from here in 32bit: https://gist.github.com/levisre/f3e591d299569db949b2e002e0e3eb12

import ctypes, struct, subprocess
from keystone import *

# separate assembly instructions by ; or \n
CODE = (
" start: " #
 " int3 ;" # Breakpoint for Windbg. REMOVE ME WHEN NOT DEBUGGING!!!!
 " mov ebp, esp ;" #
 " sub esp, 60h ;" 
 " find_kernel32: " #
 " xor ecx, ecx ;" # ECX = 0
 " mov esi,fs:[ecx+30h] ;" # ESI = &(PEB) ([FS:0x30])
 " mov esi,[esi+0Ch] ;" # ESI = PEB->Ldr
 " mov esi,[esi+1Ch] ;" # ESI = PEB->Ldr.InInitOrder
 " next_module: " #
 " mov ebx, [esi+8h] ;" # EBX = InInitOrder[X].base_address
 " mov edi, [esi+20h] ;" # EDI = InInitOrder[X].module_name
 " mov esi, [esi] ;" # ESI = InInitOrder[X].flink (next)
 " cmp [edi+12*2], cx ;" # (unicode) modulename[12] == 0x00?
 " jne next_module ;" # No: try next module.
 " ret " #
)
try:
   # Initialize engine in X86-32bit mode
   ks = Ks(KS_ARCH_X86, KS_MODE_32)
   encoding, count = ks.asm(CODE)
   print("Encoded %d instructions..." % count)

   # Take the Machine Code
   sh = b""
   for e in encoding:
    sh += struct.pack("B", e)
   shellcode = bytearray(sh)
   print("[+] Shellcode Generated: %s"%shellcode)
except KsError as e:
   print("ERROR: %s" %e)

#file for holding the machine code we obtained
file = 'shellcode.bin'
try:
    with open(file, 'wb') as f:
        print("[+] Creating shellcode file: %s..." %file)
        f.write(shellcode)
        f.close()
        print("[+] File created Successfully!!")
except:
    print("File cannot be created!")

#put the path of the shellcodeloader
shellcodeloader = "C:\\none\\just\\write\\the\\path2\\shellcodeloader.exe"
try:
    print("[+] Executing shellcodeloader.exe...")
    # Executing it with argument file
    subprocess.run([shellcodeloader] + [file], check=True)
except subprocess.CalledProcessError as e:
    print(f"shellcodeloader execution failed with error: {e}")
