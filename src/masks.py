def get_mask_card_number(number: int) -> str:
    """Функция маскировки номера банковской карты"""

    some_list = []
    conv_number = str(number)
    count_stars = "*" * (len(conv_number) - 10)
    divide_number = f"{conv_number[:6]}{count_stars}{conv_number[-4:]}"

    for i in range(0, len(conv_number), 4):
        some_list.append(divide_number[i : i + 4])
    return " ".join(some_list)


def get_mask_card_account(number: int) -> str:
    """Функция маскировки номера банковского счёта"""
    conv_number = str(number)
    return f"**{conv_number[-4:]}"


print(get_mask_card_number(7000792289606361))
print(get_mask_card_account(73654108430135874305))
