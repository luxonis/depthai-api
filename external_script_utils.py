def unindentMethod(methodString):
    lines = methodString.split('\n')
    methodString = ''
    for line in lines:
        if len(line)>4 and line[0:3] != 'def':
            methodString+=line[4:]+'\n'
    return(methodString)