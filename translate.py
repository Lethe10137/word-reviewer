from pygtrans import Translate



def google_word(word_to_find):
    """
    The following commented codes work sometimes,however performances rather volatile.
    input : a word to be translated
    output: translating result or "****FAILED_TO_BE_TRANSLATED****"
    """
    answer = "****FAILED_TO_BE_TRANSLATED****"
    # try:
    #     client = Translate()
    #     text = client.translate(word_to_find);
    #     answer = text.translatedText;
    #     # answer = translator.translate(word_to_find, dest="zh-CN").text;
    # except:
    #     pass
    return answer;

