import regex
import json

def fun():
    temp_s = set()
    
    t2s = dict()
    multi_s = set()
    
    re_split = regex.compile(r'\s+')
    count = 0
    with open('TSCharacters.txt', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            t = re_split.split(line)
            assert t[0] not in t2s
            
            # 特例
            if t[0] == '餘':
                assert t == ['餘', '余', '馀']
                t = ('餘', '馀')
            elif t[0] == '鉅':
                assert t == ['鉅', '巨', '钜']
                t = ('鉅', '钜')
            elif t[0] == '瀰':
                assert t == ['瀰', '弥', '㳽']
                t = ('瀰', '㳽')
            
            # 只保留BMP字符
            if ord(t[0]) > 0xffff or \
                all(True if ord(i) > 0xffff else False for i in t[1:]):
                continue

            # 一样的情况
            #if t[0] == t[1]:
            #    continue
            
            # 保存 繁简映射
            assert ord(t[1]) <= 0xffff
            t2s[t[0]] = t[1]

            # 保存 多繁对一简
            if t[1] in temp_s:
                multi_s.add(t[1])
            else:
                temp_s.add(t[1])
            
            # 打印 多简的情况
            #if len(t) > 2:
            #    print(t, [1 if ord(ch)>0xffff else 0 for ch in t])

    #print(multi_s)
    print('繁->简映射：', len(t2s))
    print('多繁对一简：', len(multi_s))
    return t2s, multi_s

t2s, multi_s = fun()
t2s = {ord(k):ord(v) for k,v in t2s.items()}
multi_s = [ord(i) for i in multi_s]

with open('map.json', 'w') as f:
    json.dump([t2s, multi_s], f, separators=(',', ':'))
