import os
import sys
import win32print
import win32api
import ghostscript
import locale

USELESS_PRINTER = ['OneNote for Windows 10', 'OneNote (Desktop)', 'Microsoft XPS Document Writer',
                   'Microsoft Print to PDF', 'Fax']

HELP = """pyPrinter - Author: Arthur SICARD - Date: 19/05/2021
\n-help
\tDisplay this message.
\n-list [-virtual]
\tReturn list of available printer (excepted: """ + ", ".join(USELESS_PRINTER) + """)
\n-file filepath [-printer printer_name] [-virtual]
\tPrint specified file on default system printer. Use -printer to specify printer to use. Printer name must be available un -list response.
\n-batch filepath [-printer printer_name] [-virtual]
\tPrint each document specified un batch file on default system printer. Batch file must be a .txt. Each file to print must be write on its own line.
\tUse -printer to specify printer to use. Printer name must be available un -list response.
\n-virtual
\tUse this option after all other arguments to enable printing on virtual printer 'Microsoft Print to PDF'
"""


# Safe accessor to argv. Return None if index is not set
def getArgv(index):
    try:
        return (sys.argv[1:])[index]
    except:
        return None


# Return list of local printer available without "virtual printer" define in USELESS_PRINTER list.
def getAvailablePrinters():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
    printer_list = []
    for x in range(len(printers)):
        if printers[x][2] not in USELESS_PRINTER:
            printer_list.append(printers[x][2])
    return printer_list


# Return printer name to use. If -printer is set it will return this value only if value match with available
# printers list. Return a error if -printer not in list. If no printer specified, retrieve default printer and return
# its name. Sometime default printer is on USELESS_PRINTER list so first printer return by getAvailablePrinters() is
# return. If no printer is return display an error.
def getPrinter():
    default_printer = win32print.GetDefaultPrinter()
    if default_printer in USELESS_PRINTER:
        if len(getAvailablePrinters()) == 0:
            print("No printer available, unable to print. Use -virtual if you want enable virtual printer.")
            sys.exit(1801)
        default_printer = getAvailablePrinters()[0]
    if getArgv(2) is not None:
        if getArgv(2) == "-printer":
            printer = getArgv(3)
            if printer in getAvailablePrinters():
                return printer
            else:
                if printer is not None:
                    print("Given printer not found. Defaut printer configured: ", default_printer)
    return default_printer


# Use GhostScript API to silent print .pdf and .ps. Use win32api to print .txt. Return a error if printing failed or
# file ext doesn't match.
def printFile(filepath):
    try:
        if os.path.splitext(filepath)[1] in [".pdf", ".ps"]:
            args = [
                "-dPrinted", "-dBATCH", "-dNOSAFER", "-dNOPAUSE", "-dNOPROMPT"
                                                                  "-q",
                "-dNumCopies#1",
                "-sDEVICE#mswinpr2",
                f'-sOutputFile#"%printer%{getPrinter()}"',
                f'"{filepath}"'
            ]

            encoding = locale.getpreferredencoding()
            args = [a.encode(encoding) for a in args]
            ghostscript.Ghostscript(*args)
        elif os.path.splitext(filepath)[1] in [".txt"]:
            # '"%s"' % enable to encapsulate string with quote
            win32api.ShellExecute(0, "printto", '"%s"' % filepath, '"%s"' % getPrinter(), ".", 0)
        return True

    except:
        print("Printing error for file: ", '"%s"' % filepath, "| Printer: ", '"%s"' % getPrinter())
        return False


def main(argv):
    if len(argv) in [1, 2, 4, 5]:
        cmd1 = getArgv(0)
        filepath = getArgv(1)

        if argv[-1] == "-virtual":
            USELESS_PRINTER.remove('Microsoft Print to PDF')

        # Batch printing mode
        if cmd1 == "-batch" and len(argv) in [2, 4, 5]:
            if not os.path.isfile(filepath) and not os.path.exists(filepath):
                print("Path provide for batch file is not a valid file path or doesn't exist.")
                sys.exit(2)
            if os.path.splitext(filepath)[1] in [".txt"]:
                with open(filepath) as fp:
                    line = fp.readline().strip('\n')
                    while line:
                        if not os.path.isfile(line) and not os.path.exists(line):
                            print("Path provide is not a valid file path or doesn't exist: ", line)
                        else:
                            printFile(line)
                        line = fp.readline().strip('\n')
                fp.close()
            else:
                print("Not supported file format for batch printing.")
                sys.exit(50)

        # Single file printing mode
        elif cmd1 == "-file" and len(argv) in [2, 4, 5]:
            if not os.path.isfile(filepath) and not os.path.exists(filepath):
                print("Path provide is not a file path.")
                sys.exit(2)
            if not printFile(filepath):
                sys.exit(1)

        # Get printers list
        elif cmd1 == "-list" and len(argv) in [1, 2]:
            for printer in getAvailablePrinters():
                print(printer)

        # Display help
        elif cmd1 == "-help" and len(argv) in [1]:
            print(HELP)
            sys.exit(0)
        else:
            print("Unknow option. Use -help to obtain more informations about supported options.")
            sys.exit(50)
    else:
        print("Wrong arguments number. Use -help to obtain more informations about supported options.")
        sys.exit(50)
    exit(0)


if __name__ == '__main__':
    main(sys.argv[1:])