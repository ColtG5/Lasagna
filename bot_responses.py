async def send_message(message, message_to_send):
    try:
        await message.channel.send(message_to_send)
        print(f"\tbot: {message_to_send} ({message.channel} in {message.guild})")
    except Exception as e:
        print(e)

async def f_say_hi(bot, message, user_message):
    if user_message.lower() != "hi": return
    # await send_message(message, f"Hello there {message.author.mention}!")
    await send_message(message, f"Hello there {message.author.nick}!")

async def f_new_reminder(bot, message, user_message):
    # print(user_message)
    # print(str(user_message).lower().startswith("new reminder"))
    if not str(user_message).lower().startswith("new reminder"): return

    user_message = str(user_message)[12:]
    # if not user_message

