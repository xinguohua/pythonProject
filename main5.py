import subprocess
import os
import gzip
import shutil

from concurrent.futures import ThreadPoolExecutor, as_completed


def run_java_cmd(file_path, jar_path, schema_path, log4j_options):
    print(f"Processing file: {file_path}")
    input_file = f"file:{file_path}"
    # 构造命令
    cmd = [
        "java"
    ] + log4j_options + [
        "-cp", f"{jar_path}",
        "com.bbn.tc.services.kafka.FileConsumer", # Java 主类
        input_file,
        "-np",
        "-psf", schema_path,
        "-csf", schema_path,
        "-rg", "-call",
        "-co", "earliest",
        "-cdm", "-c",
        "-roll", "5000000",
        "-wj",
        "-d", "10000000",
        # "-startTime", start_time,
        # "-endTime", end_time,
        # "-uuid", "barephone-instr.apk,189.141.204.211,153.4.41.7,208.203.20.42"
        # "-time"
    ]
    # 执行命令
    print(f"Running command for {file_path}:")
    print(" ".join(cmd))
    # 执行命令并等待每个命令执行完成
    subprocess.run(cmd)

#############################固定参数###########################################################
# 定义 Java JAR 的路径
jar_path = "jar5/kafkaclients-1.0-SNAPSHOT-jar-with-dependencies.jar"
# 定义 schema 文件路径
schema_path = "jar5/TCCDMDatum.avsc"
# # 定义 Log4j 配置和调试选项
log4j_options = [
    "-Dlog4j.debug=true",
    "-Dlog4j.configuration= file:jar/nochecker.log4j.properties"
]

#############################可调参数###########################################################

# 模式选择：'unzip' 为解压模式，'direct' 为直接处理 bin 文件模式
mode = 'direct'  # 可选 'unzip' 或 'direct'
# 定义开始和结束时间（格式必须为 yyyy-MM-dd HH:mm:ss）
start_time = "2019-05-14 16:00:00"
end_time = "2019-05-14 17:00:00"
# 定义要筛选的 UUID（多个用逗号分隔字符串）
# uuid_filter = "CAE9180E-98E9-A5FB-A375-E99EAECC8B7C"
#############################################################################################

if mode == 'unzip':
    # 定义 .tar.gz 文件的路径
    gz_dirs = "/Volumes/Elements/data-E5/theia/"
    # 解压目录
    output_dir = f"/Volumes/Elements/data-E5/theia/bin/"  # 解压后的文件存放目录
    print(f"Extracted files to {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 如果解压目录不存在，创建它
        for root, dirs, files in os.walk(gz_dirs):
            for file_name in files:
                if not file_name.endswith(".gz"):
                    continue
                if file_name.startswith("._"):
                    continue
                gz_file = os.path.join(root, file_name)
                base_name = os.path.splitext(os.path.basename(gz_file))[0]
                extract_path = os.path.join(output_dir, base_name)
                # 解压文件
                with gzip.open(gz_file, "rb") as f_in:
                    with open(extract_path, "wb") as f_out:
                        print(f"gz_file{gz_file}, extract_path{extract_path}")
                        shutil.copyfileobj(f_in, f_out)

    # 获取解压后的文件列表
    extracted_files = sorted(os.listdir(output_dir))

    # 多线程执行部分
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []

        # 遍历解压后的文件
        for extracted_file in extracted_files:
            file_path = os.path.join(output_dir, extracted_file)
            if os.path.isdir(file_path):
                continue

            if file_path.startswith("._"):
                continue

            if ".bin" in extracted_file:
                print(f"Submitting task for: {file_path}")
                futures.append(
                    executor.submit(run_java_cmd, file_path, jar_path, schema_path, log4j_options)
                )

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing file: {e}")


elif mode == 'direct':

    base_path = "/Volumes/Elements/data-E5/theia/bin/"
    bin_list = [
        'ta1-theia-1-e5-official-2.bin.25',
        'ta1-theia-2-e5-official-2.bin.27',
        'ta1-theia-3-e5-official-2.bin.21'
    ]

    full_paths = [os.path.join(base_path, name) for name in bin_list]

    max_workers = min(8, len(full_paths))  # 自适应一点
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_java_cmd, p, jar_path, schema_path, log4j_options): p
                   for p in full_paths}
        for fut in as_completed(futures):
            path = futures[fut]
            try:
                fut.result()
                print(f"[OK] {path}")
            except Exception as e:
                print(f"[ERR] {path} -> {e}")

else:
    print("Invalid mode selected. Choose 'unzip' or 'direct'.")






