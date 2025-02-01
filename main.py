from astrbot.api.message_components import *
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain, Image
import aiohttp

@register("mccloud_site", "MC云-小馒头", "一个集成了网站测试工具的插件，支持网站连通性测试、速度测试、域名查询、端口扫描和网站截图功能。使用/sitehelp查看帮助", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("sitehelp")
    async def pinghelp(self, event: AstrMessageEvent):
        help_text = """\n站长 工具使用帮助:

/sitehelp - 显示此帮助信息
/ping <网址> - 测试指定网址的连通性
/siteno <网址> - 测试指定网址的延迟
/whois <域名> - 查询指定域名的whois信息
/port <IP地址> - 扫描指定IP地址的端口
/site <网址> - 截图指定网址

示例:
/ping mcsqz.stay33.cn
/siteno https://mcsqz.stay33.cn
/whois mcsqz.stay33.cn
/port 8.8.8.8
/site https://mcsqz.stay33.cn"""
        yield event.plain_result(help_text)

    @filter.command("ping")
    async def ping(self, event: AstrMessageEvent):
        # 获取消息内容
        messages = event.get_messages()
        print("Debug - Raw messages:", messages)
        
        if not messages:
            yield event.plain_result("\n请输入要测试的域名!\n示例: /ping mcsqz.stay33.cn")
            return
            
        # 获取原始消息文本
        message_text = messages[0].text  # 直接获取 Plain 对象的 text 属性
        print(f"Debug - Message text: {message_text}")
        
        parts = message_text.split()  # 分割消息文本
        print(f"Debug - Split parts: {parts}")
        
        if len(parts) < 2:  # 检查是否有域名参数
            yield event.plain_result("\n请输入要测试的域名!\n示例: /ping mcsqz.stay33.cn")
            return
            
        domain = parts[1]  # 获取域名参数
        print(f"Debug - Domain: {domain}")
        
        # 设置请求头
        headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'
        }
        print(f"Debug - Headers: {headers}")
        
        # 创建一个不验证SSL的连接上下文
        ssl_context = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=ssl_context) as session:
            try:
                url = f"https://v2.xxapi.cn/api/ping?url={domain}"
                print(f"Debug - Request URL: {url}")
                
                async with session.get(url, headers=headers) as response:
                    print(f"Debug - Response status: {response.status}")
                    response_text = await response.text()
                    print(f"Debug - Response text: {response_text}")
                    
                    data = await response.json()
                    print(f"Debug - Parsed JSON: {data}")
                    
                    if data["code"] == 200:
                        result = f"""\n信息：{data['msg']}
延迟：{data['data']['time']}
IP地址：{data['data']['server']}"""
                    else:
                        result = f"\n信息：{data['msg']}"
                    
                    print(f"Debug - Final result: {result}")
                    yield event.plain_result(result)
            except Exception as e:
                print(f"Debug - Error occurred: {str(e)}")
                yield event.plain_result(f"请求失败: {str(e)}")

    @filter.command("siteno")
    async def siteno(self, event: AstrMessageEvent):
        # 获取消息内容
        messages = event.get_messages()
        print("Debug - Raw messages:", messages)
        
        if not messages:
            yield event.plain_result("\n请输入要测试的网址!\n示例: /siteno https://mcsqz.stay33.cn")
            return
            
        # 获取原始消息文本
        message_text = messages[0].text  # 直接获取 Plain 对象的 text 属性
        print(f"Debug - Message text: {message_text}")
        
        parts = message_text.split()  # 分割消息文本
        print(f"Debug - Split parts: {parts}")
        
        if len(parts) < 2:  # 检查是否有网址参数
            yield event.plain_result("\n请输入要测试的网址!\n示例: /siteno https://mcsqz.stay33.cn")
            return
            
        url = parts[1]  # 获取网址参数
        print(f"Debug - URL: {url}")
        
        # 设置请求头
        headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'
        }
        print(f"Debug - Headers: {headers}")
        
        # 创建一个不验证SSL的连接上下文
        ssl_context = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=ssl_context) as session:
            try:
                api_url = f"https://v2.xxapi.cn/api/speed?url={url}"
                print(f"Debug - Request URL: {api_url}")
                
                async with session.get(api_url, headers=headers) as response:
                    print(f"Debug - Response status: {response.status}")
                    response_text = await response.text()
                    print(f"Debug - Response text: {response_text}")
                    
                    data = await response.json()
                    print(f"Debug - Parsed JSON: {data}")
                    
                    if data["code"] == 200:
                        result = f"""\n信息：{data['msg']}
延迟：{data['data']}"""
                    else:
                        result = f"\n信息：{data['msg']}"
                    
                    print(f"Debug - Final result: {result}")
                    yield event.plain_result(result)
            except Exception as e:
                print(f"Debug - Error occurred: {str(e)}")
                yield event.plain_result(f"\n请求失败: {str(e)}")

    @filter.command("whois")
    async def whois(self, event: AstrMessageEvent):
        # 获取消息内容
        messages = event.get_messages()
        print("Debug - Raw messages:", messages)
        
        if not messages:
            yield event.plain_result("\n请输入要查询的域名!\n示例: /whois baidu.com")
            return
            
        # 获取原始消息文本
        message_text = messages[0].text  # 直接获取 Plain 对象的 text 属性
        print(f"Debug - Message text: {message_text}")
        
        parts = message_text.split()  # 分割消息文本
        print(f"Debug - Split parts: {parts}")
        
        if len(parts) < 2:  # 检查是否有域名参数
            yield event.plain_result("\n请输入要查询的域名!\n示例: /whois baidu.com")
            return
            
        domain = parts[1]  # 获取域名参数
        print(f"Debug - Domain: {domain}")
        
        # 设置请求头
        headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'
        }
        print(f"Debug - Headers: {headers}")
        
        # 创建一个不验证SSL的连接上下文
        ssl_context = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=ssl_context) as session:
            try:
                url = f"https://v2.xxapi.cn/api/whois?domain={domain}"
                print(f"Debug - Request URL: {url}")
                
                async with session.get(url, headers=headers) as response:
                    print(f"Debug - Response status: {response.status}")
                    response_text = await response.text()
                    print(f"Debug - Response text: {response_text}")
                    
                    data = await response.json()
                    print(f"Debug - Parsed JSON: {data}")
                    
                    if data["code"] == 200:
                        result = f"""\n信息：{data['msg']}
域名：{data['data']['Domain Name']}
注册商：{data['data']['Sponsoring Registrar']}
注册人：{data['data']['Registrant']}
注册人邮件：{data['data']['Registrant Contact Email']}
DNS1：{data['data']['DNS Serve'][0]}
DNS2：{data['data']['DNS Serve'][1]}
注册时间：{data['data']['Registration Time']}
到期时间：{data['data']['Expiration Time']}"""
                    else:
                        result = f"\n信息：{data['msg']}"
                    
                    print(f"Debug - Final result: {result}")
                    yield event.plain_result(result)
            except Exception as e:
                print(f"Debug - Error occurred: {str(e)}")
                yield event.plain_result(f"\n请求失败: {str(e)}")

    @filter.command("port")
    async def port(self, event: AstrMessageEvent):
        # 获取消息内容
        messages = event.get_messages()
        print("Debug - Raw messages:", messages)
        
        if not messages:
            yield event.plain_result("\n请输入要扫描的IP地址!\n示例: /port 8.8.8.8")
            return
            
        # 获取原始消息文本
        message_text = messages[0].text  # 直接获取 Plain 对象的 text 属性
        print(f"Debug - Message text: {message_text}")
        
        parts = message_text.split()  # 分割消息文本
        print(f"Debug - Split parts: {parts}")
        
        if len(parts) < 2:  # 检查是否有IP参数
            yield event.plain_result("\n请输入要扫描的IP地址!\n示例: /port 8.8.8.8")
            return
            
        ip_address = parts[1]  # 获取IP参数
        print(f"Debug - IP Address: {ip_address}")
        
        # 设置请求头
        headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'
        }
        print(f"Debug - Headers: {headers}")
        
        # 创建一个不验证SSL的连接上下文
        ssl_context = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=ssl_context) as session:
            try:
                url = f"https://v2.xxapi.cn/api/portscan?address={ip_address}"
                print(f"Debug - Request URL: {url}")
                
                async with session.get(url, headers=headers) as response:
                    print(f"Debug - Response status: {response.status}")
                    response_text = await response.text()
                    print(f"Debug - Response text: {response_text}")
                    
                    data = await response.json()
                    print(f"Debug - Parsed JSON: {data}")
                    
                    if data["code"] == 200:
                        # 分别收集开放和未开放的端口
                        open_ports = []
                        closed_ports = []
                        
                        for port, is_open in data['data'].items():
                            if is_open:
                                open_ports.append(port)
                            else:
                                closed_ports.append(port)
                                
                        # 使用 | 连接端口号
                        open_ports_str = " | ".join(open_ports) if open_ports else "无"
                        closed_ports_str = " | ".join(closed_ports) if closed_ports else "无"
                        
                        result = f"""\n信息：{data['msg']}
开放端口：{open_ports_str}
未开放端口：{closed_ports_str}"""
                    else:
                        result = f"\n信息：{data['msg']}"
                    
                    print(f"Debug - Final result: {result}")
                    yield event.plain_result(result)
            except Exception as e:
                print(f"Debug - Error occurred: {str(e)}")
                yield event.plain_result(f"\n请求失败: {str(e)}")

    @filter.command("site")
    async def site(self, event: AstrMessageEvent):
        # 获取消息内容
        messages = event.get_messages()
        print("Debug - Raw messages:", messages)
        
        if not messages:
            yield event.plain_result("\n请输入要截图的网址!\n示例: /site https://mcsqz.stay33.cn")
            return
            
        # 获取原始消息文本
        message_text = messages[0].text  # 直接获取 Plain 对象的 text 属性
        print(f"Debug - Message text: {message_text}")
        
        parts = message_text.split()  # 分割消息文本
        print(f"Debug - Split parts: {parts}")
        
        if len(parts) < 2:  # 检查是否有网址参数
            yield event.plain_result("\n请输入要截图的网址!\n示例: /site https://mcsqz.stay33.cn")
            return
            
        url = parts[1]  # 获取网址参数
        print(f"Debug - URL: {url}")
        
        # 设置请求头
        headers = {
            'User-Agent': 'xiaoxiaoapi/1.0.0 (https://xxapi.cn)'
        }
        print(f"Debug - Headers: {headers}")
        
        # 创建一个不验证SSL的连接上下文
        ssl_context = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=ssl_context) as session:
            try:
                api_url = f"https://v2.xxapi.cn/api/screenshot?url={url}"
                print(f"Debug - Request URL: {api_url}")
                
                async with session.get(api_url, headers=headers) as response:
                    print(f"Debug - Response status: {response.status}")
                    response_text = await response.text()
                    print(f"Debug - Response text: {response_text}")
                    
                    data = await response.json()
                    print(f"Debug - Parsed JSON: {data}")
                    
                    if data["code"] == 200:
                        # 使用 MessageChain 构建包含文本和图片的消息
                        chain = [
                            Plain(f"信息：{data['msg']}\n"),
                            Image.fromURL(data['data'])  # 从URL加载图片
                        ]
                        yield event.chain_result(chain)
                    else:
                        result = f"\n信息：系统错误"
                        yield event.plain_result(result)
            except Exception as e:
                print(f"Debug - Error occurred: {str(e)}")
                yield event.plain_result(f"\n请求失败: {str(e)}")