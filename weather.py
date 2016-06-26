import random


class Climat:
    def __init__(self, world):
        self.world = world
        self.rndm = random.Random()
        self.weather = Fair(world.move_number, world)

    def make_move(self):
        res = []
        if self.weather.end_condition():
            self.weather.end()
            last_weather = self.weather
            self.make_random_weather()
            if self.weather.get_name() != last_weather.get_name():
                res.append(('weather', self.weather.get_name()))
        return res + self.weather.effect()

    def get_symbol(self):
        if self.rndm.randint(0, 3) == 0:
            return self.weather.get_symbol()
        return '.'

    def make_random_weather(self):
        attrs = (self.world.move_number, self.world)
        r = self.rndm.randint(0, 99)
        if r < 50:
            self.weather = Fair(*attrs)
        elif r < 65:
            self.weather = Rain(*attrs)
        elif r < 80:
            self.weather = Snow(*attrs)
        elif r < 95:
            self.weather = RainAndSnow(*attrs)
        else:
            self.weather = Hail(*attrs)


class Weather:
    def __init__(self, day_begin, world):
        self.day_begin = day_begin
        self.world = world
        self.rndm = random.Random()

    def effect(self):
        return []

    def end(self):
        pass

    def get_symbol(self):
        return '.'


class Fair(Weather):
    def end_condition(self):
        return self.rndm.randint(0, 19) == 0

    def get_name(self):
        return 'fair'


class Rain(Weather):
    def end_condition(self):
        return self.rndm.randint(0, 19) == 0

    def get_name(self):
        return 'rain'

    def get_symbol(self):
        return '/'

    def effect(self):
        if self.day_begin == self.world.move_number:
            for m in self.world.monsters:
                m.visibility -= 3
        return []

    def end(self):
        for m in self.world.monsters:
            m.visibility += 3


class Snow(Weather):
    def end_condition(self):
        return self.rndm.randint(0, 19) == 0

    def get_name(self):
        return 'snow'

    def get_symbol(self):
        return '*'

    def effect(self):
        res = []
        for m in self.world.monsters:
            if self.day_begin == self.world.move_number:
                m.force = max(0, m.force - 2)
                m.visibility = max(0, m.visibility - 2)
            m.hp -= 1
            if m.hp <= 0:
                res.append(m.die('snow'))
        return res

    def end(self):
        for m in self.world.monsters:
            m.force = m.max_force
            m.visibility = m.max_visibility


class RainAndSnow(Weather):
    def end_condition(self):
        return self.rndm.randint(0, 19) == 0

    def get_name(self):
        return 'rain and snow'

    def get_symbol(self):
        if self.rndm.randint(0, 1) == 0:
            return '/'
        return '*'

    def effect(self):
        res = []
        for m in self.world.monsters:
            if self.day_begin == self.world.move_number:
                m.force = max(0, m.force - 2)
                m.visibility = max(0, m.visibility - 4)
            m.hp -= 1
            if m.hp <= 0:
                res.append(m.die('rain and snow'))
        return res

    def end(self):
        for m in self.world.monsters:
            m.force = m.max_force
            m.visibility = m.max_visibility


class Hail(Weather):
    def end_condition(self):
        return (self.world.move_number - self.day_begin >= 10 or
                self.rndm.randint(0, 9) == 0)

    def get_name(self):
        return 'hail'

    def get_symbol(self):
        return '`'

    def effect(self):
        res = []
        for m in self.world.monsters:
            m.hp -= 5
            if m.hp <= 0:
                res.append(m.die('hail'))
        return res
