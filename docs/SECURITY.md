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
