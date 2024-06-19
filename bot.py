import discord
from discord.ext import commands
from config import TOKEN

# Создаем объект intents для бота, чтобы бот мог получать сообщения
intents = discord.Intents.default()
intents.messages = True

# Создаем объект бота с префиксом '!' для команд
bot = commands.Bot(command_prefix='!', intents=intents)

# Словарь для хранения задач пользователей. Ключ - ID пользователя, значение - список задач
tasks = {}

# Событие, которое срабатывает при успешном запуске бота
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Команда для управления задачами
@bot.command()
async def task(ctx, action=None, *, content=None):
    # Получаем ID пользователя, вызвавшего команду
    user_id = ctx.author.id
    # Если у пользователя еще нет задач, создаем для него пустой список задач
    if user_id not in tasks:
        tasks[user_id] = []

    # Обработка команды для добавления задачи
    if action == 'add':
        task_id = len(tasks[user_id]) + 1  # Генерируем ID задачи
        tasks[user_id].append({'id': task_id, 'content': content})  # Добавляем задачу в список пользователя
        await ctx.send(f'Задача добавлена: {content} (ID: {task_id})')  # Отправляем подтверждение

    # Обработка команды для удаления задачи
    elif action == 'remove':
        if content and content.isdigit():  # Проверяем, что передан корректный ID задачи
            task_id = int(content)  # Преобразуем ID задачи в число
            task_list = tasks[user_id]  # Получаем список задач пользователя
            # Ищем задачу по ID
            task_to_remove = next((task for task in task_list if task['id'] == task_id), None)
            if task_to_remove:
                task_list.remove(task_to_remove)  # Удаляем задачу из списка
                await ctx.send(f'Задача с ID {task_id} удалена.')  # Отправляем подтверждение
            else:
                await ctx.send(f'Задача с ID {task_id} не найдена.')  # Сообщаем, если задача не найдена
        else:
            await ctx.send('Укажите правильный ID задачи для удаления.')  # Сообщаем об ошибке

    # Обработка команды для отображения списка задач
    elif action == 'list':
        task_list = tasks[user_id]  # Получаем список задач пользователя
        if task_list:
            # Формируем ответ с перечнем задач
            response = "Ваши текущие задачи:\n"
            response += "\n".join([f"ID: {task['id']}, Описание: {task['content']}" for task in task_list])
        else:
            response = "У вас нет текущих задач."  # Сообщаем, если задач нет
        await ctx.send(response)  # Отправляем список задач

    # Обработка неизвестной команды
    else:
        await ctx.send('Неизвестное действие. Пожалуйста, используйте add, remove или list.')

# Отдельная команда для отображения справочной информации
@bot.command()
async def info(ctx):
    response = (
        "Доступные команды:\n"
        "!task add [описание задачи] - добавляет новую задачу.\n"
        "!task remove [ID задачи] - удаляет задачу по указанному ID.\n"
        "!task list - показывает список текущих задач.\n"
        "!info - отображает эту справочную информацию."
    )
    await ctx.send(response)  # Отправляем справочную информацию

# Запуск бота с вашим токеном
bot.run(TOKEN)
