from typing import List

from rasa_core_sdk.forms import FormAction, EntityFormField
from rasa_core_sdk.events import SlotSet
from requests import (
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    Timeout
)
import ipdb
from duckling import Duckling 
from duckling.language import Language
from api import get_weather_by_day

duckling_engine = Duckling()
duckling_engine.load()

def compute_relative_time(data_context):
    current_data_config = duckling_engine.parse('now')
    input_data_config = duckling_engine.parse(data_context, language=Language.CHINESE)
    current_data_value = current_data_config[-1]['value']['value']
    input_data_value = input_data_config[-1]['value']['value']
    current_date = current_data_value.split('T')[0].split('-')[-1]
    input_date = input_data_value.split('T')[0].split('-')[-1]
    relative_time = int(input_date) - int(current_date)
    return relative_time

class ActionReportWeather(FormAction):
    RANDOMIZE = True

    @staticmethod
    def required_fields():
        return [
            EntityFormField("address", "address"),
            EntityFormField("date-time", "date-time"),
        ]

    def name(self):
        # type: () -> Text
        return "action_report_weather"

    def submit(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        address = tracker.get_slot('address')
        date_time = tracker.get_slot('date-time')
        date_time_number = text_date_to_number_date(date_time)
        if isinstance(date_time_number, str):  # parse date_time failed
            return [SlotSet("matches", "暂不支持查询 {} 的天气".format([address, date_time_number]))]
        else:
            weather_data = get_text_weather_date(address, date_time, date_time_number)
            return [SlotSet("matches", "{}".format(weather_data))]


def get_text_weather_date(address, date_time, date_time_number):
    try:
        result = get_weather_by_day(address, date_time_number)
    except (ConnectionError, HTTPError, TooManyRedirects, Timeout) as e:
        text_message = "{}".format(e)
    else:
        text_message_tpl = """
            {} {} ({}) 的天气情况为：白天：{}；夜晚：{}；气温：{}-{} °C
        """
        text_message = text_message_tpl.format(
            result['location']['name'],
            date_time,
            result['result']['date'],
            result['result']['text_day'],
            result['result']['text_night'],
            result['result']["high"],
            result['result']["low"],
        )

    return text_message


def text_date_to_number_date(text_date):
    if text_date == "今天":
        return 0
    elif text_date == "明天":
        return 1
    elif text_date == "后天":
        return 2

    # Not supported by weather API provider freely
    elif text_date == "大后天":
        # return 3
        return text_date
    elif text_date == "昨天":
        return text_date
    elif text_date == "前天":
        return text_date
    elif text_date == "大前天":
        return text_date
    else:
        return compute_relative_time(text_date)
    """
    if text_date.startswith("星期"):
        # TODO: using calender to compute relative date
        return text_date

    if text_date.startswith("下星期"):
        # TODO: using calender to compute relative date
        return text_date

    # follow APIs are not supported by weather API provider freely
    """