# Эта программа выполняет всё что нужно по домашнему заданию. Выводить можно как на экран (просто написать 
# print(нужная переменная)), так и в файл (переменная.use_file). Создаются переменные как способом "with" так
# и без него (в тестовом поле можно увидеть пример создания такой переменной). Большая слабость програаммы в том, 
# что важно соблюдать порядок прибавления тегов друг в друга и то, что нельзя разом объеинять кучу тегов в один.
# Также может показаться неприятным кучааа отступов которые образуются при выводе. 



class Tag:
    def __init__(self, tag, klass=None, **kwargs):
        self.tag = tag

        self.text = ""
        self.attributes = {}

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value
    
    def __iadd__(self,other):
        new_text= " {old_text} \n {in_tag} \n".format(old_text=self.text, in_tag=str(other))
        self.text=new_text
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        return "<{tag} {attrs}>\n{text}\n</{tag}>".format(
            tag=self.tag, attrs=attrs, text=self.text
        )
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        doingnothing=None

class sTag(Tag):
    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        return "<{tag} {attrs}>\n{text}\n".format(
            tag=self.tag, attrs=attrs, text=self.text
        )

class HTML(Tag):
    def __init__(self, output=None, **kwargs):
        self.tag="html"
        self.src= output
        self.text=""
        self.attributes = {}

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        return "<!DOCTYPE html> \n<{tag} {attrs}>\n{text}\n</{tag}>".format(
            tag=self.tag, attrs=attrs, text=self.text, srcu=self.src
        )

    # def __add__(self, other):
    #     self.add_this_function=0

    def use_src(self, new_src):
        self.src=new_src

    def use_file(self):
        using_file=open(self.src,"w")
        using_file.write(str(self))
        using_file.close()

    def __exit__(self, type, value, traceback):
        using_file=open(self.src,"w")
        using_file.write(str(self))
        using_file.close()

class TopLevelTag(Tag): #Зачем делать отдельный тэг когда стандартный может выполнять все нужные функции???
    def is_top(self):
        return True
#------------------TEST_FIELD---------------------
# rog= Tag('div', klass=("asdf", "assf"), asd="fdfdf")
# gafd= Tag("p", asds="df")
# rog+=gafd
# srog= sTag("link", src="./css/css.css")
# rog+=srog
# hent= HTML("test.html")
# hent+=rog
# print(hent)
# hent.use_file()


with HTML(output="test.html") as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body