import os
import random
import time

try:
    import msvcrt  # Windows: для режима «нажми Enter или подожди»
except ImportError:
    msvcrt = None


class Hero:

    def __init__(self, name, trans, hp, damage, armor):
        self.name = name
        self.trans = trans
        self.hp = hp
        self.damage = damage
        self.armor = armor
        self.lvl = 1

    def print_info(self):
        print(f"Имя: {self.name}")
        print(f"Пол: {self.trans}")


    def strike(self, enemy):
        dice = random.randint(1, 20)

        if dice == 1:
            print(f"{self.name} кинул кубик d20: 1 — промах!")
            return

        if dice == 20:
            print(f"{self.name} кинул кубик d20: 20 — КРИТИЧЕСКИЙ УДАР!")
            dmg = self.damage * 3
        else:
            print(f"{self.name} кинул кубик d20: {dice}")
            dmg = round(self.damage * dice / 10)

        print(f"{self.name} атакует {enemy.name} на {dmg} урона")
        enemy.armor -= dmg
        if enemy.armor <= 0:
            enemy.hp += enemy.armor
            enemy.armor = 0
        if enemy.hp < 0:
            enemy.hp = 0
        print(f"Осталось HP: у {enemy.name} — {enemy.hp}, у {self.name} — {self.hp}")

    def fight(self, enemy):
        while self.hp > 0 and enemy.hp > 0:
            print()
            input(f"{self.name}: нажми Enter, чтобы бросить кубик...")
            self.strike(enemy)
            if enemy.hp <= 0:
                print()
                print(f"{self.name} ПОБЕДИЛ")
                self.lvl += 1
                print(f"Уровень повышен до {self.lvl}")
                return True

            print()
            input(f"{enemy.name}: нажми Enter, чтобы бросить кубик...")
            enemy.strike(self)
            if self.hp <= 0:
                print()
                print(f"{self.name} повержен!")
                return False

class Warrior(Hero):
    pass

class Rogue(Hero):
    pass

class Mage(Hero):
    pass

warrior = Warrior("Алексей", "женщина", 100, 15, 10)
rogue = Rogue("Гриша", "мужчина", 80, 20, 5)
anya = Mage("Аня", "женщина", 60, 30, 2)
igor = Warrior("Игорь", "мужчина", 120, 12, 14)
sonya = Rogue("Соня", "женщина", 75, 22, 4)

heroes = [warrior, rogue, anya, igor, sonya]

CLASS_NAMES = {"Warrior": "Воин", "Rogue": "Разбойник", "Mage": "Маг"}


# ============================================================
#  СУНДУК И ДИАЛОГ С ФРОСТМОРНОМ
# ============================================================

def wait_or_enter(seconds=5):
    """Пауза после реплики: можно нажать Enter или просто подождать."""
    end = time.time() + seconds
    while time.time() < end:
        if msvcrt is not None and msvcrt.kbhit():
            key = msvcrt.getch()
            if key in (b"\r", b"\n"):
                print()
                return
        time.sleep(0.1)
    print()


def open_frostmourne_image():
    """Открыть картинку i.png из той же папки, где лежит код."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()
    image_path = os.path.join(script_dir, "i.png")

    if os.path.exists(image_path):
        os.startfile(image_path)
    else:
        print()
        print(f"Картинка не найдена: {image_path}")
        print("Положи файл i.png рядом с main.py и запусти снова.")


def frostmourne_dialogue(hero):
    """Диалог у ледяного постамента: твой герой играет роль Артаса."""
    print()
    print("=" * 42)
    print("      У ЛЕДЯНОГО ПОСТАМЕНТА")
    print("=" * 42)
    print("  (Enter — дальше, или просто подожди пару секунд)")
    print()

    lines = [
        f"{hero.name}: Смотри, Мурадин, наше спасение — Фростморн.",
        "Мурадин: (подходит к постаменту и читает надпись) Постой, парень. "
        "На постаменте есть надпись. Это предупреждение. Там написано: "
        "«Кто бы ни поднял этот клинок, обретёт вечную силу. Как лезвие разит "
        "плоть, так сила калечит дух». О, я должен был догадаться! "
        "Клинок проклят! Убираемся отсюда к чёртям!",
        f"{hero.name}: Я с радостью приму любое проклятие, чтобы спасти мою родину.",
        f"Мурадин: Оставь его, {hero.name}. Забудь об этом деле и веди своих "
        "людей домой.",
        f"{hero.name}: К чёрту людей! Ничто не помешает мне отомстить, старый "
        "друг. Даже ты. (поворачивается к постаменту и произносит заклинание) "
        "Теперь я взываю к духам этого места. Я отдам всё и заплачу любую цену, "
        "лишь бы вы помогли мне спасти мой народ.",
    ]

    for line in lines:
        print(line)
        wait_or_enter(5)

    # Картинка открывается ТОЛЬКО после того, как весь диалог дочитан
    open_frostmourne_image()


def open_chest(hero):
    """После боя: предложить открыть сундук. Внутри всегда Фростморн."""
    print()
    print("После боя ты замечаешь старый сундук.")
    answer = input("Открыть сундук? (1 — да, 0 — нет): ").strip()
    if answer != "1":
        print()
        print("Ты проходишь мимо сундука. Кто знает, что там было...")
        return

    print()
    print("Ты открываешь сундук...")
    wait_or_enter(2)

    print()
    print("Внутри ослепительно сверкает клинок — ФРОСТМОРН!")
    print("Ты берёшь его в руки, и лёд вокруг начинает шептать...")
    frostmourne_dialogue(hero)


print("Выбери героя:")
for i, hero in enumerate(heroes, 1):
    print(f"{i}. {hero.name} — {CLASS_NAMES[hero.__class__.__name__]}, пол: {hero.trans}")

while True:
    number = input("Введи номер героя: ")
    try:
        chosen = heroes[int(number) - 1]
        break
    except (ValueError, IndexError):
        print("Нет такого героя, попробуй ещё раз.")

print()
chosen.print_info()

opponents = [h for h in heroes if h is not chosen]
enemy = random.choice(opponents)
print()
print(f"БОЙ: {chosen.name} против {enemy.name}!")
print()
won = chosen.fight(enemy)

if won:
    open_chest(chosen)



        
