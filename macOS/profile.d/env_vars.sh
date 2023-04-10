#export proxy_server="`ipconfig getifaddr en0`:3128"
export proxy_server="127.0.0.1:3128"
#export ALL_PROXY="http://${proxy_server}"
export http_proxy="http://${proxy_server}"
export HTTP_PROXY="http://${proxy_server}"
export https_proxy="http://${proxy_server}"
export HTTPS_PROXY="http://${proxy_server}"
export no_proxy=".local,.test,.crc.testing,.testing,127.0.0.1,${WIFICIDR}"
export NO_PROXY=".local,.test,.crc.testing,.testing,127.0.0.1,${WIFICIDR}"

