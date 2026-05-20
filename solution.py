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