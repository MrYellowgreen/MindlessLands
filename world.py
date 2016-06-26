import random
import copy
from monster import Monster
from worldstat import WorldStat
import weather


class World:
    def __init__(self, size):
        self.field = []
        self.size = size
        self.move_number = 0
        self.monsters = set()
        self.stat = WorldStat(self)
        self.rndm = random.Random()
        self.weather = weather.Climat(self)
        for i in range(self.size):
            r = self.rndm.randint(0, 2)
            if r == 0:
                m = Monster(coord=i, world=self)
                self.field.append(m)
                self.monsters.add(m)
                self.stat.add_monster(m)
            else:
                self.field.append(False)

    def game_is_finished(self):
        return len(self.monsters) < 2

    def make_move(self):
        self.move_number += 1
        res = []
        res += self.weather.make_move()
        res.append(self.spawn_time())
        for m in self.monsters:
            res.append(m.make_move())
            self.update_field()
        for m in copy.copy(self.monsters):
            if not m.alive:
                self.monsters.remove(m)
        return res

    def spawn_time(self):
        if self.rndm.randint(0, 2) == 0:
            spawn = self.try_spawn_monster()
            if spawn:
                self.update_field()
                return spawn

    def try_spawn_monster(self):
        if len(self.monsters) != len(self):
            parentset = set()
            for m in self.monsters:
                if self.rndm.randint(0, 1):
                    parentset.add(m)
            if len(parentset) < 2:
                return None
            return self.spawn_monster(parentset)

    def spawn_monster(self, parentset):
        coord = self.rndm.randint(0, len(self) - 1 - len(self.monsters))
        for i in range(0, len(self)):
            if i <= coord and self[i]:
                coord = (coord + 1) % len(self)
        new_monster = self.create_monster(parentset, coord)
        self.monsters.add(new_monster)
        self.stat.add_monster(new_monster)
        return ('spawn', new_monster, coord, parentset)

    def create_monster(self, parentset, coord):
        hp =  0
        force = 0
        visibility = 0
        regeneration = 0
        generation = 1
        for m in parentset:
            m.children += 1
            generation = max(generation, m.generation + 1)
            hp += m.max_hp
            force += m.max_force
            visibility += m.max_visibility
            regeneration += m.max_regeneration
        l = len(parentset)
        hp = self.characteristic_formula(hp // l + 1, 10)
        force = self.characteristic_formula(force // l + 1, 1)
        visibility = self.characteristic_formula(visibility // l + 1, 4)
        regeneration = self.characteristic_formula(regeneration // l + 1, 0)
        return Monster(coord, self, hp=hp, force=force,
                       visibility=visibility, regeneration=regeneration,
                       birthday=self.move_number, generation=generation)

    def characteristic_formula(self, average_value, min_value):
        return max(min_value, int(average_value *
                                  (self.rndm.random() * 0.4 + 0.8)))

    def go(self):
        yield []
        while not self.game_is_finished():
            yield self.make_move()

    def update_field(self):
        for i in range(len(self.field)):
            self.field[i] = False
        for m in self.monsters:
            if m.alive:
                self.field[m.coord] = m

    def __str__(self):
        res = ''
        for i in self.field:
            if i == False:
                res += self.weather.get_symbol()
            else:
                res += i.name[0]
        return res

    def __getitem__(self, key):
        if 0 <= key < len(self.field):
            return self.field[key]
        return None

    def __len__(self):
        return len(self.field)
