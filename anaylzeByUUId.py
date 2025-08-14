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

    input_files = [
        "ta1-cadets-1-e5-official-2.bin.116.json.1",
        "ta1-cadets-1-e5-official-2.bin.116.json",
        "ta1-cadets-1-e5-official-2.bin.117.json.1",
        "ta1-cadets-1-e5-official-2.bin.117.json",
        "ta1-cadets-1-e5-official-2.bin.118.json.1",
        "ta1-cadets-1-e5-official-2.bin.118.json",
                   ]
    # uuid_list = [
    #     "barephone-instr.apk", "189.141.204.211", "153.4.41.7", "208.203.20.42"
    # ]
    uuid_list = [
            # "98.23.182.25"
            # "7616CEF5-78AE-11E9-A28B-D4AE52C1DBD3"
            # "1E2E3C6D-77E5-11E9-A28B-D4AE52C1DBD3"
            #"26E2310C-E0FA-5A46-825B-237BA4DFE4BA"
            # "7616A7B7-78AE-11E9-A28B-D4AE52C1DBD3"
            # "98DB63EF-78AF-11E9-B41B-D4AE52C1DBD3"
            # "B7977DD7-78B2-11E9-A28B-D4AE52C1DBD3"
            # "F6A4219C-415F-523A-9C36-C87EC385FD07"
            # "26E2310C-E0FA-5A46-825B-237BA4DFE4BA"
            # "7616A7B7-78AE-11E9-A28B-D4AE52C1DBD3"
            # "1553A05F-DAD0-5BAE-99BC-0129C60716D2"
            # "2C491B63-03B2-5BB9-9EC7-1E37622FFFE81",
             # "C0ED5476-D19B-5FF0-93A9-D3E9CA2A4020",
             # "1553A05F-DAD0-5BAE-99BC-0129C60716D2",
            # "98A2F9DC-78AF-11E9-B41B-D4AE52C1DBD3"
            "128.55.12.167"

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
