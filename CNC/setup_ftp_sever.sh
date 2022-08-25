sudo apt update
sudo apt install vsftpd
sudo ufw allow 20/tcp
sudo ufw allow 21/tcp
sudo cp /etc/vsftpd.conf /etc/vsftpd.conf.orig
echo "listen=YES
listen_ipv6=NO
connect_from_port_20=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
chroot_local_user=YES
allow_writeable_chroot=YES
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
pasv_enable=YES
pasv_min_port=40000
pasv_max_port=45000
userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO" >> /etc/vsftpd.conf

sudo adduser tin
sudo passwd tin
echo "tin" | sudo tee -a /etc/vsftpd.userlist
sudo systemctl restart vsftpd
sudo systemctl enable vsftpd