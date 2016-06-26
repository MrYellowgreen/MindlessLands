class WorldStat:
    def __init__(self, world):
        self.all_monsters = []
        self.world = world
        self.best_killer = None
        self.best_parent = None
        self.longliver = None
        self.zero_lifespan = []

    def add_monster(self, monster):
        self.all_monsters.append(monster)

    def get_stat(self):
        self.zero_lifespan = []
        for m in self.all_monsters:
            self.update_stat(m)
        return self

    def update_stat(self, monster):
        self.update_best_killer(monster)
        self.update_best_parent(monster)
        self.update_longliver(monster)
        self.update_zero_lifespan(monster)

    def update_zero_lifespan(self, monster):
        if self.get_lifespan(monster) == 0 and not monster.alive:
            self.zero_lifespan.append(monster)

    def update_longliver(self, monster):
        if self.longliver is None:
            self.longliver = monster
            return
        current_lifespan = self.get_lifespan(self.longliver)
        monster_lifespan = self.get_lifespan(monster)
        if monster_lifespan > current_lifespan:
            self.longliver = monster

    def get_lifespan(self, monster):
        if monster.death:
            return monster.death - monster.birthday
        else:
            return monster.world.move_number - monster.birthday

    def update_best_killer(self, monster):
        if self.best_killer is None or self.best_killer.kills < monster.kills:
            self.best_killer = monster

    def update_best_parent(self, monster):
        if (self.best_parent is None or self.best_parent.children <
          monster.children):
            self.best_parent = monster

    def __str__(self):
        res = 'Total amount of monsters: {}\n'.format(len(self.all_monsters))
        res += 'Amount of days: {}\n'.format(self.world.move_number)
        res += 'Best killer: {} ({} kills)\n'.format(self.best_killer.name,
                                                     self.best_killer.kills)
        res += 'Best parent: {} ({} children)\n'.format(self.best_parent.name,
                                                self.best_parent.children)
        res += 'The longest life: {} ({} days)\n'.format(self.longliver.name,
                                            self.get_lifespan(self.longliver))
        if self.zero_lifespan:
            res += 'Killed in cradle: {}\n'.format(self.str_monster_list(
                self.zero_lifespan))
        res += 'Table of monsters:\n'
        res += 'Name:      Bth: Dth: Frc: Hth: Reg: Vis: Gen: | Kil: Cld: \n'
        for m in self.all_monsters:
            res += self.get_stat_string(m) + '\n'
        res += '---------------------------------------------------------\n'
        res += 'Bth - birthday, Dth - day of death, Frc - force, Hth - health,'
        res += '\nReg - regeneration, Vis - visibility, Gen - generation,\n'
        res += 'Kil - amount of kills, Cld - amount of children'
        return res

    def str_monster_list(self, monster_list):
        res = ''
        for m in monster_list:
            res += '{}, '.format(m.name)
        return res[:-2]

    def get_stat_string(self, monster):
        res = monster.name
        while len(res) < 11:
            res += ' '
        res += self.get_stat_elem(str(monster.birthday))
        if monster.death is not None:
            res += self.get_stat_elem(str(monster.death))
        else:
            res += '--   '
        res += self.get_stat_elem(str(monster.max_force))
        res += self.get_stat_elem(str(monster.max_hp))
        res += self.get_stat_elem(str(monster.max_regeneration))
        res += self.get_stat_elem(str(monster.max_visibility))
        res += self.get_stat_elem(str(monster.generation))
        res += '| '
        res += self.get_stat_elem(str(monster.kills))
        res += self.get_stat_elem(str(monster.children))
        return res

    def get_stat_elem(self, elem):
        res = elem
        for i in range(5 - len(elem)):
            res += ' '
        return res
