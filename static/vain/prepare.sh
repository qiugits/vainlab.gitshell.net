# https://askubuntu.com/questions/271776/how-to-resize-an-image-through-the-terminal
# https://qiita.com/sowd/items/832594dd22d99aebc8a2
for n in items/*.png; do
    newfname=$(echo "${n}" | sed "s/items/items_resized/g")
    convert -resize 64x64 "${n}" "${newfname}"
done
