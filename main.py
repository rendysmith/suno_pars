# This is a sample Python script.
import asyncio
import playwright

from utils.user_agent import get_playwright

from constant import login, password


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


async def parser(url):
    name_playlist = input('Укажите имя плейлиста: ')

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
            print(len(blocks))
            break
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

            tool_time = 0

            data = f'#EXTINF:{tool_time},{title}\n{link}\n'

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
