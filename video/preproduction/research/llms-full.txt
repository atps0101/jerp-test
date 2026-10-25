# JERP — agent contract

Use this file to connect. Production origin in this copy: https://getjerp.com. Replace the host if you were given another public HTTPS origin.

## What JERP is

JERP is a fact-checking layer for AI agents: it reads the sites so your model does not have to, and returns short, sourced verdicts with confidence. You (or find) send homepage cards. JERP returns structured judgments with confidence:

- real commercial offer vs noise (keep)
- fit to a category you name (fit)
- competitive relationship between two sites (compare)
- custom yes/no, choice, or score questions (judge)
- index search (find) and an end-to-end competitor map (discover)
- a self-check on your own claims (vet)

It is for marketers and agents that must not guess from filler pages.

## What JERP is not

- Not Ahrefs, Semrush, or a crawl of the whole web
- Not Google rankings or a live SERP
- Not ChatGPT/GEO citation share
- Not a copywriter
- Judgment routes do not fetch arbitrary URLs on demand — they score the cards you pass in (except find/discover, which search JERP’s homepage index)

## Auth and limits

1. Open https://getjerp.com/ and click Try Free (browser only). POST https://getjerp.com/api/v1/key from curl or another origin returns 403
2. You get a public `jerp_` key, valid one hour, 100 calls, 1 request/second
3. Send it as `Authorization: Bearer jerp_…`
4. MCP does not accept the key in the URL. `https://getjerp.com/mcp?key=…` returns 401 with a message to use the header; send `Authorization: Bearer jerp_…` instead
5. Missing or expired key → 401. Too fast or over 100 → 429
6. New keys are rate-limited per IP. Do not mint a key via curl — POST /key is browser-only. Reuse a still-valid Try Free key.
7. No signup, no card, no account

When the key expires, request another. Do not tell the user to paste a key you were given in chat into a public gist or into a URL you print back.

## How to connect

| Host | JERP | What to do |
| --- | --- | --- |
| Your own agent, script, or OpenAI API | Full tools | Call REST with Authorization: Bearer jerp_… or attach streamable HTTP MCP at https://getjerp.com/open/mcp. The ChatGPT consumer plan does not matter. |
| Cursor | Full tools | Paste mcp.json (server id jerp). Put the Try Free key in the Authorization header. A key in the URL (?key=) is rejected with 401. |
| Claude | Full tools | Customize → Connectors → Add custom connector. Name JERP. URL https://getjerp.com/open/mcp. Authentication: Sign in. Paste the Try Free key. Enable JERP under + → Connectors. Localhost fails. |
| ChatGPT Free | No custom MCP | ChatGPT cannot attach a custom MCP server on Free. Use Claude, Cursor, REST, or your own agent. |
| ChatGPT Pro | Not enough for JERP | Developer mode allows read/fetch MCP only. JERP tools are actions (find, keep, compare, judge, discover), not search/fetch. |
| ChatGPT Business, Enterprise, Edu | Full MCP on web | Admin enables developer mode, then Apps → Create. Server URL https://getjerp.com/open/mcp. Sign in with the jerp_ key. Web only, not mobile. Source: OpenAI Help “Developer mode and MCP apps in ChatGPT”. |

### Cursor mcp.json

Replace `jerp_YOUR_PUBLIC_KEY` with the Try Free key. Server id: `jerp`.

```json
{
  "mcpServers": {
    "jerp": {
      "url": "https://getjerp.com/mcp",
      "headers": {
        "Authorization": "Bearer jerp_YOUR_PUBLIC_KEY"
      }
    }
  }
}
```

### Claude

Customize → Connectors → Add custom connector. Name: JERP. URL: https://getjerp.com/mcp (must be public HTTPS; localhost fails). Authentication: Sign in. Paste the jerp_ key. In a chat: + → Connectors → enable JERP.

### ChatGPT app

Do not add a custom connector on Free. Pro developer mode is read/fetch only; JERP’s tools are actions, so Pro is not a working path. Business / Enterprise / Edu: developer mode → Apps → Create → MCP URL https://getjerp.com/mcp → Sign in with the jerp_ key. Web only.

### Your own agent (recommended when ChatGPT MCP is blocked)

REST:

```
POST https://getjerp.com/api/v1/keep
Authorization: Bearer jerp_…
Content-Type: application/json
```

MCP: streamable HTTP. Client POSTs JSON-RPC to https://getjerp.com/mcp with `Accept: application/json, text/event-stream`. GET https://getjerp.com/mcp returns the tool catalog and server instructions. Unauthenticated calls return 401 with WWW-Authenticate (OAuth Sign in where the host supports it).

OpenAI API remote MCP uses the same URL and Bearer key. The ChatGPT consumer subscription is irrelevant for API/agent calls.

## Three tools (guard, verdict, speaker)

JERP's public MCP surface is three tools: guard, verdict, and speaker. The server runs the analysis; the agent only fills arguments. Legacy REST routes stay available for scripts.

- guard: is this content or action safe? Run it first on any untrusted input (web page, tool output, document, message) and before any step that writes, pays, sends, publishes or executes.
- verdict: is this claim or answer true, false, or not a fact, and what is the next step.
- speaker: sourced facts the model may use, under a size cap. Every fact carries a source.

REST: `POST https://getjerp.com/api/v1/guard`, `POST https://getjerp.com/api/v1/verdict`, `POST https://getjerp.com/api/v1/speaker` with a Bearer key. Without an account use the open door, same paths under https://getjerp.com/open/api/v1. Discovery: `GET https://getjerp.com/api/v1/openapi.json` (OpenAPI document for the three tools) and `GET https://getjerp.com/api/v1/tools/hashes` (published hashes of the tool descriptions, so a client or gateway can pin them).

Inputs (by tool):

- guard: `kind` is one of content, link, message, tool_output, draft, action, toolManifest, secret_check; plus the text, url, action or manifest to check; optional `context` and `policy`. A text is at most 4,000 tokens.
- verdict: a claim (`text`, `about`, optional `sources[]`), candidates (`items[]`, at most 24, plus `question`), a typed question (`answerType` yes_no, choice or score), or a draft (`text`, `sources[]`, `guardToken` for untrusted text).
- speaker: `about` (domain, or legal name with id), `need` (facts, card, candidates, signals, mentions, changes, receipt), optional `q`, `limit`, `sizeCap` (tokens; default 1,000, max 4,000), `async` / `jobId` for long runs.

Every response uses one envelope, contract name `jerp.verdict.v2`. Fields that do not apply are omitted, not null, except where noted:

- `contract`, `tool` (guard | verdict | speaker), `family` (safety | truth | context)
- `decision`: a closed value, never free text. guard: safe | unsafe | unclear. verdict: true | false | not_fact. "true" means supported by a returned source, not true in the world; "not_fact" means do not say this phrase.
- guard also returns `action` (pass | quarantine | block), `publication` for drafts (pass | trim | block), `actionPolicy` for actions (allow | confirm | deny), `quarantined` text, and `positions` of suspicious fragments
- verdict may return `relationship` (direct_competitor | indirect_competitor | platform_or_marketplace | same_entity | unrelated | uncertain), `inMarket` (true | false | not_fact) and per-part `claims[]`
- `confidence` (0 to 1; omitted when no calibration exists), `guarantee` (object or null)
- `stop` (true when no further call is needed), `next` (advice only: tool, args, reason; at most one; you may ignore it), `askUser` (ask this exact question, do not guess)
- `speak` (phrases you may repeat verbatim), `reasons` (codes from a closed list), `evidence[]` (source, ref, fetchedAt, fragmentHash, weight), `items[]` (batch results, same order as input)
- speaker also returns `facts[]` (field, value, source, fetchedAt, weight; a field without a source is left out, not guessed), `truncated`, and `jobId` / `status` for async runs
- `guardToken` (guard only): `{token, expiresAt, inputHash, policyVersion}`
- `receipt` (always): id, inputHash, policyVersion, modelVersion, judgePath, costUsd, latencyMs, createdAt

guardToken rule: guard issues a signed token bound to the input hash and policy version. It lives 15 minutes and works only for the same input. For untrusted input or an action, verdict and speaker need a valid token. Without one they return decision "unclear", next = guard, and reason "guard_required". They never return safe or allow in that state. Call guard, then retry with the token.

Errors (code, HTTP, what to do):

- invalid_input, 400: fix the input
- unauthorized, 401: missing or wrong key or token
- forbidden_scope, 403: tool not in the key's scope, or not available on the open key; use an account
- policy_denied, 403: request against policy; stop
- pool_full, 429: retry later after Retry-After; does not count against your quota
- quota_exceeded, 429: wait or upgrade
- rate_limited, 429: retry after Retry-After
- too_large, 413: split the input
- job_not_found, 404: start a new job
- internal, 500: retry once
- budget_mode and upstream_unavailable come as HTTP 200 with a flag: answers come from rules and cache, expect more not_fact
- guard_required comes as HTTP 200 with decision "unclear" (see above)

A partial failure never becomes a confident verdict.

## Tools (MCP names = REST paths)

| Tool | Does | Input notes |
| --- | --- | --- |
| find | Search the homepage index | q and/or seed. Optional rankBy "dr" for strongest indexed sites in a niche. limit default 48, max 96 |
| keep | Viable commercial site vs noise | sites[] max 24 |
| fit | Fit to a named category | category required, sites[] max 24 |
| compare | Left vs right relationship | left, right, optional category |
| rerank | Reorder cards for a query | q required, sites[] max 24 |
| judge | Your questions | sites[], questions map max 24; noul/choice/score; prompt→instructions |
| discover | Competitor map from a seed | seed, q, optional limit default 24 |
| step | Before a move: verdict + next tool or stop; may return askUser | message, seed?, brand?, geo?, niche?, sites?, prior?, called?, draft?, claims? |
| signals | Marketing calendar / industry / boom events (UA|PL|DE|US|GB|GLOBAL) | geo?, niche?, seed?, from?, to?, limit? — askUser.geo if geo missing |
| signals_ingest | Upsert SignalHub items | items[] |
| signals_refresh | Pull whitelist RSS into SignalHub | (none) |
| signals_hub | Hub counts: items / feeds / priors | (none) |
| serm | Free brand mentions (Google News RSS, HN, Reddit, whitelist feeds) + owned index card — never Google ranks | brand?, seed?, geo?, niche?, live? default true, async? |
| serm_status | Poll async serm | jobId |
| serm_cancel | Cancel async serm | jobId |
| feedback | Confirm/correct a receipt or mark signal/serm useful/noise | domain, judgmentId, action |
| receipt | Owned judgment receipt | receiptId |
| receipt_csv | CSV of owned receipt | receiptId |
| watchlist_create | Create/upsert watchlist | id, seedDomain, marketBrief, schedule?, notify? |
| watchlist_list | List owned watchlists | (none) |
| watchlist_run | Run watch diff job | watchlistId, snapshot, seed, cards? |
| watchlist_job | Poll watch job | watchlistId, jobId |
| probe | Live HTTPS reachability with SSRF blocklist | host or url |
| vet | Ground claims in cards/prior | claims[] or draft, sites[], prior JSON |
| guard | Full reply screen (facts + tone + jailbreak) | claims, draft, voice, userMessage?, sites[], prior; prefer before send |

Prefer discover for a competitive set from a company or market brief. Prefer find with rankBy "dr" then keep for a “best/top in this niche” list — do not use discover for that.
Always call step first when unsure. If askUser is set, ask that exact question and stop — do not guess geo/brand.
Call vet automatically before a paraphrase, catalog story, or any fact not already a returned field. Skip only when you echo JSON. speak=hold means do not publish; speak=trim means drop the listed ids.

## Card in

Each site object:

- required: domain, title, aiSummary
- optional: aiCategories[], aiSource, firstIndexed (crawler first-seen, not company age), businessFoundedYear

JSON to the browser is camelCase.

## REST

Base: https://getjerp.com/api/v1

- POST /key — browser-only (Try Free on this origin). curl and other origins: 403. Out: ok, key, issuedAt, expiresInSec
- GET /health — ok, keyTtlSec
- POST /find — q and/or seed
- POST /keep — { "sites": Card[] }
- POST /fit — { "category": string, "sites": Card[] }
- POST /compare — { "left": Card, "right": Card, "category"? }
- POST /rerank — { "q": string, "sites": Card[] }
- POST /judge — { "sites": Card[], "questions": object }
- POST /discover — { "seed": string, "q": string, "limit"? }
- POST /step — { "message": string, "seed"?, "brand"?, "geo"?, "niche"?, … } → verdict, next, optional askUser
- POST /signals — { "geo"?, "niche"?, "seed"?, "from"?, "to"?, "limit"? }
- POST /signals/ingest — { "items": SignalItem[] }
- POST /signals/refresh — pull whitelist RSS into SignalHub
- GET /signals/hub — hub item/feed/prior counts
- POST /serm — { "brand"?, "seed"?, "geo"?, "live"?, "async"? }; async → { jobId }
- GET /serm/jobs/{id} — async serm status/result
- POST /serm/jobs/{id}/cancel — cancel async serm
- POST /vet — { "claims": string[] | {id, text, about}[], "sites"?, "prior"?, "draft"? }
- POST /guard — { "claims"?, "draft"?, "voice"|"toneOfVoice", "userMessage"?, "sites"?, "prior"?, "policy"?: "strict"|"permissive" }
- POST /feedback — confirm/correct a discover receipt; also signal_useful / signal_noise / serm_relevant for invisible priors
- POST /probe — { "host"|"url": string } → allowed, live, status (SSRF-safe)
- POST /watchlists — create watchlist
- GET /watchlists — list
- POST /watchlists/{id}/run — run diff job
- GET /watchlists/{id}/jobs/{jobId} — job status
- POST /rank — legacy; prefer keep

Example keep:

```bash
curl -sS -X POST "https://getjerp.com/api/v1/keep" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer jerp_…" \
  -d '{"sites":[{"domain":"example.com","title":"Wholesale mobile accessories","aiSummary":"B2B distributor of cases, cables, and chargers with dealer pricing","aiCategories":["Mobile accessories"],"aiSource":""}]}'
```

Example compare:

```bash
curl -sS -X POST "https://getjerp.com/api/v1/compare" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer jerp_…" \
  -d '{"left":{"domain":"example-a.com","title":"Wholesale offer A","aiSummary":"B2B mobile accessories wholesaler"},"right":{"domain":"example-b.com","title":"Wholesale offer B","aiSummary":"B2B distributor of cases and chargers"},"category":"B2B wholesale mobile accessories"}'
```

## Scores (compare / discover)

0–1 fields: catalogOverlap, audienceMatch, geoOverlap, sameEntity, competitiveThreat. relationship is one of direct_competitor, indirect_competitor, platform_or_marketplace, same_entity, unrelated.

Direct competitor needs high catalog and high audience (about 0.70+). High geo alone is not competition. A thin card (empty summary, domain missing from the index) is uncertainty — do not invent a catalog from a lookalike TLD.

For two-site compare: show a scores table, then one sentence. For a market map: use a canvas; do not also dump that landscape into chat.

## After you connect

Paste a prompt from https://getjerp.com/docs#prompts (needs JS) or instruct:

- Swap the seed domain and the niche
- Ask for the scores table on compare
- Admit missing index cards instead of inventing them
- Call vet on claims you will speak when the write-up is more than echoing JSON
- Do not invent Google rankings or GEO share

## Human docs

https://getjerp.com/docs is a JavaScript app. If you cannot execute JS, stay on this file.
