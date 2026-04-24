# 🛡️ Telegram Security Bot

Telegram grupları için gelişmiş güvenlik botu.

## Özellikler

- 🚨 **Flood koruması** — Kısa sürede çok mesaj atanları otomatik susturur
- 🚫 **Yasaklı kelime filtresi** — Belirlenen kelimeleri içeren mesajları siler
- 🔗 **Link filtresi** — Tüm linkleri veya belirli domainleri engeller
- 🔨 **Ban / Unban** — Kullanıcı banlama
- ⚠️ **Warn / Unwarn** — Uyarı sistemi (max uyarıya ulaşınca otomatik ban)
- 🔇 **Mute / Unmute** — Geçici susturma

## Komutlar

| Komut | Açıklama |
|-------|----------|
| `/ban @kullanici [sebep]` | Kullanıcıyı banla |
| `/unban @kullanici` | Banı kaldır |
| `/warn @kullanici [sebep]` | Uyarı ver |
| `/unwarn @kullanici` | Son uyarıyı kaldır |
| `/warns @kullanici` | Uyarı listesini göster |
| `/mute @kullanici [dakika]` | Sustur |
| `/unmute @kullanici` | Susturmayı kaldır |

> Reply ile de kullanılabilir: Mesaja reply at ve komutu yaz.

---

## 🚀 Kurulum

### 1. Bot Token Al
1. Telegram'da [@BotFather](https://t.me/BotFather)'a git
2. `/newbot` ile yeni bot oluştur
3. Token'ı kopyala

### 2. GitHub'a Yükle
```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/KULLANICI/telegram-security-bot.git
git push -u origin main
```

### 3. Railway Deployment
1. [railway.app](https://railway.app) sitesine git
2. **New Project → Deploy from GitHub repo** seç
3. Repoyu seç
4. **Variables** sekmesine git ve şunları ekle:

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `BOT_TOKEN` | BotFather'dan aldığın token | `123456:ABC...` |
| `MAX_WARNINGS` | Kaç uyarıda ban? | `3` |
| `FLOOD_MAX_MESSAGES` | X saniyede kaç mesaj? | `5` |
| `FLOOD_TIME_WINDOW` | Flood penceresi (saniye) | `5` |
| `BANNED_WORDS` | Yasaklı kelimeler (virgülle) | `spam,reklam,kazan` |
| `BANNED_LINKS` | Yasaklı domainler (virgülle) | `bit.ly,tinyurl.com` |
| `ALLOW_LINKS` | Linklere izin var mı? | `true` veya `false` |

5. Deploy otomatik başlar ✅

### 4. Botu Gruba Ekle
1. Botu gruba ekle
2. **Admin yap** ve şu izinleri ver:
   - Üyeleri yasakla
   - Mesajları sil
   - Üyeleri kısıtla

---

## ⚙️ Yapılandırma

Tüm ayarlar Railway environment variable'ları üzerinden yapılır, kod değişikliği gerekmez.

### Flood Koruması
- `FLOOD_MAX_MESSAGES=5` ve `FLOOD_TIME_WINDOW=5` → 5 saniyede 5'ten fazla mesaj = flood

### Yasaklı Kelimeler
```
BANNED_WORDS=spam,reklam,kazan,ücretsiz kazan,para kazan
```

### Link Ayarları
- `ALLOW_LINKS=false` → Tüm linkler yasak
- `ALLOW_LINKS=true` + `BANNED_LINKS=bit.ly,tinyurl.com` → Sadece bu domainler yasak

---

## 📁 Proje Yapısı

```
telegram-security-bot/
├── bot.py              # Ana dosya
├── config.py           # Yapılandırma
├── database.py         # SQLite veritabanı
├── handlers/
│   ├── admin.py        # Ban/Unban/Warn/Mute komutları
│   ├── filters.py      # Kelime/link filtresi
│   └── flood.py        # Flood koruması
├── requirements.txt
├── Procfile            # Railway için
└── README.md
```
