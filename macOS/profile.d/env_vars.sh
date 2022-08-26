export proxy_server="`ipconfig getifaddr en0`:3128"
#export ALL_PROXY="http://${proxy_server}"
export http_proxy="http://${proxy_server}"
export HTTP_PROXY="http://${proxy_server}"
export https_proxy="http://${proxy_server}"
export HTTPS_PROXY="http://${proxy_server}"
export no_proxy=localhost,127.0.0.1,.local,.test,testing,.amazonaws.com,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12
export NO_PROXY=localhost,127.0.0.1,.local,.test,.testing,.amazonaws.com,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12

