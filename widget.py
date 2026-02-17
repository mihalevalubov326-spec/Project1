def mask_account_card(card_info: str) -> str:
    """Функция обработки информации о карте"""

    parts = card_info.rsplit(" ", 1)

    if len(parts) != 2:
        return card_info

    name_part, number = parts

    if name_part.strip() == "Счет":
        if len(number) >= 4:
            masked_number = "**" + number[-4:]
        else:
            masked_number = number
    else:
        if len(number) == 16:
            masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        elif len(number) >= 8:
            masked_number = number[:4] + " ** **** " + number[-4:]
        else:
            masked_number = number

    return f"{name_part} {masked_number}"

print(mask_account_card("Maestro 7000792289606361"))

def get_date(date_string: str) -> str:
    """Преобразует ISO дату в формат ДД.ММ.ГГГГ"""
    date_part = date_string.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"

formatted_date = get_date("2024-03-11T02:26:18.671407")
print("Отформатированная дата:", formatted_date)
