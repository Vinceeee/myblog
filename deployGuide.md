1. 安装Docker以及Docker-compose,具体请参考[Docker —— 从入门到实践](https://www.gitbook.com/book/yeasy/docker_practice/details)
  
2. 第一遍启动docker-compose,因为相关数据库还没有建立,所以会抛出异常,可以先不管。

3. 先部署数据库,设置应用账号及其密码.进入数据库容器根目录执行
 `` docker exec -it <container-db> sh # 进入MySQL容器 ``
 `` sh /root/bin/entrypoint.sh # 执行建库脚本``

4. 建库成功后,重启web服务
 `` docker-compose restart web_app # 单独重启web服务``
