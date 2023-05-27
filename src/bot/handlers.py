from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.bot.constants import commands, states
from src.bot.keyboards import get_categories_keyboard, get_subcategories_keyboard, MENU_KEYBOARD
from src.core.services.user import UserService


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_service = UserService()
    await user_service.register_user(
        telegram_id=update.effective_chat.id,
        username=update.effective_chat.username,
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Начнём",
                    callback_data=commands.GREETING,
                )
            ]
        ]
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! 👋 \n\n"
        'Я бот платформы интеллектуального волонтерства <a href="https://procharity.ru/">ProCharity</a>. '
        "Буду держать тебя в курсе новых задач и помогу "
        "оперативно связаться с командой поддержки.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    return states.GREETING


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create button menu."""
    keyboard = MENU_KEYBOARD
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выбери, что тебя интересует:", reply_markup=reply_markup)


async def categories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_service = UserService()
    categories = await user_service.get_user_categories(update.effective_user.id)
    context.user_data["selected_categories"] = {category: None for category in categories}
    context.user_data["parent_id"] = None
    await update.message.reply_text(
        "Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=await get_categories_keyboard(),
    )


async def subcategories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    parent_id = int(context.match.group(1))
    context.user_data["parent_id"] = parent_id

    await query.message.edit_text(
        "Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=await get_subcategories_keyboard(parent_id, context),
    )


async def select_subcategory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    subcategory_id = int(context.match.group(1))
    selected_categories = context.user_data.setdefault("selected_categories", {})

    if subcategory_id not in selected_categories:
        selected_categories[subcategory_id] = None
    else:
        del selected_categories[subcategory_id]

    parent_id = context.user_data["parent_id"]

    await query.message.edit_text(
        "Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=await get_subcategories_keyboard(parent_id, context),
    )


async def back_subcategory_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.message.edit_text(
        "Чтобы я знал, с какими задачами ты готов помогать, "
        "выбери свои профессиональные компетенции (можно выбрать "
        'несколько). После этого, нажми на пункт "Готово 👌"',
        reply_markup=await get_categories_keyboard(),
    )


async def confirm_categories_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Записывает выбранные категории в базу данных и
    отправляет пользователю отчет о выбранных категориях.
    """
    query = update.callback_query
    telegram_id = update.effective_user.id
    user_service = UserService()

    users_categories_ids = context.user_data.get("selected_categories", {}).keys()

    await user_service.set_categories_to_user(
        telegram_id=telegram_id,
        categories_ids=users_categories_ids,
    )

    categories = await user_service.get_user_categories(telegram_id)
    if not categories:
        await query.message.edit_text(text="Категории не выбраны.")
    else:
        await query.message.edit_text(
            text="Отлично! Теперь я буду присылать тебе уведомления о новых "
                 f"заданиях в категориях: *{', '.join(categories.values())}*.\n\n",
            parse_mode=ParseMode.MARKDOWN
        )
