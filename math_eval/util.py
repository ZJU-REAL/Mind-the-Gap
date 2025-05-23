import os
import json

def parse_ground_truth(example, data_name):
    if data_name in [
        "math",
        "math500",
        "aime",
        "aime24",
    ]:
        gt_cot, gt_ans = example["solution"], example["answer"]
    elif data_name == "gsm8k":
        gt_cot, gt_ans = example["answer"].split("####")
    elif data_name == "gaokao2023en":
        gt_cot, gt_ans = None, example["answer"].replace("$", "").strip()
    elif data_name == "olympiadbench":
        gt_cot, gt_ans = None, example["final_answer"][0].strip("$")
    elif data_name == "odyssey":
        gt_cot, gt_ans = example["reasoning"], example["answer"]
    elif data_name in [
        "amc23",
        "mathematics",
        "aime25"
    ]:
        gt_cot, gt_ans = None, example["answer"]
    else:
        raise NotImplementedError(f"`{data_name}`")
    return gt_cot, gt_ans


def parse_question(example, data_name):
    question = ""
    for key in ["question", "problem", "Question", "input"]:
        if key in example:
            question = example[key]
            break
    return question.strip()

def load_jsonl(file):
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except:
                print("Error in loading:", line)
                exit()

def load_data(data_name, split, data_dir="./data"):
    data_file = f"{data_dir}/{data_name}/{split}.jsonl"
    if os.path.exists(data_file):
        examples = list(load_jsonl(data_file))
    return examples

EXAMPLES = [(
            "There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?",
            "There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is 6.",
        ),
        (
            "If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?",
            "There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. The answer is 5.",
        ),
        (
            "Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?",
            "Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is 39.",
        ),
        (
            "Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?",
            "Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. The answer is 8.",
        )]