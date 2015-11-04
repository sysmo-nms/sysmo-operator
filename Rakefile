# -*- mode: ruby -*-

ROOT     = Dir.pwd
JAVA_DIR = File.join(ROOT, "rrd4qt")
GRADLE   = File.join(JAVA_DIR, "gradlew")

RELEASE_VER = "1.0"
RELEASE_DIR = "sysmo-operator-${RELEASE_VER}/"

task :default => :java_ressource


desc "Build good sized pixmap for tree and side icons"
task :graphics => [:side_icons, :tree_pixmaps]


desc "Only under linux, build a deployable release"
task :linux_release do
  cd ROOT
  FileUtils.rm_rf(RELEASE_DIR)
  sh "make clean"
  sh "qmake -config release"
  sh "make"
  FileUtils.mkdir(RELEASE_DIR)
  FileUtils.mkdir(RELEASE_DIR + "platforms")
  FileUtils.cp("sysmo-operator", RELEASE_DIR)
  FileUtils.cp("release_utils/sysmo-operator.sh", "output/")
  FileUtils.cp("/home/seb/Qt/5.4/gcc_64/lib/libQt5Core.so.5", RELEASE_DIR)
  FileUtils.cp("/home/seb/Qt/5.4/gcc_64/lib/libQt5Gui.so.5", RELEASE_DIR)
  FileUtils.cp("/home/seb/Qt/5.4/gcc_64/lib/libQt5Widgets.so.5", RELEASE_DIR)
  FileUtils.cp("/home/seb/Qt/5.4/gcc_64/lib/libQt5Xml.so.5", RELEASE_DIR)
  FileUtils.cp("/home/seb/Qt/5.4/gcc_64/lib/libQt5Network.so.5", RELEASE_DIR)
  FileUtils.cp("/home/seb/Qt/5.4/gcc_64/plugins/platforms/libqxcb.so",
               RELEASE_DIR + "platforms/")
  sh "tar czvf ${RELEASE_DIR}.tar.gz ${RELEASE_DIR}"
end



desc "TODO why does this not work under win32?"
task :rrd4qt do
  cd JAVA_DIR; sh "#{GRADLE} installDist"
end



desc "Build side icons from SVG src"
task :side_icons do
  sh "inkscape -z --export-png=ressources/images/dashboard-black.png -w 30 ressources/src/dashboard-black.svg"
  sh "inkscape -z --export-png=ressources/images/monitor-black.png   -w 30 ressources/src/monitor-black.svg"
end



desc "Build tree pixmaps from SVG src"
task :tree_pixmaps do
  pix_size = 26
  pixs = ["hub", "router", "server-generic",
          "wireless-router", "firewall", "printer", "computer-generic",
          "weather-clear-night", "weather-clear", "weather-few-clouds",
          "weather-few-clouds-night", "weather-overcast",
          "weather-severe-alert", "weather-showers-scattered", "weather-showers",
          "weather-snow", "weather-storm", "media-playback-pause",
          "media-playback-start"]
  pixs.each{ |p|
   sh "inkscape -z --export-png=ressources/pixmaps/#{p}.png -w #{pix_size} -h #{pix_size} ressources/src/#{p}.svg"
  }
end


desc "Build box icons from SVG src"
task :box_icons do
  pix_size = 48
  pixs = ["dialog-warning", "dialog-information", "dialog-error"]
  pixs.each{ |p|
   sh "inkscape -z --export-png=ressources/box_icons/#{p}.png -w #{pix_size} -h #{pix_size} ressources/src/#{p}.svg"
  }
end


desc "Build std icons from SVG src"
task :std_icons do
  icon_size = 32
  sh "inkscape -z --export-png=ressources/icons/hub.png -w #{pix_size} -h #{pix_size} ressources/src/hub.svg"
end

task :rpm_icons do
  sizes = ["16", "22", "24", "256", "32", "48"]
  hcolorSrc = "ressources/src/sysmo-logo-src.svg"
  hcontrastSrc = "ressources/src/sysmo-logo-hc-src.svg"
  FileUtils.cp(hcolorSrc, "ressources/rpm/icons/hicolor/scalable/apps/")
  sizes.each{ |s|
    colorPath = "rpm_icons/icons/hicolor/#{s}x#{s}/apps"
    contrastPath = "rpm_icons/icons/HighContrast/#{s}x#{s}/apps"
    sh "inkscape -z --export-png=#{colorPath}/sysmo.png -w #{s} -h #{s} #{hcolorSrc}"
    sh "inkscape -z --export-png=#{contrastPath}/sysmo.png -w #{s} -h #{s} #{hcontrastSrc}"
  }
end

task :deb_icons do
  sizes = ["128", "64"]
  hcolorSrc = "ressources/src/sysmo-logo-src.svg"
  sizes.each{ |s|
    colorPath = "deb_icons/#{s}x#{s}"
    sh "inkscape -z --export-png=#{colorPath}/sysmo.png -w #{s} -h #{s} #{hcolorSrc}"
  }
end
