sphinx-template
===============

python-code-block
-----------------


.. code-block:: python

   # 注意这里是三个空格
   import os
   import sys
   sys.path.insert(0, os.path.abspath('../../src'))

inline-markup
-------------
*斜体字* 后面必须要带有空格，不然效果不会展现出来。

**加粗字体** 原理同上，还是需要在后面添加空格。

``python-wechaty`` 这个就类似于Markdown里面的 ``


列表
----------

* one
* two
* three

1. one
2. two
3. three


* one
   * one-one
   * one-two
* two

引用快
------

| one 
| two
| three


代码块
-------
这只是一个简单的代码展示输出::

   # 上面两个冒号是非常重要的标识符
   print("sdfsdf")

表格
----

+--------------+----------+-----------+-----------+
| row 1, col 1 | column 2 | column 3  | column 4  |
+--------------+----------+-----------+-----------+
| row 2        | Use the command ``ls | more``.   |
|              |                                  |
+--------------+----------+-----------+-----------+
| row 3        |          |           |           |
+--------------+----------+-----------+-----------+

当然还是有另外一种方式来构建表格：

.. list-table:: Frozen Delights!
   :widths: 15 10 30
   :header-rows: 1

   * - Treat
     - Quantity
     - Description
   * - Albatross
     - 2.99
     - On a stick!
   * - Crunchy Frog
     - 1.49
     - If we took the bones out, it wouldn't be
       crunchy, now would it?
   * - Gannet Ripple
     - 1.99
     - On a stick!

链接
----

* 外部链接

`百度 <https://www.baidu.com/>`_

提醒
----

.. danger::
   
   当使用这种方式的时候，需要注意ready函数的鲁棒性


* attention
* caution
* danger
* error
* hint
* important
* note
* tip
* warning


图片
----

.. image:: ./_static/picture.jpg
   :alt: alternate text
   :align: center

自动生成模块文档
-------------

.. autoclass:: wechaty.wechaty.Wechaty