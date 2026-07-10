# 🌤️ Weerfeitjes

Dagelijks weerfeitje op Discord via GitHub Actions!

## Setup

1. **Discord Webhook Secret toevoegen:**
   - Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `DISCORD_WEBHOOK`
   - Value: Je Discord Webhook URL

2. **Weerfeitjes toevoegen:**
   - Edit `.github/workflows/daily-weather.yml`
   - Vul de FACTS array in met jouw feitjes

3. **Testen:**
   - Actions → Dagelijks Weerfeitje → Run workflow

Done! 🚀
[Create workflow file](.github/workflows/daily-weather.yml)
