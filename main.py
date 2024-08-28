# This is a sample Python script.
import asyncio
import playwright

from utils.user_agent import get_playwright

from constant import login, password


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests

# def fetch_json_data(url):
#     headers = {
#         'Accept-Encoding': 'gzip, deflate, br, zstd',
#         'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
#         'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yT1o2eU1EZzhscWRKRWloMXJvemY4T3ptZG4iLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJzdW5vLWFwaSIsImF6cCI6Imh0dHBzOi8vc3Vuby5jb20iLCJleHAiOjE3MjQ4NDUxMzYsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvY2xlcmtfaWQiOiJ1c2VyXzJldGxqNzVJTWN1WlI1em9nUHVodHRsTjBieSIsImh0dHBzOi8vc3Vuby5haS9jbGFpbXMvZW1haWwiOiJyaXRtb3JpY2FAZ21haWwuY29tIiwiaHR0cHM6Ly9zdW5vLmFpL2NsYWltcy9waG9uZSI6bnVsbCwiaWF0IjoxNzI0ODQ1MDc2LCJpc3MiOiJodHRwczovL2NsZXJrLnN1bm8uY29tIiwianRpIjoiMDhhOTE1YWRjZDYxOTg4ODlhOWUiLCJuYmYiOjE3MjQ4NDUwNjYsInNpZCI6InNlc3NfMmxFTkdUd2tuVWhZQ3ZFUXBhYlBRZE9hTENzIiwic3ViIjoidXNlcl8yZXRsajc1SU1jdVpSNXpvZ1B1aHR0bE4wYnkifQ.WMa60WXs9JKO4rsn-xKgB0UHt4HF9lGM9yzJvS2SC_kz5YxA9naAOdW4OEGzqjn5lMEQOVXmaMpRt8NTWEXBI7p3tdPwobIthRxjFDiNumNWrEmFD_ReQDOInzEHRN5CrRTWkHZ6p4sE-CfZUPNZ7ObcuOxOaNsEbt5IzIQzwClAWnUA5Zn2Wz_05Pzi54A253UswiS2DFfMsfu71RJxQI9NofO0ggyQ-Yj7tppvAUTdn6HY3V7DkastMfzbt_29qTFXq044P8-Jod_7D0B9-XV2zVvPITbP7j5yENw6YoL0Lew2bqQk1MSQ5SCHWnZYWKWqaN8Apfw9TMedy7WETQ',
#         'Connection': 'keep-alive',
#         'DNT': '1',
#         'Host': 'studio-api.suno.ai',
#         'Origin': 'https://suno.com',
#         'Priority': 'u=4',
#         'Referer': 'https://suno.com/',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'cross-site',
#         'TE': 'trailers',
#         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
#     }
#
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
#     return response.json()
#
# # Пример использования:
#
# url = 'https://studio-api.suno.ai/api/feed/v2?page=0'  # Замените на реальный URL
# data = fetch_json_data(url)
# print(data)
#
# input()





async def parser(url):
    name_playlist = url.split('/')[-1]
    input(name_playlist)

    playwright, browser, page = await get_playwright(url, headless=False)

    while True:
        try:
            button_ms = await page.query_selector('img[alt="Sign in with Microsoft"]')
            await button_ms.click()
            break

        except:
            await asyncio.sleep(2)

    while True:
        try:
            button_name = await page.query_selector('input[type="email"]')
            await button_name.fill(login)
            # Нажатие Enter
            await button_name.press('Enter')
            break

        except:
            await asyncio.sleep(2)

    await asyncio.sleep(5)
    while True:
        try:
            button_pass = await page.query_selector('input[type="password"]')
            await button_pass.fill(password)
            # Нажатие Enter
            await button_pass.press('Enter')
            break

        except:
            await asyncio.sleep(2)

    await asyncio.sleep(5)
    while True:
        try:
            button_yes = await page.query_selector('button[id="acceptButton"]')
            await button_yes.click()
            break

        except:
            await asyncio.sleep(2)

    while True:
        try:
            blocks = await page.query_selector_all('div[class="react-aria-GridListItem"]')
            len_blocks = len(blocks)
            print(len_blocks)
            if len_blocks != 0:
                break

            else:
                await asyncio.sleep(2)

        except:
            await asyncio.sleep(2)

    with open(f"{name_playlist}.m3u", "w", encoding="utf-8") as file:
        file.write("#EXTM3U\n")

        for block in blocks:
            artist_content = await block.query_selector('a[title][color="white"]')
            artist = await artist_content.inner_text()
            print(artist)

            title_content = await block.query_selector('span[class="hover:underline cursor-pointer"]')
            title = await title_content.inner_text()
            print(title)

            link_content = await block.query_selector('div[class="css-xuleq2"]')
            link = await link_content.get_attribute('data-clip-id')
            link = f"https://cdn1.suno.ai/{link}.mp3"

            tool_time_content = await block.query_selector('div[class="relative"]')
            tool_time = await tool_time_content.inner_text()
            tool_time = tool_time.split(':')
            tool_time = int(tool_time[0]) * 60 + int(tool_time[1])

            data = f'#EXTINF:{tool_time},{artist} - {title}\n{link}\n'

            try:
                file.write(data)
            except:
                print(f'{index} --- Error --- :\n{data}')


async def main():
    url = input('Укажите адрес для парсинга: ')
    await parser(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
