async def send_message(message, message_to_send):
    try:
        await message.channel.send(message_to_send)
        print(f"\tbot: {message_to_send} ({message.channel} in {message.guild})")
    except Exception as e:
        print(e)

async def f_say_hi(client, message, user_message):
    if user_message.lower() != "hi": return
    # await send_message(message, f"Hello there {message.author.mention}!")
    await send_message(message, f"Hello there {message.author.nick}!")