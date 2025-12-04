from random import randint, choice

LOCATIONS = ("Дикий лес", "Подземелье", "Снежные горы", "Деревня", "Луга")
ITEMS = ("Граната", "Граната", "Граната",
         "Динамит", "Динамит",
         "Лекарства", "Лекарства", "Лекарства",
         "Лечебное зелье", "Лечебное зелье",
         "Мясо", "Мясо", "Мясо",
         "Лунный камень",
         "Зелье урона", "Зелье урона",
         "Щит", "Щит", "Щит")


ENEMIES_1_LVL = ("Гоблин", "Волк", "Дикий кабан")
ENEMIES_2_LVL = ("Скелет", "Зомби", "Бандит")
ENEMIES_3_LVL = ("Голем", "Лавовый слизень")
ENEMIES_4_LVL = ("Колдун", "Адская гончая")
ENEMIES_5_LVL = ("Староста Давид", "Фенрир")


class Player:
    def __init__(self):
        self.enemy = None
        self.name = input("Введите ваше имя: ").capitalize()
        player_choice = False
        self.xp = 0
        self.level = 5

        self.items = ["Граната"] # Предметы
        self.effects = [] # Эффекты
        self.temp_effects = [] # Эффекты на 1 атаку

        while not player_choice:
            self.health = randint(90, 110)
            self.damage = randint(30,60)
            self.armor = randint(10, 20)
            self.avoidance = randint(30, 55)

            self.show_status()
            if input("1 - оставить характеристики\n"
                     "Любой другой ввод - заново\n") == "1":
                player_choice = True
        self.max_health = self.health

        input("Нажмите enter чтобы начать")
        self.walk()


    def show_status(self):
        print(f"Ваши характеристики: {self.name}\n"
              f"Здоровье: {self.health}\n"
              f"Броня: {self.armor}\n"
              f"Урон: {self.damage}\n"
              f"Уклоняемость: {self.avoidance}\n"
              f"Предметы: {self.items}\n"
              f"Эффекты: {self.effects}")

    def walk(self):

        print("="*100)

        location = choice(LOCATIONS)
        location_type = choice(("нашли сундук", "нашли сундук",
                                "встретили врага", "встретили врага", "встретили врага",
                                "увидели, что всё спокойно", "увидели, что всё спокойно"))
        print(f"Вы случайно забрели в {location} и {location_type}")

        match location_type:
            case "нашли сундук":
                print()
                print("Случайный сундук перед вами")

                if self.level < 2:
                    count = randint(1, 2)
                elif self.level < 4:
                    count = randint(2, 3)
                else:
                    count = randint(3, 4)

                loot = []

                print("Вы видите в сундуке следующие предметы:")

                for _ in range(count):
                    item = choice(ITEMS)
                    loot.append(item)
                    print("-> " + item)



                print()
                print("Вы залутали сундук")


                for item in loot:
                    self.items.append(item)

                input("Нажмите enter для продолжения")
                self.walk()


            case "встретили врага":
                print()

                match self.level:
                    case 1:
                        enemy_name = choice(ENEMIES_1_LVL)
                    case 2:
                        enemy_name = choice((choice(ENEMIES_1_LVL), choice(ENEMIES_2_LVL)))
                    case 3:
                        enemy_name = choice((choice(ENEMIES_3_LVL), choice(ENEMIES_2_LVL), choice(ENEMIES_1_LVL)))
                    case 4:
                        enemy_name = choice((choice(ENEMIES_4_LVL), choice(ENEMIES_3_LVL), choice(ENEMIES_2_LVL),
                                             choice(ENEMIES_1_LVL)))
                    case 5:
                        enemy_name = choice(ENEMIES_5_LVL)
                    case _:
                        enemy_name = "Если ты это видишь то что то не так"

                self.enemy = Enemy(enemy_name)
                self.battle()

            case "увидели, что всё спокойно":
                print()

                if self.health < self.max_health:
                    self.health = self.max_health
                    print("Вы отдохнули и восстановили здоровье")
                else:
                    print("Вы отдохнули")

                input("Нажмите enter чтобы продолжить")

                self.walk()



    def battle(self):
        print("-" * 50 + "Враг" + "-" * 50)

        print("|" + self.enemy.name + "|")
        print(f"Здоровье: {self.enemy.health}")
        print(f"Атака:  {self.enemy.damage}")
        print(f"Защита: {self.enemy.armor}%")
        print("-"*10)
        print("|" + self.name + "|")
        print(f"Ваше здоровье: {self.health}  {bar(self.health, self.max_health, 20)}")
        print(f"Ваша атака: {self.get_damage(self.enemy)[0]}")

        damage = self.get_damage(self.enemy)[1]
        if len(damage) > 0:
            print("Бонусы к атаке: ",*damage)

        print(f"Ваша защита: {self.armor}%")
        print(f"Шанс уклонения: {self.avoidance}")
        print()
        print(f"Ваш уровень: {self.level}  {bar(self.level, 5, 5)}")
        print(f"Ваш опыт: {self.xp}  {bar(self.xp, self.level * 100, 20)}")



        print()
        print("Ваши действия:")
        print("1 - Атака")
        print("2 - Использовать предмет")
        print("3 - Увернуться")

        player_choice = None
        try:
            player_choice = int(input("Выберите действие: "))
        except ValueError:
            print("Ошибка, вы ввели не число")
        match player_choice:
            case 1:
                self.attack(self.enemy)
            case 2:
                self.use_item()
            case 3:
                self.avoid(self.enemy)
            case _:
                print("Неизвестный выбор")
                self.battle()


    def attack(self, enemy):
        armor = 1 - (enemy.armor / 100)
        damage =  self.get_damage(enemy)[0] * armor
        enemy.health -= damage
        self.temp_effects = []
        print("-" * 50 + "Атака" + "-" * 50)
        print(f"Вы нанесли врагу {damage} урона")

        if enemy.health <= 0:
            print("-" * 50 + "Победа" + "-" * 50)
            print("Вы победили!")

            if enemy.name in ("Староста Давид", "Фенрир"):
                self.victory()
            else:
                self.health += 30
                if self.health <= self.max_health:
                    print("Вы восстановили 30 здоровья")
                else:
                    print("Вы восстановили здоровье до предела")
                    self.health = self.max_health

                self.xp += enemy.xp
                max_xp = self.level * 100
                print(f"Опыт +{enemy.xp}")

                if self.xp >= max_xp:
                    self.xp = 0
                    self.level += 1
                    print(f"Новый {self.level} уровень!")


                self.walk()
        else:
            armor = 1 - (self.armor / 100)
            enemy_damage = enemy.damage * armor
            self.health -= enemy_damage
            print(f"{enemy.name} нанёс вам {enemy_damage} урона")

            if self.health <= 0:
                self.death()
            else:
                self.battle()



    def use_item(self):
        print("-" * 50 + "Использование" + "-" * 50)

        if len(self.items) == 0:
            print("У вас нет предметов")
        else:
            for i, item in enumerate(self.items):
                print(i + 1, item)


            player_choice = False
            while not player_choice:
                try:
                    player_choice = int(input("Выберите действие: "))
                except ValueError:
                    print("Ошибка, вы ввели не число")

                if player_choice == 0:
                    break

                else:
                    is_werewolf = "Оборотень" in self.effects
                    try:
                        item = self.items[player_choice - 1]
                    except IndexError:
                        print("Предмет с таким номером не найден")
                        continue

                    print()

                    match item:
                        case "Граната"| "Динамит"| "Зелье урона":
                            if is_werewolf:
                                print(f"Оборотни не умеют пользоваться предметами, вы теряете {item}")
                            else:
                                print(f"Вы использовали {item}")
                                self.temp_effects.append(item)
                            self.items.remove(item)

                        case "Лекарства":
                            if is_werewolf:
                                print(f"Оборотням нельзя питаться человеческими лекарствами, вы теряете их")
                            else:
                                print("Вы подлечились")
                                self.health += 20
                            self.items.remove(item)

                        case "Лечебное зелье":
                            if is_werewolf:
                                print(f"Оборотни не умеют пить из бутылок")
                            else:
                                print("Вы подлечились")
                                self.health += 50
                            self.items.remove(item)

                        case "Мясо":
                            self.temp_effects.append("Мясо")
                            self.items.remove(self.items[player_choice - 1])
                            if is_werewolf:
                                self.health += 50
                                print("Вы съели мясо, ррррр (+50 здоровья оборотню)")
                            else:
                                self.health += 30
                                print("Вы съели мясо (+30 здоровья)")
                        case "Лунный камень":
                            if is_werewolf:
                                self.effects.remove("Оборотень")
                                print("Вы превратились в человека")
                            else:
                                self.effects.append("Оборотень")
                                print("Вы превратились в оборотня")
                        case "Щит":
                            if is_werewolf:
                                print("Вы не можете использовать этот предмет будучи оборотнем")
                            else:
                                self.armor += 5
                                print("Вы прибавили 5% к своей защите")
                            self.items.remove(item)
        print()
        self.battle()


    def avoid(self, enemy):
        print("-" * 50 + "Уворот" + "-" * 50)
        chance = randint(1, 100)
        if chance < self.avoidance:
            print("Вы успешно увернулись от атаки и восстановили 20 здоровья")
            self.health += 20
            self.battle()
        else:
            print("Вы не смогли увернуться от атаки")
            armor = 1 - (self.armor / 100)
            self.health -= enemy.damage * armor
            print(f"Вы потеряли {enemy.damage * armor} здоровья")
            if self.health <= 0:
                self.death()
            else:
                self.battle()



    def get_damage(self, enemy) -> (int, list):
        descriptions = []
        damage = self.damage
        for effect in self.effects:
            match effect:
                case "Оборотень":
                    descriptions.append("+20 Оборотень")
                    damage += 20
        for effect in self.temp_effects:
            match effect:
                case "Граната":
                    descriptions.append("+30 Граната")
                    damage += 30
                case "Динамит":
                    descriptions.append("+50 Динамит")
                    damage += 50
                case "Мясо":
                    if "Оборотень" in self.effects:
                        descriptions.append("+30 Мясо(оборотень)")
                        damage += 30
                    else:
                        damage += 20
                        descriptions.append("+20 Мясо")
                case "Зелье урона":
                    descriptions.append("+30 Зелье урона")
                    damage += 30
        if "Волк" in enemy.effects and "Оборотень" in self.effects:
            damage -= 20
            descriptions.append("-20 Враг-волк (вы оборотень)")


        return damage, descriptions

    def death(self):
        print("-" * 50 + "Смерть" + "-" * 50)
        print(f"{self.enemy.name} уничтожил вас")
        print("Игра окончена")

        input("Нажмите enter чтобы закончить игру")

    def victory(self):
        print(f"Поздравляем! Вы прошли игру, победив {self.enemy.name}")

        input("Нажмите enter чтобы закончить игру")




class Enemy:
    def __init__(self, name):
        self.name = name
        match name:
            case "Староста Давид":
                self.health = 5
                self.damage = 100
                self.armor = 99
                self.xp = 0
                self.effects = []
            case "Гоблин"| "Дикий кабан"| "Скелет"| "Зомби"| "Бандит":
                self.health = randint(80, 120)
                self.damage = randint(20, 40)
                self.armor = randint(0, 10)
                self.xp = 40
                self.effects = []
            case "Голем"| "Колдун":
                self.health = randint(110, 150)
                self.damage = randint(50, 70)
                self.armor = randint(5, 20)
                self.xp = 80
                self.effects = []
            case "Волк":
                self.health = 50
                self.damage = 20
                self.armor = 0
                self.xp = 20
                self.effects = ["Волк"]
            case "Фенрир":
                self.health = 500
                self.damage = 200
                self.armor = 0
                self.xp = 0
                self.effects = ["Волк"]
            case "Лавовый слизень":
                self.health = 100
                self.damage = 40
                self.armor = 0
                self.xp = 100
                self.effects = []
            case "Адская гончая":
                self.health = 150
                self.damage = 70
                self.armor = 5
                self.xp = 150
                self.effects = []


def bar(xp: int, max_xp: int, length: int) -> str:
    k = round((xp / max_xp) * length)
    s = "=" * k + "-" * (length - k)
    return "|" + s + "|"




print("Very good RPG game")
player = Player()

