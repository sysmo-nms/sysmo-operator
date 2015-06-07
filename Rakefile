# -*- mode: ruby -*-

task :default => :build

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

task :graphics => [:side_icons, :tree_pixmaps] 

task :side_icons do
  sh "inkscape -z --export-png=graphics/images/dashboard-black.png -w 30 graphics/src/dashboard-black.svg"
  sh "inkscape -z --export-png=graphics/images/monitor-black.png   -w 30 graphics/src/monitor-black.svg"
end

task :tree_pixmaps do
  pix_size = 22
  sh "inkscape -z --export-png=graphics/pixmaps/hub.png -w #{pix_size} -h #{pix_size} graphics/src/hub.svg"
end

task :std_icons do
  icon_size = 32
  sh "inkscape -z --export-png=graphics/icons/hub.png -w #{pix_size} -h #{pix_size} graphics/src/hub.svg"
end
