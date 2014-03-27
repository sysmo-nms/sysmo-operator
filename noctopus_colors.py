from    PySide.QtGui    import QPalette, QColor
import  PySide

def getPalette(key):
    if key == 'dark':
        colorDict = _getDarkPalette()
    else:
        return None

    palette = QPalette()
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
