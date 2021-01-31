from jinja2 import Template
from jinja2.ext import Extension


namex = "Федор"

tm = Template("ПРивет {{name}}")
msg = tm.render(name = namex)

msg_2 = f"Привееет {namex}"
print(msg, msg_2, sep="\n")
""""Альтернатива jinja"""


age = 28
tm = Template("Мне {{a*2}} лет и зовут {{n.upper()}}")
msg_3 = tm.render(n=namex, a=age)
print(msg_3)


''''
Пример jinja с классами
'''
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

per = Person("Зина", 160)

tm = Template("Мне {{p.age}} лет и зовут {{p.name}}")
msg_4 = tm.render(p = per)
print(msg_4)



''''
Пример jinja с классами ПОсложнее
'''

class Person_2:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def getName(self):
        return self.name

    def getAge(self):
        return self.age


pers = Person_2("Просковья", 210)

tm_p = Template("\nМне {{p.getAge()}} лет и зовут {{p.getName()}}")
msg_5 = tm_p.render(p = pers)
print(msg_5)



''''
Jinja со Словарями

'''
my_dict = {'nam': 'Иоган', 'ag': 230}
tm_p = Template("\nМне {{p.ag}} лет и зовут {{p.nam}}")
#tm_p = Template("\nМне {{p ['ag'] }} лет и зовут {{p ['nam'] }}") #разновидность
msg_6 = tm_p.render(p = my_dict)
print(msg_6)








