"""Build script, cue sheet, brand manifest, and review documents from story.json."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parent
s=json.loads((R/'data/story.json').read_text())
words=sum(len(re.findall(r"\b[\w]+(?:[’'-][\w]+)*\b",x['vo'])) for x in s['shots'])
md=f'''# JERP — The Unsupported Leap

Сценарно-режиссёрская разработка v1.0 · 25 октября 2026 · **49 секунд · английский язык**.
Это пакет preproduction, не новый готовый ролик. Предыдущий 30-секундный MP4 — ранний визуальный эскиз и не является основой новой драматургии.

## Что должен понять зритель

AI может уверенно смешать факт, ложное обещание и мнение. JERP помогает проверить утверждения по источникам и вернуть агенту компактные факты. Пользователь получает более проверяемую основу для решения и меньше лишнего текста в AI-контексте.

Аудитория: люди, которые с помощью AI исследуют сервисы, сравнивают поставщиков, готовят рекомендации. Ролик для первого знакомства на главной, без необходимости знать термин MCP.

Одна цель: после просмотра зритель понимает, зачем поставить JERP перед ответом своего AI, и нажимает **Try Free**.

## Концепция: утверждение вышло за край основания

На странице вымышленного поставщика написано: «есть бесплатный пробный период; после него нужна платная подписка». Черновик AI отвечает: **The best choice. Free forever.**

Предложение становится объёмной стеклянной лентой. Слова *Free forever* физически выходят за край исходного документа: у уверенного утверждения нет опоры. JERP разделяет черновик на утверждения, сопоставляет их с источником и возвращает небольшой пакет фактов. Финальный ответ больше не обещает «лучший навсегда бесплатный сервис» — он показывает реальные условия и источник.

Это один понятный случай, а не каталог возможностей. Изменение состояния видно: уверенная рекомендация → проверка → конкретные условия с источником.

## Проблемы и решения

| Проблема пользователя | Решение JERP | Как зритель это увидит |
|---|---|---|
| Уверенный ответ может добавить неподтверждённые условия | verdict сопоставляет утверждение с источником | Free forever упирается в прямое противоречие: после trial нужна подписка |
| Реклама и мнение звучат как факт | verdict различает true / false / not_fact | Best choice получает Opinion, а не False |
| Агент получает внешний, недоверенный контент | guard проверяет входящий контент | Проверка до использования страницы; без изображения абсолютной защиты |
| Модель читает лишний контекст | speaker возвращает факты с источниками в заданном размере | В контекст переходит маленькая карточка фактов, страница остаётся снаружи |
| Непонятно, откуда взялся вывод | Источник сопровождает факт | В финале source-tab раскрывает ту же цитату, которую зритель уже видел |

## Финальный английский текст диктора

**{words} слова**. Общая длительность 49 s. При чтении 135–145 слов/мин речь занимает около 39–41 s: оставшееся время нужно на паузы, чтение и финальный CTA. Это расчёт по тексту, не измерение записанного голоса.

'''
md+='\n\n'.join('> '+x['vo'] for x in s['shots'])
md+='''

## Экранный пример — точный текст

Метка **Illustrative example · fictional vendor** сохраняется на всех демонстрационных кадрах 01–08. URL **northstar.example/product**: зарезервированный пример, не реальная компания.

**Запрос:** Choose a time tracker for our team.

**Страница:**

> Time tracking for your team  
> Free trial available.  
> A paid subscription is required after the trial.

**Черновик AI:** The best choice. Free forever.

**Разбор:**

| Утверждение | Метка | Почему |
|---|---|---|
| Free trial | true | Supported by source: Free trial available |
| Free forever | false | Contradicted by source: A paid subscription is required after the trial |
| Best choice | not_fact | Opinion; это оценка, а не проверяемое условие |

**Итоговый ответ:**

> The page offers a free trial. A paid subscription is required afterward.  
> Source: northstar.example/product

Не показывать в постановочном примере настоящий API-лог, реальные receipt ID, время ответа, confidence-процент или численную экономию токенов. Это объяснение механики по документации, не запись аутентифицированного вызова MCP.

## Покадровая режиссура

'''
for x in s['shots']:
 md+=f'''### {x['id']} · {x['start']:02d}–{x['end']:02d} s · {x['title']}

**Задача:** {x['problem']}

**В кадре:** {x['action_ru']}

**Экранный текст:** {' / '.join(x['screen'])}

**VO:** “{x['vo']}”

**Камера:** {x['camera_ru']}

**Переход:** {x['transition_ru']}

**Звук:** {x['sound_ru']}

**Читаемый hold:** не меньше {x['read_hold_seconds']} s. Для кадров с длинными условиями камера останавливается прежде, чем зритель начинает читать.

'''
md+='''## Tone of voice

**Спокойная уверенность, которую можно проверить.** Бренд показывает основание, объясняет простыми словами и не стыдит пользователя или его AI.

- Короткие конкретные предложения: “The page says…”, “Supported by source”, “You can check the source.”
- Сначала задача и результат, затем названия инструментов. guard / verdict / speaker — малые функциональные лейблы, не экзамен на знание MCP.
- Тон: взрослый, точный, немного сухой; эмоциональный эффект рождается из наглядного открытия.
- Пользователь сохраняет право решения. JERP даёт основания, а не назначает победителя или гарантирует правильную покупку.
- Не использовать: revolutionary, ultimate, magic, never hallucinates, 100% safe, instantly knows the truth, guaranteed savings.
- Называть отсутствие оснований прямо. Мнение не считать ложью; противоречие не смешивать с отсутствием информации.

| Слабая формулировка | Формулировка ролика |
|---|---|
| JERP makes your AI always right | Check the claims against sources |
| All the internet, reduced to truth | Compact facts, with sources, inside your size limit |
| Eliminate prompt injection | Screen incoming content |
| The smartest recommendation | An answer you can inspect |
| Save 90% on every answer | Less for your AI to read |

## Что сознательно не входит

Длинный onboarding, тарифы, логотипы чужих AI-продуктов, вся legacy-номенклатура API, обещание полного устранения галлюцинаций, количественный benchmark. Числа отвлекли бы от объяснения механики и потребовали бы отдельной проверяемой демонстрации.

Не повторяем суд из исходного видео: роль «окончательного судьи истины» слишком сильна. Стеклянная сфера сохраняется как бренд-деталь, а не как магический очиститель всего интернета.

## Точность и статус

Функции сверены с публичными материалами getjerp.com и разделом Three tools в контракте. Живой JERP MCP в этой сессии не подключён; вызовы инструмента не выполнялись. Некоторые тексты главной шире технического контракта: например, confidence может отсутствовать без калибровки. В сценарии выбрана более точная трактовка.

Связка guard → verdict → speaker — режиссёрская схема именно этого примера, а не утверждение, что любой запрос всегда проходит три обязательных сетевых вызова.

Следующий этап производства: озвученный черновой animatic с этим таймингом, затем финальная анимация и рендер. Точный темп и произношение JERP нужно проверить на записи голоса до дорогого рендера.
'''
(R/'SCENARIO-RU.md').write_text(md)
(R/'voiceover-en.txt').write_text('\n\n'.join(x['vo'] for x in s['shots'])+'\n')
# Cues are editorial timing, not a fabricated recorded speech alignment.
def tc(sec): return f'{sec//3600:02d}:{sec//60%60:02d}:{sec%60:02d},000'
srt=[]
for i,x in enumerate(s['shots'],1):
 t=x['vo'];parts=t.split();mid=len(parts)//2
 if len(t)>70:t=' '.join(parts[:mid])+'\n'+' '.join(parts[mid:])
 srt.append(f'{i}\n{tc(x["start"])} --> {tc(x["end"])}\n{t}\n')
(R/'voiceover-draft.srt').write_text('\n'.join(srt))
# Compact primary-source evidence for review.
evidence=[
 {'id':'E01','url':'https://getjerp.com/','section':'Three tools. The server does the rest.','quote':'Your agent sees three tools. The checks behind them run on our side, so your model never reads them.','use':'Product framing; not a universal cost guarantee.'},
 {'id':'E02','url':'https://getjerp.com/','section':'guard','quote':'Screens text, links, and actions before your AI reads or does them.','use':'Shot04 screening only.'},
 {'id':'E03','url':'https://getjerp.com/','section':'verdict','quote':'Says whether an answer is true, false, or not a fact, with a confidence score, and what to check next.','use':'Shots05–06, qualified by E06 for confidence.'},
 {'id':'E04','url':'https://getjerp.com/','section':'speaker','quote':'Gives your AI sourced facts within a size limit, so it does not guess.','use':'Shot07; film describes sourced input, not guaranteed downstream behavior.'},
 {'id':'E05','url':'https://getjerp.com/llms-full.txt','section':'Three tools / response envelope','quote':'"true" means supported by a returned source, not true in the world; "not_fact" means do not say this phrase.','use':'Show Supported by source, not universal truth.'},
 {'id':'E06','url':'https://getjerp.com/llms-full.txt','section':'response envelope','quote':'confidence (0 to 1; omitted when no calibration exists)','use':'Do not invent a score or mandatory confidence gauge.'},
 {'id':'E07','url':'https://getjerp.com/llms-full.txt','section':'Inputs by tool / speaker','quote':'sizeCap (tokens; default 1,000, max 4,000)','use':'Size limit is supported; no exact number needed in film.'},
 {'id':'E08','url':'https://getjerp.com/','section':'What JERP does not do','quote':'Complete protection from prompt injection. No detector can promise that.','use':'No unbreakable shield or all-threats-cleared graphic.'},
 {'id':'E09','url':'https://getjerp.com/','section':'Where does JERP get its information?','quote':'The free tier works on sites you name or sites already in the JERP open index; it does not crawl arbitrary URLs on demand.','use':'Single concrete input; no whole-internet scan.'},
 {'id':'E10','url':'https://getjerp.com/','section':'CTA','quote':'Stop guessing. Start checking.','use':'Use original CTA with Try Free.'}
]
for e in evidence:
 file='llms-full.txt' if 'llms-full.txt' in e['url'] else 'home-text.txt'
 raw=(R/'research'/file).read_text()
 # Some visible text is hydrated/lazy. Fall back to initial HTML after stripping tags.
 if e['quote'] not in raw and file=='home-text.txt':
  raw=re.sub('<[^>]+>',' ',(R/'research/home.html').read_text())
 normalized=lambda v:' '.join(v.replace('`','').split()).replace('“','"').replace('”','"')
 e['matched_exact_or_normalized']=normalized(e['quote']) in normalized(raw)
(R/'research/evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
manifest=[]
for p in sorted((R/'brand').glob('*')):
 if p.is_file() and p.name!='manifest.json': manifest.append({'file':'brand/'+p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
(R/'brand/manifest.json').write_text(json.dumps({'retrieved':'2026-10-25','note':'Original site fonts/favicon and extracted CSS tokens; lookdev and storyboards are original production adaptations. CSS wordmark is recreated from the actual site rules, not a supplied separate SVG logo.','assets':manifest},ensure_ascii=False,indent=2))
print('Built scenario, VO cues, evidence and manifest;',words,'VO words')
