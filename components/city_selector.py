from shiny import App, ui

cities = {
    "Indonesia": ["Jakarta", "Surabaya", "Medan", "Bali", "Makassar", "Yogyakarta", "Bandung"],
    "Malaysia": ["Kuala Lumpur", "Penang", "Kota Kinabalu", "Johor Bahru", "Kuching"],
    "Singapore": ["Singapore"],
    "Thailand": ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Hat Yai"],
    "Vietnam": ["Hanoi", "Ho Chi Minh City", "Da Nang", "Hue"],
    "Philippines": ["Manila", "Cebu", "Davao", "Quezon City"],
    "Myanmar": ["Yangon", "Mandalay", "Naypyidaw"],
    "Cambodia": ["Phnom Penh", "Siem Reap"],
    "Laos": ["Vientiane", "Luang Prabang"],
    "Brunei": ["Bandar Seri Begawan"],
    "Timor-Leste": ["Dili"]
}

def city_selector_ui():
    return ui.panel(
        ui.h2("Select Your City"),
        ui.navset_pill(
            {country: ui.input_radio_buttons(f"{country.lower()}-cities", label=country, choices=city_list)
             for country, city_list in cities.items()}
        ),
        ui.button("Confirm", id="confirm-city")
    )

city_selector_app = App(city_selector_ui, None)