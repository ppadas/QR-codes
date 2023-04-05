#поменять FN и FU


def encoding_stat(object_info):
    '''
    Логика: 
    Статистика по элементам markup
    Eсли кто-то из result с нами пересекается, то считаем, что нас нашли (выбираем bbox с наибольшей площадью пересечения).
    Результат в таком случае: TP или FU или NO_INFO в зависимости от результата декодирования найденного bbox из result
    Если с нами никто не пересекается, то FN

    Аргументы:
    object_info: словарь, который содержит ключи "image", "result", "markup"
    '''

    if "image" not in object_info or \
       "result" not in object_info or \
       "markup" not in object_info:
        raise Exception("Report object error")
    
    for markup_value in object_info["markup"]:
        bbox_markup = markup_value["bbox"]
        max_intersection = 0
        most_similar_result = None
        for markup_value in object_info["result"]:
            # нужно ли проверять тип
            bbox_result = markup_value["bbox"]
            current_intersection = compute_intersection(bbox_markup, bbox_result)
            if current_intersection > max_intersection:
                max_intersection = current_intersection
                most_similar_result = markup_value
    
        if max_intersection != 0:
            if "decoded" not in most_similar_result:
                return "NO_INFO"
            elif most_similar_result["decoded"]:
                return "TP"
            else:
                return "FU"
        else:
            return "FN"


def compute_intersection(box_1, box_2):
    x_left = max(box_1[0], box_2[0])
    x_right = min(box_1[0] + box_1[2], box_2[0] + box_2[2])
    y_top = max(box_1[1], box_2[1])
    y_bottom = min(box_1[1] + box_1[3], box_2[1] + box_2[3])

    if x_left > x_right or y_top > y_bottom:
        return 0
    else:
        return (x_right - x_left) * (y_bottom - y_top)
