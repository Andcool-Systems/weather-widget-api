# Weather Widget

![GitHub Workflow Status (API)](https://img.shields.io/github/actions/workflow/status/Andcool-Systems/weather-widget-api/deploy.yml?style=for-the-badge&logo=yandexcloud&logoColor=white&label=API%20Deploy&labelColor=1A222E&color=242B36&cacheSeconds=10)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Andcool-Systems/weather-widget-api/update-website.yml?style=for-the-badge&logo=yandexcloud&logoColor=white&label=Website%20Deploy&labelColor=1A222E&color=242B36&cacheSeconds=10)

Виджет погоды, например, для вашего профиля GitHub.

## Параметры API

> Можете воспользоваться генератором: https://weather.wavycat.ru или https://weather.andcool.ru

API расположен на GET https://weather.wavycat.ru/api

| Название | Описание                                     | По умолчанию | Возможные значения  | Обязательный |
|----------|----------------------------------------------|--------------|---------------------|--------------|
| place    | Имя населённого пункта на любом языке        | -            | Строка              | Да           |
| language | Язык который будет использоваться в картинке | ru           | Зависит от темы     | Нет          |
| theme    | Используемая тема виджета                    | default      | default, pixel-city | Нет          |

### Параметры тем

Некоторые темы могут иметь свои обязательные или необязательные параметры.

| Название | В теме     | Описание                                                    | По умолчанию | Возможные значения              | Обязательный |
|----------|------------|-------------------------------------------------------------|--------------|---------------------------------|--------------|
| timezone | default    | Название GMT времени (от -14 до +12). Например: gmt4, gmt-1 | gmt0         | gmt(число от -14 до 12)         | Нет          |
| size     | pixel-city | Размер итогового изображения                                | small        | small (512x358), big (1024x716) | Нет          |

## Ошибки API

| HTTP код | Возвращаемый code | Описание                                                 | Решение ошибки                                                                                                           |
|----------|-------------------|----------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| 404      | place_not_found   | Переданный населённый пункт не найден.                   | Передать корректное место.                                                                                               |
| 400      | lang_not_found    | Переданный язык не найден.                               | Передать язык, который поддерживает [тема](https://github.com/Andcool-Systems/weather-widget-api#темы).                  |
| 400      | tz_not_found      | Переданный Timezone не найден (только в теме default).   | Передать корректный [код временной зоны](https://github.com/Andcool-Systems/weather-widget-api#параметры-тем).           |
| 400      | theme_not_found   | Переданная тема не найдена.                              | Указать [существующую тему](https://github.com/Andcool-Systems/weather-widget-api#темы).                                 |
| 500      | internal_error    | Внутренняя ошибка (может возникнуть по разным причинам). | Решения нету. Можете создать [Issue](https://github.com/Andcool-Systems/weather-widget-api/issues) с описанием проблемы. |

## Темы

| Название   | Поддерживаемые языки              | Параметры |
|------------|-----------------------------------|-----------|
| default    | Русский (`ru`), Английский (`en`) | timezone  |
| pixel-city | Русский (`ru`), Английский (`en`) | Нет       |
