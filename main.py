import re
import discord
import requests
import gunicorn
from bs4 import BeautifulSoup
from discord.ext import commands
from googletrans import Translator
from selenium import webdriver
from wcwidth import wcswidth


# 사용할 포트 설정
PORT = process.env.PORT or '5000'
# 디스코드 봇 제작자
Director = "Lisianthus26"
# discord 봇 생성
bot = commands.Bot(command_prefix='f/')
# 웹 드라이버 호출
driver = webdriver.Chrome('C:\\gitLocation\Find-Ark\chromedriver.exe')
# 로스트아크 공식 홈페이지 공지사항 URL
notice_url = "https://lostark.game.onstove.com/News/Notice/List/"
# 로스트아크 공식 홈페이지 캐릭터 검색 URL
character_search_url = "https://lostark.game.onstove.com/Profile/Character/"
# 로아와 URL
loawa_url = "https://loawa.com/"


def fmt(x, w, align='r'):
    x = str(x)
    l = wcswidth(x)
    s = w - l
    if s <= 0:
        return x
    if align == 'l':
        return x + ' ' * s
    if align == 'c':
        sl = s // 2
        sr = s - sl
        return ' ' * sl + x + ' ' * sr
    return ' ' * s + x


@bot.event
# 봇 구동 완료
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game
    (name="Find-Ark.py | f/도움말"))  # 온라인
    print("Logged in as " + Director)
    print(bot.user.name)  # 토큰으로 로그인 된 bot 객체에서 discord.User 클래스를 가져온 뒤 name 프로퍼티를 출력
    print(bot.user.id)  # 위와 같은 클래스에서 id 프로퍼티 출력
    print('-----------------------------------------------')


@bot.command(aliases=["도움"])
# 봇 도움말
async def 도움말(ctx):
    page1 = discord.Embed(title="🔍 Find-Ark Plugin Commands", color=0xa6e3f2)
    # page1.set_background(url="https://imgur.com/df4rD7a")
    page1.set_thumbnail(
        url="https://shop-phinf.pstatic.net/20180408_271/500229060_1523117971399E3s2D_JPEG/DSC_7394-750.JPG?type=w860")
    page1.add_field(name="General Commands", value="f/Command", inline=False)
    # page1.add_field(name="Levels 🏅", value="➖➖➖➖", inline=True)
    page1.add_field(name="Basic Commands 📘", value="➖➖➖➖➖➖➖➖➖➖", inline=False)
    page1.add_field(
        name="```도움말``` ```핑``` ```날씨``` ```유저``` ```내정보``` ```모험섬``` ```카게```" + "\n" + "```항해``` ```보스``` ```캘린더섬```  ```도디언``` ```도비스```",
        value="➖➖➖➖➖➖➖➖➖➖")
    # page1.add_field(name="Search 🔍", value="➖➖➖➖", inline=False)
    # page1.add_field(name="Music 🎵", value="➖➖➖➖", inline=True)
    page1.set_footer(text="🌼 This Bot developed by Lisianthus26")
    await ctx.send(embed=page1)
    # 임베드 정상적으로 생성 및 설정완료 문구 출력
    print("Help Embed has been generated!")
    # 실행창 구분자
    print("-----------------------------------------------")


# @bot.command(aliases=["채널설정"])
# @commands.has_permissions(manage_messages=True)
# async def setchannel(ctx, name):
#     guild = ctx.message.guild
#     channel = discord.utils.get(guild.text_channels, name=name).id
#     await channel.set_permissions(bot, )


@bot.command(aliases=["핑"])
# 봇의 핑을 pong! 이라는 메세지와 함께 전송한다.
async def ping(ctx):
    await ctx.send(f'pong! {round(round(bot.latency, 4) * 1000)}ms')
    print("Current Ping = " + f"{round(round(bot.latency, 4) * 1000)}" + "ms")
    print('-----------------------------------------------')


@bot.command(aliases=['delete', '청소'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=None):
    max_of_amount = 21
    mgs = []
    if amount is None:
        await ctx.send("삭제할 메시지의 개수를 입력해주세요.")
        time.sleep(1.2)
        await ctx.channel.purge(limit=2)
    else:
        try:
            amount = int(amount)
        except Exception as e:
            print(e)
        if amount < max_of_amount:
            try:
                channel = ctx.message.channel
                messages = []
                amount = int(amount)
                async for message in channel.history(limit=amount + 1):
                    messages.append(message)
                await channel.delete_messages(messages)
                await ctx.send(str(amount) + "개의 메시지가 삭제되었습니다.")
                time.sleep(1)
            except Exception:
                await ctx.send("2주 지난 메시지는 삭제할 수 없습니다.")
                time.sleep(1)
                await ctx.channel.purge(limit=2)
        else:
            await ctx.send(str(max_of_amount - 1) + "개 이하의 메시지만 삭제할 수 있습니다.")
            time.sleep(1.2)
            await ctx.channel.purge(limit=2)


@bot.command(aliases=['소거'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=None):
    max_of_amount = 21
    mgs = []
    if amount is None:
        await ctx.send("삭제할 메시지의 개수를 입력해주세요.")
        time.sleep(1.5)
        await ctx.channel.purge(limit=2)
    else:
        try:
            amount = int(amount)
        except Exception as e:
            print(e)
        if amount < max_of_amount:
            amount = int(amount)
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(str(amount) + "개의 메시지가 삭제되었습니다.")
            time.sleep(1.5)
            await ctx.channel.purge(limit=1)
        else:
            await ctx.send(str(max_of_amount - 1) + "개 이하의 메시지만 삭제할 수 있습니다.")
            time.sleep(1.5)
            await ctx.channel.purge(limit=2)


@bot.command(aliases=["채널"])
@commands.has_permissions(manage_messages=True)
async def channel(ctx):
    all_text_channels = ctx.guild.text_channels
    embed = discord.Embed(title="Channel List", colour=0xc6df10)
    value = []
    for x in all_text_channels:
        channel = value.append(x)
        channels = "".join(channel)
    embed.add_field(name="Channels", value=channels)
    await ctx.send(embed=embed)


@bot.command(aliases=['날씨', '기상'])
# 지역의 날씨를 알려준다.
async def weather(ctx):
    args = str(ctx.message.content).split()
    command = args[1:]
    local = "".join(command)
    print(local)

    trans = Translator(service_urls=['translate.google.com', "translate.google.co.kr"])
    detect_result = trans.detect(local)
    detect_local = detect_result.lang
    trans_local = trans.translate(local, dest='en')
    keyword_name = trans_local.text
    # print("키워드 : " + keyword_name)
    base_url = "https://www.yr.no/"

    pre_url = base_url + "nb/s%C3%B8k?q=" + keyword_name
    pre_req = requests.get(pre_url)
    pre_soup = BeautifulSoup(pre_req.text, "html.parser")
    args_location_regions = pre_soup.find("span", class_="search-results-list__item-name").text.split(",")
    strs_location_regions = "".join(args_location_regions)
    url_location = pre_soup.find("a", class_="search-results-list__item-anchor")["href"][1:]

    post_url = base_url + url_location
    post_req = requests.get(post_url)
    post_soup = BeautifulSoup(post_req.text, "html.parser")
    weather = base_url + post_soup.find("div", class_="now-hero").find("img", class_="symbol__fallback")["src"]
    # print(weather)
    temperature_str = "".join(post_soup.find("span", class_="temperature temperature--warm").text)
    temperature_index = temperature_str.rfind("r")
    temperature = temperature_str[temperature_index + 1:]
    apparent_temperature = post_soup.find("div", class_="feels-like-text").find("span",
                                                                                class_="temperature temperature--warm").text
    amount_of_precipitation = post_soup.find("span",
                                             class_="precipitation__value now-hero__next-hour-precipitation-value").text
    speed_of_wind = post_soup.find("span", class_="wind__container").text

    # print("Search Url : " + pre_url)
    # print("Target Url : " + post_url)
    # print("온도 : " + temperature)
    # print("체감온도 : " + apparent_temperature)
    # print("강수량 : " + amount_of_precipitation + " mm")
    # print("풍속 : " + speed_of_wind)

    # 임베드 생성 및 설정
    page1 = discord.Embed(title=local,
                          url=post_url,
                          colour=0x303193)
    page1.set_thumbnail(url=weather)
    page1.set_author(name="기상정보")
    page1.add_field(name="기온", value=temperature)
    page1.add_field(name="체감온도", value=apparent_temperature)
    page1.add_field(name="현재 평균 강수량", value=amount_of_precipitation + "mm", inline=False)
    page1.add_field(name="풍속", value=speed_of_wind)
    page1.set_footer(text="🌐 출처 - 노르웨이 기상청")
    msg = await ctx.send(embed=page1)
    # 임베드 정상적으로 생성 및 설정완료 문구 출력
    print("Weather Embed has been generated!")
    # 실행창 구분자
    print("-----------------------------------------------")


@bot.command(aliases=["유저"])
# 캐릭터 정보
async def user(ctx):
    # 캐릭터 정보 파싱(디스코드 네임 = 로스트아크 캐릭터 네임)
    args = str(ctx.message.content).split()
    nickname = args[1]
    character_url = character_search_url + nickname
    req = requests.get(character_url)
    soup = BeautifulSoup(req.text, "html.parser")
    server = soup.find("span", class_="profile-character-info__server")["title"][1:]
    game_class = soup.find("img", class_="profile-character-info__img")["alt"]
    logo_class = soup.find("img", class_="profile-character-info__img")["src"]
    expedition_level = soup.find("div", class_="level-info__expedition").find_all("span")[1].text.strip()
    character_level = soup.find("div", class_="level-info__item").find_all("span")[1].text.strip()
    equip_item_level = soup.find("div", class_="level-info2__expedition").find_all("span")[1].text.strip()
    achievement_item_level = soup.find("div", class_="level-info2__item").find_all("span")[1].text.strip()
    guild = soup.find("div", class_="game-info__guild").find_all("span")[1].text.strip()
    attack_power = soup.find("div", class_="profile-ability-basic").find_all("span")[1].text.strip()
    max_life_force = soup.find("div", class_="profile-ability-basic").find_all("span")[3].text.strip()
    ability_battle = soup.find("div", class_="profile-ability-battle").find("h4").text
    ability_battle_detail = soup.find("div", class_="profile-ability-battle").find_all("span")
    engraving_effects = str(soup.find("div", class_="profile-ability-engrave").find_all("span"))
    engraving_effects = re.sub('<.+?>|[|]', '', engraving_effects, 0).strip()
    engraving_effect = engraving_effects[1:len(engraving_effects) - 1].split(",")

    # 임베드 생성 및 설정
    page1 = discord.Embed(title=f"{nickname}",
                          url="https://lostark.game.onstove.com/Profile/Character/" + nickname,
                          colour=0xFFB2F5)
    page1.set_thumbnail(url=logo_class)
    page1.set_author(name=nickname + " 님의 캐릭터 정보")
    page1.add_field(name="서버", value=server, inline=True)
    page1.add_field(name="직업", value=game_class)
    page1.add_field(name="길드", value=guild)
    page1.add_field(name="원정대 레벨", value=expedition_level, inline=True)
    page1.add_field(name="캐릭터 레벨", value=character_level)
    page1.add_field(name="장착 아이템 레벨", value=equip_item_level, inline=False)
    page1.add_field(name="달성 아이템 레벨", value=achievement_item_level, inline=False)
    page1.add_field(name="⚔️공격력", value=attack_power, inline=True)
    page1.add_field(name=" 💚최대 생명력", value=max_life_force)
    page1.add_field(name=ability_battle, value="=======================", inline=False)
    page1.add_field(name=ability_battle_detail[0].text + " 💥", value=ability_battle_detail[1].text)
    page1.add_field(name=ability_battle_detail[2].text + " ✨", value=ability_battle_detail[3].text)
    page1.add_field(name=ability_battle_detail[4].text + " 💬", value=ability_battle_detail[5].text)
    page1.add_field(name=ability_battle_detail[6].text + " 💨", value=ability_battle_detail[7].text)
    page1.add_field(name=ability_battle_detail[8].text + " 💢", value=ability_battle_detail[9].text)
    page1.add_field(name=ability_battle_detail[10].text + " Ⓜ️", value=ability_battle_detail[11].text)
    page1.set_footer(text="⚠️과도한 게임이용은 건강에 좋지 않습니다.")

    page2 = discord.Embed(title=f"{nickname}",
                          url="https://lostark.game.onstove.com/Profile/Character/" + nickname,
                          colour=0xFFB2F5)
    page2.set_thumbnail(url=logo_class)
    page2.set_author(name=nickname + " 님의 캐릭터 정보")
    page2.add_field(name="서버", value=server, inline=True)
    page2.add_field(name="직업", value=game_class, inline=True)
    page2.add_field(name="길드", value=guild)
    page2.add_field(name="장착 아이템 레벨", value=equip_item_level, inline=False)
    page2.add_field(name="각인 효과", value="====================", inline=False)
    for x in engraving_effect:
        page2.add_field(name="💎  " + x.strip(), value="➖➖➖➖➖➖➖➖➖➖➖", inline=False)
    page2.set_footer(text="⚠️과도한 게임이용은 건강에 좋지 않습니다.")

    pages = [page1, page2]

    message = await ctx.send(embed=page1)

    # 임베드 정상적으로 생성 및 설정완료 문구 출력
    print("User's Embed has been generated!")
    # 실행창 구분자
    print("-----------------------------------------------")

    await message.add_reaction('◀')
    await message.add_reaction('▶')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '◀':
            if i > 0:
                i -= 1
            else:
                i = 1
            await message.edit(embed=pages[i])
            print(i)
        if str(reaction) == '▶':
            if i < 1:
                i += 1
            else:
                i = 0
            await message.edit(embed=pages[i])
            print(i)

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)
            await message.remove_reaction(reaction, user)
        except IndexError as e:
            print(e)


@bot.command(aliases=["내정보"])
# 내 주캐릭터 정보
async def myinfo(ctx):
    # 내 캐릭터 정보 파싱
    nickname = ctx.author.display_name
    character_url = character_search_url + nickname
    req = requests.get(character_url)
    soup = BeautifulSoup(req.text, "html.parser")
    server = soup.find("span", class_="profile-character-info__server")["title"][1:]
    game_class = soup.find("img", class_="profile-character-info__img")["alt"]
    logo_class = soup.find("img", class_="profile-character-info__img")["src"]
    expedition_level = soup.find("div", class_="level-info__expedition").find_all("span")[1].text.strip()
    character_level = soup.find("div", class_="level-info__item").find_all("span")[1].text.strip()
    equip_item_level = soup.find("div", class_="level-info2__expedition").find_all("span")[1].text.strip()
    achievement_item_level = soup.find("div", class_="level-info2__item").find_all("span")[1].text.strip()
    guild = soup.find("div", class_="game-info__guild").find_all("span")[1].text.strip()
    attack_power = soup.find("div", class_="profile-ability-basic").find_all("span")[1].text.strip()
    max_life_force = soup.find("div", class_="profile-ability-basic").find_all("span")[3].text.strip()
    ability_battle = soup.find("div", class_="profile-ability-battle").find("h4").text
    ability_battle_detail = soup.find("div", class_="profile-ability-battle").find_all("span")
    engraving_effects = str(soup.find("div", class_="profile-ability-engrave").find_all("span"))
    engraving_effects = re.sub('<.+?>|[|]', '', engraving_effects, 0).strip()
    engraving_effect = engraving_effects[1:len(engraving_effects) - 1].split(",")

    # 임베드 생성 및 설정
    page1 = discord.Embed(title=f"{nickname}",
                          url="https://lostark.game.onstove.com/Profile/Character/" + nickname,
                          colour=0xFFB2F5)
    page1.set_thumbnail(url=logo_class)
    page1.set_author(name=nickname + " 님의 캐릭터 정보")
    page1.add_field(name="서버", value=server, inline=True)
    page1.add_field(name="직업", value=game_class)
    page1.add_field(name="길드", value=guild)
    page1.add_field(name="원정대 레벨", value=expedition_level, inline=True)
    page1.add_field(name="캐릭터 레벨", value=character_level)
    page1.add_field(name="장착 아이템 레벨", value=equip_item_level, inline=False)
    page1.add_field(name="달성 아이템 레벨", value=achievement_item_level, inline=False)
    page1.add_field(name=" ⚔️공격력", value=attack_power, inline=True)
    page1.add_field(name=" 💚최대 생명력", value=max_life_force)
    page1.add_field(name=ability_battle, value="====================", inline=False)
    page1.add_field(name=ability_battle_detail[0].text + " 💥", value=ability_battle_detail[1].text)
    page1.add_field(name=ability_battle_detail[2].text + " ✨", value=ability_battle_detail[3].text)
    page1.add_field(name=ability_battle_detail[4].text + " 💬", value=ability_battle_detail[5].text)
    page1.add_field(name=ability_battle_detail[6].text + " 💨", value=ability_battle_detail[7].text)
    page1.add_field(name=ability_battle_detail[8].text + " 💢", value=ability_battle_detail[9].text)
    page1.add_field(name=ability_battle_detail[10].text + " Ⓜ️", value=ability_battle_detail[11].text)
    page1.set_footer(text="⚠️과도한 게임이용은 건강에 좋지 않습니다.")

    page2 = discord.Embed(title=f"{nickname}",
                          url="https://lostark.game.onstove.com/Profile/Character/" + nickname,
                          colour=0xFFB2F5)
    page2.set_thumbnail(url=logo_class)
    page2.set_author(name=nickname + " 님의 캐릭터 정보")
    page2.add_field(name="서버", value=server, inline=True)
    page2.add_field(name="직업", value=game_class, inline=True)
    page2.add_field(name="길드", value=guild)
    page2.add_field(name="장착 아이템 레벨", value=equip_item_level, inline=False)
    page2.add_field(name="각인 효과", value="====================", inline=False)
    for x in engraving_effect:
        page2.add_field(name="💎  " + x.strip(), value="➖➖➖➖➖➖➖➖➖➖➖", inline=False)
    page2.set_footer(text="⚠️과도한 게임이용은 건강에 좋지 않습니다.")

    pages = [page1, page2]

    message = await ctx.send(embed=page1)
    # 임베드 정상적으로 생성 및 설정완료 문구 출력
    print("Myinfo Embed has been generated!")
    # 실행창 구분자
    print("-----------------------------------------------")

    await message.add_reaction('◀')
    await message.add_reaction('▶')

    def check(reaction, user):
        return user == ctx.author

    i = 0
    reaction = None

    while True:
        if str(reaction) == '◀':
            if i > 0:
                i -= 1
            else:
                i = 1
            await message.edit(embed=pages[i])
            print(i)
        if str(reaction) == '▶':
            if i < 1:
                i += 1
            else:
                i = 0
            await message.edit(embed=pages[i])
            print(i)

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)
            await message.remove_reaction(reaction, user)
        except IndexError as e:
            print(e)


@bot.command(aliases=["모험섬"])
async def advisland(ctx):
    driver.get(loawa_url)
    driver.implicitly_wait(5)
    assert "로아와 - 로스트아크 시즌2 정보 제공 사이트" in driver.title
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 페이지 Y: 300까지 스크롤 다운
    adventure_island = driver.find_element_by_xpath(
        "//div[@class='col-lg-6 col-md-8 col-xl-6 pl-0 pr-0']/div[@*][2]")
    adventure_island_png = adventure_island.screenshot_as_png
    with open("adventure_islands.png", "wb") as file:
        file.write(adventure_island_png)

    file = discord.File("./adventure_islands.png")
    await ctx.send(file=file)


@bot.command(aliases=["주요알람", "알람"])
async def majoralarm(ctx):
    driver.get(loawa_url)
    driver.implicitly_wait(5)
    assert "로아와 - 로스트아크 시즌2 정보 제공 사이트" in driver.title
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 페이지 Y: 530까지 스크롤 다운
    today_major_contents = driver.find_element_by_xpath(
        "//div[@class='col-lg-6 col-md-8 col-xl-6 pl-0 pr-0']/div[@*][3]")
    today_major_contents_png = today_major_contents.screenshot_as_png
    with open("today_major_contents.png", "wb") as file:
        file.write(today_major_contents_png)

    file = discord.File("./today_major_contents.png")
    await ctx.send(file=file)


@bot.command(aliases=["항해", "항해시간"])
async def voyage(ctx):
    driver.get(loawa_url)
    driver.implicitly_wait(5)
    assert "로아와 - 로스트아크 시즌2 정보 제공 사이트" in driver.title
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 페이지 Y: 530까지 스크롤 다운
    today_voyages = driver.find_element_by_xpath(
        "//div[@class='col-lg-6 col-md-8 col-xl-6 pl-0 pr-0']/div[@*][4]")
    today_voyages_png = today_voyages.screenshot_as_png
    with open("today_voyages.png", "wb") as file:
        file.write(today_voyages_png)

    file = discord.File("./today_voyages.png")
    await ctx.send(file=file)


@bot.command(aliases=["보스"])
async def boss(ctx):
    driver.get(loawa_url)
    driver.implicitly_wait(5)
    assert "로아와 - 로스트아크 시즌2 정보 제공 사이트" in driver.title
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 페이지 Y: 1500까지 스크롤 다운
    fieldboss_schedule = driver.find_element_by_xpath(
        "//div[@class='col-lg-6 col-md-8 col-xl-6 pl-0 pr-0']/div[@*][5]")
    fieldboss_schedule_png = fieldboss_schedule.screenshot_as_png
    with open("fieldboss_schedule.png", "wb") as file:
        file.write(fieldboss_schedule_png)

    file = discord.File("./fieldboss_schedule.png")
    await ctx.send(file=file)


@bot.command(aliases=["캘린더섬"])
async def calendarisland(ctx):
    driver.get(loawa_url)
    driver.implicitly_wait(5)
    assert "로아와 - 로스트아크 시즌2 정보 제공 사이트" in driver.title
    driver.execute_script("window.scrollTo(0, 1900)")  # 페이지 Y: 1700까지 스크롤 다운
    calendar_islands = driver.find_element_by_xpath(
        "//div[@class='col-lg-6 col-md-8 col-xl-6 pl-0 pr-0']/div[@*][6]")
    calendar_islands_png = calendar_islands.screenshot_as_png
    with open("calendar_islands.png", "wb") as file:
        file.write(calendar_islands_png)

    file = discord.File("./calendar_islands.png")
    await ctx.send(file=file)


@bot.command(aliases=["도디언", "도전가디언"])
async def challdian(ctx):
    driver.get(loawa_url)
    driver.implicitly_wait(5)
    assert "로아와 - 로스트아크 시즌2 정보 제공 사이트" in driver.title
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 페이지 Y: 530까지 스크롤 다운
    challenge_guardians = driver.find_element_by_xpath(
        "//div[@class='col-lg-6 col-md-8 col-xl-6 pl-0 pr-0']/div[@*][7]")
    challenge_guardians_png = challenge_guardians.screenshot_as_png
    with open("challenge_guardians.png", "wb") as file:
        file.write(challenge_guardians_png)

    file = discord.File("./challenge_guardians.png")
    await ctx.send(file=file)


@bot.command(aliases=["도비스", "도전어비스"])
async def challbyss(ctx):
    driver.get(loawa_url)
    driver.implicitly_wait(5)
    assert "로아와 - 로스트아크 시즌2 정보 제공 사이트" in driver.title
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")  # 페이지 Y: 530까지 스크롤 다운
    challenge_abysses = driver.find_element_by_xpath(
        "//div[@class='col-lg-6 col-md-8 col-xl-6 pl-0 pr-0']/div[@*][8]")
    challenge_abysses_png = challenge_abysses.screenshot_as_png
    with open("challenge_abysses.png", "wb") as file:
        file.write(challenge_abysses_png)

    file = discord.File("./challenge_abysses.png")
    await ctx.send(file=file)


@bot.command(aliases=["거래소", "거래"])
async def exchange(ctx, keyword):
    # 거래소 정보 파싱
    base_url = "https://lostark.game.onstove.com/Market/"
    result_url = base_url + keyword
    driver.get(base_url)
    driver.implicitly_wait(5)
    input_keyword = driver.find_element_by_id('txtItemName').send_keys(keyword)
    search_item = driver.find_element_by_xpath(
        '/html/body/div[2]/div/main/div/div[2]/div[2]/form/fieldset/div/div[4]/button[1]').click()
    driver.implicitly_wait(5)
    trs = driver.find_elements_by_xpath('//tr')
    item_name = []
    average_daily_trading_price = []
    recent_transaction = []
    lowest_price = []
    data = []

    for i in range(1, len(trs)):
        item_name.append(
            str(driver.find_element_by_xpath('//*[@id="tbodyItemList"]/tr[' + str(i) + ']/td[1]/div/span[2]').text))
        average_daily_trading_price.append(
            str(driver.find_element_by_xpath('//*[@id="tbodyItemList"]/tr[' + str(i) + ']/td[2]/div/em').text))
        recent_transaction.append(
            str(driver.find_element_by_xpath('//*[@id="tbodyItemList"]/tr[' + str(i) + ']/td[3]/div/em').text))
        lowest_price.append(
            str(driver.find_element_by_xpath('//*[@id="tbodyItemList"]/tr[' + str(i) + ']/td[4]/div/em').text))
        driver.implicitly_wait(5)

    print(item_name)
    print(average_daily_trading_price)
    print(recent_transaction)
    print(lowest_price)

    for i in range(0, len(item_name)):
        data.append([item_name[i], average_daily_trading_price[i], recent_transaction[i], lowest_price[i]])
    print(data)

    for a, b, c, d in zip(item_name, average_daily_trading_price, recent_transaction, lowest_price):
        print('%10s | %s | %s | %s' % (fmt(a, 6), fmt(b, 6), fmt(c, 6), fmt(d, 6)))
        await ctx.send('%10s | %s | %s | %s' % (fmt(a, 6), fmt(b, 6), fmt(c, 6), fmt(d, 6)))

    # massage = await ctx.send('```' + msg + '```')
    #
    # await massage.add_reaction('⏮')
    # await massage.add_reaction('◀')
    # await massage.add_reaction('▶')
    # await massage.add_reaction('⏭')
    #
    # def check(reaction, user):
    #     return user == ctx.author
    #
    # i = 0
    # reaction = None
    #
    # while True:
    #     if str(reaction) == '⏮':
    #         i = 0
    #         await message.edit(embed=pages[i])
    #     elif str(reaction) == '◀':
    #         if i > 0:
    #             i -= 1
    #             await message.edit(embed=pages[i])
    #     elif str(reaction) == '▶':
    #         if i < 2:
    #             i += 1
    #             await message.edit(embed=pages[i])
    #     elif str(reaction) == '⏭':
    #         i = 2
    #         await message.edit(embed=pages[i])
    #
    #     try:
    #         reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)
    #         await message.remove_reaction(reaction, user)
    #     except IndexError as e:
    #         print(e)


# @bot.command()
# async def auction(ctx):
#     # 경매장 정보 파싱
#     args = str(ctx.message.content).split()
#     keyword = args[1:]
#     url = "https://lostark.game.onstove.com/Auction/" + keyword
#     req = requests.get(url)


bot.run(process.env.TOKEN)
