def setTag(tag):        #由于此装饰器需要参数，所以要再套一层
    def myDecorator(func):    #装饰器的核心，接受函数对象做参数，返回包装后的函数对象
        def myWrapper(*arg, **kvargs):    #包装的具体过程
            sign = "<" + tag + ">"
            return sign + func(*arg, **kvargs) + sign
        return myWrapper
    return myDecorator

@setTag("div")    #用@标签在定义函数时套上装饰器
def hello(name):
    return 'hello' + name
if __name__ == '__main__':
   print(hello("john"))