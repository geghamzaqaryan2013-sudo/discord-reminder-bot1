import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks


# =========================
# ԿԱՐԳԱՎՈՐՈՒՄՆԵՐ
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

# Discord channel ID
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ՄՌԿ բաժնի role ID
MRK_ROLE_ID = int(os.getenv("MRK_ROLE_ID"))

# Հայաստանի ժամային գոտի
ARMENIA_TZ = ZoneInfo("Asia/Yerevan")


# =========================
# BOT
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# Որպեսզի նույն օրը նույն հաղորդագրությունը
# մի քանի անգամ չուղարկվի
sent_messages = set()


@bot.event
async def on_ready():
    print(f"Bot-ը միացված է՝ {bot.user}")

    if not reminder_loop.is_running():
        reminder_loop.start()


# =========================
# ՀԻՇԵՑՈՒՄՆԵՐ
# =========================

@tasks.loop(seconds=20)
async def reminder_loop():

    now = datetime.now(ARMENIA_TZ)

    # Միայն ուրբաթ
    # Monday = 0 ... Friday = 4
    if now.weekday() != 4:
        return

    # YYYY-MM-DD + ժամ
    reminder_key = f"{now.date()}-{now.hour}:{now.minute}"

    # ---------- 14:00 ----------

    if now.hour == 14 and now.minute == 0:

        if reminder_key not in sent_messages:

            channel = bot.get_channel(CHANNEL_ID)

            if channel:
                message = (
                    "Սիրելի թիմակիցներ, մեր ուժը մեր միասնականության մեջ է։ "
                    "Հիշեք վաղը 20:30-21:30, մեր կարևոր հանդիպումն է։ "
                    "Սպասում ենք Ձեզ, որպեսզի միասին կիսվենք գաղափարներով, "
                    "ոգեշնչվենք միմյանցից ու քայլ առ քայլ մոտենանք մեր մեծ նպատակներին։"
                )

                await channel.send(message)

            sent_messages.add(reminder_key)


    # ---------- 19:30 ----------

    elif now.hour == 19 and now.minute == 30:

        if reminder_key not in sent_messages:

            channel = bot.get_channel(CHANNEL_ID)

            if channel:
                role = channel.guild.get_role(MRK_ROLE_ID)

                mention = role.mention if role else f"<@&{MRK_ROLE_ID}>"

                message = (
                    "Սիրելի թիմակիցներ, մեր ուժը մեր միասնականության մեջ է։ "
                    "Հիշեք 1 ժամից մեր կարևոր հանդիպումն է։ "
                    "Սպասում ենք Ձեզ, որպեսզի միասին կիսվենք գաղափարներով, "
                    "ոգեշնչվենք միմյանցից ու քայլ առ քայլ մոտենանք մեր մեծ նպատակներին։\n\n"
                    f"{mention}"
                )

                await channel.send(
                    message,
                    allowed_mentions=discord.AllowedMentions(roles=True)
                )

            sent_messages.add(reminder_key)


    # ---------- 20:25 ----------

    elif now.hour == 20 and now.minute == 25:

        if reminder_key not in sent_messages:

            channel = bot.get_channel(CHANNEL_ID)

            if channel:
                role = channel.guild.get_role(MRK_ROLE_ID)

                mention = role.mention if role else f"<@&{MRK_ROLE_ID}>"

                message = (
                    f"{mention} ջան, կարող եք միանալ"
                )

                await channel.send(
                    message,
                    allowed_mentions=discord.AllowedMentions(roles=True)
                )

            sent_messages.add(reminder_key)


@reminder_loop.before_loop
async def before_reminder_loop():
    await bot.wait_until_ready()


# =========================
# START
# =========================

if not TOKEN:
    raise ValueError("DISCORD_TOKEN-ը նշված չէ։")

bot.run(TOKEN)
