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
    input_file = "ta1-theia-e3-official-6r.bin.json"

    # 输出 JSON 文件路径
    output_file = "filtered_by_uuid.json"

    # UUID 列表（可以改成你想查找的 UUID）
    uuid_list = [
       # "BA14551F-0000-0000-0000-000000000020",
       #  "80370C6E-1795-FFFF-FFFF-000000000040",
       #  "0015CD1F-0000-0000-0000-000000000020"
       #  "BA14551F-0000-0000-0000-000000000020"
       #  "208.75.117.2"
       #  "208.75.117.3"
       #  "80370C6E-1795-D04B-7503-500000000040"
       #  "80370C6E-1895-D04B-7503-500000000040"
       #  "80370C6E-1995-D04B-7503-500000000040"
       #  "80370C6E-6395-D04B-7503-500000000040"
       #  "80370C6E-6495-D04B-7503-500000000040"
        "80370C6E-6595-D04B-7503-500000000040"
    ]

    # 执行过滤
    filter_lines_by_uuids(input_file, output_file, uuid_list)