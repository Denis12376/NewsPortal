from django import template

register = template.Library()

BLOCK_WORD = {
    'побит': 'по*ит',
}


@register.filter()
def censor(text):
    """
    Фильтр для замены запрещенных слов
    text: значение, к которому нужно применить фильтр
    """
    if not isinstance(text, str):
        return text
    words = text.split()

    processed_words = []
    for word in words:
        clean_word = word.strip('.,!?;:"()[]{}')

        if clean_word.lower() in BLOCK_WORD:
            replacement = BLOCK_WORD[clean_word.lower()]
            if clean_word and clean_word[0].isupper():
                replacement = replacement.capitalize()
            if word != clean_word:
                prefix = word[:len(word) - len(word.lstrip())]
                suffix = word[len(word.rstrip()):]
                replacement = prefix + replacement + suffix

            processed_words.append(replacement)
        else:
            processed_words.append(word)
    return ' '.join(processed_words)


@register.filter
def sort_by_time_desc(posts):
    """
    Сортировка постов от новых к старым
    """
    if not posts:
        return []
    try:
        # Для QuerySet
        if hasattr(posts, 'order_by'):
            return posts.order_by('-created_at')
        else:
            return sorted(posts, key=lambda x: x.created_at, reverse=True)
    except (AttributeError, TypeError):
        return posts