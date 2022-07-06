def parseTime(date_time):
    print(date_time)
    date, time = date_time.split("T")
    year, month, day = date.split("-")
    hour, minute, k, v = time.split(":")
    return int(year), int(month), int(day), int(hour) - 3, int(minute)


webhook_url = "https://api.telegram.org/bot5433238053:AAFiO1viOtq5URnvh-1byyOK32-4cRiX2iM/setWebhook?url=https://417d" \
              "-5-59-53-0.eu.ngrok.io/webhooks/start/ "
