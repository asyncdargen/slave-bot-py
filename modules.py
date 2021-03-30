from typing import Mapping
from threading import Thread
import re
import requests
import random
import time
import string
import math


# Упрощённое чтение Mapping
class JsonReader:

    def __init__(self, json: Mapping = {}):
        self.json = json

    def read(self, path: str):
        splited_path = path.split(".")
        obj = self.json
        for s in splited_path:
            obj = obj[s]
        return obj

    def section(self, path: str):
        return JsonReader(self.read(path))


# Отправка request`ов
class Request:

    def __init__(self, cfg: JsonReader):
        value = cfg.read("VALUE")
        if str(cfg.read("METHOD").upper()) == "TOKEN":
            get = requests.get(
                "https://api.vk.com/method/apps.get",
                params={
                    "app_id": 7794757,
                    "platform": "ios",
                    "v": 5.23,
                    "access_token": value,
                },
            ).json()
            if "response" not in get:
                raise Exception("invalid response")
            url = get["response"]["mobile_iframe_url"]
            match = re.search(r"index.html\?(.*)", url)
            try:
                self.auth = match.group(1)
            except:
                raise Exception("can't parse bearer")
        else:
            self.auth = value

    def request(
            self, endpoint: str, query: Mapping = {}, body: Mapping = {}
    ) -> Mapping:
        method = "GET"
        if body != {}:
            method = "POST"
        return requests.request(
            method,
            "https://pixel.w84.vkforms.ru/HappySanta/slaves/1.0.0" + endpoint,
            params=query,
            json=body,
            headers={
                "authorization": "Bearer " + self.auth,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                "origin": "https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com",
                "referer": f'https://prod-app7794757-c1ffb3285f12.pages-ac.vk-apps.com/index.html?{self.auth}',
            },
        ).json()

    def start(self, ref_id: int = 0) -> Mapping:
        return self.request("/start", query=({"ref": ref_id} if ref_id != 0 else {}))

    def user(self, id: int = 0) -> Mapping:
        return self.request("/user", query=({"id": id} if id != 0 else {}))

    def slave_list(self, id: int = 0) -> Mapping:
        return self.request("/slaveList", query=({"id": id} if id != 0 else {}))

    def top_users(self) -> Mapping:
        return self.request("/topUsers")

    def sale_slave(self, slave_id: int) -> Mapping:
        return self.request("/saleSlave", body={"slave_id": slave_id})

    def buy_slave(self, slave_id: int) -> Mapping:
        return self.request("/buySlave", body={"slave_id": slave_id})

    def job_slave(self, slave_id: int, job_name: str) -> Mapping:
        return self.request("/jobSlave", body={"slave_id": slave_id, "name": job_name})

    def buy_fetter(self, slave_id: int) -> Mapping:
        return self.request("/buyFetter", body={"slave_id": slave_id})


# Генерация работ
class JobGen:

    def __init__(self, cfg: JsonReader):
        self.type = str(cfg.read("METHOD")).upper()
        self.list = cfg.read("LIST")

    def get(self):
        if self.type == 'RANDOM':
            return self.randomChar();
        elif self.type == 'LIST':
            return self.randomJob()
        else:
            if random.randint(0, 1) == 1:
                return self.randomChar()
            else:
                return self.randomJob()

    def randomJob(self):
        return str(self.list[random.randint(0, len(self.list) - 1)])

    def randomChar(self):
        if random.randint(0, 1) == 1:
            return random.choice(string.ascii_letters).upper()
        else:
            return str(random.randint(0, 10))


# Клиент-апи
class Client:

    def __init__(self, request: Request):
        self.req = request

    def setLogger(self, log):
        self.log = log.get()

    def start(self):
        try:
            start = self.req.start()
            return start
        except Exception as e:
            self.log.debug(str(e))
            self.log.debug("Ошибка в запросе start")
            time.sleep(15)
            return start()

    def get_user(self, id):
        try:
            user = self.req.user(id=id)
            return user
        except Exception as e:
            self.log.debug(str(e))
            self.log.debug("Ошибка в запросе user")
            time.sleep(15)
            return self.get_user(id)

    def get_slaves(self, id):
        try:
            slaves = self.req.slave_list(id=id)
            return slaves
        except Exception as e:
            self.log.debug(str(e))
            self.log.debug("Ошибка в запросе slavesList")
            time.sleep(15)
            return self.get_slaves(id)

    def buy(self, id):
        try:
            buy = self.req.buy_slave(slave_id=id)
            set = False
            try:
                if 'ErrFlood' in buy['error']['message']:
                    set = True
            except Exception as e:
                set = False
            self.log.buyban = set
            if set:
                self.log.debug("Возможен бан на покупку")
                time.sleep(15)
                return self.buy(id)
            return buy
        except Exception as e:
            self.log.debug(str(e))
            self.log.debug("Ошибка в запросе buySlave")
            time.sleep(15)
            return self.buy(id)

    def job(self, id, name):
        try:
            job = self.req.job_slave(slave_id=id, job_name=name)
            set = False
            try:
                if 'ErrFlood' in job['error']['message']:
                    set = True
            except Exception as e:
                set = False
            self.log.jobban = set
            if set:
                self.log.debug("Возможен бан на работу")
                time.sleep(15)
                return self.job(id, name)
            return job
        except Exception as e:
            self.log.debug(str(e))
            self.log.debug("Ошибка в запросе jobSlave")
            time.sleep(15)
            return self.job(id)

    def fetter(self, id):
        try:
            fetter = self.req.buy_fetter(slave_id=id)
            set = False
            try:
                if 'ErrFlood' in fetter['error']['message']:
                    set = True
            except Exception as e:
                set = False
            self.log.fetterban = set
            if set:
                self.log.debug("Возможен бан на оковы")
                time.sleep(15)
                return self.fetter(id)
            return fetter
        except Exception as e:
            self.log.debug(str(e))
            self.log.debug("Ошибка в запросе fetterSlave")
            time.sleep(15)
            return self.fetter(id)

    def sale(self, id):
        try:
            sale = self.req.sale_slave(slave_id=id)
            set = False
            try:
                if 'ErrFlood' in sale['error']['message']:
                    set = True
            except Exception as e:
                set = False
            self.log.saleban = set
            if set:
                self.log.debug("Возможен бан на продажу")
                time.sleep(15)
                return self.sale(id)
            return sale
        except Exception as e:
            self.log.debug(str(e))
            self.log.debug("Ошибка в запросе jobSale")
            time.sleep(15)
            return self.sale(id)


# Логер бота
class Logger:

    def __init__(self, cfg: JsonReader, request: Request):
        self.req = request;
        self.id = cfg.read("ACCOUNT.ID")
        self.tge = cfg.read("TG_LOG.ENABLED")
        self.tg_token = cfg.read("TG_LOG.TOKEN")
        self.tg_debug = cfg.read("TG_LOG.DEBUG")
        self.tg_chat_id = f'@{cfg.read("TG_LOG.CHAT_ID")}'
        self.dg = cfg.read("ACCOUNT.DEBUG")
        self.initValues()
        Thread(target=self.logging).start()

    def initValues(self):
        req = self.req.user(self.id)
        self.last_slaves = req['slaves_count']
        self.last_balance = req['balance']
        self.last_income = req['slaves_profit_per_min']
        self.last_pos = req['rating_position']
        self.fetterban = False
        self.saleban = False
        self.buyban = False
        self.jobban = False
        self.start = time.time()

    def logging(self):
        while True:
            try:
                req = self.req.user(self.id)
                out = "===== Статистика =====\n"
                out += "💵 Баланс: " + str(req['balance']) + " RUB" + "\n"
                out += "💸 Доход: " + str(req['slaves_profit_per_min']) + " RUB/мин (+" + str(
                    req['slaves_profit_per_min'] - self.last_income) + ")" + "\n"
                out += "⏱ Время работы: " + str(math.floor((time.time() - self.start) / 60)) + "мин" + "\n"
                out += "📊 Позиция в топе: " + str(req['rating_position']) + " (+" + str(
                    self.last_pos - req['rating_position']) + ")" + "\n"
                out += "👥 Рабы: " + str(req['slaves_count']) + " (+" + str(
                    req['slaves_count'] - self.last_slaves) + ")" + "\n"
                out += "💢 Возможные баны" + "\n"
                out += "  Покупка: " + ("✔" if self.buyban else "❌") + "\n"
                out += "  Продажа: " + ("✔" if self.saleban else "❌") + "\n"
                out += "  Оковы: " + ("✔" if self.fetterban else "❌") + "\n"
                out += "  Работа: " + ("✔" if self.jobban else "❌") + "\n"
                out += "===== Статистика ====="
                self.log(out)
                time.sleep(15)
            except Exception as e:
                self.debug(str(e))
                self.debug("Ошибка в получении статистики")

    def tg(self, msg):
        if self.tge:
            requests.request(
                "GET",
                f'https://api.telegram.org/bot{self.tg_token}/sendMessage',
                params={"chat_id": self.tg_chat_id, "text": str(msg)},
                json={}
            )

    def log(self, msg):
        print(str(msg))
        self.tg(msg)

    def debug(self, msg):
        if self.dg:
            out = f'[DEBUG] >> {str(msg)}'
            print(out)
            if self.tg_debug:
                self.tg(out)

    def get(self):
        return self;