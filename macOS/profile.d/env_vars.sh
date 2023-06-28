export proxy_server="`ipconfig getifaddr en1`:3128"
#export proxy_server="127.0.0.1:3128"
#export ALL_PROXY="http://${proxy_server}"
export http_proxy="http://${proxy_server}"
export HTTP_PROXY="http://${proxy_server}"
export https_proxy="http://${proxy_server}"
export HTTPS_PROXY="http://${proxy_server}"
export no_proxy=".local,.crc.testing,.test,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1,${WIFICIDR}"
export NO_PROXY=".local,.crc.testing,.test,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1,${WIFICIDR}"

# Set default Vagrant provider
export VAGRANT_DEFAULT_PROVIDER="vmware_desktop"

