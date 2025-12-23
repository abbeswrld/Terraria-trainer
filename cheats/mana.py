PATTERN = "29 BE 0C 04 00 00"  # sub [esi+0000040C], edi

def toggle_infinite_mana(pm, mana_addr, original_bytes, enabled):
    if enabled:
        pm.write_bytes(mana_addr, b'\x90' * 6, 6)
    else:
        pm.write_bytes(mana_addr, original_bytes, 6)