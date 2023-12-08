import requests
import json

class ConvertionExeptions(Exception):
    pass

class ValuteConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeptions("Данная операция не имеет смысла")

        try:
            quote_tiker = Valutes.base_value_dict[quote]
        except:
            raise ConvertionExeptions(f'Не знаю о валюте "{quote}"')

        try:
            base_tiker = Valutes.base_value_dict[base]
        except:
            raise ConvertionExeptions(f'Не знаю о валюте "{base}"')
        try:
            amount = float(amount)
        except:
            raise ConvertionExeptions(f"Не удалось обработать количество: {amount}")

        valute_one = quote
        valute_one_rub = Valutes.base_value_dict[quote]['Value']/Valutes.base_value_dict[quote]['Nominal']
        valute_two = base
        valute_two_rub = Valutes.base_value_dict[base]['Value']/Valutes.base_value_dict[base]['Nominal']
        valute_one_total_rub = valute_one_rub * amount
        valute_two_total = valute_one_total_rub / valute_two_rub

        return valute_two_total

class Valutes:
    base_value_dict = {}
    update_time = ""
    def update_valutes():
        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        text_js = json.loads(r.content)
        Valutes.update_time = text_js['PreviousDate']
        dict_value = text_js["Valute"]

        Valutes.base_value_dict['RUB'] = {"Name": "Российский рубль", "Value": 1, "Nominal": 1}
        for each in dict_value:
            name = dict_value[each]["Name"]
            char_code = dict_value[each]['CharCode']
            value = dict_value[each]['Value']
            nominal = dict_value[each]['Nominal']
            Valutes.base_value_dict[char_code] = {'Name': name, 'Value': value, 'Nominal':nominal}