使用tornado和jwt构建账号系统、实现权限控制


#环境需求

ubuntu 18.04  python3.6

#配置参数

配置 source/turing/config.py文件即可

#安装项目依赖模块

pip3 install -r requirements.txt

#开启web服务

python3  source/main.py

#测试web服务

浏览器输入

http://localhost:9050/

#日志

在/tmp目录下， turing_server.log"


管理员用户和密码:  admin     123456
用户角色分为：管理员、普通用户


#接口使用说明：
注意： 示例中的token为实时生成。实际使用时，需要替换成自己的token。

1、登录，获取token。所有用户权限。
$ curl -d "username=admin&password=123456" http://127.0.0.1:9050/auth/login
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTI4OTcxMzgzfQ.QEyKqNUs77toZTqeN9qMtOhSInFIp-Vhp75DXqZgNz0"}

$ curl -d "username=simba&password=123456" http://127.0.0.1:9050/auth/login
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNpbWJhIiwiZXhwIjoxNTI4OTczMjcwfQ.bR2bJheaHdejDIYR9WeVPFR2POWb7j3lEGpCudsidVw"}

此处获取的token，有效期是10分钟。后续各个接口需要传递此token。 在报文头部放置token，传递给后端程序验证权限。

2、刷新token。 所有用户权限。在token有效期内，可以使用现有的token换取新的token。否则，token过期之后，只能重新登录获取token。 另外：新token生成之后，现有的token失效。
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTI4OTcxMzgzfQ.QEyKqNUs77toZTqeN9qMtOhSInFIp-Vhp75DXqZgNz0"  http://127.0.0.1:9050/auth/refresh
{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTI4OTcxNjM3fQ.j3fFHEdNKQC058Ix4JlCi4_R9T7IFTjyBRx5_pg6zX0"}

3、创建用户。管理员权限。参数为需要创建的用户名和密码。
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTI4OTcxMzgzfQ.QEyKqNUs77toZTqeN9qMtOhSInFIp-Vhp75DXqZgNz0" -d "username=binbo&password=123456" http://127.0.0.1:9050/user/create
{"result": true, "code": 0, "message": "\u521b\u5efa\u7528\u6237\u6210\u529f"}

4、禁用/恢复用户。管理员权限。参数为需要禁用/恢复的用户名。
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTI4OTcxMzgzfQ.QEyKqNUs77toZTqeN9qMtOhSInFIp-Vhp75DXqZgNz0" -d "username=binbo" http://127.0.0.1:9050/user/forbidden
{"result": true, "code": 0, "message": "\u7981\u7528\u7528\u6237\u6210\u529f"}

curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTI4OTcxMzgzfQ.QEyKqNUs77toZTqeN9qMtOhSInFIp-Vhp75DXqZgNz0" -d "username=binbo" http://127.0.0.1:9050/user/recovery
{"result": true, "code": 0, "message": "\u6062\u590d\u7528\u6237\u6210\u529f"}


5、首页和测试。所有用户权限。用于测试服务是否正常启动。
$ curl http://127.0.0.1:9050/
welcome to turing!


6、打招呼。分别需要普通用户和管理员权限。用于测试权限体系是否正常。

$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNpbWJhIiwiZXhwIjoxNTI4OTczMjcwfQ.bR2bJheaHdejDIYR9WeVPFR2POWb7j3lEGpCudsidVw"  http://127.0.0.1:9050/customer
Hello, simba!   You are customer

$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTI4OTcxMzgzfQ.QEyKqNUs77toZTqeN9qMtOhSInFIp-Vhp75DXqZgNz0"  http://127.0.0.1:9050/admin
Hello, admin!   You are admin


7、踢出用户。管理员权限。参数为需要踢出的用户名。 普通用户被踢出之后，需要重新登录获取token。
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1Mjg5NjI5ODksImlhdCI6MTUyODk2MjkyOSwiaXNzIjoia2VuIiwiZGF0YSI6eyJ1c2VybmFtZSI6ImFkbWluIiwidG9rZW5fdGltZSI6MTUyODk2MjkyOX19.RCl5O5uWaEytk6ocnMejBnJ12rfpV1p61vGa8KuvScA" -d "username=simba" http://127.0.0.1:9050/user/kick
{"result": true, "code": 0, "message": "\u8e22\u51fa\u7528\u6237\u6210\u529f"}

8、修改密码。管理员权限。参数为需要修改密码的用户名、新密码。密码被修改后，该用户现有的token失效，需要重新登陆获取token。
$ curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MjkxMTcyNDYsImlhdCI6MTUyOTExNjY0NiwiaXNzIjoia2VuIiwiZGF0YSI6eyJ1c2VybmFtZSI6ImFkbWluIiwidG9rZW5fdGltZSI6MTUyOTExNjY0Nn19.PaRiG4_FG1mH6JHdSBWQqGXKv7TixvtJJz77Y5akq5A" -d "username=simba&password=123456" http://127.0.0.1:9050/user/change_password
{"result": true, "code": 0, "message": "\u4fee\u6539\u5bc6\u7801\u6210\u529f"}

