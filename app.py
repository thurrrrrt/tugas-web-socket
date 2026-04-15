import asyncio
import requests
from bs4 import BeautifulSoup
import websockets
import json

# Fungsi scraping
def scrape_wartabromo():
    url = "https://www.wartabromo.com/"
    response = requests.get(url)

    hasil = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="td_module_7")

        for article in articles:
            title_tag = article.find("h3", class_="entry-title")
            title = title_tag.text.strip() if title_tag else "Tanpa Judul"

            link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else "#"

            date_tag = article.find("time", class_="entry-date")
            date = date_tag.text.strip() if date_tag else "Tanggal tidak tersedia"

            hasil.append({
                "judul": title,
                "tanggal": date,
                "link": link
            })

    return hasil


# WebSocket handler (SUDAH DI-FIX)
async def handler(websocket):
    print("Client terhubung")
    try:
        while True:
            data = scrape_wartabromo()
            await websocket.send(json.dumps(data, indent=2))
            await asyncio.sleep(10)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnect")


# Menjalankan server
async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server WebSocket jalan di ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())