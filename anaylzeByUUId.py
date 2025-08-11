import os
from concurrent.futures import ThreadPoolExecutor


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

    input_files = ['ta1-theia-1-e5-official-2.bin.26.json',
                   'ta1-theia-2-e5-official-2.bin.28.json',
                   'ta1-theia-3-e5-official-2.bin.22.json']
    # uuid_list = [
    #     "barephone-instr.apk", "189.141.204.211", "153.4.41.7", "208.203.20.42"
    # ]
    uuid_list = [
        "128.55.12.110"
    ]
    max_workers = min(len(input_files), max(4, (os.cpu_count() or 1) * 2))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for input_file in input_files:
            output_file = input_file + "filtered_by_uuid.json"
            futures.append(
                executor.submit(filter_lines_by_uuids, input_file, output_file, uuid_list)
            )

        # 等待所有任务完成并把异常抛出来
        for f in futures:
            try:
                f.result()
            except Exception as e:
                print(f"Error processing file: {e}")
