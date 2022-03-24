#Generate codes for console patches.
#Supported platform and formats: PS3 (RPCS3 Game Patches), PS4 (py-patch), Xbox 360 (Xenia Game Patches)
#Note that PS4 must have the address base set to 0x400000, to match disabled ASLR address.
#Usage:
#Check the tickbox for the script
#Highlight your code
#Press the keybind

#@author illusion0001
#@category Conversion
#@keybinding Alt-Shift-Q
#@menupath
#@toolbar

from binascii import hexlify

def getdata(codeUnit):
    address        = (codeUnit.getAddress())
    value          = (hexlify(codeUnit.getBytes()))
    oprand_comment = (codeUnit.toString())
    return address, value, oprand_comment

# https://blog.finxter.com/how-to-find-the-longest-string-in-a-python-list
def get_max_str(lst):
    return max(lst, key=len)

def gen_patch():
        # https://github.com/lwerdna/ghidra/blob/master/XorMemoryScript.py
        if currentSelection is None or currentSelection.isEmpty():
            print("Use your mouse to highlight data to generation patch. then press Alt-Shift-Q to generate code.")
            return # exit
                   # else
        # https://github.com/HackOvert/GhidraSnippets#print-all-instructions-in-a-select-function
        processor = str(currentProgram.getLanguageID())
        listing   = currentProgram.getListing()
        addrSet   = currentSelection
        minAddr   = str(currentProgram.getMinAddress())
        codeUnits = listing.getCodeUnits(addrSet, True)

        if processor == 'PowerPC:BE:64:64-32addr' or processor == 'PowerPC:BE:64:A2-32addr': # PS3
            print('Platform is PS3 ({0}).'.format(processor))
            for codeUnit in codeUnits:
                getdata(codeUnit)
                addr, val, oprand = getdata(codeUnit)
                print('- [ be32, 0x{0}, 0x{1} ] # {2}'.format(addr, val, oprand))
        elif processor == 'PowerPC:BE:64:VLE-32addr': # X360
            print('Platform is Xbox 360 ({0}).'.format(processor))
            for codeUnit in codeUnits:
                getdata(codeUnit)
                addr, val, oprand = getdata(codeUnit)
                print('    [[patch.be32]]\n'
                      '        address = 0x{0}\n'
                      '        value = 0x{1} # {2}'.format(addr, val, oprand))
        elif processor == 'x86:LE:64:default':
            if minAddr == '00400000':
                # use 0x400000 (disabled aslr) addr for now
                # who knows what the correct one will be
                print('Image Base {} is correct.'.format(minAddr))
                print('Platform is PS4 ({0}).'.format(processor))
                patch_list  = []
                oprand_list = []
                for codeUnit in codeUnits:
                    getdata(codeUnit)
                    addr, val, oprand = getdata(codeUnit)
                    patch = '- [ bytes, 0x{0}, \"{1}\" ]'.format(addr, val) # thanks aero+kiwi
                    patch_list.append(patch)
                    oprand_list.append(oprand)
                length = (get_max_str(patch_list))
                real_length = (len(length))
                for patch, oprand in zip(patch_list, oprand_list):
                    print('{0:<{2}} # {1}'.format(patch, oprand, real_length))
            else:
                print('Image Base {} is not correct, patch address will be wrong! Make sure it is set to 0x400000.\nExiting script.'.format(minAddr))
                return
        else:
            print('Processor: {} is not supported!\nExiting script.'.format(processor))
            return

gen_patch()
