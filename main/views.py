from django.shortcuts import render
import requests

def HomeView(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        from_currency = request.POST.get('from_currency')
        to_currency = request.POST.get('to_currency')
        converted_amount = None

        if amount and from_currency and to_currency:
            try:
                # Fetch currency rates
                cbu_url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
                cbu_response = requests.get(cbu_url)
                cbu_data = cbu_response.json()

                # Handle UZS conversion directly
                from_rate = 1.0 if from_currency == "UZS" else float(next((item for item in cbu_data if item["Ccy"] == from_currency), {}).get("Rate", 0))
                to_rate = 1.0 if to_currency == "UZS" else float(next((item for item in cbu_data if item["Ccy"] == to_currency), {}).get("Rate", 0))

                if from_rate == 0 or to_rate == 0:
                    converted_amount = "Kiritilgan valyutalar topilmadi."
                else:
                    # Perform conversion
                    amount = float(amount)
                    converted_amount = (amount * from_rate) / to_rate
                    converted_amount = round(converted_amount, 2)
            except Exception as e:
                converted_amount = f"Xatolik yuz berdi: {str(e)}"
        else:
            converted_amount = "Barcha maydonlarni to'ldiring."

        return render(request, 'home.html', context={'converted_amount': converted_amount})

    return render(request, 'home.html')
