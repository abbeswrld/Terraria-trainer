def find_pattern_in_full_memory(pm, pattern_hex):
    pattern = bytes.fromhex(pattern_hex.replace(' ', ''))
    PAGE_SIZE = 0x10000
    MAX_ADDR = 0x7FFFFFFF

    #print(f"Поиск паттерна по всему адресному пространству: {pattern_hex}")

    addr = 0x00010000
    while addr < MAX_ADDR:
        try:
            data = pm.read_bytes(addr, PAGE_SIZE)
            index = data.find(pattern)
            if index != -1:
                found = addr + index
                print(f"Паттерн найден по адресу: {hex(found)}")
                return found
        except:
            pass
        addr += PAGE_SIZE

    print("Паттерн не найден в диапазоне 0x00010000 – 0x7FFFFFFF")
    return None