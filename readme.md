# 五笔86字根查询工具

字根表来源 [rime-wubi86-jidian](http://github.com/KyleBing/rime-wubi86-jidian)

## 字根数据库设计

1. unicode码表

    极点五笔码表主要在unicode码表的以下三个分区

    - 4E00-9FFF CTF range word
    - E000−F8FF Private Use Area
    - F900−FAFF CJK Compatibility Ideographs

1. 字根数据库设计

    每0x100做为一个管理单元格，即1块保存256个int64数值(64bit)

    0000|0100 |0200|0300|0400|0500|0600|0700|0800|0900|0A00|0B00|0C00|0D00|0E00|0F00
    1000|              ......                                                  |1F00
    2000|              ......                                                  |2F00
    3000|              ......                                                  |3F00
    4000|              ......                                                  |4F00
    5000|              ......                                                  |5F00
    6000| 结束

    --- meta ---
    0000格存meta信息. magic(char x 8) version(int32 * 2)
    --- sparse mapping ---
    0100格做sparse地址映射， 即 E000−F8FF 和 F900−FAFF 两部份的unicode码
        假设该表为T , T[0x100, 0x1FF] 则为sparse地址映射表
        假设 W 属于 [E000,F8FF] 或 [F900,FAFF] , W = WH x 0x100 + WL
        则 W 的 code地址为: T[0x100 + WH] + WL
        目前统计看只有 E700 E800 F800 FA00 这四套地址, 所以
        T[0x100 + 0xE7] = 0x200
        T[0x100 + 0xE8] = 0x300
        T[0x100 + 0xF8] = 0x400
        T[0x100 + 0xFA] = 0x500
    --- data ---
    0200格 -> 映射E700
    0300格 -> 映射E800
    0400格 -> 映射F800
    0500格 -> 映射FA00
    0600格 ~ 0D00格: 此8格暂无
    0E00格 -> 5FFF 映射4E00~9FFF
        设该表名为T , T[0xE00, 0x9FFF] 为统一汉字字符表
        设字 W 属于 [4E00, 9FFF]
        则 W 的code地址为: W-0x4000
    --- end ---

    data区每个int32的值定义如下:
        - 值为0: 未定义
        - 值非0, 分为: char x 4 int8 x 4
            - char x 4 保存该字的最长编码
            - int8 * 4 每个值指示可以按最长编码进行缩减
        如: aaah,3,1,0,0
        表示最长编码为aaah, 其他合法编码为 aaa, a
        如: aca\0,2,0,0,0
        表示最长编码为aca, 其他合法编码为 ac


## 字根查询

1. 查单字

    ```bash
    wubi86.py 根
    ```

    极点五笔收录了大部分大字符集，但仍有缺漏，本工具即使收录，不代表能在您具体使用的输入法上能得到该字


1. 查词

    ```bash
    wubi86.py 字根
    ```

    查词是按五笔单词输入规则生成，您具体使用的五笔输入法可能没有收录该词


