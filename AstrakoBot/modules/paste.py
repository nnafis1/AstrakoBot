
from AstrakoBot import dispatcher
from AstrakoBot.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async
import imp
from io import BytesIO
import privatebinapi

def paste(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    chat = update.effective_chat

    if message.reply_to_message:
        data = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.document:
            file_info = context.bot.get_file(
                message.reply_to_message.document.file_id)
            with BytesIO() as file:
                file_info.download(out=file)
                file.seek(0)
                data = file.read().decode()

    elif len(args) >= 1:
        data = " ".join(message.text.split()[1:])
    else:
        message.reply_text('What am I supposed to do with this?')
        return

    txt = ''
    context.bot.send_chat_action(chat.id, 'typing')
    pvt_bin_response = privatebinapi.send(
        PRIVATEBIN_INSTANCE, text=data, expiration='1week', formatting='syntaxhighlighting')
    if not pvt_bin_response['full_url']:
        txt = 'Failed to paste data'
    else:
        txt = '<b>Successfully uploaded to PrivateBin:</b> {0}\n<b>Your paste deleting token is:</b> <code>{1}</code>\n<b>Paste Deletion Time: 1 Week</b>'.format(
            pvt_bin_response["full_url"], pvt_bin_response["deletetoken"])

    message.reply_text(txt, disable_web_page_preview=True,
                       parse_mode=ParseMode.HTML)



  PASTE_HANDLER = DisableAbleCommandHandler("paste", paste, run_async=True)
dispatcher.add_handler(PASTE_HANDLER)

__command_list__ = ["paste"]
__handlers__ = [PASTE_HANDLER]




