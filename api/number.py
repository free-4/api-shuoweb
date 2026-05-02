import json
import sys
import argparse

class PhoneLocationQuery:
    def __init__(self, data_file):
        """
        初始化查询类，加载 JSON 数据并构建查询字典。
        """
        self.data_dict = {}
        self.load_data(data_file)

    def load_data(self, data_file):
        """
        读取 JSON 数据。兼容标准的 JSON 数组格式以及 JSON Lines 格式（每行一个 JSON 对象）。
        """
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                # 尝试解析为标准 JSON 数组: [{...}, {...}]
                try:
                    data_list = json.load(f)
                    if isinstance(data_list, list):
                        for item in data_list:
                            self.data_dict[item['_id']] = item
                except json.JSONDecodeError:
                    # 如果不是标准 JSON 数组，尝试按行读取 (JSON Lines)
                    f.seek(0)
                    for line in f:
                        line = line.strip()
                        if line:
                            item = json.loads(line)
                            self.data_dict[item['_id']] = item
                            
        except FileNotFoundError:
            print(json.dumps({"error": f"找不到数据文件: {data_file}"}, ensure_ascii=False))
            sys.exit(1)
        except Exception as e:
            print(json.dumps({"error": f"加载数据时发生错误: {str(e)}"}, ensure_ascii=False))
            sys.exit(1)

    def query(self, phone_number):
        """
        查询手机号归属地信息，返回 JSON 格式字符串
        """
        phone_str = str(phone_number).strip()

        # 1. 验证手机号长度和格式（通常为11位纯数字）
        if not phone_str.isdigit() or len(phone_str) != 11:
            return json.dumps({"error": "请输入有效的11位纯数字手机号码"}, ensure_ascii=False)

        # 2. 拦截 19 开头的手机号
        if phone_str.startswith("19"):
            return json.dumps({"error": "系统暂不支持查询以 19 开头的手机号码"}, ensure_ascii=False)

        # 3. 提取前7位作为号段前缀
        prefix = phone_str[:7]

        # 4. 在字典中匹配数据
        result = self.data_dict.get(prefix)

        if result:
            return json.dumps(result, ensure_ascii=False)
        else:
            return json.dumps({"error": "数据库中未找到该手机号的归属地信息"}, ensure_ascii=False)

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="手机号归属地查询工具")
    parser.add_argument("-d", "--data", default="./data/number.json", help="指定 JSON 数据文件路径，默认值为 data.json")
    parser.add_argument("-p", "--phone", required=True, help="需要查询的 11 位手机号码")
    
    args = parser.parse_args()

    # 初始化查询器并输出结果
    query_tool = PhoneLocationQuery(args.data)
    result_json = query_tool.query(args.phone)
    
    # 打印最终的 JSON 结果
    print(result_json)

if __name__ == "__main__":
    main()
