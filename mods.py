from modules import *


class BuyMode:

    def __init__(self, config: JsonReader, log: Logger, client: Client, job: JobGen):
        if config.read("ENABLED"):
            self.jobs = job
            self.job = config.read("AUTO_JOB")
            self.fetter = config.read("AUTO_FETTER")
            self.min_profit = config.read("MIN_PROFIT")
            self.delay = config.read("DELAY")
            self.dl = config.read("DELAYED.ENABLED")
            self.dl_delay = config.read("DELAYED.DELAY")
            self.log = log
            self.client = client
            self.slaves = []
            print("Включен режим автозакупки")
            Thread(target=self.start).start()

    def delayed(self):
        time.sleep(self.dl_delay if self.dl else 0.1)
        id = self.slaves.pop()
        profit = 1
        if self.job:
            time.sleep(random.random() + 0.5)
            job = self.jobs.get()
            set = self.client.job(id, job)
            try:
                profit = set["profit_per_min"];
            except:
                profit = 1
            self.log.debug(f'Установлена работа `{job}` vk.com/id{id}')
        if profit >= self.min_profit and self.fetter:
            time.sleep(random.random() + 0.5)
            self.client.fetter(id)
            self.log.debug(f'Куплены оковы на vk.com/id{id} | {profit}RUB/мин')

    def start(self):
        while True:
            id = random.randint(0, 999999999)
            self.client.buy(id)
            self.log.debug(f'Куплен раб vk.com/id{id}')
            if self.job or self.fetter:
                self.slaves.append(id)
                Thread(target=self.delayed).start()
            time.sleep(self.delay + random.random())


class FetterMode:

    def __init__(self, config: JsonReader, log: Logger, client: Client):
        if config.read("ENABLED"):
            self.max_price = config.read("MAX_PRICE")
            self.min_profit = config.read("MIN_PROFIT")
            self.delay = config.read("DELAY")
            self.log = log
            self.client = client
            print("Включен режим оцепенения")
            Thread(target=self.start).start()

    def getSlaves(self):
        try:
            slaves = self.client.get_slaves(self.log.id)['slaves']
        except Exception as e:
            slaves = []

        to_fetter = []
        for slave in slaves:
            if slave["profit_per_min"] >= self.min_profit and slave["fetter_price"] <= self.max_price:
                to_fetter.append(slave['id'])
        return to_fetter

    def start(self):
        while True:
            slaves = self.getSlaves()
            self.log.debug(f'Найдено {len(slaves)} рабов под оцепенение')
            for slave in slaves:
                self.client.fetter(slave)
                self.log.debug(f'Куплены оковы на vk.com/id{slave}')
                time.sleep(self.delay + random.random())
            time.sleep(30000)


class JobMode:

    def __init__(self, config: JsonReader, log: Logger, client: Client, job: JobGen):
        if config.read("ENABLED"):
            self.delay = config.read("DELAY")
            self.jobs = job
            self.log = log
            self.client = client
            print("Включен режим установки работы")
            Thread(target=self.start).start()

    def getSlaves(self):
        try:
            slaves = self.client.get_slaves(self.log.id)['slaves']
        except Exception as e:
            slaves = []

        to_job = []
        for slave in slaves:
            if slave['job']['name'] == '':
                to_job.append(slave['id'])
        return to_job

    def start(self):
        while True:
            slaves = self.getSlaves()
            self.log.debug(f'Найдено {len(slaves)} рабов для установки работы')
            for slave in slaves:
                job = self.jobs.get()
                self.client.job(slave, job)
                self.log.debug(f'Установлена работа `{job}` vk.com/id{slave}')
                time.sleep(self.delay + random.random())
            time.sleep(30000)


class StealMode:

    def __init__(self, config: JsonReader, log: Logger, client: Client, job: JobGen):
        if config.read("ENABLED"):
            self.jobs = job
            self.log = log
            self.client = client
            self.job = config.read("AUTO_JOB")
            self.fetter = config.read("AUTO_FETTER")
            self.target = config.read("TARGET")
            self.min_profit = config.read("MIN_PROFIT")
            self.min_price = config.read("MIN_PRICE")
            self.max_price = config.read("MAX_PRICE")
            self.delay = config.read("DELAY")
            print("Включен режим кражи")
            Thread(target=self.start).start()

    def getSlaves(self, id):
        try:
            slaves = self.client.get_slaves(id)['slaves']
        except Exception as e:
            slaves = []

        to_steal = []
        for slave in slaves:
            if slave['fetter_to'] <= 0 and self.max_price >= slave["price"] >= self.min_price:
                to_steal.append(slave)
        return to_steal

    def start(self):
        while True:
            for user in self.target:
                slaves = self.getSlaves(user)
                l = len(slaves)
                if l <= 0:
                    continue
                self.log.debug(f'Найдено {l} рабов для кражи у vk.com/id{user}')
                for slave in slaves:
                    self.client.buy(slave['id'])
                    self.log.debug(f'Украден раб vk.com/id{slave["id"]}')
                    profit = 1
                    if self.job:
                        time.sleep(random.random() + 0.5)
                        job = self.jobs.get()
                        set = self.client.job(slave["id"], job)
                        try:
                            profit = set["profit_per_min"];
                        except:
                            profit = 1
                        self.log.debug(f'Установлена работа `{job}` vk.com/id{slave["id"]}')
                    if profit >= self.min_profit and self.fetter:
                        time.sleep(random.random() + 0.5)
                        self.client.fetter(slave["id"])
                        self.log.debug(f'Куплены оковы на vk.com/id{slave["id"]}')
                    time.sleep(self.delay + random.random())
            time.sleep(30000)


class AbuseMode:

    def __init__(self, config: JsonReader, log: Logger, client: Client, job: JobGen):
        if config.read("ENABLED"):
            self.jobs = job
            self.log = log
            self.client = client
            self.job = config.read("AUTO_JOB")
            self.fetter = config.read("AUTO_FETTER")
            self.min_profit = config.read("MIN_PROFIT")
            self.min_balance = config.read("MIN_BALANCE")
            self.max_sale = config.read("MAX_SALE")
            self.delay = config.read("DELAY")
            print("Включен режим абуза")
            Thread(target=self.start).start()

    def getSlaves(self):
        try:
            if self.client.get_user(self.log.id)['balance'] < self.min_balance:
                return []
        except Exception as e:
            return []

        try:
            slaves = self.client.get_slaves(self.log.id)['slaves']
        except Exception as e:
            slaves = []

        to_steal = []
        for slave in slaves:
            if slave['sale_price'] < self.max_sale:
                to_steal.append(slave)
        return to_steal

    def start(self):
        while True:
            slaves = self.getSlaves()
            l = len(slaves)
            if l <= 0:
                continue
            self.log.debug(f'Найдено {l} рабов для абуза')
            for slave in slaves:
                self.client.sale(slave['id'])
                time.sleep(random.random() + 0.5)
                self.client.buy(slave['id'])
                self.log.debug(f'Заабужен раб vk.com/id{slave["id"]}')
                profit = 1
                if self.job:
                    time.sleep(random.random() + 0.5)
                    job = self.jobs.get()
                    set = self.client.job(slave["id"], job)
                    try:
                        profit = set["profit_per_min"];
                    except:
                        profit = 1
                    self.log.debug(f'Установлена работа `{job}` vk.com/id{slave["id"]}')
                if profit >= self.min_profit and self.fetter:
                    time.sleep(random.random() + 0.5)
                    self.client.fetter(slave["id"])
                    self.log.debug(f'Куплены оковы на vk.com/id{slave["id"]}')
                time.sleep(self.delay + random.random())
        time.sleep(5000)
