import os
import sys
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = {
    'BOT_TOKEN': 'Telegram Bot Token',
    'STEAM_API_KEY': 'Steam Web API Key',
    'RIOT_API_KEY': 'Riot Games API Key',
    'WOT_APPLICATION_ID': 'Wargaming Application ID',
    'PUBG_API_KEY': 'PUBG API Key',
}

OPTIONAL_VARS = {
    'OPENAI_API_KEY': 'OpenAI API Key (для AI анализа)',
    'CRYPTO_ADDRESS': 'Криптоадрес для платежей',
    'ZERO_CRYPTO_PAY_API_KEY': 'ZeroCryptoPay API Key',
    'ADMIN_IDS': 'Telegram ID администраторов',
}

print("🔍 Проверка конфигурации...")
print("=" * 50)

all_ok = True

# Проверка обязательных переменных
print("\n📋 ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ:")
for var, desc in REQUIRED_VARS.items():
    value = os.getenv(var)
    if value and value.strip():
        status = "✅"
        masked = value[:10] + "..." if len(value) > 10 else value
        if any(keyword in var for keyword in ['KEY', 'TOKEN', 'SECRET']):
            masked = "***" + value[-4:] if len(value) > 4 else "***"
    else:
        status = "❌"
        masked = "НЕ УСТАНОВЛЕНА"
        all_ok = False
    print(f"{status} {desc}: {masked}")

# Проверка опциональных переменных
print("\n📋 ОПЦИОНАЛЬНЫЕ ПЕРЕМЕННЫЕ:")
for var, desc in OPTIONAL_VARS.items():
    value = os.getenv(var)
    if value and value.strip():
        status = "⚠️ "
        masked = value[:10] + "..." if len(value) > 10 else value
        if any(keyword in var for keyword in ['KEY', 'TOKEN', 'SECRET']):
            masked = "***" + value[-4:] if len(value) > 4 else "***"
    else:
        status = "➖"
        masked = "Не установлена"
    print(f"{status} {desc}: {masked}")

# Проверка администраторов
print("\n👑 АДМИНИСТРАТОРЫ:")
admin_ids = os.getenv('ADMIN_IDS', '')
if admin_ids:
    ids = [id.strip() for id in admin_ids.split(',')]
    print(f"✅ Найдены ID: {', '.join(ids)}")
else:
    print("❌ ADMIN_IDS не установлен")
    all_ok = False

print("=" * 50)

if all_ok:
    print("\n🎉 ВСЕ ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ УСТАНОВЛЕНЫ!")
    print("Бот готов к запуску.")
else:
    print("\n⚠️  НЕ ВСЕ ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ УСТАНОВЛЕНЫ!")
    print("Добавьте недостающие переменные в файл .env")
    sys.exit(1)