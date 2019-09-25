#! /usr/bin/env python3


def text_to_pascal_case(text, remove_spaces=True):
    if text is None or len(text) == 0:
        return ''

    if remove_spaces:
        return text.replace('_', ' ').replace('-', ' ').title().replace(' ', '')

    return text.replace('_', ' ').replace('-', ' ').title()


def normalize(value, in_min, in_max, out_min, out_max):
    return ( ((value - in_min)/(in_max - in_min)) * (out_max - out_min)) + out_min
