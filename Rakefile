#

task :default => :build

task :clean do
  sh "make clean; rm Makefile"
end

task :build do
  sh "qmake -config release; make"
  # TODO find and deplace dependencies, write startup script
end

task :linked do
  sh "ldd ./sysmo-operator"
end
