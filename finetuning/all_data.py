# 报告-攻击过程的所有组合 生成2000条
import random
import json
import os
from collections import defaultdict
import spacy
import pandas as pd
import ast
import string
# conda activate svo_env

def extract_svo_triples(text):
    doc = nlp(text)
    triples = []

    for sent in doc.sents:
        for token in sent:
            if token.dep_.endswith("subj"):
                subject = token
                verb = token.head
                for child in verb.children:
                    if child.dep_.endswith("obj"):
                        triples.append((subject.text, verb.text, child.text))
    return triples

data_dir = "/Users/xinguohua/Code/pythonProject1/finetuning/data"
json_data_list = []
samples = []

######################################################################  报告-攻击技术 ###################################################################### ###################################
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
print(f"\n 样本 {samples}")

######################################################################  攻击技术-过程 ###################################################################### ###################################

base_dir = "/Users/xinguohua/Code/pythonProject1/finetuning/mitre-ttp-mapping"
dataframes = {}
all_rows = []

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".tsv"):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path, sep="\t")
                df["source_file"] = file  # 添加来源列
                all_rows.append(df)
                print(f"✅ 读取 {file}: {df.shape[0]} 行")
            except Exception as e:
                print(f"❌ 读取失败: {file_path}，错误: {e}")

# 合并所有数据
df_all = pd.concat(all_rows, ignore_index=True)
print(f"df_all{df_all}")
label2texts = defaultdict(list)
label2triples = defaultdict(list)
nlp = spacy.load("en_core_web_sm")

for _, row in df_all.iterrows():
    try:
        labels = ast.literal_eval(row["labels"])
        if isinstance(labels, list) and len(labels) == 1:  # 只处理一个标签的情况
            label = labels[0]
            label2texts[label].append(row["text1"])
            text = row["text1"]
            triples = extract_svo_triples(text)
            label2triples[label].append(triples)
    except Exception as e:
        print(f"❌ 解析失败: {row['labels']}，错误: {e}")

# 建立 攻击技术 -> 过程三元组 的映射
print(f"🎯 映射示例: {list(label2texts.items())[:5]}")
print(f"🎯 映射示例: {list(label2triples.items())[:5]}")


combined_samples = []

for sample in samples:
    context = sample["context"]
    techniques = set(sample["techniques"])
    all_process_triples = []
    for tech in techniques:
        if tech in label2triples:
            triples_group_list = label2triples[tech]
            valid_triples = [t for t in triples_group_list if t]
            if valid_triples:
                selected_triples = random.choice(valid_triples)  # ✅ 随机选一个
                all_process_triples.append(selected_triples)
    combined_samples.append({
        "report": context,
        "technique": tech,
        "triples": all_process_triples
    })

print(f"combined_samples{combined_samples}")

# # 构建选择题
# {
#   "instruction": "Select the candidate tuple(s) below that best match the described attack behavior. Multiple or no selections are allowed. Each tuple is in the format (Entity_1, Relation, Entity_2).",
#   "input": "Report: {The attack report in motivate.pdf}\nOptions: {The corresponding candidate tuple in reason.json}",
#   "output": "Options"
# }
#
# # 构建判断题
# {
#   "instruction": "Determine whether the described attack paths fully support the attack report. Each path consists of multiple entity-relation elements in the format (Entity_1, Relation_1, Entity_2, Relation_2, Entity_3).",
#   "input": "Report: {The attack report in motivate.pdf}\nAttack Path: {The corresponding path in reason.json}",
#   "output": "Yes"
# }

multiple_choice_questions = []
true_false_questions = []


for sample in combined_samples:
    report = sample["report"]
    triple_groups = sample["triples"]
    techniques = sample["technique"]
    flat_triples = [t for group in triple_groups for t in group]

    non_related_triples = []
    for label, triples_list in label2triples.items():
        if label not in techniques:
            for group in triples_list:
                if group:
                    non_related_triples.extend(group)

    if not flat_triples:
        continue
     #  多生成几组题（比如每个 sample 生成 3～5 道题）
    repeat_count = random.randint(2, 4)
    for _ in range(repeat_count):
    # 将真实三元组打乱，确保不会集中出现在同一题中
        formatted_triples = ["({}, {}, {})".format(*t) for t in flat_triples]
        random.shuffle(formatted_triples)

        # 分批构建题目，每题包含 1~2 个真实三元组
        i = 0
        while i < len(formatted_triples):
            num_correct = min(random.randint(1, 2), len(formatted_triples) - i)
            selected_correct = formatted_triples[i:i + num_correct]
            i += num_correct

            # 选 2~3 个假三元组
            fake_count = random.randint(2, 3)
            fake_samples = random.sample(non_related_triples, k=fake_count)
            fake_options = ["({}, {}, {})".format(*t) for t in fake_samples]

            # 组合并打乱选项
            all_options = selected_correct + fake_options
            random.shuffle(all_options)

            # 编号 A. B. C. ...
            lettered_options = []
            correct_answers = []
            for idx, opt in enumerate(all_options):
                letter = string.ascii_uppercase[idx]
                option_str = f"{letter}. {opt}"
                lettered_options.append(option_str)
                if opt in selected_correct:
                    correct_answers.append(letter)

            multiple_choice_questions.append({
                "instruction": "Select the candidate tuple(s) below that best match the described attack behavior. Multiple or no selections are allowed. Each tuple is in the format (Entity_1, Relation, Entity_2).",
                "input": f"Report: {report}\nOptions:\n" + "\n".join(lettered_options),
                "output": ",".join(correct_answers)
            })

    # 2、构建判断题（构造攻击路径）
    #  构建完整路径（Yes）
    full_path = []
    for group in triple_groups:
        for t in group:
            full_path.extend(t)

    if len(full_path) < 6:
        continue  # 至少两个三元组，跳过过短路径

    true_false_questions.append({
        "instruction": "Determine whether the described attack paths fully support the attack report. Each path consists of multiple entity-relation elements in the format (Entity_1, Relation_1, Entity_2...).",
        "input": f"Report: {report}\nAttack Path: {tuple(full_path)}",
        "output": "Yes"
    })

    #  构建各种子路径（No）
    n = len(triple_groups)
    for i in range(1, n):  # 从1开始，跳过完整长度
        # a -> b
        partial = triple_groups[:i]
        partial_path = []
        for group in partial:
            for t in group:
                partial_path.extend(t)
        true_false_questions.append({
            "instruction": "Determine whether the described attack paths fully support the attack report. Each path consists of multiple entity-relation elements in the format (Entity_1, Relation_1, Entity_2...).",
            "input": f"Report: {report}\nAttack Path: {tuple(partial_path)}",
            "output": "No"
        })

    # 可选：a、b、c 单独也可以当 No，加上这部分也行
    for group in triple_groups:
        if len(group) < 2:
            continue
        partial_path = []
        for t in group:
            partial_path.extend(t)
        true_false_questions.append({
            "instruction": "Determine whether the described attack paths fully support the attack report. Each path consists of multiple entity-relation elements in the format (Entity_1, Relation_1, Entity_2...).",
            "input": f"Report: {report}\nAttack Path: {tuple(partial_path)}",
            "output": "No"
        })


# 共 2788 条
mc_path = "multiple_choice_questions.json"
with open(mc_path, "w", encoding="utf-8") as f:
    json.dump(multiple_choice_questions, f, ensure_ascii=False, indent=2)
print(f" Multiple-choice questions saved to {mc_path}，共 {len(multiple_choice_questions)} 条")

# 共 1127 条
# 保存 true/false 题目
tf_path = "true_false_questions.json"
with open(tf_path, "w", encoding="utf-8") as f:
    json.dump(true_false_questions, f, ensure_ascii=False, indent=2)
print(f" True/False questions saved to {tf_path}，共 {len(true_false_questions)} 条")