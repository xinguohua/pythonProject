import os

def filter_lines_by_uuids(input_file, output_file, uuid_list):
    """
    从 input_file 中提取包含任意一个 UUID 的行，写入 output_file。

    :param input_file: 输入文件路径（每行一个 JSON）
    :param output_file: 输出文件路径（匹配的行）
    :param uuid_list: 包含要匹配的 UUID 字符串列表
    """
    matched = 0
    total = 0
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            total += 1
            if any(uuid in line for uuid in uuid_list):
                outfile.write(line)
                matched += 1

    print(f"==Done. Matched {matched} lines out of {total} total lines.")
    print(f"==Output written to: {output_file}")

if __name__ == "__main__":
    # 输入 JSON 文件路径
    input_file = "/Users/xinguohua/Code/pythonProject1/ta1-trace-e3-official-1.bin.3.json"

    # 输出 JSON 文件路径
    output_file = "filtered_by_uuid.json"

    # UUID 列表（可以改成你想查找的 UUID）
    uuid_list = [
        "D64910E4-454E-156D-BF13-BC7AD66F7A6A",
    ]

    # 执行过滤
    filter_lines_by_uuids(input_file, output_file, uuid_list)