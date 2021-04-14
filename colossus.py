import parser
import os
import sys

if __name__ == '__main__':
    print(' ---- TRANSLATION STARTS ---- ')
    with open(sys.argv[1]) as f:
        source = parser.translate(f.read())

    print(' ---- SOURCE ---- ')
    print(source)

    with open('.source.cpp', 'w') as f:
        f.write(source)

    print(' ---- COMPILATION STARTS ---- ')
    os.system(f'g++ .source.cpp')
    os.system(f'rm .source.cpp')

    if not {"--compile", "-c"} & set(sys.argv):
        print(' ---- LAUNCH STARTS ---- ')
        os.system('./a.out')
