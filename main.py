import sys
import console_play


class Game():
    def __init__(self):
        self.size = 25
        self.slowness = 0.5

    def menu(self):
        print()
        print('Menu:')
        print('1. Play')
        print('2. FAQ')
        print('3. Settings')
        print('4. Exit')
        answer = input()
        if answer == '4':
            sys.exit(0)
        if answer == '1':
            print()
            console_play.main(self.size, self.slowness)
            print('Enter or any command for back to menu')
            input()
            self.menu()
        elif answer == '2':
            self.faq()
        elif answer == '3':
            self.settings()
        else:
            print('There is no command like "{}"! Use numerals.'.
                  format(answer))
            self.menu()

    def settings(self):
        print()
        print('Settings:')
        print('1. Change size of world')
        print('2. Change slowness of game')
        print('3. Back to menu')
        answer = input()
        if answer == '1':
            self.change_size()
        elif answer == '2':
            self.change_slowness()
        elif answer == '3':
            self.menu()
        else:
            print('Incorrect command. Read list again, silly one!')
            self.settings()

    def change_size(self):
        print()
        print('Change size of world')
        print('Current size: {}'.format(self.size))
        print('10 - small')
        print('25 - medium')
        print('50 - big. Game can be veeeery loooooong')
        print('Or any natural number.' + 
              ' Caution! Big numbers can crash something :)')
        print("...or 'menu' for back to menu")
        answer = input()
        if answer == 'menu':
            self.menu()
        try:
            answer = int(answer)
        except ValueError:
            print("It is not natural number. Didn't you know it?")
            self.change_size()
        if answer <= 0:
            print("'Natural' means bigger than 0, okay?")
            self.change_size()
        self.size = answer
        print('Changed to {}'.format(self.size))
        self.menu()

    def change_slowness(self):
        print()
        print('Change slowness of game')
        print('Current slowness: {}'.format(self.slowness))
        print('0 - as fast as possible')
        print('0.25 - fast')
        print('0.5 - standart. Recommended')
        print('1 - slow. If you want to read all')
        print('Or any real number not less than 0')
        print('Just remember, Ctrl + C can help you to kill really slow game')
        print("...or 'menu' to back to menu")
        answer = input()
        if answer == 'menu':
            self.menu()
        try:
            answer = float(answer)
        except ValueError:
            print("It's not real number. It doesn't exist!")
            self.change_slowness()
        if answer < 0:
            print("'not less than 0' - I wrote it, didn't I?")
            self.change_slowness()
        self.slowness = answer
        print('Changed to {}'.format(self.slowness))
        self.menu()

    def faq(self):
        print()
        print('FAQ:')
        with open('faq.txt') as f:
            for s in f.readlines():
                print(s[:-1])
        print('Enter or any command for return to menu')
        input()
        self.menu()


def main():
    print('                          ***   MINDLESS LANDS   ***')
    print('                              Last hero dies too')
    g = Game()
    g.menu()


if __name__ == '__main__':
    main()
