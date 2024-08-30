# This is a sample Python script.
import asyncio
import json
import re
from pprint import pprint

import playwright

from utils.user_agent import get_playwright, get_soup

from constant import login, password

async def get_with_auth(page, name_playlist):
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

    input("Next?")

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


async def get_without_auth(page):
    print('Name Author')
    n = 0
    while True:
        print('n = ', n)
        if n > 10:
            return

        try:
            blocks = await page.query_selector_all('a[title]')
            len_blocks = len(blocks)
            print("len_blocks", len_blocks)

            if len_blocks > 0:
                break

            await asyncio.sleep(2)

        except:
            await asyncio.sleep(2)

        n += 1

    with open(f"{name_playlist}.m3u", "w", encoding="utf-8") as file:
        file.write("#EXTM3U\n")

        for block in blocks:
            url_splite = url.split('@')
            artist = url_splite[-1]
            print(artist)

            title = await block.inner_text()
            print(title)

            link_content = await block.get_attribute('href')
            link = link_content.split('/')[-1]
            link = f"https://cdn1.suno.ai/{link}.mp3"

            tool_time = 180

            data = f'#EXTINF:{tool_time},{artist} - {title}\n{link}\n'

            try:
                file.write(data)
            except:
                print(f'{index} --- Error --- :\n{data}')

async def get_soup_without_auth(url):
    soup = await get_soup(url)
    script_content = str(soup)

    script_content = script_content.replace("\\", "")
    print(script_content)

    # Используем регулярные выражения для поиска всех JSON объектов
    pattern = r'\{"id":[a-zA-Z0-9_.+-]"continue_at":\d+\}'
    pattern = r'\{"clip":"[a-zA-Z0-9-]+","relative_index":(?:None|\d+)\}'
    pattern = r'\{"id":"[^"]*".*?"relative_index":\d+\}'
    #json_strings = re.findall(pattern, script_content)
    pattern = r"'clip':\s*{[^}]*?}\s*'relative_index':\d+}"
    pattern = r'"clip":\s*\{[^}]*?\}\s*"relative_index":\d+}'
    json_strings = re.findall(pattern, script_content, re.DOTALL)
    print(len(json_strings))

    # Список для хранения словарей
    json_objects = []

    # Парсим каждый JSON и добавляем в список
    for json_str in json_strings:
        print(json_str)
        input('OK!')

        if 'audio_url' in json_str:
            print(json_str)
            parsed_json = eval(json_str)
            input(parsed_json)

        #
        #
        #
        # try:
        #     parsed_json = json.loads(json_str)
        #     json_objects.append(parsed_json)
        #
        # except json.JSONDecodeError:
        #     # Обрабатываем возможные ошибки при парсинге JSON
        #     print(f"Ошибка парсинга JSON: {json_str}")

    # Пример вывода ID и URL из каждого словаря
    for obj in json_objects:
        clip_data = obj.get('clip', {})
        print("ID:", clip_data.get('id'))
        print("Video URL:", clip_data.get('video_url'))
        print("Tags:", clip_data.get('metadata', {}).get('tags'))



async def parser(url):
    name_playlist = url.split('/')[-1]
    #input(name_playlist)
    #playwright, browser, page = await get_playwright(url, headless=False)

    if '@' in url:
        #await get_without_auth(page)
        await get_soup_without_auth(url)

    else:
        await get_with_auth(page)



async def main():
    #url = input('Укажите адрес для парсинга: ')
    url = 'https://suno.com/@lungcorf'
    await parser(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
