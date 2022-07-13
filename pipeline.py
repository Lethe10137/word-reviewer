import os


def pipline():
    """
    参考 https://github.com/zhaochenyang20/TOFEL_words_reviewer
    批量生成 10 个单词本
    """
    import os
    for _ in range(10):
        os.system("python test.py --r -n 100")


if __name__ == "__main__":
    pipline()