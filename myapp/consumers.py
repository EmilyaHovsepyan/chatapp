import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import base64
import uuid
from django.core.files.base import ContentFile

class ChatPage(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.groupid = self.scope['url_route']['kwargs']['groupid']

        print('GROUP ID HERE ')
        print(self.groupid)
        self.username = self.scope['user'].username
        self.group_room = 'room_' + self.groupid
        
        print(self.groupid)
        self.groupname = f"group_{self.username}"
        await self.channel_layer.group_add(self.group_room, self.channel_name)
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        message = await self.oldmssgget(self.groupid)
        print(message)
        await self.send(json.dumps({'oldmessage':message}))
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'text' in data:
            id = data['id']
            print('jiji')
            user = await self.findmembers(id)
            print(user)
            print('text sent')
            for i in user:
                name = f"group_{i}"
                print(name)
                await self.channel_layer.group_send(name, {
                    'type':'notification',
                    'data':data
                })

            print('text sent')
            await self.channel_layer.group_send(self.group_room, {
                'type':'sendnewmssg',
                'data':data
            })

        elif 'image' in data:
            img = data['image']
            res, b64 = img.split(';base64,')
            ext = res.split('/')[-1]
            print(res)
            print(ext)
            unique_name = f'image_{uuid.uuid4()}.{ext}'
            file = ContentFile(base64.b64decode(b64), name=unique_name)
            url = await self.savenewchatimages(self.groupid, file)
            await self.channel_layer.group_send(self.group_room, {
                'type': 'sendnewphoto',
                'url':url
            })

        elif 'txt' in data:
            txt = data['txt']
            print(txt)
            # result = await self.getallusernames(txt)
            # print(result)

        elif 'userprofile' in data:
            username = data['userprofile']
            name, bio, url= await self.getuserinfo(username)
            await self.send(json.dumps({'profileuser': {
                'username':username,
                'name':name,
                'bio': bio,
                'url':url
            }}))

        elif 'typinguser' in data:
            user = data['typinguser']
            await self.channel_layer.group_send(self.group_room, {
                'type':'typinguser',
                'user':user
            })

        elif 'notypinguser' in data:
            user = data['notypinguser']
            await self.channel_layer.group_send(self.group_room, {
                'type':'notypinguser',
                'user':user
            })

        elif 'newgroupname' in data:
            id = data['id']
            print(id)
            members = await self.findmembers(id)
            for i in members:
                room = f'group_{i}'
                await self.channel_layer.group_send(room, {
                    'type':'newgroupname',
                    'groupname':data['newgroupname']
                })

        elif 'background' in data:
            background = data['background']
            id = self.groupid
            members = await self.findmembers(id)
            for i in members:
                name = f'group_{i}'
                await self.channel_layer.group_send(name, {
                    'type':'backgroundchange',
                    'background':background,
                    'id': data['id']
                })
        elif 'addmember' in data:
            print('kiss on ur cheek')
            id = data['id']
            userinfo = await self.allusersinfo()
            list = await self.findmembers(id)
            userlist = []
            for i in list:
                userlist.append(str(i))
            await self.send(json.dumps({'addmembersearch':userinfo, 'userlist':userlist}))

        elif 'clickedmembers' in data:
            clickedmembers = data['clickedmembers']
        
            members, groupnamee, bg, groupimg, id = await self.addnewmembers(clickedmembers)
            for i in clickedmembers:
                groupname = f"group_{i}"

                print(groupname)
                await self.channel_layer.group_send(groupname, {
                    'type':'addnewmemberss',
                    'groupname':groupnamee,
                    'bg':bg,
                    'groupimg':groupimg,
                    'id': id,
                })


    async def addnewmemberss(self, event):
        groupname = event['groupname']
        bg = event['bg']
        groupimg = event['groupimg']
        id = event['id']
        print('9999')
        print(groupname)

        print('lolypop')
    
        print('hasar?')
        print("^^^^^^^^^^^^^^^^^^UWU 2^^^^^^^^^^^^^^^^")
        print(bg)
        print('999999999999')
        print(groupimg)
        await self.send(json.dumps({'addnewmember':True, 'groupnam':groupname, 'id':id, 'bg':bg, 'groupimg':groupimg}))

    async def backgroundchange(self, event):
        bg = event['background']
        id = event['id']
        print(bg)
        await self.savebackground(bg, id)
        await self.send(json.dumps({'background':bg, 'id': id})) #heto en myus classn el

    async def notification(self, event):
        print('we are in notifications')
        print('the original sender is')
        sender = event['data']['sender']
        id = event['data']['id']
        text = event['data']['text']
        groupname = event['data']['groupname']
        print(event['data'])
        if sender != self.username and id != self.groupid:
            await self.send(json.dumps({'notif':{
                'text':text,
                'sender':sender,
                'groupname':groupname
            }}))
        else:
            print('no')

    async def newgroupname(self, event):
        groupname = event['groupname']
        print('groupname here')
        await self.send(json.dumps({'newgroupname':groupname}))
        
    async def notypinguser(self, event):
        typinguser = event['user']
        await self.send(json.dumps({'notypinguser':typinguser}))

    async def typinguser(self, event):
        typinguser = event['user']
        await self.send(json.dumps({'typinguser':typinguser}))
        
    async def sendnewmssg(self, event):     #new messages written by user
        data = event['data']
        print("messagesentfromusernayiiiiii ems")
        print(data)
        await self.send(json.dumps({'message':data['text'], 'sender':data['sender'], 'photourl':data['profileurl']}))
        # await self.savenewmessage(self.groupid, data['text'])
    
    async def sendnewphoto(self, event):
        url = event['url']
        await self.send(json.dumps({'url':url}))

    async def experiment(self, event):
        groupname = event['groupname']
        id = event['id']
        await self.send(json.dumps({'groupsent':True, 'groupname':groupname, 'id': id}))
        

    @database_sync_to_async
    def addnewmembers(self, clickedmembers):
        from .models import groupinfo
        from django.contrib.auth.models import User
        print('kukareku')
        members = []
        group = groupinfo.objects.get(id = self.groupid)
        print(group.groupname)
        for i in clickedmembers:
            user = User.objects.get(username = i)
            group.members.add(user)
        
        res = group.members.all()
        groupname = group.groupname
        bg = group.bgname
        id = group.id
        groupimg = group.groupimg.url if group.groupimg else 'nogroupimg'

        for j in res:
            members.append(j.username)  #memberneri anunnery 
        
        return members, groupname, bg, groupimg, id 
    
    @database_sync_to_async
    def allusersinfo(self):
        from .models import userinfo
        users = userinfo.objects.all()
        resultinfo = []
        for user in users:
            resultinfo.append({
                'photo': user.photo.url if user.photo else 'nophoto',
                'username': user.username.username
            })
        return resultinfo
    
    @database_sync_to_async 
    def savebackground(self, bg, id):
        from .models import groupinfo
        info = groupinfo.objects.get(id = id)
        print(info)
        info.bgname = bg
        info.save()
        print('the new background in model')
        print(info.bgname)
            
    @database_sync_to_async
    def findmembers(self, id):
        from .models import groupinfo
        user = []
        res = groupinfo.objects.get(id = id)
        user = list(res.members.all())
        return user

    @database_sync_to_async
    def getuserinfo(self, username):
        from .models import userinfo
        print('getuser info reached')
        res = userinfo.objects.get(username__username = username)
        return res.name, res.bio, res.photo.url
    
    @database_sync_to_async
    def oldmssgget(self, groupid): #fetching old mssges for db
        from .models import groupinfo, messages
        res = groupinfo.objects.get(id=groupid)
        print('old messages below')
        print(res)
        # print(self.scope)
        mess = messages.objects.filter(groupname=res.groupname)
        message = []
        for i in mess:
            if i.image:
                message.append({'message':i.message,'url':i.image.url, 'sender':i.sender.username})
            else:
                 message.append({'message':i.message,'url':None, 'sender':i.sender.username})

        print(message)
        return message
    
    @database_sync_to_async
    def savenewmessage(self, groupid, message):
        from .models import groupinfo, messages
        from django.contrib.auth.models import User
        res = groupinfo.objects.get(id = groupid)
        user = User.objects.get(username = self.username)
        messages.objects.create(groupname=res.groupname, message=message, sender=user)

    @database_sync_to_async
    def savenewchatimages(self, groupid, file):
        from .models import groupinfo, messages
        from django.contrib.auth.models import User

        res = groupinfo.objects.get(id = groupid)
        user = User.objects.get(username = self.username)
        mess = messages.objects.create(groupname=res.groupname, sender=user, image=file)
        return mess.image.url

    @database_sync_to_async
    def getallusernames(self, txt):
        from .models import userinfo

        res = userinfo.objects.all().values_list('username', flat=True)
        print(res)
        result = []
        for item in res:
            lower = item.lower()
            if lower.startswith(txt.lower):
                result.append(item)
        print(result)
        return result


class search(AsyncWebsocketConsumer):

    async def connect(self):
        print('hehehe')
        self.username = self.scope['user'].username
        self.groupname = f"group_{self.username}"
        await self.channel_layer.group_add(self.groupname, self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'txt' in data:
            txt = data['txt']
            result = await self.getallusernames(txt)
            await self.send(json.dumps({'userlist':result, 'input':txt}))
        elif 'picked' in data:
            print('here1')
            picked = data['picked']

            picked.append(self.username)
            username = data['username']
            groupname, id = await self.addnewgroup(picked, username)
            for i in picked:
                group_name = f"group_{i}"
                print(group_name)
                await self.channel_layer.group_send(group_name, {
                    'type' : 'experiment',
                    'groupname':groupname,
                    'id':id
                })

    async def newgroupname(self, event):
        name = event['groupname']
        await self.send(json.dumps({'newgroupname':name}))  

    async def experiment(self, event):
        groupname = event['groupname']
        id = event['id']
        print('i am here mom')
        await self.send(json.dumps({'groupsent':True, 'groupname':groupname, 'id': id}))
        
    @database_sync_to_async
    def getallusernames(self, txt):
        from .models import userinfo
        start = []
        contain = []
        # if txt == '':
        #     return ''
        # else:
        print(txt)
        users = userinfo.objects.all().values_list('username__username', flat=True)
        for item in users:
            if item.startswith(txt):
                start.append(item)
                print('start is here')
                print(start)
            elif txt in item:
                contain.append(item)
        
        result = start + contain
        print('the result is hereeeeee')
        print(result)
        return result
    
    @database_sync_to_async
    def addnewgroup(self, picked, username):
        from .models import groupinfo
        from django.contrib.auth.models import User
        print('picked printed here')
        print(picked)
        print(username)
        res = groupinfo.objects.create(groupname = 'pipi')
        for i in picked:
            user = User.objects.get(username = i)
            res.members.add(user)

        print (res.id)
        print(res.groupname) 
        return res.groupname, res.id