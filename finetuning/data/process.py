import os
import json

data_dir = "/Users/xinguohua/Code/pythonProject1/finetuning/data"
json_data_list = []
samples = []

for root, dirs, files in os.walk(data_dir):
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(root, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    full_context = []
                    techniques = []
                    for item in json_data:
                        ctx = item.get("context", "")
                        tech = item.get("technique", "")
                        if ctx and isinstance(ctx, str) and ctx.strip():
                            full_context.append(ctx.strip())
                        if tech and isinstance(tech, str) and tech.strip():
                            techniques.append(tech.strip())
                    if full_context and techniques:
                        samples.append({
                            "context": " ".join(full_context),
                            "techniques": techniques,
                            "source_file": file_path
                        })
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    json_data_list.append(data)
            except Exception as e:
                print(f"读取失败：{file_path}，错误：{e}")

print(f"\n 读取数据 {len(json_data_list)} 个 JSON 文件。")
# report--攻击
print(f"\n 样本 {samples}")
