from    PyQt4.QtGui    import QPalette, QColor
import  PyQt4

def getPalette(key):
    palette = QPalette()

    if key == 'dark':
        colorDict = _getDarkPalette()
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

    for group in colorDict.keys():
        colorGroup = colorDict[group]
        for role in colorGroup.keys():
            (r, g, b, a)    = colorGroup[role]
            roleColor       = QColor(r,g,b,a)
            palette.setColor(group, role, roleColor)

    return palette

def _getDarkPalette():
    return {
        PyQt4.QtGui.QPalette.ColorGroup.Normal: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (224, 222, 219, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (64, 63, 62, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (79, 77, 77, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (65, 64, 64, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (23, 22, 22, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (41, 40, 40, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (212, 210, 207, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (232, 230, 227, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (32, 31, 31, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (48, 47, 47, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (16, 16, 16, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (24, 72, 128, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (80, 142, 216, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (142, 121, 165, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (36, 35, 35, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (16, 48, 80, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (196, 209, 224, 255)
        },
        PyQt4.QtGui.QPalette.ColorGroup.Disabled: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (96, 95, 94, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (56, 55, 54, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (75, 73, 73, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (61, 59, 59, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (20, 20, 20, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (36, 35, 35, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (83, 82, 81, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (108, 106, 105, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (28, 27, 27, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (42, 41, 41, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (14, 14, 14, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (42, 41, 41, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (96, 95, 94, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (42, 61, 84, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (62, 55, 68, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (31, 30, 30, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (16, 48, 80, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (196, 209, 224, 255)
        },
        PyQt4.QtGui.QPalette.ColorGroup.Inactive: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (224, 222, 219, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (64, 63, 62, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (79, 77, 77, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (65, 64, 64, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (23, 22, 22, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (41, 40, 40, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (212, 210, 207, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (232, 230, 227, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (32, 31, 31, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (48, 47, 47, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (16, 16, 16, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (25, 57, 95, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (224, 222, 219, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (80, 142, 216, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (142, 121, 165, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (36, 35, 35, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (16, 48, 80, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (196, 209, 224, 255)
        }
    }

def _getTerraPalette():
    return {
        PyQt4.QtGui.QPalette.ColorGroup.Normal: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (203, 194, 191, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (226, 220, 211, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (203, 196, 184, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (92, 88, 83, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (157, 151, 142, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (244, 234, 231, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (189, 182, 171, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (57, 55, 52, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (106, 141, 210, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (17, 44, 12, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (74, 96, 57, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (235, 226, 223, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (164, 162, 139, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (19, 24, 17, 255)
        },
        PyQt4.QtGui.QPalette.ColorGroup.Disabled: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (95, 91, 84, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (190, 182, 177, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (215, 207, 193, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (192, 185, 172, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (86, 83, 77, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (148, 143, 133, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (119, 114, 111, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (101, 97, 93, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (226, 217, 212, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (178, 171, 159, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (55, 53, 49, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (178, 171, 159, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (95, 91, 84, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (127, 134, 116, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (152, 156, 136, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (218, 210, 205, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (164, 162, 139, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (19, 24, 17, 255)
        },
        PyQt4.QtGui.QPalette.ColorGroup.Inactive: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (203, 194, 191, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (226, 220, 211, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (203, 196, 184, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (92, 88, 83, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (157, 151, 142, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (244, 234, 231, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (189, 182, 171, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (57, 55, 52, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (151, 169, 210, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (0, 0, 0, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (17, 44, 12, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (74, 96, 57, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (235, 226, 223, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (164, 162, 139, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (19, 24, 17, 255)
        }
    }

def _getLagoonPalette():
    return {
        PyQt4.QtGui.QPalette.ColorGroup.Normal: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (206, 227, 213, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (63, 85, 135, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (130, 169, 215, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (109, 151, 199, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (48, 66, 87, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (84, 116, 152, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (205, 197, 231, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (227, 217, 201, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (48, 65, 105, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (99, 137, 180, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (32, 45, 59, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (122, 102, 41, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (31, 147, 218, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (59, 114, 214, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (55, 62, 79, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (67, 91, 122, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (247, 234, 234, 255)
        },
        PyQt4.QtGui.QPalette.ColorGroup.Disabled: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (120, 148, 168, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (55, 74, 118, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (109, 151, 198, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (97, 134, 177, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (42, 58, 77, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (74, 102, 134, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (90, 97, 131, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (106, 115, 139, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (42, 57, 92, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (87, 120, 158, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (29, 40, 53, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (87, 120, 158, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (120, 148, 168, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (37, 82, 127, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (45, 72, 126, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (48, 54, 69, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (67, 91, 122, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (247, 234, 234, 255)
        },
        PyQt4.QtGui.QPalette.ColorGroup.Inactive: {
            PyQt4.QtGui.QPalette.ColorRole.Foreground: (206, 227, 213, 255),
            PyQt4.QtGui.QPalette.ColorRole.Button: (63, 85, 135, 255),
            PyQt4.QtGui.QPalette.ColorRole.Light: (130, 169, 215, 255),
            PyQt4.QtGui.QPalette.ColorRole.Midlight: (109, 151, 199, 255),
            PyQt4.QtGui.QPalette.ColorRole.Dark: (48, 66, 87, 255),
            PyQt4.QtGui.QPalette.ColorRole.Mid: (84, 116, 152, 255),
            PyQt4.QtGui.QPalette.ColorRole.Text: (205, 197, 231, 255),
            PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PyQt4.QtGui.QPalette.ColorRole.ButtonText: (227, 217, 201, 255),
            PyQt4.QtGui.QPalette.ColorRole.Base: (48, 65, 105, 255),
            PyQt4.QtGui.QPalette.ColorRole.Window: (99, 137, 180, 255),
            PyQt4.QtGui.QPalette.ColorRole.Shadow: (32, 45, 59, 255),
            PyQt4.QtGui.QPalette.ColorRole.Highlight: (133, 124, 79, 255),
            PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (206, 227, 213, 255),
            PyQt4.QtGui.QPalette.ColorRole.Link: (31, 147, 218, 255),
            PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (59, 114, 214, 255),
            PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (55, 62, 79, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (67, 91, 122, 255),
            PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (247, 234, 234, 255)
        }
    }


def _getDesertPalette(): return {PyQt4.QtGui.QPalette.ColorGroup.Normal: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (217, 211, 197, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (247, 245, 242, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (223, 217, 202, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (102, 99, 92, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (173, 168, 156, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (252, 251, 247, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (210, 204, 190, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (60, 59, 54, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (125, 10, 10, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (0, 102, 255, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (117, 87, 182, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (248, 247, 244, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (229, 221, 210, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (0, 0, 0, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Disabled: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (102, 99, 92, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (200, 195, 182, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (232, 227, 216, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (208, 202, 188, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (94, 91, 85, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (161, 156, 145, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (120, 119, 117, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (105, 102, 95, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (231, 230, 226, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (194, 188, 175, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (58, 56, 52, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (194, 188, 175, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (102, 99, 92, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (120, 164, 229, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (172, 158, 197, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (227, 226, 223, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (229, 221, 210, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (0, 0, 0, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Inactive: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (217, 211, 197, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (247, 245, 242, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (223, 217, 202, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (102, 99, 92, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (173, 168, 156, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (252, 251, 247, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (210, 204, 190, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (60, 59, 54, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (230, 143, 141, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (0, 102, 255, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (117, 87, 182, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (248, 247, 244, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (229, 221, 210, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (0, 0, 0, 255)}}

def _getHoneyPalette(): return {PyQt4.QtGui.QPalette.ColorGroup.Normal: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (186, 189, 183, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (224, 227, 220, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (103, 105, 101, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (173, 176, 170, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (212, 215, 208, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (59, 60, 58, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (227, 170, 0, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (232, 82, 144, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (100, 74, 155, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (255, 251, 231, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (255, 242, 153, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (64, 48, 0, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Disabled: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (99, 99, 95, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (169, 171, 164, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (231, 233, 224, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (205, 207, 199, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (93, 94, 90, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (158, 160, 154, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (118, 117, 115, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (87, 88, 84, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (230, 229, 227, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (192, 194, 186, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (57, 57, 55, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (192, 194, 186, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (99, 99, 95, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (219, 153, 179, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (161, 149, 183, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (230, 225, 206, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (255, 242, 153, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (64, 48, 0, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Inactive: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (186, 189, 183, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (224, 227, 220, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (103, 105, 101, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (173, 176, 170, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (212, 215, 208, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (59, 60, 58, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (244, 193, 41, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (232, 82, 144, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (100, 74, 155, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (255, 251, 231, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (255, 242, 153, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (64, 48, 0, 255)}}

def _getSnowPalette(): return {PyQt4.QtGui.QPalette.ColorGroup.Normal: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (211, 211, 211, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (233, 233, 233, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (185, 185, 185, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (211, 211, 211, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (252, 252, 252, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (134, 134, 134, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (176, 192, 255, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (0, 0, 192, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (88, 0, 176, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (252, 252, 252, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (0, 0, 0, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Disabled: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (164, 164, 164, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (211, 211, 211, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (233, 233, 233, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (185, 185, 185, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (211, 211, 211, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (166, 166, 166, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (166, 166, 166, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (252, 252, 252, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (134, 134, 134, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (252, 252, 252, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (164, 164, 164, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (166, 166, 233, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (197, 166, 228, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (252, 252, 252, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (0, 0, 0, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Inactive: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (211, 211, 211, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (233, 233, 233, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (185, 185, 185, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (211, 211, 211, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (252, 252, 252, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (134, 134, 134, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (228, 233, 255, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (0, 0, 0, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (0, 0, 192, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (88, 0, 176, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (252, 252, 252, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (0, 0, 0, 255)}}

def _getKritaPalette(): return {PyQt4.QtGui.QPalette.ColorGroup.Normal: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (20, 20, 20, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (116, 116, 116, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (159, 159, 159, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (142, 142, 142, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (62, 62, 62, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (108, 108, 108, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (40, 40, 40, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (10, 10, 10, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (160, 160, 160, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (128, 128, 128, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (42, 42, 42, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (82, 98, 118, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (180, 180, 180, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (18, 64, 0, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (5, 0, 82, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (140, 140, 140, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (60, 60, 60, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (180, 180, 180, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Disabled: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (68, 68, 68, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (116, 116, 116, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (159, 159, 159, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (142, 142, 142, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (62, 62, 62, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (108, 108, 108, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (94, 94, 94, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (57, 57, 57, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (160, 160, 160, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (128, 128, 128, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (42, 42, 42, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (128, 128, 128, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (68, 68, 68, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (86, 106, 78, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (75, 73, 110, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (140, 140, 140, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (60, 60, 60, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (180, 180, 180, 255)}, PyQt4.QtGui.QPalette.ColorGroup.Inactive: {PyQt4.QtGui.QPalette.ColorRole.Foreground: (20, 20, 20, 255), PyQt4.QtGui.QPalette.ColorRole.Button: (116, 116, 116, 255), PyQt4.QtGui.QPalette.ColorRole.Light: (159, 159, 159, 255), PyQt4.QtGui.QPalette.ColorRole.Midlight: (142, 142, 142, 255), PyQt4.QtGui.QPalette.ColorRole.Dark: (62, 62, 62, 255), PyQt4.QtGui.QPalette.ColorRole.Mid: (108, 108, 108, 255), PyQt4.QtGui.QPalette.ColorRole.Text: (40, 40, 40, 255), PyQt4.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255), PyQt4.QtGui.QPalette.ColorRole.ButtonText: (10, 10, 10, 255), PyQt4.QtGui.QPalette.ColorRole.Base: (160, 160, 160, 255), PyQt4.QtGui.QPalette.ColorRole.Window: (128, 128, 128, 255), PyQt4.QtGui.QPalette.ColorRole.Shadow: (42, 42, 42, 255), PyQt4.QtGui.QPalette.ColorRole.Highlight: (104, 119, 137, 255), PyQt4.QtGui.QPalette.ColorRole.HighlightedText: (20, 20, 20, 255), PyQt4.QtGui.QPalette.ColorRole.Link: (18, 64, 0, 255), PyQt4.QtGui.QPalette.ColorRole.LinkVisited: (5, 0, 82, 255), PyQt4.QtGui.QPalette.ColorRole.AlternateBase: (140, 140, 140, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipBase: (60, 60, 60, 255), PyQt4.QtGui.QPalette.ColorRole.ToolTipText: (180, 180, 180, 255)}}
