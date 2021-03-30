# slave-bot by dargen
 
Этот бот написан для мини-игры в [VK](https://vk.com) 'Рабы'

Если возникли ошибки или появился фикс пишите в любую сеть из [контактов](https://github.com/asyncdargen/slave-bot-py#контакты)

**Т.к он бесплатный я бы хотел от вас звёздочку GutHub**

**НЕ СОВЕТУЮ: Использовать несколько режимов одновременно, делать маленькие задержки и запускать несколько ботов**


## Функционал

 - Покупка рабов
 - Кража рабов
 - Прокачка рабов
 - Выдача работы безработным
 - Покупка цепей свободным
 - Полное логирование и возможность вывода в [Telegram](https://telegram.org)


## Преимущества

 - Гибкая настройка
 - Вывод всех статистики
 - Предупреждения о банах
 - Уведомления об обновления


## Конфигурация
 
 - `ACCOUNT` - основные данные:
   - `METHOD` - это вид так назваемой авторизации:
     - `AUTH` - авторизация через `authorization` ключ
    
        Получение:
       - Открываем [VK](https://vk.com)
       - Нажимаем `F12`
       - В появившейся панели выбираем вкладку `Network`
       - Ищем файлы с названием `start`, `user`, `jobSlave`, `buySlave` и т.д
       - Нашли - нажимаем по нему, иначе попробуйте купить раба, оковы или нажать `F5`
       - Появится еще одна панель, выбираем в ней вкладку `Headers`
       - Ищем поле `authorization`
       - Копируем его значение **(после `Bearer`)**
       - И вставляем в `VALUE` в `config.py`
     - `TOKEN` - авторизация через токен вашего аккаунта [VK](https://vk.com)
   
       Получение:
       - Переходим [сюда](https://vkhost.github.io)
       - Выбираем `VK Admin`
       - Копируем его значение **(после `Bearer`)**
       - И вставляем в `VALUE` в `config.py`
   - `VALUE` - это ключ авторизации или токен от вашего аккаунта, зависит от `METHOD`
   - `ID` - ID вашего аккаунта **ЧИСЛОВОЙ**
   - `UPDATE_CHECK` - будет проверять на обновления раз в минуту
   - `DEBUG` - вывод полной информации
- `TG_LOG` - данные [Telegram](https://telegram.org) логгирования
  - `ENABLED` - вкл/выкл (True/False)
  - `TOKEN` - токен вашего бота
  - `CHAT_ID` - ID чата для лога *(без @)*
  - `DEBUG` - вывод дебага если он включен в чат
- `JOB` - генерация работ
  - `METHOD` - тип генерации:
    - `RANDOM` - генерируется рандомный ангийский символ или цифра от 1 до 10
    - `LIST` - рандомная работа из списка `LIST`
    - `BOTH` - объединение `RANDOM` и `LIST`
  - `LIST` - список работ
- `JOB_MODE` - режим установки работы безработным
  - `ENABLED` - вкл/выкл (True/False)
  - `DELAY` - задержка между рабами
- `FETTER_MODE` - режим установки цепей свободным
  - `ENABLED` - вкл/выкл (True/False)
  - `MAX_PRICE` - макимальная цена оков
  - `MIN_PROFIT` - минимальный доход для установки оков
  - `DELAY` - задержка между рабами
- `BUY_MODE` - режим покупки рабов
  - `ENABLED` - вкл/выкл (True/False)
  - `AUTO_JOB` - выдача работы
  - `AUTO_FETTER` - покупка оков
  - `MAX_PRICE` - макимальная цена оков
  - `MIN_PROFIT` - минимальный доход для установки оков
  - `DELAY` - задержка между рабами
  - `DELAYED` - режим установки работы и покупки оков с задержкой:
    - `ENABLED` - вкл/выкл (True/False)
    - `DELAY` - задержка
- `ABUSE_MODE` - режим прокачки рабов
  - `ENABLED` - вкл/выкл (True/False)
  - `AUTO_JOB` - выдача работы
  - `AUTO_FETTER` - покупка оков
  - `MAX_SALE` - максимальная цена продажи раба
  - `MIN_BALANCE` - баланс при котором будет происходить прокачка
  - `MIN_PROFIT` - минимальный доход для установки оков
  - `DELAY` - задержка между рабами
- `STEAL_MODE` - режим прокачки рабов
  - `ENABLED` - вкл/выкл (True/False)
  - `TARGET` - ID аккаунтов для кражи **ЧИСЛОВОЙ**
  - `AUTO_JOB` - выдача работы
  - `AUTO_FETTER` - покупка оков
  - `MIN_PROFIT` - минимальный доход для установки оков
  - `MAX_PRICE` - максимальная цена раба
  - `MIN_PRICE` - минимальная цена раба
  - `DELAY` - задержка между рабами


## Контакты
 - [ВКонтакте](https://vk.com/asyncdargen)
 - [Telegram](https://t.me/asyncdargen)
 - Discord - **`dragen#0722`**


## Установка Windows
 - Устанавите [Python](https://www.python.org/downloads/windows). Во время установки ставим галочку `Add Python to PATH (Добавить Python в PATH)`
 - Скачиваем бота [тут](https://github.com/asyncdargen/slave-bot-py/archive/refs/heads/main.zip)
 - Распакуйте архив в любую папку
 - Найстройте `config.py` 
 - Откройте `cmd` *(Командную строку)*
 - И пропишите `python bot.py` *(Для некоторых версий `python3 bot.py`)*
 - Для остановки нажмите `CTRL +C` или закройте консоль


## Установка на Android через Termux
 - Устанавливаем Termux
 - Открываем и пишем:
   - `pkg install -y git`
   - `pkg install -y python`
   - `git clone` https://github.com/asyncdargen/slave-bot-py
   - `python bot.py` *(Для некоторых версий `python3 bot.py`)*
 - Для остановки нажмите `CTRL +C` или завершите сессию


## Переустанновка
 - **Termux:**
   - `rm -rf slave-bot-py`
   - `git clone` https://github.com/asyncdargen/slave-bot-py
 - **Windows:**
   - Удалите папку с ботом
   - Поавторите действия установки *(не включая установку Python ;3)*
