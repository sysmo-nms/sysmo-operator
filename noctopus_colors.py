from    PyQt5.QtGui    import QPalette, QColor
import  PyQt5

def getPalette(key):
    palette = QPalette()

    if key == 'dark':
        colorDict = _getDarkPalette()
    elif key == 'wintest':
        colorDict = _getWintestPalette()
    elif key == 'terra':
        colorDict = _getTerraPalette()
    elif key == 'lagoon':
        colorDict = _getLagoonPalette()
    elif key == 'krita':
        colorDict = _getKritaPalette()
    elif key == 'desert':
        colorDict = _getDesertPalette()
    elif key == 'honey':
        colorDict = _getHoneyPalette()
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

def _getLagoonPalette():
    return {
        PyQt5.QtGui.QPalette.Normal: {
            PyQt5.QtGui.QPalette.Foreground: (206, 227, 213, 255),
            PyQt5.QtGui.QPalette.Button: (63, 85, 135, 255),
            PyQt5.QtGui.QPalette.Light: (130, 169, 215, 255),
            PyQt5.QtGui.QPalette.Midlight: (109, 151, 199, 255),
            PyQt5.QtGui.QPalette.Dark: (48, 66, 87, 255),
            PyQt5.QtGui.QPalette.Mid: (84, 116, 152, 255),
            PyQt5.QtGui.QPalette.Text: (205, 197, 231, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (227, 217, 201, 255),
            PyQt5.QtGui.QPalette.Base: (48, 65, 105, 255),
            PyQt5.QtGui.QPalette.Window: (99, 137, 180, 255),
            PyQt5.QtGui.QPalette.Shadow: (32, 45, 59, 255),
            PyQt5.QtGui.QPalette.Highlight: (122, 102, 41, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.Link: (31, 147, 218, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (59, 114, 214, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (55, 62, 79, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (67, 91, 122, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (247, 234, 234, 255)
        },
        PyQt5.QtGui.QPalette.Disabled: {
            PyQt5.QtGui.QPalette.Foreground: (120, 148, 168, 255),
            PyQt5.QtGui.QPalette.Button: (55, 74, 118, 255),
            PyQt5.QtGui.QPalette.Light: (109, 151, 198, 255),
            PyQt5.QtGui.QPalette.Midlight: (97, 134, 177, 255),
            PyQt5.QtGui.QPalette.Dark: (42, 58, 77, 255),
            PyQt5.QtGui.QPalette.Mid: (74, 102, 134, 255),
            PyQt5.QtGui.QPalette.Text: (90, 97, 131, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (106, 115, 139, 255),
            PyQt5.QtGui.QPalette.Base: (42, 57, 92, 255),
            PyQt5.QtGui.QPalette.Window: (87, 120, 158, 255),
            PyQt5.QtGui.QPalette.Shadow: (29, 40, 53, 255),
            PyQt5.QtGui.QPalette.Highlight: (87, 120, 158, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (120, 148, 168, 255),
            PyQt5.QtGui.QPalette.Link: (37, 82, 127, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (45, 72, 126, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (48, 54, 69, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (67, 91, 122, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (247, 234, 234, 255)
        },
        PyQt5.QtGui.QPalette.Inactive: {
            PyQt5.QtGui.QPalette.Foreground: (206, 227, 213, 255),
            PyQt5.QtGui.QPalette.Button: (63, 85, 135, 255),
            PyQt5.QtGui.QPalette.Light: (130, 169, 215, 255),
            PyQt5.QtGui.QPalette.Midlight: (109, 151, 199, 255),
            PyQt5.QtGui.QPalette.Dark: (48, 66, 87, 255),
            PyQt5.QtGui.QPalette.Mid: (84, 116, 152, 255),
            PyQt5.QtGui.QPalette.Text: (205, 197, 231, 255),
            PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255),
            PyQt5.QtGui.QPalette.ButtonText: (227, 217, 201, 255),
            PyQt5.QtGui.QPalette.Base: (48, 65, 105, 255),
            PyQt5.QtGui.QPalette.Window: (99, 137, 180, 255),
            PyQt5.QtGui.QPalette.Shadow: (32, 45, 59, 255),
            PyQt5.QtGui.QPalette.Highlight: (133, 124, 79, 255),
            PyQt5.QtGui.QPalette.HighlightedText: (206, 227, 213, 255),
            PyQt5.QtGui.QPalette.Link: (31, 147, 218, 255),
            PyQt5.QtGui.QPalette.LinkVisited: (59, 114, 214, 255),
            PyQt5.QtGui.QPalette.AlternateBase: (55, 62, 79, 255),
            PyQt5.QtGui.QPalette.ToolTipBase: (67, 91, 122, 255),
            PyQt5.QtGui.QPalette.ToolTipText: (247, 234, 234, 255)
        }
    }


def _getDesertPalette(): return {PyQt5.QtGui.QPalette.Normal: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (217, 211, 197, 255), PyQt5.QtGui.QPalette.Light: (247, 245, 242, 255), PyQt5.QtGui.QPalette.Midlight: (223, 217, 202, 255), PyQt5.QtGui.QPalette.Dark: (102, 99, 92, 255), PyQt5.QtGui.QPalette.Mid: (173, 168, 156, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (252, 251, 247, 255), PyQt5.QtGui.QPalette.Window: (210, 204, 190, 255), PyQt5.QtGui.QPalette.Shadow: (60, 59, 54, 255), PyQt5.QtGui.QPalette.Highlight: (125, 10, 10, 255), PyQt5.QtGui.QPalette.HighlightedText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Link: (0, 102, 255, 255), PyQt5.QtGui.QPalette.LinkVisited: (117, 87, 182, 255), PyQt5.QtGui.QPalette.AlternateBase: (248, 247, 244, 255), PyQt5.QtGui.QPalette.ToolTipBase: (229, 221, 210, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}, PyQt5.QtGui.QPalette.Disabled: {PyQt5.QtGui.QPalette.Foreground: (102, 99, 92, 255), PyQt5.QtGui.QPalette.Button: (200, 195, 182, 255), PyQt5.QtGui.QPalette.Light: (232, 227, 216, 255), PyQt5.QtGui.QPalette.Midlight: (208, 202, 188, 255), PyQt5.QtGui.QPalette.Dark: (94, 91, 85, 255), PyQt5.QtGui.QPalette.Mid: (161, 156, 145, 255), PyQt5.QtGui.QPalette.Text: (120, 119, 117, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (105, 102, 95, 255), PyQt5.QtGui.QPalette.Base: (231, 230, 226, 255), PyQt5.QtGui.QPalette.Window: (194, 188, 175, 255), PyQt5.QtGui.QPalette.Shadow: (58, 56, 52, 255), PyQt5.QtGui.QPalette.Highlight: (194, 188, 175, 255), PyQt5.QtGui.QPalette.HighlightedText: (102, 99, 92, 255), PyQt5.QtGui.QPalette.Link: (120, 164, 229, 255), PyQt5.QtGui.QPalette.LinkVisited: (172, 158, 197, 255), PyQt5.QtGui.QPalette.AlternateBase: (227, 226, 223, 255), PyQt5.QtGui.QPalette.ToolTipBase: (229, 221, 210, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}, PyQt5.QtGui.QPalette.Inactive: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (217, 211, 197, 255), PyQt5.QtGui.QPalette.Light: (247, 245, 242, 255), PyQt5.QtGui.QPalette.Midlight: (223, 217, 202, 255), PyQt5.QtGui.QPalette.Dark: (102, 99, 92, 255), PyQt5.QtGui.QPalette.Mid: (173, 168, 156, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (252, 251, 247, 255), PyQt5.QtGui.QPalette.Window: (210, 204, 190, 255), PyQt5.QtGui.QPalette.Shadow: (60, 59, 54, 255), PyQt5.QtGui.QPalette.Highlight: (230, 143, 141, 255), PyQt5.QtGui.QPalette.HighlightedText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Link: (0, 102, 255, 255), PyQt5.QtGui.QPalette.LinkVisited: (117, 87, 182, 255), PyQt5.QtGui.QPalette.AlternateBase: (248, 247, 244, 255), PyQt5.QtGui.QPalette.ToolTipBase: (229, 221, 210, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}}

def _getHoneyPalette(): return {PyQt5.QtGui.QPalette.Normal: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (186, 189, 183, 255), PyQt5.QtGui.QPalette.Light: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Midlight: (224, 227, 220, 255), PyQt5.QtGui.QPalette.Dark: (103, 105, 101, 255), PyQt5.QtGui.QPalette.Mid: (173, 176, 170, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (212, 215, 208, 255), PyQt5.QtGui.QPalette.Shadow: (59, 60, 58, 255), PyQt5.QtGui.QPalette.Highlight: (227, 170, 0, 255), PyQt5.QtGui.QPalette.HighlightedText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Link: (232, 82, 144, 255), PyQt5.QtGui.QPalette.LinkVisited: (100, 74, 155, 255), PyQt5.QtGui.QPalette.AlternateBase: (255, 251, 231, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 242, 153, 255), PyQt5.QtGui.QPalette.ToolTipText: (64, 48, 0, 255)}, PyQt5.QtGui.QPalette.Disabled: {PyQt5.QtGui.QPalette.Foreground: (99, 99, 95, 255), PyQt5.QtGui.QPalette.Button: (169, 171, 164, 255), PyQt5.QtGui.QPalette.Light: (231, 233, 224, 255), PyQt5.QtGui.QPalette.Midlight: (205, 207, 199, 255), PyQt5.QtGui.QPalette.Dark: (93, 94, 90, 255), PyQt5.QtGui.QPalette.Mid: (158, 160, 154, 255), PyQt5.QtGui.QPalette.Text: (118, 117, 115, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (87, 88, 84, 255), PyQt5.QtGui.QPalette.Base: (230, 229, 227, 255), PyQt5.QtGui.QPalette.Window: (192, 194, 186, 255), PyQt5.QtGui.QPalette.Shadow: (57, 57, 55, 255), PyQt5.QtGui.QPalette.Highlight: (192, 194, 186, 255), PyQt5.QtGui.QPalette.HighlightedText: (99, 99, 95, 255), PyQt5.QtGui.QPalette.Link: (219, 153, 179, 255), PyQt5.QtGui.QPalette.LinkVisited: (161, 149, 183, 255), PyQt5.QtGui.QPalette.AlternateBase: (230, 225, 206, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 242, 153, 255), PyQt5.QtGui.QPalette.ToolTipText: (64, 48, 0, 255)}, PyQt5.QtGui.QPalette.Inactive: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (186, 189, 183, 255), PyQt5.QtGui.QPalette.Light: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Midlight: (224, 227, 220, 255), PyQt5.QtGui.QPalette.Dark: (103, 105, 101, 255), PyQt5.QtGui.QPalette.Mid: (173, 176, 170, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (212, 215, 208, 255), PyQt5.QtGui.QPalette.Shadow: (59, 60, 58, 255), PyQt5.QtGui.QPalette.Highlight: (244, 193, 41, 255), PyQt5.QtGui.QPalette.HighlightedText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Link: (232, 82, 144, 255), PyQt5.QtGui.QPalette.LinkVisited: (100, 74, 155, 255), PyQt5.QtGui.QPalette.AlternateBase: (255, 251, 231, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 242, 153, 255), PyQt5.QtGui.QPalette.ToolTipText: (64, 48, 0, 255)}}

def _getSnowPalette(): return {PyQt5.QtGui.QPalette.Normal: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Light: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Midlight: (233, 233, 233, 255), PyQt5.QtGui.QPalette.Dark: (185, 185, 185, 255), PyQt5.QtGui.QPalette.Mid: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (252, 252, 252, 255), PyQt5.QtGui.QPalette.Shadow: (134, 134, 134, 255), PyQt5.QtGui.QPalette.Highlight: (176, 192, 255, 255), PyQt5.QtGui.QPalette.HighlightedText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Link: (0, 0, 192, 255), PyQt5.QtGui.QPalette.LinkVisited: (88, 0, 176, 255), PyQt5.QtGui.QPalette.AlternateBase: (252, 252, 252, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}, PyQt5.QtGui.QPalette.Disabled: {PyQt5.QtGui.QPalette.Foreground: (164, 164, 164, 255), PyQt5.QtGui.QPalette.Button: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Light: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Midlight: (233, 233, 233, 255), PyQt5.QtGui.QPalette.Dark: (185, 185, 185, 255), PyQt5.QtGui.QPalette.Mid: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Text: (166, 166, 166, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (166, 166, 166, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (252, 252, 252, 255), PyQt5.QtGui.QPalette.Shadow: (134, 134, 134, 255), PyQt5.QtGui.QPalette.Highlight: (252, 252, 252, 255), PyQt5.QtGui.QPalette.HighlightedText: (164, 164, 164, 255), PyQt5.QtGui.QPalette.Link: (166, 166, 233, 255), PyQt5.QtGui.QPalette.LinkVisited: (197, 166, 228, 255), PyQt5.QtGui.QPalette.AlternateBase: (252, 252, 252, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}, PyQt5.QtGui.QPalette.Inactive: {PyQt5.QtGui.QPalette.Foreground: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Button: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Light: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Midlight: (233, 233, 233, 255), PyQt5.QtGui.QPalette.Dark: (185, 185, 185, 255), PyQt5.QtGui.QPalette.Mid: (211, 211, 211, 255), PyQt5.QtGui.QPalette.Text: (0, 0, 0, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Base: (255, 255, 255, 255), PyQt5.QtGui.QPalette.Window: (252, 252, 252, 255), PyQt5.QtGui.QPalette.Shadow: (134, 134, 134, 255), PyQt5.QtGui.QPalette.Highlight: (228, 233, 255, 255), PyQt5.QtGui.QPalette.HighlightedText: (0, 0, 0, 255), PyQt5.QtGui.QPalette.Link: (0, 0, 192, 255), PyQt5.QtGui.QPalette.LinkVisited: (88, 0, 176, 255), PyQt5.QtGui.QPalette.AlternateBase: (252, 252, 252, 255), PyQt5.QtGui.QPalette.ToolTipBase: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ToolTipText: (0, 0, 0, 255)}}

def _getKritaPalette(): return {PyQt5.QtGui.QPalette.Normal: {PyQt5.QtGui.QPalette.Foreground: (20, 20, 20, 255), PyQt5.QtGui.QPalette.Button: (116, 116, 116, 255), PyQt5.QtGui.QPalette.Light: (159, 159, 159, 255), PyQt5.QtGui.QPalette.Midlight: (142, 142, 142, 255), PyQt5.QtGui.QPalette.Dark: (62, 62, 62, 255), PyQt5.QtGui.QPalette.Mid: (108, 108, 108, 255), PyQt5.QtGui.QPalette.Text: (40, 40, 40, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (10, 10, 10, 255), PyQt5.QtGui.QPalette.Base: (160, 160, 160, 255), PyQt5.QtGui.QPalette.Window: (128, 128, 128, 255), PyQt5.QtGui.QPalette.Shadow: (42, 42, 42, 255), PyQt5.QtGui.QPalette.Highlight: (82, 98, 118, 255), PyQt5.QtGui.QPalette.HighlightedText: (180, 180, 180, 255), PyQt5.QtGui.QPalette.Link: (18, 64, 0, 255), PyQt5.QtGui.QPalette.LinkVisited: (5, 0, 82, 255), PyQt5.QtGui.QPalette.AlternateBase: (140, 140, 140, 255), PyQt5.QtGui.QPalette.ToolTipBase: (60, 60, 60, 255), PyQt5.QtGui.QPalette.ToolTipText: (180, 180, 180, 255)}, PyQt5.QtGui.QPalette.Disabled: {PyQt5.QtGui.QPalette.Foreground: (68, 68, 68, 255), PyQt5.QtGui.QPalette.Button: (116, 116, 116, 255), PyQt5.QtGui.QPalette.Light: (159, 159, 159, 255), PyQt5.QtGui.QPalette.Midlight: (142, 142, 142, 255), PyQt5.QtGui.QPalette.Dark: (62, 62, 62, 255), PyQt5.QtGui.QPalette.Mid: (108, 108, 108, 255), PyQt5.QtGui.QPalette.Text: (94, 94, 94, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (57, 57, 57, 255), PyQt5.QtGui.QPalette.Base: (160, 160, 160, 255), PyQt5.QtGui.QPalette.Window: (128, 128, 128, 255), PyQt5.QtGui.QPalette.Shadow: (42, 42, 42, 255), PyQt5.QtGui.QPalette.Highlight: (128, 128, 128, 255), PyQt5.QtGui.QPalette.HighlightedText: (68, 68, 68, 255), PyQt5.QtGui.QPalette.Link: (86, 106, 78, 255), PyQt5.QtGui.QPalette.LinkVisited: (75, 73, 110, 255), PyQt5.QtGui.QPalette.AlternateBase: (140, 140, 140, 255), PyQt5.QtGui.QPalette.ToolTipBase: (60, 60, 60, 255), PyQt5.QtGui.QPalette.ToolTipText: (180, 180, 180, 255)}, PyQt5.QtGui.QPalette.Inactive: {PyQt5.QtGui.QPalette.Foreground: (20, 20, 20, 255), PyQt5.QtGui.QPalette.Button: (116, 116, 116, 255), PyQt5.QtGui.QPalette.Light: (159, 159, 159, 255), PyQt5.QtGui.QPalette.Midlight: (142, 142, 142, 255), PyQt5.QtGui.QPalette.Dark: (62, 62, 62, 255), PyQt5.QtGui.QPalette.Mid: (108, 108, 108, 255), PyQt5.QtGui.QPalette.Text: (40, 40, 40, 255), PyQt5.QtGui.QPalette.BrightText: (255, 255, 255, 255), PyQt5.QtGui.QPalette.ButtonText: (10, 10, 10, 255), PyQt5.QtGui.QPalette.Base: (160, 160, 160, 255), PyQt5.QtGui.QPalette.Window: (128, 128, 128, 255), PyQt5.QtGui.QPalette.Shadow: (42, 42, 42, 255), PyQt5.QtGui.QPalette.Highlight: (104, 119, 137, 255), PyQt5.QtGui.QPalette.HighlightedText: (20, 20, 20, 255), PyQt5.QtGui.QPalette.Link: (18, 64, 0, 255), PyQt5.QtGui.QPalette.LinkVisited: (5, 0, 82, 255), PyQt5.QtGui.QPalette.AlternateBase: (140, 140, 140, 255), PyQt5.QtGui.QPalette.ToolTipBase: (60, 60, 60, 255), PyQt5.QtGui.QPalette.ToolTipText: (180, 180, 180, 255)}}

def _getWintestPalette(): return {0: {0: (0, 0, 0, 255), 1: (240, 240, 240, 255), 2: (255, 255, 255, 255), 3: (227, 227, 227, 255), 4: (160, 160, 160, 255), 5: (160, 160, 160, 255), 6: (0, 0, 0, 255), 7: (255, 255, 255, 255), 8: (0, 0, 0, 255), 9: (255, 255, 255, 255), 10: (240, 240, 240, 255), 11: (105, 105, 105, 255), 12: (51, 153, 255, 255), 13: (255, 255, 255, 255), 14: (0, 0, 255, 255), 15: (255, 0, 255, 255), 16: (246, 246, 246, 255), 18: (255, 255, 220, 255), 19: (0, 0, 0, 255)}, 1: {0: (120, 120, 120, 255), 1: (240, 240, 240, 255), 2: (255, 255, 255, 255), 3: (247, 247, 247, 255), 4: (160, 160, 160, 255), 5: (160, 160, 160, 255), 6: (120, 120, 120, 255), 7: (255, 255, 255, 255), 8: (120, 120, 120, 255), 9: (240, 240, 240, 255), 10: (240, 240, 240, 255), 11: (0, 0, 0, 255), 12: (51, 153, 255, 255), 13: (255, 255, 255, 255), 14: (0, 0, 255, 255), 15: (255, 0, 255, 255), 16: (246, 246, 246, 255), 18: (255, 255, 220, 255), 19: (0, 0, 0, 255)}, 2: {0: (0, 0, 0, 255), 1: (240, 240, 240, 255), 2: (255, 255, 255, 255), 3: (227, 227, 227, 255), 4: (160, 160, 160, 255), 5: (160, 160, 160, 255), 6: (0, 0, 0, 255), 7: (255, 255, 255, 255), 8: (0, 0, 0, 255), 9: (255, 255, 255, 255), 10: (240, 240, 240, 255), 11: (105, 105, 105, 255), 12: (240, 240, 240, 255), 13: (0, 0, 0, 255), 14: (0, 0, 255, 255), 15: (255, 0, 255, 255), 16: (246, 246, 246, 255), 18: (255, 255, 220, 255), 19: (0, 0, 0, 255)}}
