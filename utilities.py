def st(style: str, msg: str) -> str:
    """
    Method to format a string based on style.

    Parameters:
    style (str): Style to choose.
    msg (str): String to format.

    Returns:
    str: msg formated.
    """

    styles = {
        # Colors Definition
        "HEADER": "\033[95m",
        "BLUE": "\033[94m",
        "CYAN": "\033[96m",
        "GREEN": "\033[92m",
        "OK": "\033[92m[OK]: ",
        "YEL": "\033[93m",
        "WARN": "\033[93m[WARNING]: ",
        "RED": "\033[91m",
        "ERROR": "\033[91m[ERROR]: ",
        "ENDC": "\033[0m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
    }

    if style.upper() in styles.keys():
        return f"{styles[style.upper()]}{msg}{styles['ENDC']}"
    else:
        print(
            f"{styles['ERROR']}"
            f"No style available to transform the string {msg}"
        )
        exit(1)

def format_es(n, decimals=2):
    return f"{n:,.{decimals}f}".replace(",", " ")
