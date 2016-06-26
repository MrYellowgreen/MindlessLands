import random


class Monster:
    def __init__(self, coord, world, hp=None, force=None, name=None,
                 visibility=None, regeneration=None, birthday=0, generation=0):
        self.rndm = random.Random()
        self.alive = True
        self.birthday = birthday
        self.death = None
        self.generation = generation
        self.kills = 0
        self.children = 0
        if regeneration is None:
            self.regeneration = self.rndm.randint(0, 3)
        else:
            self.regeneration = regeneration
        self.max_regeneration = self.regeneration
        if visibility:
            self.visibility = visibility
        else:
            self.visibility = self.rndm.randint(4, 10)
        self.max_visibility = self.visibility
        if hp:
            self.hp = hp
        else:
            self.hp = self.rndm.randint(10, 50)
        self.max_hp = self.hp
        if force:
            self.force = force
        else:
            self.force = self.rndm.randint(1, 12)
        self.max_force = self.force
        if name:
            self.name = name
        else:
            self.generate_name()
        self.coord = coord
        self.world = world

    def generate_name(self):
        vowel = ['a', 'e', 'i', 'o', 'u', 'y']
        consonant = [x for x in [chr(x) for x in range(97, 123)]
                     if x not in vowel]
        vowel_amount = 0
        name_length = self.rndm.randint(3, 10)
        name_builder = chr(self.rndm.randint(65, 90))
        if name_builder in vowel:
            vowel_amount += 1
        for i in range(name_length - 1):
            if self.rndm.randint(0, 5) == 0:
                name_builder += chr(self.rndm.randint(97, 122))
            elif vowel_amount > len(name_builder) / 2:
                name_builder += consonant[self.rndm.randint(0, 19)]
            elif vowel_amount < len(name_builder) / 3:
                name_builder += vowel[self.rndm.randint(0, 5)]
            else:
                name_builder += chr(self.rndm.randint(97, 122))
            if name_builder[-1] in vowel:
                vowel_amount += 1
        self.name = name_builder

    def die(self, reason):
        self.alive = False
        self.death = self.world.move_number
        if type(reason) == Monster:
            return ('murder', reason, self)
        if reason == 'snow':
            return ('killed by weather', 'snow', self)
        if reason == 'rain and snow':
            return ('killed by weather', 'rain and snow', self)
        if reason == 'hail':
            return ('killed by weather', 'hail', self)

    def make_move(self):
        if not self.alive:
            return
        strike = self.try_strike()
        if strike is None:
            self.hp = min(self.max_hp, self.hp + self.regeneration)
            return self.walk()
        if strike[0] == 'murder':
            self.kills += 1
            return strike

    def try_find_enemy(self):
        enemy_left = None
        enemy_right = None
        for cell in range(self.coord - self.visibility, self.coord):
            if self.world[cell]:
                enemy_left = cell
        for cell in range(self.coord + 1, self.coord + self.visibility + 1):
            if self.world[cell]:
                enemy_right = cell
                break
        if not (enemy_left or enemy_right):
            return None
        if not enemy_left:
            return 1
        if not enemy_right:
            return -1
        left_dist = -enemy_left + self.coord
        right_dist = enemy_right - self.coord
        if left_dist < right_dist:
            return -1
        if left_dist > right_dist:
            return 1
        return self.rndm.randint(-1, 1)

    def walk(self):
        direction = self.try_find_enemy()
        if direction:
            self.coord += direction
            return
        if self.coord == 0:
            self.coord += 1
        elif self.coord == len(self.world) - 1:
            self.coord -= 1
        else:
            direction = self.rndm.randint(-2, 2)
            if direction != 0:
                direction //= abs(direction)
            self.coord += direction

    def try_strike(self):
        left_cell = self.world[self.coord - 1]
        right_cell = self.world[self.coord + 1]
        direction = self.rndm.randint(0, 1)
        if left_cell or right_cell:
            if (direction == 0 or not right_cell) and left_cell:
                return self.strike(self.coord - 1)
            return self.strike(self.coord + 1)

    def strike(self, coord):
        if abs(self.coord - coord) != 1:
            raise ValueError("Monster can't strike this cell")
        opponent = self.world[coord]
        if type(opponent) != Monster:
            raise ValueError("No monster to strike it")
        brunt = self.brunt_formula(opponent)
        opponent.hp -= brunt
        if opponent.hp <= 0:
            return opponent.die(self)
        return ('strike', self, opponent)

    def brunt_formula(self, other):
        r = (self.rndm.random()/2) + 0.5
        return int(self.force * r + 0.5)
