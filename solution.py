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
    # Делаем data атрибутом самого класса, а не конкретного объекта
    data = []

    @classmethod
    def write(cls, file_path):
        cls.data = []  # Очищаем перед загрузкой
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Читаем строки, игнорируя абсолютно пустые
                lines = [line.strip() for line in file if line.strip()]

                if not lines:
                    print(f" ПРЕДУПРЕЖДЕНИЕ: Файл '{file_path}' пустой!")
                    return cls.data

                # Заголовки (первая строка) пропускаем, идем по данным
                for line_num, line in enumerate(lines[1:], start=2):
                    # Разбиваем строку по точке с запятой
                    values = line.split(';')

                    # Если полей вдруг меньше 8, добьем их пустыми строками, чтобы код не падал
                    while len(values) < 8:
                        values.append("")

                    # Берем только первые 8 значений, если их больше
                    ticket = AirTicket(*values[:8])
                    cls.data.append(ticket)

        except FileNotFoundError:
            print(f" ОШИБКА: Файл '{file_path}' не найден в папке с проектом!")
            print("Убедитесь, что он лежит в той же директории, откуда вы запускаете код.")

        return cls.data