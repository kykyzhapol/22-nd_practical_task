import math
import re
from datetime import datetime


class Date:
    def __init__(self, in_date):
        try:
            datetime.strptime(in_date, "%d.%m.%Y")
            self.__in_date = in_date
        except ValueError:
            print('ошибка')
            self.__in_date = None

    @property
    def date(self):
        if self.__in_date == None:
            return None
        # словарь сокращений для русских месяцев
        MONTH_MAP = {
            1: "янв", 2: "фев", 3: "мар", 4: "апр",
            5: "мая", 6: "июн", 7: "июл", 8: "авг",
            9: "сен", 10: "окт", 11: "ноя", 12: "дек"
        }
        dt = datetime.strptime(self.__in_date, "%d.%m.%Y")

        formatted = f"{dt.day} {MONTH_MAP[dt.month]} {dt.year} г."
        return formatted

    @date.setter
    def date(self, value):
        if re.fullmatch(r'\d{1,2}.\d{1,2}.\d{2,4}', value):
            self.__in_date = value
        else:
            print('ошибка')
            self.__in_date = None


    def to_timestamp(self):
        dt = datetime.strptime(self.__in_date, "%d.%m.%Y")
        return int(dt.timestamp())

    def __eq__(self, other):
        dt_self = datetime.strptime(self.__in_date, "%d.%m.%Y")
        dt_other = datetime.strptime(str(other), "%d.%m.%Y")
        return dt_self == dt_other

    def __ne__(self, other):
        dt_self = datetime.strptime(self.__in_date, "%d.%m.%Y")
        dt_other = datetime.strptime(str(other), "%d.%m.%Y")
        return dt_self != dt_other

    def __lt__(self, other):
        dt_self = datetime.strptime(self.__in_date, "%d.%m.%Y")
        dt_other = datetime.strptime(str(other), "%d.%m.%Y")
        return dt_self < dt_other

    def __le__(self, other):
        dt_self = datetime.strptime(self.__in_date, "%d.%m.%Y")
        dt_other = datetime.strptime(str(other), "%d.%m.%Y")
        return dt_self <= dt_other

    def __gt__(self, other):
        dt_self = datetime.strptime(self.__in_date, "%d.%m.%Y")
        dt_other = datetime.strptime(str(other), "%d.%m.%Y")
        return dt_self > dt_other

    def __ge__(self, other):
        dt_self = datetime.strptime(self.__in_date, "%d.%m.%Y")
        dt_other = datetime.strptime(str(other), "%d.%m.%Y")
        return dt_self >= dt_other

    def __str__(self):
        return self.__in_date


class AirTicket:
    def __init__(self, passenger_name, _from, to, date_time, flight, seat, _class, gate):
        self.passenger_name = passenger_name
        self._from = _from
        self.to = to
        self.date_time = date_time
        self.flight = flight
        self.seat = seat
        self._class = _class
        self.gate = gate

    def __str__(self):
        # Форматируем под ширину столбцов вашей шапки:
        # |     NAME       |FROM|TO |   DATE/TIME    |       FLIGHT       |SEAT|CLS|GATE|
        return (f"| {self.passenger_name:<14} "
                f"|{self._from:<4}"
                f"|{self.to:<3} "
                f"| {self.date_time:<14} "
                f"| {self.flight:<18} "
                f"|{self.seat:<4}"
                f"|{self._class:<3}"
                f"|{self.gate:<4}|")


class Load:
    data = []

    @staticmethod
    def read_csv_file(file_path):
        """Вспомогательный метод: просто читает любой файл с ';' в список списков строк"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                if not lines:
                    return []
                # Возвращаем только строки с данными (без шапки), разбитые по ';'
                return [line.split(';') for line in lines[1:]]
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден.")
            return []

    @classmethod
    def write(cls, *args, **kwargs):
        """
        Универсальный метод. Автоматически адаптируется под переданные аргументы.
        """
        cls.data = []

        # СЦЕНАРИЙ 1: Передано 3 файла (Задание со встречами)
        # Load.write('meetings.txt', 'persons.txt', 'pers_meetings.txt')
        if len(args) == 3:
            meetings_file, persons_file, pers_meetings_file = args

            # Читаем сырые данные
            raw_meetings = cls.read_csv_file(meetings_file)
            raw_persons = cls.read_csv_file(persons_file)
            raw_relations = cls.read_csv_file(pers_meetings_file)

            # Создаем словари для быстрого связывания
            users_dict = {p[0].strip(): User(*p[:3]) for p in raw_persons if len(p) >= 3}
            meetings_dict = {}

            Meeting.lst_meeting = []  # Очищаем глобальный список класса Meeting

            for m in raw_meetings:
                if len(m) >= 3:
                    meeting = Meeting(*m[:3])
                    meetings_dict[m[0].strip()] = meeting
                    Meeting.lst_meeting.append(meeting)

            # Связываем сотрудников со встречами
            for r in raw_relations:
                if len(r) >= 2:
                    m_id, u_id = r[0].strip(), r[1].strip()
                    if m_id in meetings_dict and u_id in users_dict:
                        meetings_dict[m_id].add_person(users_dict[u_id])

            cls.data = Meeting.lst_meeting
            return cls.data

        # СЦЕНАРИЙ 2: Передан 1 файл (Задание с авиабилетами)
        # Параметр target_class указывает, в какой класс превращать строки (по умолчанию AirTicket)
        elif len(args) == 1:
            file_path = args[0]
            target_class = kwargs.get('target_class', AirTicket)

            raw_data = cls.read_csv_file(file_path)
            for row in raw_data:
                # Создаем объект динамически переданного класса
                obj = target_class(*row)
                cls.data.append(obj)

            return cls.data

        else:
            print("Ошибка: Неподдерживаемое количество аргументов в Load.write()")
            return cls.data

class User:
    def __init__(self, id, name, position):
        self.id = id.strip()
        self.name = name.strip()
        self.position = position.strip()

    def __str__(self):
        return f"{self.name} ({self.position})"


class Meeting:
    # Атрибут класса для хранения всех встреч
    lst_meeting = []

    def __init__(self, id, date, title):
        self.id = id.strip()
        # Оборачиваем строку даты в объект Date для корректного сравнения
        self.date = Date(date) if isinstance(date, str) else date
        self.title = title.strip()
        self.employees = []  # Список объектов User

    def add_person(self, person):
        """Добавляет сотрудника (объект User) на встречу"""
        if isinstance(person, User):
            self.employees.append(person)

    def count(self):
        """Возвращает количество участников на этой встрече"""
        return len(self.employees)

    @classmethod
    def count_meeting(cls, date):
        """Возвращает количество встреч, проходящих в указанную дату"""
        count = 0
        for meeting in cls.lst_meeting:
            if meeting.date == date:
                count += 1
        return count

    @classmethod
    def total(cls):
        """Возвращает суммарное количество участников на всех встречах"""
        return sum(meeting.count() for meeting in cls.lst_meeting)

    def __str__(self):
        # Заголовок встречи
        result = f"Рабочая встреча {self.id}\n{self.date} {self.title} \n"

        # Если участники есть, добавляем каждого с новой строки с отступом
        if self.employees:
            counter = 1
            for emp in self.employees:
                pattern = r'([^()]+)?(?:\(([^()]+)\))?'
                matches = re.findall(pattern, str(emp))
                result += f"ID: {counter} LOGIN: {matches[0][0]} NAME: {matches[0][1]}\n"
                counter +=1
        else:
            result += " [Нет участников]"

        return result


class GeometricObject:
    def __init__(self, x: float = 0.0, y: float = 0.0, color: str = "black", filled: bool = False):
        # Приватные атрибуты (согласно диаграмме __x, __y)
        self.__x = x
        self.__y = y
        # Публичные атрибуты
        self.color = color
        self.filled = filled

    def set_coordinate(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y

    def set_color(self, color: str) -> None:
        self.color = color

    def set_filled(self, filled: bool) -> None:
        self.filled = filled

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def get_color(self) -> str:
        return self.color

    def is_filled(self) -> bool:
        return self.filled

    def __str__(self) -> str:
        return f"GeometricObject(x={self.__x}, y={self.__y}, color='{self.color}', filled={self.filled})"

    def __repr__(self) -> str:
        return self.__str__()


class Circle(GeometricObject):
    def __init__(self, radius: float = 0, x: float = 0.0, y: float = 0.0, color: str = "black", filled: bool = False):
        # Вызов конструктора родительского класса
        super().__init__(x, y, color, filled)
        # Приватный атрибут
        self.__radius = radius

    # Реализация radius.getter() через декоратор property
    @property
    def radius(self) -> float:
        return self.__radius

    # Реализация radius.setter(Real)
    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            self.__radius = 0
        self.__radius = value

    def get_area(self) -> float:
        return math.pi * (self.__radius ** 2)

    def get_perimetr(self) -> float:
        return 2 * math.pi * self.__radius

    def get_diametr(self) -> float:
        return 2 * self.__radius

    def __str__(self) -> str:
        return f"Circle(radius={self.__radius}, x={self.get_x()}, y={self.get_y()}, color='{self.color}', filled={self.filled})"

    def __repr__(self) -> str:
        return self.__str__()


class Rectangle(GeometricObject):
    def __init__(self, width: float = 0, height: float = 0, x: float = 0.0, y: float = 0.0, color: str = "black", filled: bool = False):
        # Вызов конструктора родительского класса
        super().__init__(x, y, color, filled)
        # Публичные атрибуты (судя по отсутствию __ в диаграмме)
        self.width = width
        self.height = height

    def set_width(self, width: float) -> None:
        if width < 0:
             self.width = 0
        self.width = width

    def set_height(self, height: float) -> None:
        if height < 0:
             self.height = 0
        self.height = height

    def get_width(self) -> float:
        return self.width

    def get_height(self) -> float:
        return self.height

    def get_area(self) -> float:
        return self.width * self.height

    def get_perimetr(self) -> float:
        return 2 * (self.width + self.height)

    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height}, x={self.get_x()}, y={self.get_y()}, color='{self.color}', filled={self.filled})"

    def __repr__(self) -> str:
        return self.__str__()