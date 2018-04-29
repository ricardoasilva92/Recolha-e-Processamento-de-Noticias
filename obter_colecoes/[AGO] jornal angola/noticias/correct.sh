for file in *.xml
do
VAR="\<?xml version=\"1.0\" encoding=\"UTF-8\"?\>\<xml\>"
sed -i "1s/.*/$VAR/" $file
echo \<\/xml\> >> $file
done
