PATTERN = "29 82 08 04 00 00"

def toggle_godmode(pm, damage_addr, original_bytes, enabled):
    if enabled:
        pm.write_bytes(damage_addr, b'\x90' * 6, 6)
    else:
        pm.write_bytes(damage_addr, original_bytes, 6)