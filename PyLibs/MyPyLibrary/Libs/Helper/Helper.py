from Libs.Misc import *
from Libs.IO.FileIo import *

def every(iter, n):
    for i in range(0, len(iter), n):
        yield iter[i : i + n]

def ForEachFile(filelist, callback, filter = '*.*'):
    if type(filelist) == str:
        filelist = [filelist]

    for f in filelist:
        if os.path.isdir(f):
            for x in EnumDirectoryFiles(f, filter):
                callback(x)
        else:
            callback(f)

def TryForEachFile(filelist, callback, filter = '*.*'):
    TryInvoke(ForEachFile, filelist, callback, filter)

def TryForEachFileMP(filelist, callback, filter = '*.*'):
    TryInvoke(ForEachFileMP, filelist, callback, filter)


def ForEachFileMPInvoker(cb, flist):
    for f in flist:
        cb(f)

def ForEachFileMP(filelist, callback, filter = '*.*'):
    if type(filelist) == str:
        filelist = [filelist]

    allfile = []
    for f in filelist:
        if os.path.isdir(f):
            allfile += EnumDirectoryFiles(f, filter)
        else:
            allfile.append(f)

    if len(allfile) == 0:
        return

    import multiprocessing

    core = multiprocessing.cpu_count()
    if core == 1:
        return ForEachFileMPInvoker(callback, allfile)

    files = []
    step = int(len(allfile) / core + 1)
    n = 0
    for i in range(core):
        files.append(allfile[n:n + step])
        n += step

    process = []
    for f in range(len(files) - 1):
        f = files[f]
        t = multiprocessing.Process(target = ForEachFileMPInvoker, args = [callback, f])
        t.start()
        process.append(t)

    ForEachFileMPInvoker(callback, files[-1])

    for t in process:
        t.join()

def TryInvoke(method, *values):
    try:
        return method(*values) if len(values) != 0 else method()
    except Exception as e:
        #traceback.print_exception(type(e), e, e.__traceback__)
        #exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(*sys.exc_info())
        PauseConsole()

    return None

def TryInvokeDbg(method, *values):
    try:
        return method(*values) if len(values) != 0 else method()
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        bp()

    return None

def ReadTextToList(filename, cp = '936'):
    stm = open(filename,'rb').read()
    if stm[0:2] == b'\xff\xfe':
        stm = stm.decode('U16')
    elif stm[0:3] == b'\xef\xbb\xbf':
        stm = stm.decode('utf-8-sig')
    else:
        try:
            stm = stm.decode(cp)
        except UnicodeDecodeError:
            stm = stm.decode('UTF8')

    return stm.replace('\r\n','\n').replace('\r','\n').split('\n')
