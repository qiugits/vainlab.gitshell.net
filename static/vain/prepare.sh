# https://askubuntu.com/questions/271776/how-to-resize-an-image-through-the-terminal
# https://qiita.com/sowd/items/832594dd22d99aebc8a2
mkdir items-64
for n in items/*.png; do
    newfname=$(echo "${n}" | sed "s/items/items-64/g")
    convert -resize 64x64 "${n}" "${newfname}"
done
rm sprite/items-64.css
glue items-64 sprite -p=1 --css-template sprite/css-template.css
