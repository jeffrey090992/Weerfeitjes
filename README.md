
name: Dagelijks Weerfeitje

on:
  schedule:
    - cron: '0 8 * * *'
  workflow_dispatch:

jobs:
  send-weather-fact:
    runs-on: ubuntu-latest

    steps:
      - name: Select Random Weather Fact
        id: fact
        run: |
          FACTS=(
            "🌧️ test 1"
            "⚡ Feitje 2"
          )

          RANDOM_INDEX=$((RANDOM % ${#FACTS[@]}))
          SELECTED_FACT="${FACTS[$RANDOM_INDEX]}"

          echo "FACT=$SELECTED_FACT" >> $GITHUB_OUTPUT

      - name: Verzend naar Discord
        env:
          FACT: ${{ steps.fact.outputs.FACT }}
          WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
        run: |
          curl -X POST "$WEBHOOK" \
          -H "Content-Type: application/json" \
          -d "$(jq -n --arg content "$FACT" '{content: $content}')"
