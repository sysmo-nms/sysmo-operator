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

task :side_icons do
  sh "inkscape -z --export-png=images/custom/dashboard-black.png -w 30 images/dashboard-black.svg"
  sh "inkscape -z --export-png=images/custom/monitor-black.png -w 30 images/monitor-black.svg"
end
