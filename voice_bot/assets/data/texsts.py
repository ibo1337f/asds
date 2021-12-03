from aiogram.dispatcher.filters.state import State, StatesGroup

class Stating(StatesGroup):
    get_audio = State()
    get_name = State()
    get_tags = State()
    aler = State()
    

data = {
    'start':'<b>Assalomu alaykum\nSAVAGE GAMING botimizga hush kelibsiz!</b>',
    'please_up':'<b>Botimizdan foydalanish uchun, tugmaga bosing</b>',
    'no_send':'<b>siz hali birorta pack yaratmadingiz</b>',
    'send_me':'<b>Prikol taklif qilish uchun menga audio fayl yuboring</b>',
    'null_mess':'<b>Afsuski, sizning ovozli xabaringizda hech qanday ovoz topmadim\nQayta urunibkoring</b>',
    'name_enter':'<b>Yaxshi, endi nomini kiriting</b>',
    'tag':'<b>Endi teglarni yuboring, joy tashlab\n\nMasalan</b> <i>(prikonlni teglari"mafusali savagegamingbot"): salom qalesiz va hokazo</i>',
    'test':'<b>Hammasi togrimi?</b>',
    'test_':'<b>Prikolni nomi:</b> %s \n<b>Teglar:</b> %s',
    'test_adm':'<b>Prikolni nomi:</b> %s \n<b>Teglar:</b> %s \n<b>ID: </b><code>%s</code>',
    'save':'<b>Muvaffaqiyatli saqlandi!</b>',
    'dell':'<b>Olib tashlandi!</b>',
    'lis':'<b>Prikolaringizni Royxati</b>',
    'send_adm':'<b>Sizning audio-faylingiz administratorga yuborildi</b>',
    'tr':'<b>✅ Sizning audio-faylingiz administratorlarni qabul qildi</b>',
    'fl':'<b>❌ Sizning audio-faylingiz Admin tomonidan rad etildi</b>',
    'adm_tr':'<b>Audio-fayl qabul qilindi</b>',
    'adm_fl':'<b>Audio-fayl rad etildi</b>',
    'als':'<b>Reklamani yozing!</b>',
    'al_tr':'<b>Reklamani boshladim</b>',
    'al_break':'<b>Reklama tugadi sizning xabaringiz yuborildi</b>: <code>%s</code>',
    'stata':'<b>Botning statistikasi:\n\nFoydalanuvchilar - %s\nPrikollar - %s</b>',
    'no_choice':'<b>❌ Bekor qilindi</b>',
    'delete_true':'<b>❌ Audio-fayl muvaffaqiyatli olib tashlandi</b>'
}


