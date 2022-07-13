import os
import re
import argparse;
import numpy as np;
from pathlib import Path;
from random import shuffle;
# from pygtrans import translate

import translate

def parser_data():
    """
    参考 https://github.com/zhaochenyang20/TOFEL_words_reviewer
    从命令行读取用户参数
    做出如下约定：
    1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
    2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
    3. -s 表示用户希望从第几个单词开始
    4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
    具体的边界条件请查看代码细节
    Returns:
        _type_: _description_
    """
    parser = argparse.ArgumentParser(
        prog="TOELF words reviewer",
        description="choose random or sorted method.",
        allow_abbrev=True,
    )
    parser.add_argument(
        "-n",
        "--num",
        dest="num",
        type=int,
        default=50,
        help="how many words would you like to review",
    )
    parser.add_argument(
        "--r",
        action="store_true",
        dest="random",
        help="if you want to random select, then input --r, ohterwise do not",
    )
    # store_true 是 argpaser 的特殊行为，请自行查找使用方法
    parser.add_argument(
        '-s',
        dest="start",
        type=int,
        default=0,
        help='which index to start reading from',
    )
    parser.add_argument(
        '-l',
        dest="length",
        type=int,
        default=0,
        help='how many words would you randomly choose from',
    )
    args = parser.parse_args()
    return args.random, args.num, args.start, args.length

dictionary = {};
def read_npy_dictionary():
    dictionary_location = str(Path.cwd()/"dict.npy");
    m_dictionary = np.load(dictionary_location,allow_pickle=True).item();
    return m_dictionary;



def find_word(word_to_find):
    word_to_find = word_to_find.strip()

    try:
        answer = dictionary[word_to_find]
    except (KeyError):
        answer = translate.google_word(word_to_find);
    print(answer)
    return answer;



def make_review(random, num, start, length, index):
    """
    部分参考 https://github.com/zhaochenyang20/TOFEL_words_reviewer
    生成单词本的主函数
    Args:
        random ( bool ): 是否生成随机单词本
        num ( int ): 生成单词本所含单词的个数
        start ( int ): 从生词本的第几个单词开始
        length ( int ): 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
        index (_type_): 从 ./data 文件夹下查找所有单词本最大的编号，即 index，将 index + 1 记为当做单词本的编号
    """
    with open("./collection.txt", "r") as f:
        word = list(filter(None, f.read().split("\n")));


    if len(word) <= 0:
        return;

    if random:
        shuffle(word);
    if start < 0:
        start = 0;

    if 0 < length <= len(word):
        if  start + length < len(word):
            word = word[start : start + length];
        else:
            word = word[start:];

    if num > length:
        num = length;

    data_path = Path.cwd()/"data";
    with open(data_path/f"untraslated_{index + 1}.txt", "w") as f:
        for idx, each in enumerate(word):
            similar_words = each.split(",");
            f.write(f"Number {idx + 1}:")
            for word_ in similar_words:
                f.write(f"{word_.strip()} ")
            f.write("\n")

    with open(data_path/f"traslated_{index + 1}.txt", "w") as f:
        for idx, each in enumerate(word):
            similar_words = each.split(",");
            f.write(f"Number {idx + 1}:\n")
            for word_ in similar_words:
                f.write("     ");
                f.write(f"{word_.strip()} :")
                f.write(find_word(word_))
                f.write("\n")


def get_index():
    """
    使用 os.walk 方法来获取所有单词本的编号，返回单词本的最大编号，即 index
    Returns:
        index: 单词本的最大编号
    """
    index = 0
    for _, __, files in os.walk(".\\data"):
        index = 0
        for file in files:
            if file.endswith(".txt"):
                index = max(
                    index, max([int(each) for each in (re.findall(r"\d+", file))])
                )
    return index


def main():
    global dictionary;
    dictionary = read_npy_dictionary();
    # print(find_word("express"));
    # print(find_word("c7w"));
    # print(find_word("anchor"))
    make_review(*parser_data(), get_index())

if __name__ == "__main__":
    main();

del dictionary;