import re
obj = re.compile(r'云胶片防火墙|云胶片服务器|')
it = obj.findall('云胶片防火墙放在哪儿')
result = ' '.join(it)
print(result)
