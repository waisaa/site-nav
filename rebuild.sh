# docker rm -f wlf_webnav wlf_mysql > /dev/null 2>&1
docker rm -f wlf_webnav
# docker rmi `docker images | grep wlf_webnav | awk '{print $3}'` > /dev/null 2>&1
docker rmi `docker images | grep wlf_webnav | awk '{print $3}'`
docker build -t wlf_webnav:v1.0.0 .