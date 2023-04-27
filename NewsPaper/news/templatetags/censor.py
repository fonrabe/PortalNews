from django import template
import re

# Функция ищет пересечение слов в двух списках
def intersection(list1, list2):
    temp = set(list2)
    list3 = [value for value in list1 if value in temp]
    return  list3

list = ['вредные', 'фильтр', 'title']

register = template.Library()

@register.filter()
def censor(text):
    # разбиваем текст на список слов
    list_words = re.findall(r'\b\w+\b', text.lower())
    # определяем нужные слова
    find_words = intersection(list, list_words)

    # заменяем
    for word in find_words:
        l = word[0] + ('*' * (len(word) - 1))
        text = text.replace(word.lower(), l)

    return text
