import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Maksimum uyarı sayısı (bu kadar uyarı alırsa otomatik ban)
MAX_WARNINGS = int(os.environ.get("MAX_WARNINGS", 3))

# Flood koruması: kaç saniyede kaç mesaj
FLOOD_MAX_MESSAGES = int(os.environ.get("FLOOD_MAX_MESSAGES", 5))
FLOOD_TIME_WINDOW = int(os.environ.get("FLOOD_TIME_WINDOW", 5))  # saniye

# Varsayılan mute süresi (dakika)
DEFAULT_MUTE_DURATION = int(os.environ.get("DEFAULT_MUTE_DURATION", 10))

# Yasaklı kelimeler (virgülle ayır)
BANNED_WORDS_RAW = os.environ.get("BANNED_WORDS", "spam,reklam,kazan,ücretsiz kazan")
BANNED_WORDS = [w.strip().lower() for w in BANNED_WORDS_RAW.split(",")]

# Yasaklı linkler / domain'ler
BANNED_LINKS_RAW = os.environ.get("BANNED_LINKS", "bit.ly,tinyurl.com")
BANNED_LINKS = [l.strip().lower() for l in BANNED_LINKS_RAW.split(",")]

# Linklere izin verilsin mi? (False = tüm linkler yasak)
ALLOW_LINKS = os.environ.get("ALLOW_LINKS", "true").lower() == "true"
