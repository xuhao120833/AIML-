 # coding=utf-8

import sys
import codecs
import shelve

from aiml.constants import unicode


db = shelve.open("simple_rules.db", "c", writeback=True)

template = """<?xml version="1.0" encoding="UTF-8"?>
<aiml version="1.0">
{rules}
</aiml>
"""

category_template = """
<category>
<pattern>{pattern}</pattern>
<template>
{answer}
</template>
</category>
"""

#print sys.argv
if len(sys.argv) == 3:
    _, rule, temp= sys.argv
    rule="".join(rule.split( ))
    temp="".join(temp.split( ))
    db[rule] = temp
    db.sync()#保存
    rules = []
    for r in db:
        rules.append(category_template.format(pattern=r,
                                              answer=db[r]))#format将对应的参数写到模板category_template对应的位置，把修改后的模板通过append()全部加入到rules中
    #rules = '\n'.join(rules)
    #print(rules)
    content = template.format(rules = '\n'.join(rules))#
    with open("auto-learn.aiml", 'w',encoding='utf-8') as fp:#打开文件写进去
        fp.write(content)
