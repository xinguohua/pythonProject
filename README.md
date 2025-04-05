1、通过报告的攻击时间确定发生的bin文件
要处理的压缩文件存放位置data目录下，解压的文件会自动创建目录

2. 可以选的参数如下，两种模式unzip，direct,看看到底哪个bin文件 在时间范围内，哪个json有数据就是在哪个文件里
start_time = "2018-04-12 00:00:00"
end_time = "2018-04-13 00:00:00"
mode = 'unzip' #批量处理tar.gz压缩包的
mode = 'direct' #批量处理bin文件的
"-time" 是开启时间 可以粗略判断
例子：
start_time = "2018-04-13 00:00:00"
end_time = "2018-04-14 00:00:00"
mode = 'direct'
文件索引bin的下标
start_index = 147
end_index = 157
"-time" 是开启时间 可以粗略判断
恶意时间段尽量小范围（h单位），良性时间段 选用恶意时间段的前面和后面bin文件：
start_time = "2018-04-13 12:00:00"
end_time = "2018-04-14 00:00:00"
ta1-trace-e3-official-1.bin.2-4.json

3、通过md的uuid进行脚本细致分析画出日志图能和报告对起来，更新原来的语雀文档
