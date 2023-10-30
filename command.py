import backend

HELP_TEXT='''欢迎使用 JBPhiSystem

'''


def Command(RawCommand):
    CommandArg=RawCommand.split(' ')
    if CommandArg[0]=='help':
        print(HELP_TEXT)
    elif CommandArg[0]=='get':
        backend.GetData()
    elif CommandArg[0]=='exit':
        return 'EX'
    else:
        return 'NF'