# Кабачев С.С.
import random
import random as rnd


# Класс, хранящий параметры игры
class Param:
    size_field_square = 6  # размер игрового поля рекомендуемое максимальное значение 9, минимальное 6
    numb_torpedo = 4       # количество одноклеточных кораблей
    numb_destroyer = 2     # количество двухклеточных кораблей
    numb_cruiser = 1       # количество трехклеточных кораблей
    max_score = numb_torpedo + numb_destroyer * 2 + numb_cruiser * 3  # общее количество кораблей


# класс позиции, хранящий значения х и у
class Pos:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


class Ship:  # Корабль
    def __init__(self, pos) -> None:
        self.setpos(pos)

    def setpos(self, pos):
        self.pos = pos

    def getpos(self):
        return self.pos


class Torpedo(Ship):  # 1-клеточный корабль
    def __init__(self, pos=None) -> None:
        super().__init__(pos)
        self.len_ = 1
        self.name = 'Torpedo     ■'


class Destroyer(Ship):  # 2-клеточный корабль
    def __init__(self, pos=None) -> None:
        super().__init__(pos)
        self.len_ = 2
        self.name = 'Destroyer   ■ ■'


class Cruiser(Ship):  # 3-клеточный корабль
    def __init__(self, pos=None) -> None:
        super().__init__(pos)
        self.len_ = 3
        self.name = 'Cruiser     ■ ■ ■'


class Desk:  # Игровая доска
    def __init__(self, size_fild, max_score) -> None:
        self.max_score = max_score                          # Максимально возможное количество попаданий
        self.PC_occupied_cells = self.gen_mtx(size_fild)    # Таблица с занятыми клетками поля PC
        self.PC_mtx_ship = self.gen_mtx(size_fild)          # Таблица с кораблями ПК
        self.PC_draw_mtx = self.gen_mtx(size_fild)          # Таблица ПК отображаемая
        self.User_occupied_cells = self.gen_mtx(size_fild)  # Таблица с занятыми клетками поля PC
        self.User_mtx_ship = self.gen_mtx(size_fild)        # Таблица с кораблями игрока/отображаемая
        self.numb_ship = NumbShip(Param.numb_torpedo, Param.numb_destroyer, Param.numb_cruiser).list  # Набор кораблей
        self.user_score = 0  # текущие попадания в поле игрока
        self.PC_score = 0    # текущие попадания в поле ПК

    @staticmethod
    def gen_mtx(size):  # метод генерации игровых матриц игроков
        mtx = [['o' for i in range(size)] for j in range(size)]
        return mtx

    def gen_pc_mtx_ships(self): # метод расстановки кораблей ПК
        res = self.ship_pos_random(self.PC_occupied_cells, self.PC_mtx_ship)
        self.PC_occupied_cells = res[1]
        self.PC_mtx_ship = res[2]

    def gen_user_mtx_ships(self):  # метод автоматической расстановки кораблей пользователя
        self.ship_pos_random(self.User_occupied_cells, self.User_mtx_ship)

    # Автоматическая расстановка кораблей по правилам игры. Используется как для ПК матрицы так и для матрицы игрока
    def ship_pos_random(self, occupied_cells, mtx_ship, count=0):

        def func(ship_obj, occupied_cells_obj, mtx_ship_obj):  # функция нахождения места для конкретного корабля

            if ship_obj.len_ > 1:   # если длина корабля больше 1 клетки
                orient = rnd.randint(1, 2)  # определим горизонтальную или вертикальную ориентацию корабля
                res = self.rand(ship_obj, occupied_cells_obj, mtx_ship_obj, orient)
                if not res[0]:  # если не получилось установить корабль, то повернем его на 90 градусов и повторим
                    orient = 3 - orient

                    res = self.rand(ship_obj, occupied_cells_obj, mtx_ship_obj, orient)

            else:   #  если длина корабля 1
                orient = 0
                res = self.rand(ship_obj, occupied_cells_obj, mtx_ship_obj, orient)

            return res

        numb_ship_gamer = self.numb_ship.copy()
        random.shuffle(numb_ship_gamer)  # "перемешаем" список кораблей, чтобы уменьшить закономерности
        fl_successfully = []
        res_ = True
        for ship in numb_ship_gamer:  # для каждого корабля из списка вызываем метод нахождения места для него

            fl_successfully = func(ship, occupied_cells, mtx_ship)
            if not fl_successfully[0]:
                res_ = fl_successfully[0]

        if res_:
            if count > 0:
                print('Попыток', count + 1)
            print("Все корабли размещены успешно!")

            return fl_successfully

        while not res_:  # если функция не справилась с первого раза, то даем ей еще максимально 100 попыток (рекусия)

            count += 1
            if count == 101:
                print("\nНе все корабли установлены, измените параметры игры в классе 'Param'")

                return count, occupied_cells, mtx_ship

            occupied_cells = self.gen_mtx(Param.size_field_square)
            mtx_ship = self.gen_mtx(Param.size_field_square)
            if count % 10 == 0:
                print("Не удалось разместить все корабли\nпопыток", count)
            res_ = self.ship_pos_random(occupied_cells, mtx_ship, count)

        return res_

    @staticmethod
    def rand(ship_obj, occupied_cells, mtx_ship, orient):  # Рандомайзер координат кораблей
        successfully = False

        # в случайном порядке перебираем строки или столбцы в зависимости от длины/ориентации корабля
        # чтобы в случайном порядке установить его в одно из свободных мест
        len_numb = len(occupied_cells) if orient < 2 else len(occupied_cells[0])
        ls = list(range(len_numb))

        random.shuffle(ls)

        for i in ls:
            list_cells = []
            for i_ in range(len_numb - (ship_obj.len_ - 1)):
                # формируем список возможных позиций корабля в выбранной строке
                fl = True
                for i__ in range(ship_obj.len_):
                    a, b = i, i_ + i__
                    if orient == 2:
                        a, b = b, a
                    if occupied_cells[a][b] != 'o':
                        fl = False
                if fl:
                    list_cells.append(i_)
            #  если список с позициями не пустой, то установим корабль в эту строку, выбрав одну из позиций рандомом
            #  устанавливаем корабль и заполняем матрицу с занятыми клетками
            if list_cells:
                successfully = True
                random.shuffle(list_cells)
                if orient < 2:  # для торпед и горизонтальных кораблей
                    for n in range(ship_obj.len_):
                        occupied_cells[i][list_cells[0] + n] = '*'
                        mtx_ship[i][list_cells[0] + n] = '■'
                        occupied_cells[min(len(occupied_cells) - 1, i + 1)][list_cells[0] + n] = '*'
                        occupied_cells[max(0, i - 1)][list_cells[0] + n] = '*'

                    occupied_cells[i][max(0, list_cells[0] - 1)] = '*'
                    occupied_cells[i][min(len(occupied_cells) - 1, list_cells[0] + ship_obj.len_)] = '*'

                    break

                else:  # для вертикальных кораблей
                    for n in range(ship_obj.len_):
                        occupied_cells[list_cells[0] + n][i] = '*'
                        mtx_ship[list_cells[0] + n][i] = '■'
                        occupied_cells[list_cells[0] + n][min(len(occupied_cells[0]) - 1, i + 1)] = '*'
                        occupied_cells[list_cells[0] + n][max(0, i - 1)] = '*'

                    occupied_cells[max(0, list_cells[0] - 1)][i] = '*'
                    occupied_cells[min(len(occupied_cells[0]) - 1, list_cells[0] + ship_obj.len_)][i] = '*'

                    break

        return successfully, occupied_cells, mtx_ship

    @staticmethod
    def user_set(ship_obj, occupied_cells, mtx_ship, orient):  # установка корабля пользователем вручную
        successfully = False
        x = ship_obj.pos.x
        y = ship_obj.pos.y
        len_numb = len(occupied_cells) if orient < 2 else len(occupied_cells[0])
        list_cells = []
        l_str = len_numb - (ship_obj.len_ - 1)
        if int(orient) < 2:
            if y + 1 > l_str:
                return successfully
        elif orient == 2:
            if x + 1 > l_str:
                return successfully
        # формируем список возможных позиций корабля в выбранной строке
        fl = True
        if orient == 2:
            x, y = y, x
        for i__ in range(ship_obj.len_):
            a, b = x, y + i__
            if orient == 2:
                a, b = b, a
            if occupied_cells[a][b] != 'o':
                fl = False
        if fl:
            list_cells.append(x)

        #  устанавливаем корабль и заполняем матрицу с занятыми клетками
        if list_cells:
            successfully = True

            if orient < 2:  # для торпед и горизонтальных кораблей
                for n in range(ship_obj.len_):
                    occupied_cells[x][y + n] = '*'
                    mtx_ship[x][y + n] = '■'

                    occupied_cells[min(len(occupied_cells) - 1, x + 1)][y + n] = '*'
                    occupied_cells[max(0, x - 1)][y + n] = '*'
                occupied_cells[x][max(0, y - 1)] = '*'
                occupied_cells[x][min(len(occupied_cells) - 1, y + ship_obj.len_)] = '*'

            else:  # для вертикальных кораблей
                for n in range(ship_obj.len_):
                    occupied_cells[y + n][x] = '*'
                    mtx_ship[y + n][x] = '■'

                    occupied_cells[y + n][min(len(occupied_cells[0]) - 1, x + 1)] = '*'
                    occupied_cells[y + n][max(0, x - 1)] = '*'
                occupied_cells[max(0, y - 1)][x] = '*'
                occupied_cells[min(len(occupied_cells[0]) - 1, y + ship_obj.len_)][x] = '*'

        return successfully

    def hits(self, pos, gamer):  # функция принимает координаты выстрела, имя игрока, возвращает результат попадания
        res = 0
        x = pos.x - 1
        y = pos.y - 1
        if gamer == 'User':
            score = self.user_score
            cell_tab = self.PC_mtx_ship
            draw_tab = self.PC_draw_mtx
        else:
            score = self.PC_score
            cell_tab = self.User_mtx_ship
            draw_tab = self.User_mtx_ship
        cell = cell_tab[x][y]

        if cell == '■':
            cell_tab[x][y] = 'X'
            draw_tab[x][y] = 'X'
            score += 1
            if score != self.max_score:
                res = 1  # Попали
            else:
                res = -1  # Выиграли

        elif cell == 'o':
            cell_tab[x][y] = '•'
            draw_tab[x][y] = '•'
            res = 0        # Мимо
        elif cell == '•' or cell == 'X':
            res = 2        # Уже стреляли сюда

        if gamer == 'User':  # Фиксируем количество попаданий
            self.user_score = score
        else:
            self.PC_score = score
        return res


class NumbShip:  # Создает набор объектов кораблей (без координат), согласно параметрам игры
    def __init__(self, numb_torpedo, numb_destroyer, numb_cruiser) -> None:
        self.list = list()
        self.add_list(numb_torpedo, numb_destroyer, numb_cruiser)

    def add_list(self, numb_torpedo, numb_destroyer, numb_cruiser):

        for i in range(numb_torpedo):
            self.list.append(Torpedo())
        for i in range(numb_destroyer):
            self.list.append(Destroyer())
        for i in range(numb_cruiser):
            self.list.append(Cruiser())
        return self.list


class ConsoleGameGui:  # Игровая консоль
    def __init__(self, size, max_score) -> None:

        self.game_desk = Desk(size, max_score)  # Создаем объект игровой доски
        self.size = size
        self.go = False
        self.list_set_ships = []     # Список видов кораблей (для установки вручную)
        self.set_list_set_ships = [] # Список всех неустановленных кораблей (для установки вручную)

    def run(self):  # запуск игры
        running = True
        self.game_desk.gen_pc_mtx_ships() # расставляем корабли компьютера (скрытая от пользователя матрица)

        while running:
            self.conclusion()  # выводим игровую доску
            if not self.go: # если корабли игрока (человека) не расставлены, то вызываем функцию "подготовки к игре"
                running = self.preparation()
                if not running:
                    continue
            else:
                running = self.hit()  # после устанвки кораблей пользователя начинаем "перестреливаться" с ПК

    def preparation(self): # подготовка к игре
        cmd = 0
        # запрашиваем команды у пользователя
        print('------------------')
        print('0. exit')
        print('1. установить корабль')
        print('2. Установить корабли автоматически')
        try:
            cmd = int(input())
            # если команда 0 - идем на выход
            if cmd == 0:
                running = False
                return running
            elif cmd < 0 or cmd > 2:
                raise ValueError('неправильный ввод')
        except ValueError:
            print('\n НЕПРАВИЛЬНЫЙ ВВОД !!!')
            return self.preparation()

        # если команда 1 запрашиваем координаты
        if cmd == 1:   # ручная установка кораблей

            for i in self.game_desk.numb_ship:
                self.list_set_ships.append(i.name)
            self.set_list_set_ships = list(set(self.list_set_ships))
            self.set_list_set_ships.sort(reverse=True)
            self.input_ship()
            return True

        if cmd == 2:  # автоматическая установка кораблей
            res = self.game_desk.ship_pos_random(self.game_desk.User_occupied_cells, self.game_desk.User_mtx_ship)
            self.game_desk.User_occupied_cells = res[1]
            self.game_desk.User_mtx_ship = res[2]
            self.go = True
            running = True
            return running

    def input_ship(self):  # пользователь расставляет корабли

        while self.list_set_ships:  # пока список с кораблями не пустой
            self.conclusion()
            str_ = '\nДоступные корабли:\n'
            z = 1
            for value in self.set_list_set_ships:
                str_ += str(z) + '. ' + str(self.list_set_ships.count(value)) + 'шт ' + value + '\n'
                z += 1
            print(str_)
            try:  # обрабатываем ошибки ввода
                cmd = int(input('Введите номер корабля: '))
                if 1 < cmd < 4 and self.list_set_ships.count(self.set_list_set_ships[cmd - 1]) > 0:
                    orient = int(input('Введите положение корабля: \n 1. Горизонтальное\n 2. Вертикальное\n'))
                    if not (orient == 1 or orient == 2):
                        raise ValueError('неправильный ввод')

                elif cmd == 1 and self.list_set_ships.count(self.set_list_set_ships[cmd - 1]) > 0:
                    orient = 0
                else:
                    raise ValueError('неправильный ввод')

                x = int(input('input X: '))
                y = int(input('input Y: '))
                if any([x < 1, x > len(self.game_desk.User_mtx_ship), y < 1,
                        y > len(self.game_desk.User_mtx_ship)]):
                    raise ValueError('неправильный ввод')

                successfully = self.set_ship(x, y, orient, cmd)
                if not successfully:
                    print("\nНЕВОЗМОЖНО установить корабль в выбранное место !")
                    self.input_ship()
                else:
                    self.list_set_ships.remove(self.set_list_set_ships[cmd - 1])  # удаляем корабль из списка
            except ValueError:
                print('\n НЕПРАВИЛЬНЫЙ ВВОД !!!')
                self.input_ship()
        self.go = True  # Начинаем стрелять!

    def set_ship(self, x, y, orient, cmd):  # передачи координат пользователя для попытки установки корабля
        set_ = Pos(x - 1, y - 1)
        if cmd == 2:
            obj = Destroyer(set_)
        elif cmd == 1:
            obj = Torpedo(set_)
        else:
            obj = Cruiser(set_)

        successfully = self.game_desk.user_set(obj, self.game_desk.User_occupied_cells, self.game_desk.User_mtx_ship,
                                                                                                                orient)
        return successfully

    def hit(self):  # Перестрелка (анализирум выстрелы, выводим сообщение в конце игры)
        running = True
        len_x = len(self.game_desk.PC_mtx_ship)
        len_y = len(self.game_desk.PC_mtx_ship[0])
        try:   # Обрабатываем ошибки ввода
            print("Введите координаты выстрела")
            hit_user = Pos(int(input('input X: ')), int(input('input Y: ')))

            if any([hit_user.x < 1, hit_user.x > len_x,
                   hit_user.y < 1, hit_user.y > len_y]):
                raise ValueError('неправильный ввод')
            else:
                print('Бьем сюда! ', hit_user.x, hit_user.y)
                res = self.game_desk.hits(hit_user, "User")
            if res == -1:
                self.conclusion()
                print('*************************\n -- Победил Человек! --\n*************************')
                running = False
            elif res == 2:
                print("УПС, сюда уже стреляли...")
                return self.hit()
            elif res == 1:
                print("Попали!")

        except ValueError:
            print('\n НЕПРАВИЛЬНЫЙ ВВОД !!!')
            return self.hit()

        res_pc = 2
        while res_pc == 2:
            hit_pc = Pos(rnd.randint(1, len_x), rnd.randint(1, len_y))
            res_pc = self.game_desk.hits(hit_pc, "PC")
        if res_pc == -1:
            self.conclusion()
            print('*************************\n ----- GAME OVER ! -----\n*************************')
            running = False

        return running

    def conclusion(self):  # вывод игровой матрицы в консоль
        max_score = str(self.game_desk.max_score)
        str_user = '  User desk' if not self.go else 'User desk ' + str(self.game_desk.PC_score) + '/' + max_score
        str_pc = '    PC desk' if not self.go else 'PC desk ' + str(self.game_desk.user_score) + '/' + max_score
        x = min(1, len(str_user) - 7)
        matrix_str = '\n          ' + str_user + '  ' * 2 * (self.size - x) + str_pc + '\n   y→\nx↓  '

        for i in range(len(self.game_desk.User_mtx_ship)):
            matrix_str += ' | ' + str(i + 1)
        matrix_str += ' |      '

        for i in range(len(self.game_desk.PC_mtx_ship)):
            matrix_str += ' | ' + str(i + 1)
        matrix_str += " |\n"

        for i in range(len(self.game_desk.User_mtx_ship)):
            matrix_str += '   ' + str(i + 1) + " | " + ' | '.join(self.game_desk.User_mtx_ship[i]) + ' |'
            matrix_str += '   ' + '  ' + str(i + 1) + " | " + ' | '.join(self.game_desk.PC_draw_mtx[i]) + ' |\n'

        print(matrix_str)


if __name__ == "__main__":

    gui = ConsoleGameGui(Param.size_field_square, Param.max_score)  # создаем объект игры
    gui.run()                                                       # стартуем игру


# SkillFactory FPW140 kabachev@bk.ru
