# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
   config.vm.box = "ubuntu/focal64"
   config.vm.synced_folder "../secrets/", "/secrets"
   config.vm.provision :shell, path: "bootstrap.sh"
   config.vm.provision "shell", inline: "sudo apt install swapspace -y"
   config.vm.provision "shell", run: "always", path: "reboot-provision.sh"
   config.vm.network "private_network", ip: "10.50.0.2"
   config.vm.network "forwarded_port", guest: 8100, host: 8100, host_ip: "0.0.0.0"

   # The default provider is Virtualbox.  This works on Windows, Linux and Mac Intel
   # but not Mac M1
   config.vm.provider "virtualbox" do |vb|
    vb.name = "coffeeshop"
    vb.memory = "2048"
    vb.customize ["modifyvm", :id, "--memory", "2048"]
   end 

   config.vm.provider :docker do |docker, override|
     config.vm.hostname = "coffeeshop"
     override.vm.box = nil
     docker.image = "mbakereth/vagrant-provider-ubuntu:focal"
     docker.create_args = ['--memory=4g']
     docker.create_args = ['--cpuset-cpus=2']

     docker.remains_running = true
     docker.has_ssh = true
     docker.privileged = true
     docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
     docker.create_args = ["--cgroupns=host"]
     # Uncomment to force arm64 for testing images
     #docker.create_args = ['--platform=linux/arm64']
   end

end
