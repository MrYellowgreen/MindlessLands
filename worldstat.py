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
        if not self.all_monsters:
            res += 'It was a little boring game'
            return res
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
        res += self.get_monster_table()
        res += '\n---------------------------------------------------------\n'
        res += 'Bth - birthday, Dth - day of death, Frc - force, Hth - health,'
        res += '\nReg - regeneration, Vis - visibility, Gen - generation,\n'
        res += 'Kil - amount of kills, Cld - amount of children'
        return res

    def get_monster_table(self):
        #The worst code you've ever seen
        if not self.all_monsters:
            return ''
        num_len = len(str(len(self.all_monsters)))
        head = '{:<{}}'.format('N:', num_len + 1) + '| Name:      '
        strings = []
        for m_num in range(len(self.all_monsters)):
            m = self.all_monsters[m_num]
            strings.append('{:>{}} | {:<11}'.format(m_num + 1,
                                                    num_len, m.name))
        max_len_birthday = 5
        max_len_death = 5
        max_len_force = 5
        max_len_health = 5
        max_len_regeneration = 5
        max_len_visibility = 5
        max_len_generation = 5
        max_len_kills = 5
        max_len_children = 5
        for m in self.all_monsters:
            max_len_birthday = max(max_len_birthday, len(str(m.birthday)))
            max_len_death = max(max_len_death, 1 + len(str(m.death)))
            max_len_force = max(max_len_force, 1 + len(str(m.force)))
            max_len_health = max(max_len_health, 1 + len(str(m.max_hp)))
            max_len_regeneration = max(max_len_regeneration,
                                       1 + len(str(m.regeneration)))
            max_len_visibility = max(max_len_visibility,
                                     1 + len(str(m.visibility)))
            max_len_generation = max(max_len_generation,
                                     1 + len(str(m.generation)))
            max_len_kills = max(max_len_kills, 1 + len(str(m.kills)))
            max_len_children = max(max_len_children, 1 + len(str(m.children)))
        head += '{:<{}}'.format('Bth:', max_len_birthday)
        head += '{:<{}}'.format('Dth:', max_len_death)
        head += '{:<{}}'.format('Frc:', max_len_force)
        head += '{:<{}}'.format('Hth:', max_len_health)
        head += '{:<{}}'.format('Reg:', max_len_regeneration)
        head += '{:<{}}'.format('Vis:', max_len_visibility)
        head += '{:<{}}'.format('Gen:', max_len_generation)
        head += '| '
        head += '{:<{}}'.format('Kil:', max_len_kills)
        head += '{:<{}}'.format('Cld:', max_len_children)
        for m_num in range(len(self.all_monsters)):
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].birthday, max_len_birthday)
            if self.all_monsters[m_num].death:
                strings[m_num] += '{:<{}}'.format(
                    self.all_monsters[m_num].death, max_len_death)
            else:
                strings[m_num] += '{:<{}}'.format('--', max_len_death)
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].max_force, max_len_force)
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].max_hp, max_len_health)
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].max_regeneration,
                    max_len_regeneration)
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].max_visibility, max_len_visibility)
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].generation, max_len_generation)
            strings[m_num] += '| '
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].kills, max_len_kills)
            strings[m_num] += '{:<{}}'.format(
                self.all_monsters[m_num].children, max_len_children)
        res = head
        for string in strings:
            res += '\n' + string
        return res

    def str_monster_list(self, monster_list):
        res = ''
        for m in monster_list:
            res += '{}, '.format(m.name)
        return res[:-2]
