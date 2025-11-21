from random import randint, choice

Location = ["Дикий лес", "Подземелье", "Снежные горы", "Деревня", "Луга"]
Items = ["Граната", "Динамит", "Лекарства", "Лечебное зелье", "Мясо", "Лунный камень"]
Enemies = ["Давид", "Гоблин", "Гоблин", "Гоблин", "Волк", "Фенрир", "Иван", "Колдун"]

class Player:
    def __init__(self):
        self.name = input("Введите ваше имя: ")
        player_choice = False
        self.specie = "Человек"
        self.xp = 0
        self.level = 0

        self.items = ["Граната"] # Предметы
        self.effects = [] # Эффекты
        self.equipment = [] # Экипировка (количество доступных предметов зависит от уровня)

        while not player_choice:
            self.health = randint(90, 110)
            self.damage = randint(30,60)
            self.armor = randint(10, 30)
            self.avoidance = randint(10, 30)

            self.show_status()
            if input("1 - оставить характеристики\n"
                     "Любой другой ввод - заново\n") == "1":
                player_choice = True

            input("Нажмите enter чтобы начать")
            self.walk()


    def show_status(self):
        print(f"Ваши характеристики: {self.name}\n"
              f"Вид: {self.specie}\n"
              f"Здоровье: {self.health}\n"
              f"Броня: {self.armor}\n"
              f"Урон: {self.damage}\n"
              f"Уклоняемость: {self.avoidance}\n"
              f"Предметы: {self.items}\n"
              f"Эффекты: {self.effects}")

    def walk(self):
        location = choice(Location)
        type = choice(("нашли сундук", "встретили врага", "встретили врага", "встретили врага",
                       "увидели, что всё спокойно"))
        print(f"Вы случайно забрели в {location} и {type}")

        match type:
            case "нашли сундук":
                print("Случайный сундук перед вами")
                if self.level < 5:
                    count = randint(1, 2)
                else:
                    count = randint(2, 3)

                loot = []

                print("Вы видите в сундуке следующие предметы:")

                for _ in range(count):
                    item = choice(Items)
                    loot.append(item)
                    print(item)

                print("Вы залутали сундук")
                self.items.append(*loot)

            case "встретили врага":





player = Player()

