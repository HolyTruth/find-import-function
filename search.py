from elftools.elf.elffile import ELFFile
import os,sys

def success(s):
    print('[+] %s'%s)
def fail(s):
    print('[-] %s'%s)
    exit(1)
def info(s):
    print('[*] %s'%s)
def finish():
    success('all done!')
    exit()

def getLibList(binaryName):
    # 获得二进制文件导入的动态库列表
    with open(binaryName,'rb') as f:
        elf = ELFFile(f)
        libList = []
        segs = elf.iter_segments()
        for seg in segs:
            if seg.header.p_type != 'PT_DYNAMIC':
                continue
            for i in seg.iter_tags():
                if i.entry.d_tag == 'DT_NEEDED':
                    libList.append(i.needed)
        if libList == [] :
            fail(f'nothing found! error in {sys._getframe().f_code.co_name} !')
        return libList

def getImportSymList(binaryName):
    # 获得二进制文件所有导入符号
    with open(binaryName,'rb') as f:
        elf = ELFFile(f)
        symbolList = []
        segs = elf.iter_segments()
        for seg in segs:
            if seg.header.p_type != 'PT_DYNAMIC':
                continue
            for i in seg.iter_symbols():
                symbolList.append(i.name)
        if symbolList == [] :
            fail(f'nothing symbol found! error in {sys._getframe().f_code.co_name} !')
    return symbolList

def isImport(binaryName, funName):
    # 检查指定函数是否是导入函数
    symList = getImportSymList(searchLib(binaryName))
    return funName in symList

def searchLib(libName ,rootPath='.'):
    # 根据文件名找到动态库, 默认在当前目录寻找
    for dir, _, fnList in os.walk(rootPath):
        for fn in fnList:
            if fn == libName:
                path = os.path.join(dir,fn)
                # info(f'found lib:{path}')
                return path

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        print(f'[*] usage: python {argv[0]} <binary> <first_expect_fun> [ second_expect_fun ...]')
        exit(1)
    binary = argv[1]
    expectList = []
    libList = getLibList(binary)
    continueFlag = 0

    # 检查是否存在非导入函数
    for expectFun in argv[2:]:
        if not isImport(binary, expectFun):
            info(f'{expectFun} is not an import function!')
            continue
        expectList.append(expectFun)

    # 搜索导入函数归属
    for lib in libList:
        if expectList == []:
            finish()
        symList = getImportSymList(searchLib(lib))
        tmpList = expectList[::]

        for expectFun in expectList:
            if expectFun in symList:
                success(f'Found {expectFun} in {lib}!')
                tmpList.pop(tmpList.index(expectFun))

        if len(expectList) != len(tmpList):
            expectList = tmpList[::]
    
    if expectList:
        print('################################################')
        print('##################### WARNING ##################')
        print('################################################')
        print('\n[-] here is not found function:')
        for fun in expectList:
            print(f'\t{fun}')
    