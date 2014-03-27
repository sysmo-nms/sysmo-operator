from    PySide.QtGui    import QPalette, QColor
import  PySide

def getPalette(key):
    palette = QPalette()

    if key == 'dark':
        colorDict = _getDarkPalette()
    elif key == 'terra':
        colorDict = _getTerraPalette()
    elif key == 'lagoon':
        colorDict = _getLagoonPalette()
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
        PySide.QtGui.QPalette.ColorGroup.Normal: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (224, 222, 219, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (64, 63, 62, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (79, 77, 77, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (65, 64, 64, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (23, 22, 22, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (41, 40, 40, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (212, 210, 207, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (232, 230, 227, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (32, 31, 31, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (48, 47, 47, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (16, 16, 16, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (24, 72, 128, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (80, 142, 216, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (142, 121, 165, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (36, 35, 35, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (16, 48, 80, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (196, 209, 224, 255)
        },
        PySide.QtGui.QPalette.ColorGroup.Disabled: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (96, 95, 94, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (56, 55, 54, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (75, 73, 73, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (61, 59, 59, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (20, 20, 20, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (36, 35, 35, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (83, 82, 81, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (108, 106, 105, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (28, 27, 27, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (42, 41, 41, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (14, 14, 14, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (42, 41, 41, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (96, 95, 94, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (42, 61, 84, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (62, 55, 68, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (31, 30, 30, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (16, 48, 80, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (196, 209, 224, 255)
        },
        PySide.QtGui.QPalette.ColorGroup.Inactive: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (224, 222, 219, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (64, 63, 62, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (79, 77, 77, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (65, 64, 64, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (23, 22, 22, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (41, 40, 40, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (212, 210, 207, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (232, 230, 227, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (32, 31, 31, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (48, 47, 47, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (16, 16, 16, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (25, 57, 95, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (224, 222, 219, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (80, 142, 216, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (142, 121, 165, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (36, 35, 35, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (16, 48, 80, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (196, 209, 224, 255)
        }
    }

def _getTerraPalette():
    return {
        PySide.QtGui.QPalette.ColorGroup.Normal: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (203, 194, 191, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (226, 220, 211, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (203, 196, 184, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (92, 88, 83, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (157, 151, 142, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (244, 234, 231, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (189, 182, 171, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (57, 55, 52, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (106, 141, 210, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (17, 44, 12, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (74, 96, 57, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (235, 226, 223, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (164, 162, 139, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (19, 24, 17, 255)
        },
        PySide.QtGui.QPalette.ColorGroup.Disabled: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (95, 91, 84, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (190, 182, 177, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (215, 207, 193, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (192, 185, 172, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (86, 83, 77, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (148, 143, 133, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (119, 114, 111, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (101, 97, 93, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (226, 217, 212, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (178, 171, 159, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (55, 53, 49, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (178, 171, 159, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (95, 91, 84, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (127, 134, 116, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (152, 156, 136, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (218, 210, 205, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (164, 162, 139, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (19, 24, 17, 255)
        },
        PySide.QtGui.QPalette.ColorGroup.Inactive: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (0, 0, 0, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (203, 194, 191, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (226, 220, 211, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (203, 196, 184, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (92, 88, 83, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (157, 151, 142, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (0, 0, 0, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (0, 0, 0, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (244, 234, 231, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (189, 182, 171, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (57, 55, 52, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (151, 169, 210, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (0, 0, 0, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (17, 44, 12, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (74, 96, 57, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (235, 226, 223, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (164, 162, 139, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (19, 24, 17, 255)
        }
    }

def _getLagoonPalette():
    return {
        PySide.QtGui.QPalette.ColorGroup.Normal: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (206, 227, 213, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (63, 85, 135, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (130, 169, 215, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (109, 151, 199, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (48, 66, 87, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (84, 116, 152, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (205, 197, 231, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (227, 217, 201, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (48, 65, 105, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (99, 137, 180, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (32, 45, 59, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (122, 102, 41, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (31, 147, 218, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (59, 114, 214, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (55, 62, 79, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (67, 91, 122, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (247, 234, 234, 255)
        },
        PySide.QtGui.QPalette.ColorGroup.Disabled: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (120, 148, 168, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (55, 74, 118, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (109, 151, 198, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (97, 134, 177, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (42, 58, 77, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (74, 102, 134, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (90, 97, 131, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (106, 115, 139, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (42, 57, 92, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (87, 120, 158, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (29, 40, 53, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (87, 120, 158, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (120, 148, 168, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (37, 82, 127, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (45, 72, 126, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (48, 54, 69, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (67, 91, 122, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (247, 234, 234, 255)
        },
        PySide.QtGui.QPalette.ColorGroup.Inactive: {
            PySide.QtGui.QPalette.ColorRole.Foreground: (206, 227, 213, 255),
            PySide.QtGui.QPalette.ColorRole.Button: (63, 85, 135, 255),
            PySide.QtGui.QPalette.ColorRole.Light: (130, 169, 215, 255),
            PySide.QtGui.QPalette.ColorRole.Midlight: (109, 151, 199, 255),
            PySide.QtGui.QPalette.ColorRole.Dark: (48, 66, 87, 255),
            PySide.QtGui.QPalette.ColorRole.Mid: (84, 116, 152, 255),
            PySide.QtGui.QPalette.ColorRole.Text: (205, 197, 231, 255),
            PySide.QtGui.QPalette.ColorRole.BrightText: (255, 255, 255, 255),
            PySide.QtGui.QPalette.ColorRole.ButtonText: (227, 217, 201, 255),
            PySide.QtGui.QPalette.ColorRole.Base: (48, 65, 105, 255),
            PySide.QtGui.QPalette.ColorRole.Window: (99, 137, 180, 255),
            PySide.QtGui.QPalette.ColorRole.Shadow: (32, 45, 59, 255),
            PySide.QtGui.QPalette.ColorRole.Highlight: (133, 124, 79, 255),
            PySide.QtGui.QPalette.ColorRole.HighlightedText: (206, 227, 213, 255),
            PySide.QtGui.QPalette.ColorRole.Link: (31, 147, 218, 255),
            PySide.QtGui.QPalette.ColorRole.LinkVisited: (59, 114, 214, 255),
            PySide.QtGui.QPalette.ColorRole.AlternateBase: (55, 62, 79, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipBase: (67, 91, 122, 255),
            PySide.QtGui.QPalette.ColorRole.ToolTipText: (247, 234, 234, 255)
        }
    }
