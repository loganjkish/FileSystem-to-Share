/usr/bin/python ./compile.py
wine python ./compile.py

mv ./fsts-bin ../dist/fsts-bin
mv ./fsts-bin.exe ../dist/fsts-bin.exe

rm -rf ./dist

cd ..

mkdir ./temp
cp ./dist/config.json ./temp
mkdir ./temp/fsts-setupFiles
cp ./scripts/windows.bat ./temp/fsts-setupFiles/windows.bat
cp ./scripts/linux.sh ./temp/fsts-setupFiles/linux.sh
cp ./scripts/mac.sh ./temp/fsts-setupFiles/mac.sh
cp ./src/fsts_main.py ./temp/fsts_main.py
cp -r ./static ./temp/static
cp ./LICENSE ./temp/LICENSE
cp ./readme.md ./temp/readme.md

cd temp
zip -r ../dist/release.zip ./*
cd ..

rm -rf ./temp