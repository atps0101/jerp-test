# Первичные источники · 25 октября 2026

| Материал | URL | Сохранённый файл / использование |
|---|---|---|
| Главная | https://getjerp.com/ | home.html, home-text.txt; сценарий, тон, CTA |
| Технический контракт | https://getjerp.com/llms-full.txt | llms-full.txt; раздел Three tools и response envelope |
| Markdown docs | https://getjerp.com/docs.md | docs.md; на дату исследования ответ совпадает с llms-full.txt |
| CSS | https://getjerp.com/assets/index-BwRGWNx0.css | site.css; токены, стекло, wordmark, шрифты |
| JS | https://getjerp.com/assets/index-C3Y2cEke.js | site.js; определение используемого video asset |
| Исходное видео | https://getjerp.com/jerp-court-desktop.mp4 | Просмотрены выборочные кадры 5 и 18 s, длительность 37.3 s; reference-18s.jpg. Полный исходный ролик в пакет не скопирован |
| Иконка | https://getjerp.com/favicon.svg?v=3 | ../brand/favicon.svg |
| Bitcount | https://getjerp.com/fonts/bitcount-latin.woff2 | ../brand/bitcount-latin.woff2 |
| Barlow 400 | https://getjerp.com/fonts/barlow-400.woff2 | ../brand/barlow-400.woff2 |
| Barlow 600 | https://getjerp.com/fonts/barlow-600.woff2 | ../brand/barlow-600.woff2 |
| Barlow 900 | https://getjerp.com/fonts/barlow-900.woff2 | ../brand/barlow-900.woff2 |

Оригинальные материалы JERP сохранены для данного производственного задания; они не объявляются нашей новой интеллектуальной собственностью. Новые режиссёрские фигуры и styleframes — адаптация, а не скриншоты реального интерфейса продукта.

## Точность исследования

Доступ получен к публичному сайту и документам; живой OAuth/MCP-клиент недоступен. Все примеры результатов постановочные.

В llms-full.txt соседствуют современный трёхинструментный контракт и legacy API. Сценарий опирается на современную поверхность guard / verdict / speaker. Например, confidence может отсутствовать без калибровки, хотя главная формулирует это шире. Гарантированную точность или отсутствие галлюцинаций не переносим из рекламного title в доказуемое обещание ролика.

В браузере сайт показан через TLS-проверенные curl-ответы, подставленные Playwright route: системный Chromium сам не доверял сертификату egress-proxy. Проверка TLS не отключалась. Внешняя аналитика и POST-запросы для исследования не выполнялись. Сохранённый browser-inspection отражает видимый hydrated desktop layout; для lazy-разделов использовался исходный HTML и публичный контракт.
