from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image, ImageDraw, ImageFont
import os

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TEMP_IMAGE = "input.jpg"
font_path = "fonts/arial.ttf"

# Store uploaded image
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    await photo.get_file().download_to_drive(TEMP_IMAGE)
    await update.message.reply_text("Image received. Now send /editcount <number> <mode>\nExample: `/editcount 50 android`", parse_mode="Markdown")

# Edit image
async def editcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(TEMP_IMAGE):
        await update.message.reply_text("Please send a screenshot first.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("Usage: /editcount <number> <android|iphone>")
        return

    count = context.args[0]
    mode = context.args[1].lower()

    if not count.isdigit() or mode not in ["android", "iphone"]:
        await update.message.reply_text("Invalid format. Example: /editcount 45 iphone")
        return

    img = Image.open(TEMP_IMAGE)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 36)

    if mode == "android":
        position = (240, 470)
        text_color = "lightgray"
        bg_color = (30, 30, 30)
    else:
        position = (200, 450)
        text_color = "gray"
        bg_color = (240, 240, 240)

    draw.rectangle([position, (position[0]+240, position[1]+40)], fill=bg_color)
    draw.text(position, f"{count} anggota", font=font, fill=text_color)

    output_path = f"output_{mode}.jpg"
    img.save(output_path)
    await update.message.reply_photo(photo=open(output_path, "rb"))

# Bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_image))
app.add_handler(CommandHandler("editcount", editcount))

app.run_polling()
