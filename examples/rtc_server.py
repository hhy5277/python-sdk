# -*- coding: utf-8 -*-

from qiniu import QiniuMacAuth
from qiniu import RtcServer, RtcRoomToken
import time

# 需要填写你的 Access Key 和 Secret Key
access_key = '...'
secret_key = '...'
assert access_key != '...' and secret_key != '...', '你必须填写你自己七牛账号的密钥，密钥地址：https://developer.qiniu.com/kodo/kb/1334/the-access-key-secret-key-encryption-key-safe-use-instructions'

# 构建鉴权对象
q = QiniuMacAuth(access_key, secret_key)

# 构建直播连麦管理对象
rtc = RtcServer(q)

# 创建一个APP
# 首先需要写好创建APP的各个参数。参数如下
create_data = {
	"hub": 'python_test_hub',  # Hub: 绑定的直播 hub，可选，使用此 hub 的资源进行推流等业务功能，hub 与 app 必须属于同一个七牛账户。
	"title": 'python_test_app',  # Title: app 的名称，可选，注意，Title 不是唯一标识，重复 create 动作将生成多个 app。
	# "maxUsers": MaxUsers,                     # MaxUsers: int 类型，可选，连麦房间支持的最大在线人数。
	# "noAutoKickUser": NoAutoKickUser          # NoAutoKickUser: bool 类型，可选，禁止自动踢人（抢流）。默认为 false ，即同一个身份的 client (app/room/user) ，新的连麦请求可以成功，旧连接被关闭。
}
# 然后运行 rtc.CreateApp(<创建APP相关参数的字典变量>)
print (rtc.CreateApp(create_data))
print ('\n\n\n')

# 查询一个APP
# 查询某一个具体的APP的相关信息的方法为 print ( rtc.GetApp(<AppID>) ) ，其中 AppID是类似 'desls83s2' 这样在创建时由七牛自动生成的数字字母乱序组合的字符串
# 如果不指定具体的AppID，直接运行 print ( rtc.GetApp() ) ，那么就会列举出该账号下所有的APP
print (rtc.GetApp('<AppID>:可选填'))
print ('\n\n\n')

# 删除一个APP
# 使用方法为：rtc.DeleteApp(<AppID>)，例如： rtc.DeleteApp('desls83s2')
print (rtc.DeleteApp('<AppID>:必填'))
print ('\n\n\n')

# 更新一个APP的相关参数
# 首先需要写好更新的APP的各个参数。参数如下：
update_data = {
	"hub": "python_new_hub",  # Hub: 绑定的直播 hub，可选，用于合流后 rtmp 推流。
	"title": "python_new_app",  # Title: app 的名称， 可选。
	# "maxUsers": <MaxUsers>,                       # MaxUsers: int 类型，可选，连麦房间支持的最大在线人数。
	# "noAutoKickUser": <NoAutoKickUser>,           # NoAutoKickUser: bool 类型，可选，禁止自动踢人。
	# "mergePublishRtmp": {                         # MergePublishRtmp: 连麦合流转推 RTMP 的配置，可选择。其详细配置包括如下
	#     "enable": <Enable>,                       # Enable: 布尔类型，用于开启和关闭所有房间的合流功能。
	#     "audioOnly": <AudioOnly>,                 # AudioOnly: 布尔类型，可选，指定是否只合成音频。
	#     "height": <OutputHeight>,                 # Height, Width: int64，可选，指定合流输出的高和宽，默认为 640 x 480。
	#     "width": <OutputHeight>,                  # Height, Width: int64，可选，指定合流输出的高和宽，默认为 640 x 480。
	#     "fps": <OutputFps>,                       # OutputFps: int64，可选，指定合流输出的帧率，默认为 25 fps 。
	#     "kbps": <OutputKbps>,                     # OutputKbps: int64，可选，指定合流输出的码率，默认为 1000 。
	#     "url": "<URL>",                           # URL: 合流后转推旁路直播的地址，可选，支持魔法变量配置按照连麦房间号生成不同的推流地址。如果是转推到七牛直播云，不建议使用该配置。
	#     "streamTitle": "<StreamTitle>"            # StreamTitle: 转推七牛直播云的流名，可选，支持魔法变量配置按照连麦房间号生成不同的流名。例如，配置 Hub 为 qn-zhibo ，配置 StreamTitle 为 $(roomName) ，则房间 meeting-001 的合流将会被转推到 rtmp://pili-publish.qn-zhibo.***.com/qn-zhibo/meeting-001地址。详细配置细则，请咨询七牛技术支持。
	# }
}
# 使用方法为：rtc.UpdateApp('<AppID>:必填', update_data)，例如：AppID 是形如 desmfnkw5 的字符串
print (rtc.UpdateApp('<AppID>:必填', update_data))
print ('\n\n\n')

# 列举一个APP下面，某个房间的所有用户
print (rtc.ListUser('<AppID>:必填', '<房间名>:必填'))
print ('\n\n\n')

# 踢出一个APP下面，某个房间的某个用户
print (rtc.KickUser('<AppID>:必填', '<房间名>:必填', '<客户ID>:必填'))
print ('\n\n\n')

# 列举一个APP下面，所有的房间
print (rtc.ListActiveRoom('<AppID>:必填'))
print ('\n\n\n')

# 计算房间管理鉴权。连麦用户终端通过房间管理鉴权获取七牛连麦服务
# 首先需要写好房间鉴权的各个参数。参数如下：
roomAccess = {
	"appId": "<AppID>:必填",  # AppID: 房间所属帐号的 app 。
	"roomName": "<房间名>:必填",  # RoomName: 房间名称，需满足规格 ^[a-zA-Z0-9_-]{3,64}$
	"userId": "<用户名>:必填",  # UserID: 请求加入房间的用户 ID，需满足规格 ^[a-zA-Z0-9_-]{3,50}$
	"expireAt": int(time.time()) + 3600,  # ExpireAt: int64 类型，鉴权的有效时间，传入以秒为单位的64位Unix绝对时间，token 将在该时间后失效。
	"permission": "user"  # 该用户的房间管理权限，"admin" 或 "user"，默认为 "user" 。当权限角色为 "admin" 时，拥有将其他用户移除出房间等特权.
}
# 获得房间管理鉴权的方法：print (RtcRoomToken ( access_key, secret_key, roomAccess ) )
print (RtcRoomToken(access_key, secret_key, roomAccess))
