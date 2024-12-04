from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import API_TOKEN, OPENAI_API_KEY, ADMIN_LIST, CHANNEL_ID
from chat_gpt_manager import ChatGPTClient
from json_db_tool import json_tool
json_tool = json_tool()
import asyncio

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

examples_db = json_tool.load_db("examples.json")
example_list = []
for example in examples_db["examples"]:
    example_list.append(example)

posted_db = json_tool.load_db("posted.json")
posted_list = []
for post in posted_db["posted"]:
    posted_list.append(post)

runned = False
ai_role = "system"
ai_prompt = f'Ты редактор платформы на которой публикуются мотивационные сообщения, связанные с жизненными ситуациями. Составь короткое на не больше 20 слов продолжение к фразе "Пора бы...", связанное с жизненной рутиной, имеющее тайный смысл. При публикации убери лишние символы и часть "Пора бы...", с маленькой буквы. \nНиже привел опирающиеся примеры, а также уже опубликованные посты (они в разных массивах). Старайся не повторяться с уже отправленными.\n\n{example_list}\n\n{posted_list}'

@dp.message_handler(content_types=['text'])
async def send_welcome(message: types.Message):
    global runned
    if str(message.from_user.id) in ADMIN_LIST:
        if message.text == "/post":
            await message.reply("Отправлен новый пост")
            print("Отправлен новый пост")
            await bot.send_message(CHANNEL_ID, text=chat_gpt_request(role=ai_role, prompt=ai_prompt))
            
        if message.text == "/start":
            if not runned:
                await message.reply("Запущено")
                print("Запущено")
                runned = True
                
                while runned:
                    await bot.send_message(CHANNEL_ID, text=chat_gpt_request(role=ai_role, prompt=ai_prompt))
                    await asyncio.sleep(3600)
            else: 
                await message.reply("Уже запущено")
        
        if message.text == "/stop":
            if runned:
                await message.reply("Остановлено")
                print("Остановлено")
                runned = False
            else:
                await message.reply("Уже остановлено")

        

def chat_gpt_request(role, prompt):
    client = ChatGPTClient(OPENAI_API_KEY)
    response = client.get_response(prompt, role)
    posted_db["posted"].append(f'Пора бы {response}')
    posted_db["posted"] = posted_db["posted"][-30:]  # Оставляем только последние 30 записей
    json_tool.save_db("posted.json", posted_db)
    return response

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
