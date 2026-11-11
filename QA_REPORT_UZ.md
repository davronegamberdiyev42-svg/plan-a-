# IELTS Boost Plan A — Release 50.2 QA hisoboti

**Build:** 50.2.0-plan-a  
**Target repository:** `plan-a-`  
**Primary entry:** `index.html`  
**Build date:** 2026-11-11

## Manba va provenance

- Asosiy 84 kunlik app/runtime — saqlangan Stage 36 full deploy source. Eski app va uning progress storage key saqlangan.
- 84 MP3 va media assetlar — saqlangan Stage 33.1 resource deploy bundle.
- Stage 40 original deploy ZIP mavjud emas; faqat SHA-256 yozuvi saqlangan: `b906aa41a07acad20e8df373d18683b0dbc44b93ffee1afc8d4d887fad2651d1`.
- Stage 41–47 uchun ayrim audit, requirements, QA, roadmap va datasetlar saqlangan. Stage 48 coverage JSON va 46–50 roadmap ham saqlangan. Biroq barcha tarixiy patch binary/commitlar yo‘q.

**Shuning uchun build original Stage 40–50 source tree’ning byte-for-byte nusxasi emas.** 50.2 Final Studio saqlangan dalillar asosida qayta implementatsiya qilingan.

## Curriculum / kontent audit

| Tekshiruv | Natija |
|---|---:|
| 84 kunlik plan + core | PASS · 84/84 |
| Har kuni 4 skill | PASS · 336/336 |
| Reading questions | PASS · 840 |
| Listening questions | PASS · 420 |
| Speaking Part 1 / 2 / 3 | PASS · 252 / 84 / 252 |
| Writing Task 1 / Task 2 | PASS · 84/84 kun |
| Maqolalar / sentence patterns / source packs | PASS · 61 / 864 / 12 |
| Noyob vocabulary index | PASS · 19,000 |
| Daily core vocabulary | PASS · 672, 84 × 8; US/UK IPA va full glossary maydonlari bor |
| Stage 47 resource map | PASS · 336 |
| Listening companions | PASS · 84 |
| Task 1 fictional visual datasets | PASS · 84; 6 visual family × 14 |
| MP3 files | PASS · 84/84 |

## Stage 40–50 Final Studio qamrovi

- Overview va 84 kunlik day selector.
- Speaking transcript: segment bo‘yicha transcript, autosave, manual fallback, bounded reconnect; MediaRecorder orqali audio yozish va IndexedDB’ga lokal saqlash (browser/device qo‘llasa).
- Audio clip management: playback, individual download, delete; binary audio JSON backup tarkibiga kirmaydi.
- Scoring: Reading objective answer-key/evidence, Listening self-review, Writing Task 1/2 alohida, Speaking 4 mezon. Ichki practice scale, official band emas.
- Error & Lab: xato jurnali, repair evidence va transfer lab.
- Adaptive: deterministic, sample/evidence-gated tavsiyalar; generative AI emas.
- Stage 47: 336 skill-resource cards, optional official companions va 84 Task 1 dataset.
- Stage 48: 19K index, 672 daily core, local SRS; barcha 19K so‘z to‘liq tarjima qilingan emas.
- Stage 49: Privacy & Data, local data inventory, JSON backup/import, explicit Studio reset, keyboard focus handling, reduced motion.
- Stage 50: dynamic release checks, provenance disclosure, project-root deploy instructions.

## Avtomatik testlar

- Static/data/asset/JS/PWA/standalone audit: **47/47 PASS**; batafsil natija `docs/STATIC_QA_50_2.json` ichida.
- Barcha 84 MP3 FFmpeg decode sinovi: 84/84 PASS.
- Task 1 84 dataset parse/structure audit: 84/84 PASS.
- HTTP project subpath `/plan-a-/` smoke test: **16/16 HEAD 200 PASS**; `docs/HTTP_SMOKE_50_2.json` da qayd etilgan.
- - ZIP CRC va har bir fayl SHA-256 manifest: `SHA256SUMS.txt` va ZIP yonidagi `.sha256` orqali tekshiriladi.

## Ochiq cheklovlar — PASS deb ko‘rsatilmaydi

1. Browser Chromium click-flow automation build environment’da `ERR_BLOCKED_BY_ADMINISTRATOR` bilan bloklangan; haqiqiy browser UI E2E PASS deb belgilanmaydi.
2. Samsung Galaxy A14 yoki boshqa Android qurilmada microphone, MediaRecorder, Web Speech API va native PWA install real sinovdan o‘tmagan.
3. GitHub Pages hosted Service Worker update/offline qayta ochish real deployment’da tekshirilmagan.
4. Tashqi dictionary/translation provider APIs uchun live network/CORS/quota acceptance bajarilmagan.
5. Standalone HTML Final Studio CSS/JS/data’ni ichiga joylaydi, ammo MP3 tinglash uchun yonidagi `audio/` papkasi kerak.
6. Synthetic practice audio rasmiy IELTS/Cambridge audio emas. 0–10 index official IELTS band emas; 8.0/9.0 natija kafolatlanmaydi.

## Yakun

50.2 — mavjud manbalardan qayta yig‘ilgan, 84 kunlik asosiy app saqlangan va Stage 40–50 funksional qamrovi kuchaytirilgan Plan A integratsiya release. Original tarixiy Stage 40–50 kod bazasi aynan tiklangan deb da’vo qilinmaydi. Browser E2E va real qurilma acceptance ochiq qoladi.
