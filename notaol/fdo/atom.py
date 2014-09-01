import enum


class AtomType(enum.IntEnum):
    UNI = 0
    '''Responsible for governing the flow of streams'''

    MAN = 1
    '''Responsible for the structure of forms and creation of objects'''

    ACT = 2
    '''Responsible for controling the action streams in a form'''

    DE = 3
    '''Works directly with client buffers to extract and store data from objects'''

    BUF = 4
    '''Used to handle the client buffer system. These buffers hold data sent to the host or stored in main.idx'''

    IDB = 5
    '''Used to store and retrieve data from main.idx'''

    XFER = 7

    FM = 8
    '''File Manager. Used to do limited direct Input/Output with the users hard drive'''

    LM = 9

    CM = 10
    '''Manages all the *.tol tools in the /tool/ directory. Verifys tools for TODs and replacements'''

    CHAT = 11

    VAR = 12
    '''Responsible for movign data in and out of the client registers'''

    ASYNC = 13
    '''Handles messageboxes and screen name issues'''

    SM = 14
    '''A collection of shorthand atoms'''

    IF = 15
    '''Responsible for allowing the programmer to test conditions'''

    MAT = 16
    '''Responsible for setting flags used to define forms created with MAN'''

    MIP = 17
    MMI = 20
    IMGXFER = 21
    IMAGE = 22
    CHART = 23
    MORG = 24
    RICH = 25
    EXAPI = 26
    DOD = 27
    RADIO = 28
    PICTALK = 29
    IRC = 30
    DOC = 31
    CCL = 34
    P3 = 35
    AD = 39
    APP = 40
    MT = 42
    MERC = 43
    VRM = 47
    WWW = 48
    JAVA = 49
    HFS = 51
    BLANK = 52
    VID = 53
    ACTIVEX = 54
    SEC_IP = 55
    GALLERY = 56
    DICE = 57
    PHONE = 60
    SPELL = 61
    ARTEXP = 62
    MF = 63
    PLUGIN = 64
    SLIDER = 65
    ADP = 66
    MAP = 69
    SAGE = 70
    BUDDY = 73
    COMIT = 74
    HTMLVIEW = 75
    DPC = 76
    SAP = 77
