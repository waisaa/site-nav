docker rm -f wlf_webnav wlf_mysql
docker rmi `docker images | grep wlf_webnav | awk '{print $3}'`
docker build -t wlf_webnav:v1.0.0 .