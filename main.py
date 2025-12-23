import keyboard
import time
from utils import find_terraria_process
from memory import find_pattern_in_full_memory
from cheats.instakill import patch_instakill, restore_original, create_instakill_code, PATTERN as INSTAKILL_PATTERN
from cheats.godmode import toggle_godmode, PATTERN as NO_DAMAGE_PATTERN
from cheats.vision import toggle_permanent_vision, PATTERN_MINER, PATTERN_HUNTER, PATTERN_DANGER
from cheats.mana import toggle_infinite_mana, PATTERN as MANA_PATTERN


def main():
    print("Terraria 1.4.4.9 Трейнер")
    print("f1 - insta kill | f2 - godmode | f3 - mana | f4 - i can see 4ever")

    pm = find_terraria_process()
    if not pm:
        print("Terraria не запущена!")
        input("Нажмите Enter...")
        return

    insta_addr = find_pattern_in_full_memory(pm, INSTAKILL_PATTERN)
    if not insta_addr:
        insta_active = False
    else:
        original_insta = pm.read_bytes(insta_addr, 6)
        newmem = create_instakill_code(pm, insta_addr)
        patch_instakill(pm, insta_addr, newmem)
        insta_active = True

    godmode_addr = find_pattern_in_full_memory(pm, NO_DAMAGE_PATTERN)
    if not godmode_addr:
        no_damage_active = False
    else:
        original_damage = pm.read_bytes(godmode_addr, 6)
        no_damage_active = False

    
    miner_addr = find_pattern_in_full_memory(pm, PATTERN_MINER)
    hunter_addr = find_pattern_in_full_memory(pm, PATTERN_HUNTER)
    danger_addr = find_pattern_in_full_memory(pm, PATTERN_DANGER)
    
    if not any([miner_addr, hunter_addr, danger_addr]):
        vision_active = False
    else:
        orig_miner = pm.read_bytes(miner_addr, 6) if miner_addr else None
        orig_hunter = pm.read_bytes(hunter_addr, 6) if hunter_addr else None
        vision_active = False
    
    
    mana_addr = find_pattern_in_full_memory(pm, MANA_PATTERN)
    if not mana_addr:
        infinite_mana_active = False
    else:
        original_mana_bytes = pm.read_bytes(mana_addr, 6)
        infinite_mana_active = False

    
        
    try:
        while True:
            if keyboard.is_pressed('f1') and insta_addr:
                insta_active = not insta_active
                if insta_active:
                    patch_instakill(pm, insta_addr, newmem)
                    print("Инста-килл ВКЛ")
                else:
                    restore_original(pm, insta_addr, original_insta)
                    print("Инста-килл ВЫКЛ")
                time.sleep(0.3)

            if keyboard.is_pressed('f2') and godmode_addr:
                no_damage_active = not no_damage_active
                toggle_godmode(pm, godmode_addr, original_damage, no_damage_active)
                status = "ВКЛ" if no_damage_active else "ВЫКЛ"
                print(f"godmode {status}")
                time.sleep(0.3)
            
            if keyboard.is_pressed('f3') and mana_addr:
                infinite_mana_active = not infinite_mana_active
                toggle_infinite_mana(pm, mana_addr, original_mana_bytes, infinite_mana_active)
                status = "ВКЛ" if infinite_mana_active else "ВЫКЛ"
                print(f"Бесконечная мана {status}")
                time.sleep(0.3)
            
            if keyboard.is_pressed('f4'):
                vision_active = not vision_active
                toggle_permanent_vision(pm, miner_addr, hunter_addr, danger_addr, orig_miner, orig_hunter, vision_active)
                status = "ВКЛ" if vision_active else "ВЫКЛ"
                print(f"Глаз алмаз {status}")
                time.sleep(0.3)
                
            if keyboard.is_pressed('backspace'):
                break


            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        if insta_addr and not insta_active:
            patch_instakill(pm, insta_addr, newmem)
        pm.close_process()

if __name__ == "__main__":
    main()