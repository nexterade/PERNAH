# PERNAH — Data Classification & Privacy Boundary

## Purpose

Dokumen ini menetapkan batas data untuk PERNAH sebelum project membuka lebih banyak input interface. Fokusnya adalah **klasifikasi dan governance**, bukan implementasi Secret Vault.

PERNAH tidak boleh memperlakukan semua data sebagai kelas risiko yang sama. Canonical persistence berarti data dapat dipertahankan, tetapi tidak berarti semua data aman untuk disimpan sebagai plaintext atau dibawa ke setiap backup/export/log.

## Data classes

### 🟢 Normal Data

Contoh:

- diary dan catatan harian;
- pengeluaran/transaksi;
- event, keputusan, commitment;
- lokasi atau objek yang memang dipilih user untuk disimpan sebagai memory.

Normal Data dapat menjadi canonical memory dan mengikuti retention permanen PERNAH.

### 🟡 Sensitive Data

Contoh umum:

- data pribadi yang lebih sensitif;
- informasi kontak atau konteks pribadi yang jika bocor dapat merugikan user;
- data lain yang secara konteks tidak cocok dimasukkan ke log, demo, atau artifact publik.

Sensitive Data **belum otomatis berarti Secret**. Namun interface, logging, export, backup, dan debugging harus memperlakukannya lebih hati-hati daripada Normal Data.

### 🔴 Secret Data

Contoh:

- password;
- API key/token;
- PIN autentikasi;
- recovery code;
- private key;
- seed phrase;
- credential login;
- secret TOTP/GAuth.

Secret Data **tidak boleh disimpan plaintext sebagai Memory Core canonical data** pada implementasi PERNAH saat ini.

## Canonical retention rule

Canonical data tidak boleh dihapus, dipangkas, atau dibuat kedaluwarsa secara otomatis sebagai bagian dari maintenance, retrieval, indexing, backup, atau optimasi.

Derived data seperti index, embedding, cache, ranking, summary, dan hasil AI boleh dibangun ulang atau dibuang sesuai kebutuhan. Hal tersebut tidak boleh menghapus canonical source.

Penghapusan canonical data harus merupakan tindakan eksplisit yang memang dirancang sebagai operasi user dan memiliki governance tersendiri.

## Secret Vault boundary

PERNAH **belum memiliki Secret Vault production-ready**.

Secret Vault adalah future capability yang terpisah dari Memory Core:

```text
PERNAH
├── MEMORY CORE
│   ├── diary / expense / event / decision
│   └── canonical persistence
└── SECRET VAULT (future capability)
    ├── password / token / API key / TOTP secret
    └── encrypted storage + unlock boundary
```

Jika Secret Vault kelak diimplementasikan, desain minimalnya harus mempertimbangkan:

- encryption/decryption, bukan sekadar encoding/Base64;
- authenticated encryption atau mekanisme integritas setara;
- key derivation dari password/PIN dengan salt dan parameter yang terdokumentasi;
- password/PIN unlock tidak disimpan sebagai plaintext database secret;
- lock/unlock lifecycle yang terpisah dari delete;
- backup/export yang tidak membocorkan plaintext secret;
- failure handling dan recovery yang diuji;
- threat model sebelum implementation dianggap production-ready.

**Jangan memasukkan credential nyata ke test drive atau test fixture PERNAH.**

## Interface and logging boundary

Input interface harus mempertahankan batas klasifikasi ini. Web, messaging, import, atau interface lain tidak boleh menjadi alasan untuk memasukkan Secret Data ke Memory Core secara diam-diam.

Log, error output, screenshot, documentation, ZIP release, dan fixture test juga tidak boleh berisi secret nyata.

## Current status

- Data classification: **governance defined**.
- Canonical retention rule: **defined**.
- Secret Vault: **roadmap / not implemented**.
- Encryption/key management for secrets: **not implemented in PERNAH Core**.
- Current manual input and upcoming Web Interface: **must not be treated as Secret Vault**.


## Web reader framing boundary

The product shell embeds the canonical Chronicle and Glossary reference documents in same-origin reader surfaces. To support that intentional integration without broadly enabling framing:

- application/product responses remain `X-Frame-Options: DENY` and `frame-ancestors 'none'`;
- static reference documents use `X-Frame-Options: SAMEORIGIN` and `frame-ancestors 'self'`;
- the product shell allows `frame-src 'self'` only, so external frame sources remain disallowed.

This is a narrow same-origin exception for the existing local documentation reader, not a general public framing policy.


## Image attachment boundary — schema v4

Image attachments are canonical evidence linked to a Memory record. They are stored as SQLite BLOBs and included in canonical JSON backup/export using validated Base64. The local Web Interface accepts only JPEG, PNG, GIF, and WebP, validates the payload signature, limits uploads to 4 images per capture, 8 MiB per image, and 12 MiB per request, and rejects SVG or arbitrary files.

A receipt or payment screenshot may contain names, account details, balances, or other Sensitive Data. Keep the current interface bound to localhost, avoid logging payload contents, and do not send attachments to external services or AI providers. The current implementation does not perform OCR, image interpretation, redaction, encryption-at-rest, or per-attachment access control; do not treat it as a secure document vault or expose it remotely.


## AI external-processing boundary — dev.72

- External provider processing is denied by default. Passing a provider object alone must not authorize transmission of memory content.
- The provider-neutral orchestration boundary requires an explicit per-call policy that acknowledges authorization and disclosure and limits data categories to `memory_text` and/or `bounded_descriptive_metadata`. Unknown categories fail closed.
- This policy object is an engineering guard, **not** a consent interface, legal disclosure, provider-terms verifier, or proof that a user actually consented. A future UI/integration must explain the provider, exact data classes sent, retention/training use, cost, and available alternatives before enabling processing.
- Secret Data, API credentials, full attachment bytes, and arbitrary storage metadata must never be included in provider context. Exception messages and provider payloads must not be written to logs.
- Timeout, network failure, rate limit, refusal, malformed output, or absent authorization must preserve deterministic behavior and must not mutate canonical memory.
- Provider retention/training terms and cost remain unreviewed; therefore no real provider, SDK, or network integration is enabled in dev.72.


## Provider failure classification — dev.72

Provider failures are mapped to stable categories without exposing exception messages or response bodies. Timeout, rate-limit, refusal, authentication, service-unavailable, invalid-response, and generic failures all preserve deterministic fallback. Automatic retries are intentionally absent so a future adapter cannot silently multiply costs or external processing. This is not a provider integration and does not replace reviewing terms, retention, training use, and disclosure.


## External AI processing disclosure gate

Before any real external AI call, PERNAH requires an explicit authorization, disclosure acknowledgement, a strict allowlist of data categories, and reviewed flags for provider identity, retention, training/data use, deletion terms, and acknowledged cost limits. Unknown or ambiguous provider terms block integration. These flags are engineering guards only: they do not constitute a consent UI, verify vendor statements, or measure actual cost. Canonical memory remains local-first and is not automatically deleted or expired to match provider retention.
