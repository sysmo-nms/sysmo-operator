# -*- mode: ruby -*-

ROOT     = Dir.pwd
JAVA_DIR = File.join(ROOT, "rrd4qt")
GRADLE   = File.join(JAVA_DIR, "gradlew")

task :default => :java_ressource

task :graphics => [:side_icons, :tree_pixmaps]

task :java_ressource do
  rrddst = File.join(ROOT, "ressources/rrd4qt")
  rrdsrc = File.join(ROOT, "rrd4qt/build/install/rrd4qt")
  FileUtils.rm_rf(rrddst)
  Dir.mkdir(rrddst)
  FileUtils.cp(
               File.join(rrdsrc, "bin/rrd4qt"),
               File.join(rrddst))
  FileUtils.cp(
               File.join(rrdsrc, "bin/rrd4qt.bat"),
               File.join(rrddst))
  FileUtils.cp(
               File.join(rrdsrc, "lib/rrd4qt-1.0-SNAPSHOT.jar"),
               File.join(rrddst))
  FileUtils.cp(
               File.join(rrdsrc, "lib/rrd4j-3.0-SYSMO-SNAPSHOT.jar"),
               File.join(rrddst))
  FileUtils.cp(
               File.join(rrdsrc, "lib/javax.json-1.0.4.jar"),
               File.join(rrddst))
end

task :rrd4qt do
  # TODO why does this not work under win32?
  cd JAVA_DIR; sh "#{GRADLE} installDist"
end

task :clean do
  sh "make clean; rm Makefile"
end

task :build do
  sh "qmake -config release"
  sh "make"
  # TODO find and deplace dependencies, write startup script
end

task :linked do
  sh "ldd ./sysmo-operator"
end


task :side_icons do
  sh "inkscape -z --export-png=ressources/images/dashboard-black.png -w 30 ressources/src/dashboard-black.svg"
  sh "inkscape -z --export-png=ressources/images/monitor-black.png   -w 30 ressources/src/monitor-black.svg"
end

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

task :box_icons do
  pix_size = 48
  pixs = ["dialog-warning", "dialog-information", "dialog-error"]
  pixs.each{ |p|
   sh "inkscape -z --export-png=ressources/box_icons/#{p}.png -w #{pix_size} -h #{pix_size} ressources/src/#{p}.svg"
  }
end

task :std_icons do
  icon_size = 32
  sh "inkscape -z --export-png=ressources/icons/hub.png -w #{pix_size} -h #{pix_size} ressources/src/hub.svg"
end
