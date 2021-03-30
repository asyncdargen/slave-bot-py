from mods import *
from modules import *
from config import config

v = 1.0

def checkUpdates():
    while True:
        ver = requests.request("GET",
                               "https://raw.githubusercontent.com/asyncdargen/slave-bot-py/main/version.json").json()
        if ver['version'] > v:
            logger.log(f'''
Найдено обновление v{v} -> v{ver["version"]}
Описание: { ver['description']}
Скачать: https://github.com/asyncdargen/slave-bot-py/archive/refs/heads/main.zip
СТАРУЮ ВЕРСИЮ ИСПОЛЬЗОВАТЬ ОПАСНО!!!!
            ''')
        time.sleep(60000)

def callStart():
    while True:
        client.start()
        time.sleep(5000)

if __name__ == '__main__':
    config = JsonReader(config)
    job = JobGen(config.section("JOB"))
    req = Request(config.section("ACCOUNT"))
    client = Client(req)
    logger = Logger(config, req)
    client.setLogger(logger)
    logger.log(f'''
╔══════ Slave-Bot v{v} by dargen ═══════
║ VK: https://vk.com/asyncdargen
║ TG: https://t.me/asyncdargen
║ GitHub: https://github.com/asyncdargen/slave-bot-py
║ Пиши - если появился фикс или ошибки
╚══════ Slave-Bot v{v} by dargen ═══════
    ''')
    Thread(target=callStart).start()
    if config.section("ACCOUNT").read("UPDATE_CHECK"):
        Thread(target=checkUpdates).start()
    BuyMode(config.section("BUY_MODE"), logger, client, job)
    FetterMode(config.section("FETTER_MODE"), logger, client)
    JobMode(config.section("JOB_MODE"), logger, client, job)
    StealMode(config.section("STEAL_MODE"), logger, client, job)
    AbuseMode(config.section("ABUSE_MODE"), logger, client, job)