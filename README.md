# Bassoon

我自己对 **Bassoon** 的定义就是:

> A toy server.
>
> A toy framework.

-----

#### A toy server:

意思就是实现了一个玩具服务器, 至少能运行了, 性能就不要考虑了.

类 `BassoonServer` 实现了一个简单的 WSGI 服务器, 使用 socket 监听指定端口, 读取传来的 HTTP 请求, 解析和添加相应的环境值, 然后将 application 返回的结果返回给客户端.



#### A toy framework:

同样地, 意思是实现了一个玩具框架, 至少表现上很像一个网络框架了, 能简单的进行路由.

类 `BassoonApp` 实现了一个简单的框架, 也就是可以当做一个 application 传给 WSGI 服务器, 类似于 Flask, Bottle 等. 实现的时候也参考了 Flask 和 Bottle. 支持 `get` 和 `post` 装饰器. 接下来计划添加一个模板引擎.



#### 示例:

`example.py`:

``` Python
#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Bassoon import app, get, post
from Bassoon import BassoonServer

@get('/')
def index():
    return "hello world"

def main():
    host = "0.0.0.0"
    port = "8888"

    bs = BassoonServer(host=host, port=port, app=app)
    bs.serve_forever()

if __name__ == "__main__":
    main()
```

如上, 启动一个服务器也比较简单.



-----

关于名称 **Bassoon**:

GitHub 创建项目时候随机推荐出来的, 查了下意思, 巴松管(乐器大管), 感觉也算有点意思, 就定了下来.

当时还随机出来了另外一个的名字: super-duper-eureka, 只是有点长而没有使用.