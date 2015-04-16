from    PyQt5.QtGui    import QPalette, QColor
import  PyQt5

def getPalette(key):
    palette = QPalette()

    if key == 'dark':
        colorDict = _getDarkPalette()
    elif key == 'terra':
        colorDict = _getTerraPalette()
    elif key == 'krita':
        colorDict = _getKritaPalette()
    elif key == 'desert':
        colorDict = _getDesertPalette()
    elif key == 'snow':
        colorDict = _getSnowPalette()
    else:
        return palette

    for group in list(colorDict.keys()):
        colorGroup = colorDict[group]
        for role in list(colorGroup.keys()):
            (r, g, b, a)    = colorGroup[role]
            roleColor       = QColor(r,g,b,a)
            palette.setColor(group, role, roleColor)

    return palette

def _getDarkPalette():
    return {
        PyQt5.QtGui.QPalette.Normal: {
            PyQt5.QtGui.QPalette.Foreground: (224, 222, 219, 255),
            PyQt5.QtGui.QPalette.Button: (64, 63, 62, 255),
            PyQt5.QtGui.QPalette.Light: (79, 77, 77, 255),
            PyQt5.QtGui.QPalette.Midlight: (65, 64, 64, 255),
            PyQt5.QtGui.QPalette.Dark: (23, 22, 22, 255),
            PyQt5.QtGui.QPalette.Mid: (41, 40, 40, 255),
            PyQt5.QtGui.QPalette.Text: (212, 210, 207, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (232, 230, 227, 255),
            PyQt5.QtGui.QPalette.Base: (32, 31, 31, 255),
            PyQt5.QtGui.QPalette.Window: (48, 47, 47, 255),
            PyQt5.QtGui.QPalette.Shadow: (16, 16, 16, 255),
            PyQt5.QtGui.QPalette.Highlight: (24, 72, 128, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.Link: (80, 142, 216, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (142, 121, 165, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (36, 35, 35, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (16, 48, 80, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (196, 209, 224, 255)
        },
        PyQt5.QtGui.QPalette.Disabled: {
            PyQt5.QtGui.QPalette.Foreground: (96, 95, 94, 255),
            PyQt5.QtGui.QPalette.Button: (56, 55, 54, 255),
            PyQt5.QtGui.QPalette.Light: (75, 73, 73, 255),
            PyQt5.QtGui.QPalette.Midlight: (61, 59, 59, 255),
            PyQt5.QtGui.QPalette.Dark: (20, 20, 20, 255),
            PyQt5.QtGui.QPalette.Mid: (36, 35, 35, 255),
            PyQt5.QtGui.QPalette.Text: (83, 82, 81, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (108, 106, 105, 255),
            PyQt5.QtGui.QPalette.Base: (28, 27, 27, 255),
            PyQt5.QtGui.QPalette.Window: (42, 41, 41, 255),
            PyQt5.QtGui.QPalette.Shadow: (14, 14, 14, 255),
            PyQt5.QtGui.QPalette.Highlight: (42, 41, 41, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (96, 95, 94, 255),
            PyQt5.QtGui.QPalette.Link: (42, 61, 84, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (62, 55, 68, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (31, 30, 30, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (16, 48, 80, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (196, 209, 224, 255)
        },
        PyQt5.QtGui.QPalette.Inactive: {
            PyQt5.QtGui.QPalette.Foreground: (224, 222, 219, 255),
            PyQt5.QtGui.QPalette.Button: (64, 63, 62, 255),
            PyQt5.QtGui.QPalette.Light: (79, 77, 77, 255),
            PyQt5.QtGui.QPalette.Midlight: (65, 64, 64, 255),
            PyQt5.QtGui.QPalette.Dark: (23, 22, 22, 255),
            PyQt5.QtGui.QPalette.Mid: (41, 40, 40, 255),
            PyQt5.QtGui.QPalette.Text: (212, 210, 207, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (232, 230, 227, 255),
            PyQt5.QtGui.QPalette.Base: (32, 31, 31, 255),
            PyQt5.QtGui.QPalette.Window: (48, 47, 47, 255),
            PyQt5.QtGui.QPalette.Shadow: (16, 16, 16, 255),
            PyQt5.QtGui.QPalette.Highlight: (25, 57, 95, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (224, 222, 219, 255),
            PyQt5.QtGui.QPalette.Link: (80, 142, 216, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (142, 121, 165, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (36, 35, 35, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (16, 48, 80, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (196, 209, 224, 255)
        }
    }

def _getTerraPalette():
    return {
        PyQt5.QtGui.QPalette.Normal: {
            PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255),
            PyQt5.QtGui.QPalette.Button: (203, 194, 191, 255),
            PyQt5.QtGui.QPalette.Light: (226, 220, 211, 255),
            PyQt5.QtGui.QPalette.Midlight: (203, 196, 184, 255),
            PyQt5.QtGui.QPalette.Dark: (92, 88, 83, 255),
            PyQt5.QtGui.QPalette.Mid: (157, 151, 142, 255),
            PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255),
            PyQt5.QtGui.QPalette.Base: (244, 234, 231, 255),
            PyQt5.QtGui.QPalette.Window: (189, 182, 171, 255),
            PyQt5.QtGui.QPalette.Shadow: (57, 55, 52, 255),
            PyQt5.QtGui.QPalette.Highlight: (106, 141, 210, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.Link: (17, 44, 12, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (74, 96, 57, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (235, 226, 223, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (164, 162, 139, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (19, 24, 17, 255)
        },
        PyQt5.QtGui.QPalette.Disabled: {
            PyQt5.QtGui.QPalette.Foreground: (95, 91, 84, 255),
            PyQt5.QtGui.QPalette.Button: (190, 182, 177, 255),
            PyQt5.QtGui.QPalette.Light: (215, 207, 193, 255),
            PyQt5.QtGui.QPalette.Midlight: (192, 185, 172, 255),
            PyQt5.QtGui.QPalette.Dark: (86, 83, 77, 255),
            PyQt5.QtGui.QPalette.Mid: (148, 143, 133, 255),
            PyQt5.QtGui.QPalette.Text: (119, 114, 111, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (101, 97, 93, 255),
            PyQt5.QtGui.QPalette.Base: (226, 217, 212, 255),
            PyQt5.QtGui.QPalette.Window: (178, 171, 159, 255),
            PyQt5.QtGui.QPalette.Shadow: (55, 53, 49, 255),
            PyQt5.QtGui.QPalette.Highlight: (178, 171, 159, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (95, 91, 84, 255),
            PyQt5.QtGui.QPalette.Link: (127, 134, 116, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (152, 156, 136, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (218, 210, 205, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (164, 162, 139, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (19, 24, 17, 255)
        },
        PyQt5.QtGui.QPalette.Inactive: {
            PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255),
            PyQt5.QtGui.QPalette.Button: (203, 194, 191, 255),
            PyQt5.QtGui.QPalette.Light: (226, 220, 211, 255),
            PyQt5.QtGui.QPalette.Midlight: (203, 196, 184, 255),
            PyQt5.QtGui.QPalette.Dark: (92, 88, 83, 255),
            PyQt5.QtGui.QPalette.Mid: (157, 151, 142, 255),
            PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255),
            PyQt5.QtGui.QPalette.Base: (244, 234, 231, 255),
            PyQt5.QtGui.QPalette.Window: (189, 182, 171, 255),
            PyQt5.QtGui.QPalette.Shadow: (57, 55, 52, 255),
            PyQt5.QtGui.QPalette.Highlight: (151, 169, 210, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (0, 0, 0, 255),
            PyQt5.QtGui.QPalette.Link: (17, 44, 12, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (74, 96, 57, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (235, 226, 223, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (164, 162, 139, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (19, 24, 17, 255)
        }
    }



def _getSnowPalette(): return {PyQt5.QtGui.QPalette.Normal: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Light: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Midlight: (233, 233, 233, 255), PyQt5.QtGui.QPalette.Dark: (185, 185, 185, 255), PyQt5.QtGui.QPalette.Mid: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (252, 252, 252, 255), PyQt5.QtGui.QPalette.Shadow: (134, 134, 134, 255), PyQt5.QtGui.QPalette.Highlight: (176, 192, 255, 255), PyQt5.QtGui.QPalette.HighlightedText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Link: (0, 0, 192, 255), PyQt5.QtGui.QPalette.LinkVisited: (88, 0, 176, 255), PyQt5.QtGui.QPalette.AlternateBase: (252, 252, 252, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}, PyQt5.QtGui.QPalette.Disabled: {PyQt5.QtGui.QPalette.Foreground: (164, 164, 164, 255), PyQt5.QtGui.QPalette.Button: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Light: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Midlight: (233, 233, 233, 255), PyQt5.QtGui.QPalette.Dark: (185, 185, 185, 255), PyQt5.QtGui.QPalette.Mid: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Text: (166, 166, 166, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (166, 166, 166, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (252, 252, 252, 255), PyQt5.QtGui.QPalette.Shadow: (134, 134, 134, 255), PyQt5.QtGui.QPalette.Highlight: (252, 252, 252, 255), PyQt5.QtGui.QPalette.HighlightedText: (164, 164, 164, 255), PyQt5.QtGui.QPalette.Link: (166, 166, 233, 255), PyQt5.QtGui.QPalette.LinkVisited: (197, 166, 228, 255), PyQt5.QtGui.QPalette.AlternateBase: (252, 252, 252, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}, PyQt5.QtGui.QPalette.Inactive: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Light: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Midlight: (233, 233, 233, 255), PyQt5.QtGui.QPalette.Dark: (185, 185, 185, 255), PyQt5.QtGui.QPalette.Mid: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (252, 252, 252, 255), PyQt5.QtGui.QPalette.Shadow: (134, 134, 134, 255), PyQt5.QtGui.QPalette.Highlight: (228, 233, 255, 255), PyQt5.QtGui.QPalette.HighlightedText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Link: (0, 0, 192, 255), PyQt5.QtGui.QPalette.LinkVisited: (88, 0, 176, 255), PyQt5.QtGui.QPalette.AlternateBase: (252, 252, 252, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}}

def _getKritaPalette(): return {PyQt5.QtGui.QPalette.Normal: {PyQt5.QtGui.QPalette.Foreground: (20, 20, 20, 255), PyQt5.QtGui.QPalette.Button: (116, 116, 116, 255), PyQt5.QtGui.QPalette.Light: (159, 159, 159, 255), PyQt5.QtGui.QPalette.Midlight: (142, 142, 142, 255), PyQt5.QtGui.QPalette.Dark: (62, 62, 62, 255), PyQt5.QtGui.QPalette.Mid: (108, 108, 108, 255), PyQt5.QtGui.QPalette.Text: (40, 40, 40, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (10, 10, 10, 255), PyQt5.QtGui.QPalette.Base: (160, 160, 160, 255), PyQt5.QtGui.QPalette.Window: (128, 128, 128, 255), PyQt5.QtGui.QPalette.Shadow: (42, 42, 42, 255), PyQt5.QtGui.QPalette.Highlight: (82, 98, 118, 255), PyQt5.QtGui.QPalette.HighlightedText: (180, 180, 180, 255), PyQt5.QtGui.QPalette.Link: (18, 64, 0, 255), PyQt5.QtGui.QPalette.LinkVisited: (5, 0, 82, 255), PyQt5.QtGui.QPalette.AlternateBase: (140, 140, 140, 255), PyQt5.QtGui.QPalette.ToolTipBase: (60, 60, 60, 255), PyQt5.QtGui.QPalette.ToolTipText: (180, 180, 180, 255)}, PyQt5.QtGui.QPalette.Disabled: {PyQt5.QtGui.QPalette.Foreground: (68, 68, 68, 255), PyQt5.QtGui.QPalette.Button: (116, 116, 116, 255), PyQt5.QtGui.QPalette.Light: (159, 159, 159, 255), PyQt5.QtGui.QPalette.Midlight: (142, 142, 142, 255), PyQt5.QtGui.QPalette.Dark: (62, 62, 62, 255), PyQt5.QtGui.QPalette.Mid: (108, 108, 108, 255), PyQt5.QtGui.QPalette.Text: (94, 94, 94, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (57, 57, 57, 255), PyQt5.QtGui.QPalette.Base: (160, 160, 160, 255), PyQt5.QtGui.QPalette.Window: (128, 128, 128, 255), PyQt5.QtGui.QPalette.Shadow: (42, 42, 42, 255), PyQt5.QtGui.QPalette.Highlight: (128, 128, 128, 255), PyQt5.QtGui.QPalette.HighlightedText: (68, 68, 68, 255), PyQt5.QtGui.QPalette.Link: (86, 106, 78, 255), PyQt5.QtGui.QPalette.LinkVisited: (75, 73, 110, 255), PyQt5.QtGui.QPalette.AlternateBase: (140, 140, 140, 255), PyQt5.QtGui.QPalette.ToolTipBase: (60, 60, 60, 255), PyQt5.QtGui.QPalette.ToolTipText: (180, 180, 180, 255)}, PyQt5.QtGui.QPalette.Inactive: {PyQt5.QtGui.QPalette.Foreground: (20, 20, 20, 255), PyQt5.QtGui.QPalette.Button: (116, 116, 116, 255), PyQt5.QtGui.QPalette.Light: (159, 159, 159, 255), PyQt5.QtGui.QPalette.Midlight: (142, 142, 142, 255), PyQt5.QtGui.QPalette.Dark: (62, 62, 62, 255), PyQt5.QtGui.QPalette.Mid: (108, 108, 108, 255), PyQt5.QtGui.QPalette.Text: (40, 40, 40, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (10, 10, 10, 255), PyQt5.QtGui.QPalette.Base: (160, 160, 160, 255), PyQt5.QtGui.QPalette.Window: (128, 128, 128, 255), PyQt5.QtGui.QPalette.Shadow: (42, 42, 42, 255), PyQt5.QtGui.QPalette.Highlight: (104, 119, 137, 255), PyQt5.QtGui.QPalette.HighlightedText: (20, 20, 20, 255), PyQt5.QtGui.QPalette.Link: (18, 64, 0, 255), PyQt5.QtGui.QPalette.LinkVisited: (5, 0, 82, 255), PyQt5.QtGui.QPalette.AlternateBase: (140, 140, 140, 255), PyQt5.QtGui.QPalette.ToolTipBase: (60, 60, 60, 255), PyQt5.QtGui.QPalette.ToolTipText: (180, 180, 180, 255)}}
