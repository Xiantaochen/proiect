import re

a = "历年黑龙江高考录取分数线(2006年-2018年)"
pattern = r"历年(.*?)高考录取分数线"

print(re.match(pattern,a).group(1))