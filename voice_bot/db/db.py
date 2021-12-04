from peewee import *
from assets.loader import load_cfg
from aiogram.types import InlineQueryResultArticle,InlineQueryResultVoice,InputTextMessageContent


db = SqliteDatabase('db/users.sqlite')

class Users(Model):
    id = PrimaryKeyField()
    stick = IntegerField(null=True)
    banned = BooleanField(default=False)

    class Meta:
        database = db

class Stickers(Model):
    voice_hash = TextField()
    creator = IntegerField()
    tags = TextField()
    name = TextField()
    used = IntegerField(default=0)
    active = BooleanField(default=False)

    class Meta:
        database = db

class Admins(Model):
    id = PrimaryKeyField()
    promot = BooleanField(default=True)

    class Meta:
        database = db


async def error_hundler(message,bot,key=None):
    if key:
        user_channel_status = await bot.get_chat_member(chat_id=load_cfg()['chat'], user_id=key)
    else:
        user_channel_status = await bot.get_chat_member(chat_id=load_cfg()['chat'], user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        return {"status": True}
    else:
        return {'status': False}

with db:
    db.create_tables([Users,Stickers,Admins])


def creat_User(_id):
    with db:
        if not Users.select().where(Users.id == _id).exists():
            Users.create(id=_id)

def get_stc(_id):
    return Stickers.get(Stickers.id ==_id)

def promote(_id):
    with db:
        if not Admins.select().where(Admins.id==_id).exists():
            Admins.create(id=_id)
            return True
        else:
            accep = not Admins.get(Admins.id==_id).promot
            Admins.update(promot=accep).where(Admins.id==_id).execute()
            return accep

def get_adms(_id):
    if Admins.select().where(Admins.id==_id).exists():
        g =  Admins.get(Admins.id==_id).promot
        print(g)
        return g
    else:
        return False

def get_me_sticker(_id):
    return Stickers.select(Stickers.name,Stickers.id).where(Stickers.creator == _id,Stickers.active==True)

def saves_st(stick_id):
    Stickers.update(active=True).where(Stickers.id == stick_id).execute()

def del_st(stick_id):
    Stickers.delete().where(Stickers.id == stick_id).execute()

def check_ban(_id):
    return Users.get(Users.id==_id).banned

async def sendd(mess):
    _id = Users.select(Users.id)
    num = 0 
    for on in _id:
        try:
            await mess.copy_to(on)
            num+=1
        except:
            pass
    return num

def get_stck():
    tex=''
    for i in Stickers.select(Stickers.active==True,Stickers.name,Stickers.id):
        tex+=f'/{i.id} - {i.name}\n'
    return tex[:30]

def get_stats():
    return len(Users.select(Users.id)),len(Stickers.select(Stickers.active==True))

def ban(_id):
    Users.update(banned=True).where(Users.id == _id).execute()

def unban(_id):
    Users.update(banned=False).where(Users.id == _id).execute()

def save_stick(voice_hash,creator,name,tags):
    with db:
        Stickers.create(voice_hash=voice_hash,creator=creator,tags=tags,name=name)
        return Stickers.get(Stickers.voice_hash==voice_hash).id

def get_stick():
    return Stickers.select(Stickers.id,Stickers.name,Stickers.tags,Stickers.voice_hash).where(Stickers.active==True)
     
def new_stc_use(_id):
    Stickers.update(used=Stickers.get(Stickers.voice_hash==_id).used + 1).where(Stickers.voice_hash==_id).execute()

def get_hash_by_id(_id):
    return Stickers.get_by_id(_id).voice_hash

async def find(text,message,bot):
    data = []
    stata = await error_hundler(message,bot,key=message)
    if stata['status'] == False:
        data.append(InlineQueryResultArticle(
                title='Для работы с ботом необходима подписка',
                id=1000000,
                url=load_cfg()['link'],
                input_message_content=InputTextMessageContent(f"<a href='{load_cfg()['link']}'>Получить доступ</a>",parse_mode='html')
                )
            )
        return data
    if text!= '':
        for i in get_stick():
            if text in i.tags.split() or text in i.name:
                data.append(InlineQueryResultVoice(
                    title=i.name,
                    id=i.id,
                    voice_url=i.voice_hash
                    )
                )
    else:
        for i in get_stick():
            data.append(InlineQueryResultVoice(
                title=i.name,
                id=i.id,
                voice_url=i.voice_hash
                )
            )
    if data == []:
        data.append(InlineQueryResultArticle(
                title='Нечего не найден',
                id=1000000,
                input_message_content=InputTextMessageContent('Нечего не найдено')
                )
            )
    return data[:25]

