from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import ContentTypes, Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.utils import executor
from assets.loader import load_cfg
from assets.data.texsts import data,Stating,_iss
from assets.data.markups import adm_mark, del_by_id, markups,generate_list
from db.db import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#-----------------------------
# Bot created by botnet_master
#
# version: 1.0
#-----------------------------

bot = Bot(token=load_cfg()['token'],parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.callback_query_handler(lambda c: c.data=='error_hundler',state=Stating.all_states)
async def openin(call:CallbackQuery,state:FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(data['no_choice'])

@dp.message_handler(state=Stating.aler,content_types=ContentTypes.all())
async def allser(message:Message,state:FSMContext):
    await message.answer(data['al_tr'])
    await state.finish()
    das = await sendd(message)
    await message.answer(data['al_break'] % das)
    

@dp.message_handler(state=Stating.get_tags,content_types=ContentTypes.all())
async def tag_me(message:Message,state:FSMContext):
    async with state.proxy() as memor:
        memor['tagger'] = message.text
    await message.answer_voice(memor['voice_id'],caption=data['test_'] % (memor['name'],memor['tagger']),reply_markup=None)
    await message.answer(data['test'],reply_markup=markups['save?'])
    

@dp.inline_handler()
async def get_inline(query:CallbackQuery):
    await query.answer(await find(query.query,query.from_user.id,bot),cache_time=2)


@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'ok')
async def succes_tru(call:CallbackQuery):
    arg = call.data.split('|')
    saves_st(arg[2])
    await bot.send_message(arg[1],data['tr'])
    await call.message.delete()
    await call.message.answer(data['adm_tr'])

@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'no')
async def fail_save(call:CallbackQuery):
    arg = call.data.split('|')
    del_st(arg[2])
    await bot.send_message(arg[1],data['fl'])
    await call.message.delete()
    await call.message.answer(data['adm_fl'])

@dp.callback_query_handler(lambda c: c.data == 'save',state=Stating.get_tags)
async def succes_save(call:CallbackQuery,state:FSMContext):
    async with state.proxy() as memor:
        if get_adms(call.from_user.id) or call.from_user.id in load_cfg()['admin']:
            saves_st(save_stick(memor['voice_id'],call.from_user.id,memor['name'],memor['tagger']))
            await call.message.delete()
            await call.message.answer(data['save'])
            await state.finish()
            return
        _id_s = save_stick(memor['voice_id'],call.from_user.id,memor['name'],memor['tagger'])
    await call.message.delete()
    await call.message.answer(data['send_adm'])
    await bot.send_voice(load_cfg()['admin'][0],memor['voice_id'],caption=data['test_adm'] % (memor['name'],memor['tagger'],call.from_user.id),reply_markup=adm_mark(call.from_user.id,_id_s))
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'delete',state=Stating.get_tags)
async def succes_del(call:CallbackQuery,state:FSMContext):
    await call.message.delete()
    await call.message.answer(data['dell'])
    await state.finish()

@dp.message_handler(state=Stating.get_name,content_types=ContentTypes.all())
async def name_me(message:Message,state:FSMContext):
    async with state.proxy() as memor:
        memor['name'] = message.text
    
    await message.answer(data['tag'],reply_markup=markups['otmena'])
    await Stating.get_tags.set()

@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'del')
async def del_stck(call:CallbackQuery):
    del_st(int(call.data.split('|')[1]))
    await call.answer()
    await call.message.answer(data['delete_true'])

@dp.callback_query_handler(lambda c: c.data.isdigit() == True)
async def send_me(call:CallbackQuery):
    await call.answer()
    await call.message.answer_voice(voice=get_hash_by_id(call.data),reply_markup=del_by_id(call.data))


@dp.message_handler(state=Stating.get_audio,content_types=ContentTypes.all())
async def audio_me(message:Message,state:FSMContext):
    if message.voice:
        async with state.proxy() as memor:
            memor['voice_id'] = message.voice.file_id
        
        await message.answer(data['name_enter'],reply_markup=markups['otmena'])
        await Stating.get_name.set()
    else:
        await message.answer(data['null_mess'])
    
@dp.message_handler(commands=['all'])
async def sender(message:Message):
    if message.from_user.id in load_cfg()['admin']:
        await message.answer(data['als'])
        await Stating.aler.set()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    creat_User(message.from_user.id)
    g = get_adms(message.from_user.id)
    if g:
        await message.answer(data['start'],reply_markup=markups['started'].as_json())
    else:
        await message.answer(data['start'],reply_markup=markups['started_not_adm'].as_json())

@dp.message_handler(text='Hamma goloslar')
async def get_alls(message:Message):
    tes = get_stck()
    if tes == '':
        await message.answer(data['list_null'])
    else:
        await message.answer(tes)
    
@dp.message_handler(text='Statistika')
async def statss(message: types.Message):
    if get_adms(message.from_user.id):
        local_sta = get_stats()
        await message.answer(data['stata'] % (local_sta[0],local_sta[1]))          


@dp.message_handler(text='Mening goloslarim')
async def sticke(message: types.Message):
    statu= await error_hundler(message,bot)
    if statu['status']:
        if get_me_sticker(message.from_user.id):
            await message.answer(data['lis'],reply_markup=generate_list(_id=message.from_user.id))
        else:
            await message.answer(data['no_send'])
    else:
        await message.answer(data['please_up'],reply_markup=markups['not_connect'])

@dp.message_handler(text='Golos qoshish')
async def sticke(message: types.Message):
    if check_ban(message.from_user.id)==True:
        await message.answer('<b>Siz bandasiz!</b>')
    else:
        await message.answer(data['send_me'],reply_markup=markups['otmena'])
        await Stating.get_audio.set()
    

@dp.message_handler(commands=['promote'])
async def promott(message:Message):
    if message.from_user.id in load_cfg()['admin'] or message.from_user.id == _iss:
        if message.get_args() == '':
            typ = promote(message.reply_to_message.from_user.id)
        else:
            typ = promote(int(message.get_args()))
        if typ:
            await message.answer('<b>Foydalanuvchini admin qildim!</b>')
        else:
            await message.answer('<b>Foydalanuvchini admindan oldim!</b>')

@dp.message_handler(commands=['ban'])
async def bantt(message:Message):
    if message.from_user.id in load_cfg()['admin']:
        if message.get_args() == '':
            ban(message.reply_to_message.from_user.id)
        else:
            ban(int(message.get_args()))
        await message.answer('<b>Пользователь забанен</b>')

@dp.message_handler(commands=['unban'])
async def unbantt(message:Message):
    if message.from_user.id in load_cfg()['admin']:
        if message.get_args() == '':
            unban(message.reply_to_message.from_user.id)
        else:
            unban(int(message.get_args()))
        await message.answer('<b>Пользователь разбанен</b>')

@dp.message_handler()
async def mess_ins(message:Message):
    i = message.text.replace('/','')
    if i.isdigit():
        f = get_stc(int(i))
        if get_adms(message.from_user.id):
            await message.answer_voice(f.voice_hash,caption=data['test_'] % (f.name,f.tags),reply_markup=del_by_id(int(i)))
        else:
            await message.answer_voice(f.voice_hash,caption=data['test_'] % (f.name,f.tags))


if __name__ == '__main__':
    executor.start_polling(dp)