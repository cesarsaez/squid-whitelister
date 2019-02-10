# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
   config.vm.network "forwarded_port", guest: 3000, host: 8080, host_ip: "127.0.0.1"
   config.vm.provision "shell", inline: <<-SHELL
      sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm  
      sudo yum update -y
      sudo yum install -y git net-tools squid python36u python36u-libs python36u-devel python36u-pip
      sudo pip3.6 install --upgrade pip
      sudo pip3.6 install pipenv
   SHELL
end
