import re
import math
import json
import string
import pendulum as pum
from typing import List
from numbers import Number
from itertools import chain
from functools import reduce
from random import shuffle,uniform,sample,randint,choices

def random_number(n:int = 1, 
                  only_int:bool = False, only_float:bool = False, 
                  negative:bool = False, 
                  bottom:Number = 1) -> List[Number]|Number:
    keyRand = lambda x: uniform(-1 if negative else 0,1) * abs(bottom*x)
    getInt = lambda x: math.ceil(keyRand(100 * x))
    getFloat = lambda x: keyRand(x)
    intList = [getInt(i) for i in range(1,n+1)]
    floatList = [getFloat(i) for i in range(1,n+1)]
    if only_int :
        return intList[0] if n == 1 else intList
    elif only_float :
        return floatList[0] if n == 1 else floatList
    else:
        aList = intList + floatList
        shuffle(aList)
        return aList[0] if n == 1 else aList[:n]

def random_words(letter:str|None = None,
                 min_letter_count:int = 1,
                 n:int = 1) -> List[str]|str :
    with open("../assets/data/words.dat", 'r') as f:
        alphabeta = json.load(f)
    if letter is None:
        all_words = [w for w 
                     in chain.from_iterable(alphabeta.values()) 
                     if len(w) >= min_letter_count]
        words = sample(all_words, k=n, 
                       counts=random_number(n=len(all_words),only_int=True,bottom=n))
    elif not isinstance(letter, str):
        raise ValueError('Param "letter" must be string.')
    elif not re.match("[a-z]",letter) :
        raise ValueError(
                'Param "letter" must be in {}.'.format(string.ascii_lowercase))
    else:
        all_words = [w for w in alphabeta[letter] if len(w) >= min_letter_count]
        words = sample(all_words, k=n, 
                       counts=random_number(n=len(all_words),only_int=True,bottom=n))
    return words[0] if n == 1 else words

def random_Lorem(n:int = 1, 
                 min_chars:int = 2, max_chars:int = 15,
                 alphabeta:str|List[str]|None = None) -> List[str]|str:
    KEYBOR = alphabeta if alphabeta is not None else string.ascii_lowercase
    wordLen = lambda : randint(min_chars,max_chars)
    getLorem = lambda x: "".join(choices(KEYBOR, k = x))
    struct = [wordLen() for i in range(0,n)]
    list_words = [getLorem(i) for i in struct]
    return list_words[0] if n == 1 else list_words

def randoms(need_word:bool = True, need_number:bool = True,
            need_char:bool = True, need_Lorem:bool = True, 
            n:int = 1) -> List:
    words = random_words(n = (n if n>1 else 25))
    numbs = random_number(n = (n if n>1 else 25))
    chars = random_Lorem(n = (n if n>1 else 25),
                         min_chars=1, max_chars=1,
                         alphabeta=string.printable)
    lores = random_Lorem(n = (n if n>1 else 25))
    res = []
    if need_word :
        res.append(words)
    if need_number :
        res.append(numbs)
    if need_char :
        res.append(chars)
    if need_Lorem :
        res.append(lores)
    if res == []:
        res = [[None, math.inf, math.nan, ""]] * n
    res = reduce(lambda x,y: x+y , res)
    shuffle(res)
    return res[0] if n == 1 else res[:n]

def birthday_random(n = 1, age = 38.8, sformat = None):
    '''
    - n : 需要随机生日的数量
    - age : 设定的平均年龄,
            默认值 38.8
            (来源第七次全国人口普查 http://finance.people.com.cn/n1/2021/0511/c1004-32100001.html )
    - sformat : 输入的日期格式化, 格式参考 https://pendulum.eustace.io/docs/#formatter
    
    - n (default: 1): The number of random birthdays to generate. 
        It must be an integer greater than or equal to 1.
    - age (default: 38.8): The average age to use for calculating the range of possible birthdates. 
        The default value is based on the average age of the 
        population from the seventh national population census in China.
    - sformat (optional): A string format to customize the output of 
        the generated dates. The formatting options can be found in the Pendulum documentation.
    '''
    if n < 1 :
        raise ValueError("The variable `n` must be an integer greater than or equal to 1.")
    today = pum.now()
    MAXAGE = 150 # 参考 https://www.nature.com/articles/s41467-021-23014-1
    resList = [uniform(0, MAXAGE/age) * age for i in range(0,n)]
    resList = [today.subtract(years=int(math.modf(i)[1]),
                              seconds=math.modf(i)[0]*31536000) for i in resList]
    if sformat:
        resList = [i.format(sformat) for i in resList]
    return resList[0] if n == 1 else resList

if __name__ == "__main__" :
    print(randoms(n = 10))