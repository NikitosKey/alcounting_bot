# Телеграмм бот Алкоучёт

in progress

...

## Что тут происходит на данный момент

### Что сделано

1) Найден хостинг: <https://www.pythonanywhere.com>
2) Выбраны бибилиотеки и язык для бота
3) Намечен примерный план работы

### Что нужно сделать

Пока не очень понимаю как на питоне это делается, дзен джавы мне поближе, но не об этом.

Надо сделать что-то типо класса пользователь и наследовать от него классы бармен, покупатель и адмимн.

Уровни доступа задаются через список логинов, который будет храниться на хосте

Проверка выполняется при запуске бота (Есть вопрос, что делать, если уровень доступа изменился, пока что нужно перезапустить бота, тогда пользователь получит обновлённые права)

#### Уровни доступа

1. Администратор.

Имеет полный доступ ко всем возможностям бота.

- выбор роли заказчика или бармена (скоро)
- различные логи (как получится)
- какая-либо статистка (не скоро)
- вносить изменения в списки прав (не скоро)
- фичи, которые я ещё не придумал (не скоро)

2. Бармен.

- может посмотреть очередь заказов (скоро)
- отмечать выполненные заказы (скоро)
- принимать заказы, заказ получит соотвествующий статус (не скоро)
- заказать что-либо самостоятельно (либо переключиться на меню заказчика) (что-то из этого скоро)

3. Покупатель (заказчик).

- Может посмотерть барную карту (скоро)
- Посмотреть информацию о позициях (не скоро)
- Выбрать из перечня, подтвердить и заказать (скоро)
- Посмотреть свои заказы (не скоро) и их статус (ещё менее скоро)
- История заказов (ещё менее скоро)
- Сумма заказов, календарь вечеринок... (просто идеи, которые скорее всего не буду делать)

Пока что не совсем понятно что и как хранить, но скорее всего лучше отталкиваться от очереди бармена, барной карты и списка прав, чтобы не хранить лишнее.

#### Очередь бармена

Что-то по типу таблицы, или пока хз в каком виде это должно быть, но она должна представлять собой список заказов, где каждый заказ содержит:

- информацию о заказчике
- информацию о бармене
- информацию о выбанном пункте из меню, либо просто номер из барной карты
- статус заказа
- список со временем изменений статуса заказа.

#### Барная карта

(Нумерованый, или нет) список коктейлей, их стоимость и может ещё что-то.

...

### Introducing

...

### Requriments

- python-telegram-bot v21.0.1 installed from pip
- python 3.8 - 3.12
- telegram bot token in src/bot_token.py

``` src/bot_token.py
token = "YOUR TOKEN"
```

### Instructions

...
