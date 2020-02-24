from django import template

register = template.Library()


def get_index(list, item):
    item_index = list.index(item)
    while list[item_index - 1].votes == item.votes and item_index > 0:
        item_index = item_index - 1
        print(abs(item_index))
    return item_index + 1


register.filter('get_index', get_index)