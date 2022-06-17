import random

class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, length: int, prow, direction: bool, lives: int):
        self.length: int = length
        self.prow = prow # Point() class, self.prow.x|y
        self.direction: bool = direction # True - vertical, False - horizontal
        self.lives: int = lives

    def get_points(self):
        points = []
        if self.direction:
            for i in range(self.length):
                points.append(Point(self.prow.x, self.prow.y + i))
        else:
            for i in range(self.length):
                points.append(Point(self.prow.x + i, self.prow.y))
        return points

class Field:
    def __init__(self, status: list, ships: list, hid: bool, alive_ships: int):
        self.status: list = status
        self.ships: list = ships
        self.hid: bool = hid
        self.alive_ships: int = alive_ships

    def show_field(self):
        print("    ", end = "")
        for i in range(6):
            print(i + 1, "| ", end = "")
        print()
        for i in range(6):
            print(i + 1, '| ', end = '')
            for j in range(6):
                if self.hid and self.status[j][i] == 'O':
                    print(' ', '| ', end = '')
                else:
                    print(self.status[j][i], '| ', end = '')
            print()

    def out(self, point):
        return point.x < 0 or point.x > 5 or point.y < 0 or point.y > 5

    def get_contour(self, ship):
        contour = []
        # ship.get_points()
        for point in ship.get_points():
            point_contour = [Point(point.x, point.y + 1),
                             Point(point.x, point.y - 1),
                             Point(point.x + 1, point.y),
                             Point(point.x - 1, point.y),
                             Point(point.x + 1, point.y + 1),
                             Point(point.x - 1, point.y + 1),
                             Point(point.x + 1, point.y - 1),
                             Point(point.x - 1, point.y - 1)]
            for each_point in point_contour:
                if not each_point in contour and not each_point in ship.get_points():
                    contour.append(each_point) 
        return contour

    def used(self, point):
        try:
            return self.status[point.x][point.y] == 'O'
        except IndexError:
            pass

    def add_ship(self, ship):
        contour = self.get_contour(ship)
        for point in ship.get_points():
            try:
                if self.out(point) or self.used(point):
                    raise PointError()
                for contour_point in contour:
                    if self.used(contour_point):
                        raise PointError()
            except PointError:
                return False
        for point in ship.get_points():
            self.status[point.x][point.y] = 'O'
        return True

    def shot(self, point):
        try:
            char = self.status[point.x][point.y]
            if char in ['.', 'X'] or self.out(point):
                raise ShotError
        except ShotError:
            return False 
        else:
            return True

class Player:
    def __init__(self, user_field, ai_field):
        self.user_field = user_field
        self.ai_field = ai_field
    
    def ask(self):
        pass

    def move(self, field):
        while True:
            point = self.ask()
            if field.shot(point):
                break
        if field.status[point.x][point.y] == 'O':
            field.status[point.x][point.y] = 'X'
            return True
        else:
            field.status[point.x][point.y] = '.'
            return False


class Ai(Player):
    def ask(self):
       return Point(random.randint(0, 5), random.randint(0, 5))

class User(Player):
    def ask(self):
        while True:
            try:
                x = int(input('Enter x:'))
                y = int(input('Enter y:'))
                return Point(x - 1, y - 1)
            except:
                continue

class Game:
    def get_random_ship(self, size, points):
        prow = random.choice(points)
        self.ship = Ship(size, prow, bool(random.randint(0, 1)), size)
        return self.ship
    
    def random_field(self):
        field = Field(status=[[' ' for _ in range(6)] for _ in range(6)], ships = [], hid = False, alive_ships = 11)
        field_points = []
        for i in range(6):
            for j in range(6):
                field_points.append(Point(j, i))
        lengths = [3, 2, 2, 1, 1, 1, 1]
        i = 0
        for length in lengths:
            while True:
                i += 1
                if i > 5000:
                    return None
                ship = self.get_random_ship(size = length, points = field_points)
                add_ship = field.add_ship(ship)
                if add_ship:
                    break
        return field
                
    def get_field(self):
        field = None
        while field is None:
            field = self.random_field()
        return field

    def greet(self):
        print('Hello!')
        print('Enter x and y to shot')

    def loop(self):
        ai_field = self.get_field()
        ai_field.hid = True
        print('ai field:')
        ai_field.show_field()
        print('---')
        user_field = self.get_field()
        print('user field:')
        user_field.show_field()
        print('---')
        ai = Ai(user_field = ai_field, ai_field = user_field)
        user = User(user_field = user_field, ai_field = ai_field)
        move_label = bool(random.randint(0, 1))
        shot_result = None
        while True:
            if move_label:
                while True:
                    if ai_field.alive_ships == 0:
                        return 'You win!'
                    shot_result = user.move(ai_field)
                    print('ai field:')
                    user_field.show_field()
                    print('---')
                    ai_field.show_field()
                    print('---')
                    if shot_result:
                        ai_field.alive_ships -= 1
                        continue
                    else:
                        break
            else:
                while True:
                    if ai_field.alive_ships == 0:
                        return 'AI win!'
                    shot_result = ai.move(user_field)
                    print('user field:')
                    user_field.show_field()
                    print('---')
                    ai_field.show_field()
                    print('---')
                    if shot_result:
                        user_field.alive_ships -= 1
                        continue
                    else:
                        break

            move_label = not move_label


    def start(self):
        self.greet()
        print(self.loop())

class Error(Exception):
    pass
class PointError(Error):
    pass
class ShotError(Error):
    pass