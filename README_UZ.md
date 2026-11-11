# IELTS Boost — Plan A · Release 50.2

## Paket nima?

Bu — GitHub Pages uchun tayyorlangan **Plan A integratsiya buildi**. Asosiy ilova sifatida saqlangan Stage 36 to‘liq 84 kunlik Academic IELTS bazasi ishlatilgan; uning ustiga Stage 40–50 talablari bo‘yicha alohida Final Studio, resurs ma’lumotlari, Task 1 vizual laboratoriyasi, lug‘at qamrovi, scoring, xato/lab va adaptive vositalar qo‘shilgan.

> Muhim manba izohi: Stage 40 original ZIP faylining o‘zi arxivda topilmadi; faqat uning SHA-256 yozuvi saqlangan. Stage 41–50 uchun ham barcha tarixiy patch binary/commitlari mavjud emas. Shu sababli bu paket asl Stage 40–50 source tree’ning aynan nusxasi emas — mavjud to‘liq baseline va saqlangan texnik hisobotlar, QA, roadmap hamda datasetlar asosida qayta yig‘ilgan integratsiya. Bu holat `docs/BUILD_PROVENANCE.json` va `docs/RELEASE_AUDIT_50_1.json` ichida qayd etilgan.

## Release 50.2 yangilanishi

- Final Studio endi 10 ta ishchi bo‘limga ega: Overview, Transcript, Scoring, Error & Lab, Adaptive, Resources, Task 1, Vocabulary, Privacy & Data va Release QA.
- Speaking audio yozuvlari foydalanuvchi tugmani bosganda MediaRecorder orqali yoziladi va IndexedDB’da qurilma ichida saqlanadi; clip’ni tinglash, yuklab olish va o‘chirish mumkin. Browser qo‘llab-quvvatlashi va microphone ruxsati talab qilinadi.
- Privacy & Data sahifasi saqlash joylarini ko‘rsatadi; Final Studio ma’lumotlarini aniq tasdiqlash bilan alohida tozalaydi. Main app progressiga tegmaydi.
- Resource filter case-insensitive; modal keyboard focus trap/restore, Escape close, reduced-motion va focus-visible holatlari qo‘shildi.
- Daily vocabulary core uchun 672/672 US/UK IPA + glossary maydonlari qayta audit qilindi. Keng 19K bankdagi barcha so‘zlar to‘liq tarjima qilingan deb da’vo qilinmaydi.

## Tez boshlash

1. ZIP’ni Extract qil.
2. `index.html`, `assets/`, `audio/`, `data/`, `icons/`, `manifest.webmanifest`, `sw.js` va `.nojekyll` fayllari **barchasi repository rootida** qolishi kerak.
3. GitHub’da `plan-a-` repository’sining `main` branch’iga shu fayl/papkalarni yukla. `index.html` ichma-ich papkada qolib ketmasin.
4. GitHub Pages sozlamasida **Deploy from a branch → main → /(root)** ni tanla.
5. Saytni HTTPS orqali birinchi marta och. PWA Service Worker va Live Speaking transcript `file://` rejimida ishlamaydi.

Paket yo‘llari `./` ko‘rinishida berilgan, shuning uchun repo `https://<username>.github.io/plan-a-/` kabi project path ostida joylashganda rootga qattiq bog‘lanmagan.

## Platformani qayerdan ochasan?

- `index.html` — asosiy GitHub Pages/PWA entry point.
- Navigatsiyadagi **Stage 40–50 Studio** — scoring, Speaking transcript + lokal audio yozuv, Error & Lab, Adaptive, 336 resurs, Task 1, Vocabulary, Privacy & Data va Release QA markazi.
- `standalone.html` — Final Studio kodi va Stage 47/48 ma’lumotlari HTML ichiga joylangan qo‘shimcha HTML varianti. Uni ham shu paket ichida och; MP3 tinglash uchun yonidagi `audio/` papkasi joyida qolishi kerak.

## Nimalar bor?

### Asosiy Academic IELTS platformasi

- 84 kun, 12 hafta, har kuni Reading, Listening, Writing va Speaking.
- 840 Reading savoli, 420 Listening savoli.
- Speaking: 252 Part 1 savoli, 84 Part 2 cue card, 252 Part 3 savoli.
- Har kuni Writing Task 1 va Task 2 promptlari.
- 61 maqola, 864 sentence pattern, 12 reading source pack.
- 84 ta MP3 — IELTS Boost uchun yaratilgan synthetic practice voice; rasmiy IELTS/Cambridge audiosi emas.
- 19 000 noyob qidiriladigan lexical entry.
- 10 advanced daily mission va eski 10 × 10 Power Labs modullari.

### Final Studio — Stage 40–50

- **Stage 40–41:** baseline, acceptance mezonlari, requirements traceability va saqlangan QA inventory.
- **Stage 42:** Speaking Part 1/2/3/daily uchun alohida transcript, final/interim natijalarni ajratish, autosave, reconnect cheklovi va manual fallback.
- **Stage 43:** yangi Studio JS/CSS/JSON modullarini asosiy compatibility app’dan ajratish. Eski runtime to‘liq feature-by-feature micro-module arxitekturaga qayta yozilmadi.
- **Stage 44:** Reading answer-key accuracy, dalil/strategy/transfer; Listening learner self-review; Writing Task 1/2 alohida; Speaking to‘rt mezonli, audio evidence talab qiladigan ichki 0–10 practice index.
- **Stage 45:** xato sababi + repair qaydi va 10 ta transfer/lab yo‘nalishi.
- **Stage 46:** minimum evidence gate’lari bilan deterministic adaptive recovery tavsiyalari.
- **Stage 47:** 84 kun × 4 skill = 336 resource row; 84 optional listening companion; olti oiladan 14 tadan jami 84 original fictional Task 1 dataset. Task 1 uchun chart, process/map ko‘rinishi, data inspector, four-part plan va 150-word completeness check bor.
- **Stage 48:** 19 000 index, 84 × 8 = 672 to‘liq dual-IPA daily core word, SRS. Keng bankda 677 ta to‘liq offline bilingual glossary yozuvi bor — 19 000 so‘zning barchasi tarjima/izoh bilan to‘liq emas.
- **Stage 49:** local-first saqlash, JSON backup/restore, explicit reset, IndexedDB audio yozuvlari, alohida download/delete, keyboard-focus boshqaruvi, reduced-motion va privacy ma’lumotlari.
- **Stage 50:** build audit, asset inventory, runtime recheck, deploy yo‘riqnomasi va release checks; yangi build v50.2.0.

## Ball va IELTS natijasi haqida

Platformadagi 0–10 ko‘rsatkichlar o‘quv jarayonini kuzatish uchun mo‘ljallangan ichki practice index. U rasmiy IELTS band emas. Transcript tahlili talaffuzni mustaqil baholamaydi; Speaking pronunciation uchun audio’ni tinglash va learner evidence kerak. Writing Task 1 completeness check so‘z soni/reja to‘liqligini tekshiradi, examiner o‘rnini bosmaydi.

Platforma IELTS 8.0 yoki 9.0 natijasini kafolatlamaydi. Bunday natija uchun rasmiy formatdagi timed mocklar, examiner/ustoz feedbacki va haqiqiy imtihon kalibrovkasi zarur.

## Audio va offline

Barcha 84 MP3 `audio/` ichida. Service Worker shell, CSS/JS va JSON data fayllarini cache qiladi; MP3’larni esa birinchi tinglashda bittalab cache’ga oladi. Shu sababli dastlabki audio tinglash uchun internet bo‘lishi kerak. Keyingi offline playback brauzer cache kvotasi va qurilma storage siyosatiga bog‘liq; 84 audio birdaniga oldindan cache qilinmaydi.

## Progress va backup

- Asosiy 84 kunlik ilova eski storage key’ni saqlaydi; eski progressning yangi Final Studio bilan avtomatik birlashtirilishi da’vo qilinmaydi.
- Final Studio alohida `IELTSBoost_PlanA_Stage4050_v1` localStorage key’dan foydalanadi; eski 50.1 state schema 2 ga migrate qilinadi.
- Final Studio ichidagi **Plan A progress backup** transcript, scores, errors, labs, SRS va draftlarni JSON qilib eksport qiladi. Binary audio yozuvlari JSON ichiga qo‘shilmaydi: Privacy & Data bo‘limidan har bir clip’ni alohida download qil. Asosiy platformadagi eski progress uchun uning o‘zidagi backup/export amalidan ham foydalan.
- Backup fayllarni boshqa joyda xavfsiz saqla; browser storage tozalansa lokal progress yo‘qolishi mumkin.

## Manba va yoshga moslik

Daily passage, prompt, chart va synthetic audio original IELTS Boost practice materialidir; rasmiy test savollari sifatida taqdim etilmaydi. Cambridge, IELTS.org, TED va boshqa provider kontenti uchun faqat rasmiy tashqi sahifalar linki beriladi. Pullik yoki mualliflik huquqi bilan himoyalangan materiallar paketga ko‘chirib kiritilmagan. Ayrim podcast linklari kattalar mavzusiga ega bo‘lishi mumkin; ularni majburiy yo‘l sifatida ishlatma.

## Qurilmada tekshirilishi kerak bo‘lganlar

MediaRecorder/IndexedDB audio capture kodi qo‘shilgan, lekin haqiqiy Android mikrofon ruxsati, SpeechRecognition sifati, Samsung A14’da PWA install, GitHub Pages’da offline qayta ochish, audio cache kvotasi va tashqi dictionary/translation API’lar ushbu build jarayonida real telefonda tekshirilmagan. Chromium click-flow automation muhit siyosati sabab bloklangan; statik, data, syntax va HTTP subpath testlari alohida ko‘rsatilgan.
