import re
from user.speaker import sayings as s
from user import excelprocess as ex

def compile_s():
    return [
        re.compile(r'.*?问(?P<name>.*?)(?:放)?(?:在|哪).*?', re.DOTALL),
        re.compile(r'.*?问(?P<add>.*?)(?:里)?(?:放|是|放了|有).*?', re.DOTALL),
        re.compile(r'.*?把(?P<name1>.*?)(?:放)(?:在)?(?P<add1>.*?)了.*?', re.DOTALL)
    ]

def execute(message, data):
    patterns = compile_s()
    stence = s.回答_w  # 默认回复
    for pattern in patterns:
        match_obj = pattern.match(message)
        if match_obj:
            if 'name' in match_obj.groupdict():
                name = match_obj.group('name').strip()
                places = ex.excel.where(name, data)
                if not places:
                    stence = s.回答_P_3 + name + s.回答_C_3
                else:
                    stence = s.回答_P_1 + name + s.回答_C_1 + "".join(places)
                break  # 匹配到name后直接退出循环
            elif 'add' in match_obj.groupdict():
                
                add = match_obj.group('add').strip()
                print(add)
                item = ex.excel.what(add, data)
                if not item:
                    stence = s.回答_P_3 + add + s.回答_C_3
                else:
                    stence = s.回答_P_2 + add + s.回答_C_2 + item
                break  # 匹配到add后直接退出循环
            elif 'add1' in match_obj.groupdict():
                add = match_obj.group('add1').strip()
                add = add.upper()
                name = match_obj.group('name1').strip()
                
                ex.excel.place(add,name)
                stence = s.回答_P_4 + name + s.回答_C_4 + add + "中了"
                break  # 匹配到add后直接退出循环

    return stence

if __name__ == "__main__":
    # 测试
    from user.speaker import speak
    path = "C:\\Users\\14676\\Desktop\\副本机房设备清单（正式版）.xlsx"
    data = ex.excel.read(path)
    ex.excel.fix_excel(path)
    print(data)
    stence = execute("问a a a在",data)
    speak(stence)
    print(stence)      # 输出: "学生"（来自 name 分组）
    stence = execute("问A02-08放的啥",data)  # 输出: "用户"（来自 add 分组）
    speak(stence)
    print(stence) 
    stence = execute("把测试放A01-10了",data)  # 输出: "用户"（来自 add 分组）
    speak(stence)
    print(stence) 