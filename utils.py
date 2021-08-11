def out(status, message, padding=0, custom=None):
    if status == '?':
        return input(
            ' ' * padding
            + '\033[1;36m'
            + '[?]'
            + '\033[0;0m'
            + ' ' + message
            + ': '
        )
    elif status == 'I':
        print(
            ' ' * padding
            + '\033[1;32m['
            + (str(custom) if custom != None else 'I')
            + ']\033[0;0m'
            + ' '
            + message
        )
    elif status == 'E':
        print(
            ' ' * padding
            + '\033[1;31m['
            + (str(custom) if custom != None else 'E')
            + ']\033[0;0m'
            + ' '
            + message
        )
    elif status == 'W':
        print(
            ' ' * padding
            + '\033[1;33m['
            + (str(custom) if custom != None else 'W')
            + ']\033[0;0m'
            + ' '
            + message
        )
