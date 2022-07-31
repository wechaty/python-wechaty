# start to build wechaty-ui into wechaty

make clean
git clone https://github.com/wechaty/wechaty-ui ui 
cd ui
cnpm i && cnpm run build

# move the dist files to 
echo "starting to copy files to the package ..."
pwd
cp -r dist/ ../src/wechaty/ui