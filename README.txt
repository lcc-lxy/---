用户可以登录和注册
* 登录凭借用户名和密码登录              #将输入信息与数据库进行对比 然后进行适应操作
* 注册要求用户必须填写用户名,密码,其他内容自定
* 用户名要求不能重复
* 要求用户信息能够长期保存
可以通过基本的图形界面print以提示客户端输入。   #网络结构使用tcp
* 程序分为服务端和客户端两部分                #使用两个类  客户端 和服务端
* 客户端通过print打印简单界面输入命令发起请求   #并发使用多线程
* 服务端主要负责逻辑数据处理
* 启动服务端后应该能满足多个客户端同时操作

客户端启动后即进入一级界面,包含如下功能:登录 注册 退出
* 退出后即退出该软件
* 登录成功即进入二级界面,失败回到一级界面
* 注册成功可以回到一级界面继续登录,也可以直接用注册用户进入二级界面
用户登录后进入二级界面,功能如下:查单词 历史记录 注销
* 选择注销则回到一级界面
* 查单词:循环输入单词,得到单词解释,输入特殊符号退出单词查询状态
* 历史记录:查询当前用户的查词记录,要求记录包含name word time。
可以查看所有记录或者前10条均可


设计过程
1.确定技术点

  并发模型和网络模型
  确定细节功能,注册要注册什么,注册后是否能直接登录
  一级界面,二级界面如何切换
2.mysql 数据库设计 dict
    words  user   hist(记录表)
3.结构设计,功能模型划分
  如何封装 客户端与服务端工作流程,有几个功能模块
4.通信搭建

cookie:
    import getpass
    pwd = getpass.getpass()  注意:只能在终端中使用
