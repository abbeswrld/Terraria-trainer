import threading
import time

PATTERN_MINER = "88 96 79 08 00 00"
PATTERN_HUNTER = "88 96 7C 08 00 00"
PATTERN_DANGER = "C6 86 BE 06 00 00"

def toggle_permanent_vision(pm, miner_addr, hunter_addr, danger_addr, orig_miner, orig_hunter, enabled):
    if enabled:
        if miner_addr:
            newmem = pm.allocate(64)
            if newmem:
                payload = b"\xC6\x86\x79\x08\x00\x00\x01"
                jump_back = (miner_addr + 6) - (newmem + len(payload) + 5)
                jmp_back = b"\xE9" + int.to_bytes(jump_back & 0xFFFFFFFF, 4, 'little')
                code = payload + jmp_back
                pm.write_bytes(newmem, code, len(code))

                jump_to = newmem - (miner_addr + 5)
                patch = b"\xE9" + int.to_bytes(jump_to & 0xFFFFFFFF, 4, 'little') + b"\x90"
                pm.write_bytes(miner_addr, patch, 6)
                
        if hunter_addr:
            newmem = pm.allocate(64)
            if newmem:
                payload = b"\xC6\x86\x7C\x08\x00\x00\x01"
                jump_back = (hunter_addr + 6) - (newmem + len(payload) + 5)
                jmp_back = b"\xE9" + int.to_bytes(jump_back & 0xFFFFFFFF, 4, 'little')
                code = payload + jmp_back
                pm.write_bytes(newmem, code, len(code))

                jump_to = newmem - (hunter_addr + 5)
                patch = b"\xE9" + int.to_bytes(jump_to & 0xFFFFFFFF, 4, 'little') + b"\x90"
                pm.write_bytes(hunter_addr, patch, 6)

        if danger_addr:
            pm.write_bytes(danger_addr + 6, b"\x01", 1)

    else:
        if miner_addr and orig_miner:
            pm.write_bytes(miner_addr, orig_miner, len(orig_miner))
        if hunter_addr and orig_hunter:
            pm.write_bytes(hunter_addr, orig_hunter, len(orig_hunter))
        if danger_addr:
            pm.write_bytes(danger_addr + 6, b"\x00", 1)