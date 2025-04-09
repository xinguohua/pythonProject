import subprocess
import os
import tarfile
from concurrent.futures import ThreadPoolExecutor

def generate_input_files(base_path, base_name, start_idx, end_idx):
    input_files = []
    for i in range(start_idx, end_idx + 1):
        file_path = f"{base_path}/{base_name}.{i}"
        input_files.append(file_path)
    return input_files

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
        # "-uuid", uuid_filter，
        "-time"
    ]
    # 执行命令
    print(f"Running command for {file_path}:")
    print(" ".join(cmd))
    # 执行命令并等待每个命令执行完成
    subprocess.run(cmd)

#############################固定参数###########################################################
# 定义 Java JAR 的路径
jar_path = "jar/kafkaclients-1.0-SNAPSHOT-jar-with-dependencies.jar"
# 定义 schema 文件路径
schema_path = "jar/TCCDMDatum.avsc"
# # 定义 Log4j 配置和调试选项
log4j_options = [
    "-Dlog4j.debug=true",
    "-Dlog4j.configuration= file:jar/nochecker.log4j.properties"
]

#############################可调参数###########################################################

# 模式选择：'unzip' 为解压模式，'direct' 为直接处理 bin 文件模式
mode = 'direct'  # 可选 'unzip' 或 'direct'
# 定义开始和结束时间（格式必须为 yyyy-MM-dd HH:mm:ss）
start_time = "2018-04-10 13:00:00"
end_time = "2018-04-10 15:00:00"
# 定义要筛选的 UUID（多个用逗号分隔字符串）
# uuid_filter = "CAE9180E-98E9-A5FB-A375-E99EAECC8B7C"
#############################################################################################

if mode == 'unzip':
    # 定义 .tar.gz 文件的路径
    # tar_gz_file = "/Users/xinguohua/Code/pythonProject1/data/ta1-trace-e3-official.bin.tar.gz"
    tar_gz_file = "data/ta1-theia-e3-official-6r.bin.tar.gz"

    base_name = os.path.splitext(os.path.basename(tar_gz_file))[0]
    output_dir = f"data/{base_name}_unzipped"  # 解压后的文件存放目录
    print(f"Extracted files to {output_dir}")

    # 解压 .tar.gz 文件
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 如果解压目录不存在，创建它

    # 解压文件
    with tarfile.open(tar_gz_file, "r:gz") as tar:
        tar.extractall(path=output_dir)  # 解压所有文件到 output_dir

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
    # 定义多个输入文件路径
    # input_files = [
    #     "/Users/xinguohua/Code/ta3-java-consumer/data/ta1-trace-e3-official.bin.1",
    #     "/Users/xinguohua/Code/ta3-java-consumer/data/ta1-trace-e3-official.bin.2"
    #     # 可以继续添加更多文件路径
    # ]

    base_path = "data/ta1-theia-e3-official-6r.bin.tar_unzipped"
    base_name = "ta1-theia-e3-official-6r.bin"
    # start_index = 2
    # end_index = 4
    start_index = 9
    end_index = 9

    input_files = generate_input_files(base_path, base_name, start_index, end_index)

    for input_file in input_files:
        run_java_cmd(input_file, jar_path, schema_path, log4j_options)

else:
    print("Invalid mode selected. Choose 'unzip' or 'direct'.")






