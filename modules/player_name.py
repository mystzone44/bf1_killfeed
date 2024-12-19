import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
common_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

available_nickname_symbols = f'{common_symbols}-_[]'

def recognize_player(image) -> str:
    text: str = pytesseract.image_to_string(image, lang = 'bf1', config = f'--psm 7 --oem 3 -c tessedit_char_whitelist={available_nickname_symbols}')
    words = text.strip() # string cleanup
    return words or None