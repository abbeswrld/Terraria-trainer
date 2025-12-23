PATTERN = "29 86 0C 01 00 00"

def create_instakill_code(pm, original_addr):
    newmem = pm.allocate(1024)
    if not newmem:
        raise Exception("Не удалось выделить память")

    code_array = bytearray([
        0x81, 0xAE, 0x0C, 0x01, 0x00, 0x00,
        0x3F, 0x42, 0xF4, 0x00
    ])
    jump_back = original_addr + 6 - (newmem + len(code_array))
    code_array += b'\xE9' + int.to_bytes(jump_back & 0xFFFFFFFF, 4, 'little')
    code_bytes = bytes(code_array)

    pm.write_bytes(newmem, code_bytes, len(code_bytes))
    return newmem

def patch_instakill(pm, addr, newmem):
    jump_to = newmem - (addr + 5)
    patch = b'\xE9' + int.to_bytes(jump_to & 0xFFFFFFFF, 4, 'little') + b'\x90'
    pm.write_bytes(addr, patch, 6)

def restore_original(pm, addr, original_bytes):
    pm.write_bytes(addr, original_bytes, len(original_bytes))
