import random
import time
import sys
from world import World


def text_winner(monster):
    res = 'Force: {}\n'.format(monster.force)
    res += 'Health: {}/{}\n'.format(monster.hp, monster.max_hp)
    res += 'Regeneration: {}\n'.format(monster.regeneration)
    res += 'Visibility: {}\n'.format(monster.visibility)
    res += 'Generarion: {}\n'.format(monster.generation)
    res += 'Kills: {} Children: {}'.format(monster.kills, monster.children)
    return res

def murder_message(event):
    return 'MURDER: {} was killed by {}!'.format(event[2].name, event[1].name)

def rip_message(monster):
    return 'RIP {} {}-{} (gen: {}, kills: {}, children: {})'.format(
        monster.name, monster.birthday,
        monster.death, monster.generation,
        monster.kills, monster.children)

def spawn_message(event):
    res = 'SPAWN: {} spawned on cell {}.'.format(event[1].name, event[2])
    if event[3]:
        res += '\nHappy parents: {}.'.format(get_parents_names(event[3]))
    return res

def event_message(event):
    if event[0] == 'murder':
        return '{}\n{}'.format(murder_message(event), rip_message(event[2]))
    elif event[0] == 'spawn':
        return spawn_message(event)
    elif event[0] == 'weather':
        return 'WEATHER: ' + WEATHER_MESSAGE[event[1]]
    elif event[0] == 'killed by weather':
        return 'ACCIDENT: {}\n{}'.format(
            KILLED_BY_WEATHER_MESSAGE[event[1]](event[2].name),
            rip_message(event[2]))
    raise ValueError('Can not handle this event:\n{}'.format(event))

WEATHER_MESSAGE = { 'fair': 'Good news, now it is fair!',
                    'rain': 'It rains. I hope, you have an umbrella!',
                    'snow': "Well, now it's snowing. What's next?",
                    'rain and snow': ("Rain with snow. Worse than rain and" +
                                      " worse than snow."),
                    'hail': "Run and hide! Hail began." }

KILLED_BY_WEATHER_MESSAGE = {
    'snow' : lambda x: 'Snow was too cold for {}.'.format(x),
    'rain and snow': lambda x: '{} caught a cold and died.'.format(x),
    'hail': lambda x: x + ' could not hide and was killed by a big hailstone.'
    }

def get_parents_names(parentset):
    res = ''
    for m in parentset:
        res += '{}, '.format(m.name)
    return res[:-2]

def coord_line(world):
    res = '-' * len(str(world.move_number)) + '--'
    counter = 0
    while counter < world.size:
        res += str(counter)
        res += '-' * (5 - len(str(counter)))
        counter += 5
    return res

def main(world_size, slowness):
    world = World(world_size)
    game = world.go()
    print('New world was born')
    for m in world.monsters:
        print(event_message(('spawn', m, m.coord, None)))
    try:
        for step in game:
            was_event = False
            for event in step:
                if event:
                    was_event = True
                    print(event_message(event))
                    time.sleep(slowness)
            if world.move_number == 0 or was_event:
                print(coord_line(world))
            print('{}) {}'.format(world.move_number, world))
            time.sleep(slowness)
    except KeyboardInterrupt:
        print(world.stat.get_stat())
        sys.exit(1)
    if world.monsters:
        winner = world.monsters.pop()
        print('Finished! Last hero is {}'.format(winner.name))
        print(text_winner(winner))
    else:
        print('Finished. No one survived')
    print('Enter or any command to see game statistics.')
    input()
    print(world.stat.get_stat())

if __name__ == '__main__':
    main(25, 0.5)
