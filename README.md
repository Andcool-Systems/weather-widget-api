# Weather Widget
![GitHub Workflow Status (API)](https://img.shields.io/github/actions/workflow/status/Andcool-Systems/weather-widget-api/deploy.yml?style=for-the-badge&logo=yandexcloud&logoColor=white&label=API%20Deploy&labelColor=1A222E&color=242B36&cacheSeconds=0)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Andcool-Systems/weather-widget-api/update-website.yml?style=for-the-badge&logo=yandexcloud&logoColor=white&label=Website%20Deploy&labelColor=1A222E&color=242B36&cacheSeconds=0)
![GitHub repo size](https://img.shields.io/github/repo-size/Andcool-Systems/weather-widget-api?style=for-the-badge&logo=github&logoColor=white&labelColor=1A222E&color=242B36&cacheSeconds=0)

Виджет погоды в виде изображения, который вы можете установить куда угодно, например, в readme своего профиля GitHub.

## Архитектура
Проект имеет Serverless архитектуру типа AWS Lambda.
Текущая реализация написана для Cloud Functions в Yandex.Cloud.
Директория `web` никак не связана с остальным кодом, она загружается в объектное хранилище и связывается через API Gateway.
> По какой-то причине шлюз облачных функций YC не умеет корректно обрабатывать изображения, поэтому генерация работает только через API Gateway. Возможно, это исправимая проблема.

## Подробнее об API
API расположен на **GET** https://weather.wavycat.ru/api и https://weather.andcool.ru/api (можете использовать любой из них)

> Для упрощения создания виджета, можете использовать конструктор на [сайте](https://weather.wavycat.ru) (либо [тут](https://weather.andcool.ru))

### Параметры
| Название | Описание                                      | По умолчанию | Возможные значения  | Обязательный |
|----------|-----------------------------------------------|--------------|---------------------|--------------|
| place    | Название населённого пункта на любом языке    | -            | Строка              | Да           |
| language | Язык, который будет использоваться в картинке | ru           | Зависит от темы     | Нет          |
| theme    | Используемая тема виджета                     | default      | default, pixel-city | Нет          |

Некоторые темы могут иметь свои обязательные или необязательные параметры.
Подробнее о них можно узнать в разделе [Темы](https://github.com/Andcool-Systems/weather-widget-api#темы).

### Ограничение запросов
По умолчанию, API шлюз weather.wavycat.ru и weather.andcool.ru ограничивает все запросы до указанных ниже значений.

| Путь    | Ограничение |
|---------|-------------|
| /api    | 10 rps      |
| /       | 100 rpm     |
| /static | 100 rpm     |

### Ошибки API

| HTTP код | Возвращаемый code | Описание                                                     | Решение ошибки                                                                                                           |
|----------|-------------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| 404      | place_not_found   | Переданный населённый пункт не найден.                       | Передать корректное место.                                                                                               |
| 400      | lang_not_found    | Переданный язык не найден.                                   | Передать язык, который поддерживает [тема](https://github.com/Andcool-Systems/weather-widget-api#темы).                  |
| 400      | tz_not_found      | Переданный часовой пояс не найден (только в теме default).   | Передать корректный [код временной зоны](https://github.com/Andcool-Systems/weather-widget-api#параметры-тем).           |
| 400      | theme_not_found   | Переданная тема не найдена.                                  | Указать [существующую тему](https://github.com/Andcool-Systems/weather-widget-api#темы).                                 |
| 500      | internal_error    | Внутренняя ошибка (может возникнуть по разным причинам).     | Решения нету. Можете создать [Issue](https://github.com/Andcool-Systems/weather-widget-api/issues) с описанием проблемы. |

> Внутренние ошибки бывают двух видов: на уровне облачной функции, обрабатываемые в try-except и на уровне шлюза.
> Ошибки на уровне шлюза обычно являются более критичными, однако ошибки на уровне функции проще отследить, поэтому в Issue прикладывайте UUID код ошибки, если он присутствует.

## Темы
### default
**Тема по умолчанию.**
Содержит наибольшее количество информации о погоде. Подстроена под стандартную тёмную тему GitHub.
Автор: @Andcool-Systems

#### Поддерживаемые языки
* Русский - `ru`
* Английский - `en`.

#### Параметры
| Название | Описание     | Обязательный | По умолчанию  | Возможные значения      |
|----------|--------------|--------------|---------------|-------------------------|
| timezone | Часовой пояс | Нет          | `gmt0`        | gmt(число от -14 до 12) |

#### Пример темы
![default theme](https://weather.wavycat.ru/api?place=andcool&timezone=gmt3)


### pixel-city
Города в стиле pixel art. Нарисовано нейросетью SDXL 1.0.
Автор: @wavy-cat

#### Поддерживаемые языки
* Русский - `ru`
* Английский - `en`
* Итальянский - `it`
* Испанский - `es` или `sp`
* Украинский - `ua` или `uk`
* Немецкий - `de`
* Португальский - `pt`
* Румынский - `ro`
* Польский - `pl`
* Финский - `fi`
* Голландский - `nl`
* Французский - `fr`
* Болгарский - `bg`
* Шведский - `sv` или `se`
* Китайский Традиционный - `zh_tw`
* Китайский Упрощённый - `zh` или `zh_cn`
* Турецкий - `tr`
* Хорватский - `hr`
* Каталанский - `ca`

#### Параметры
| Название | Описание                     | Обязательный | По умолчанию | Возможные значения                  |
|----------|------------------------------|--------------|--------------|-------------------------------------|
| size     | Размер итогового изображения | Нет          | `small`      | `small` (512x358), `big` (1024x716) |

#### Пример темы
![default theme](https://weather.wavycat.ru/api?place=nightcity&theme=pixel-city&size=small)

