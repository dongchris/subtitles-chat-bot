echo "Specify where you want to store the urls"
read url
echo "Specify the file path that contains your YouTube API key"
read api
echo "Are you searching for a user or channel?"
read type
echo "Specify the relevant id youtube.com/{user or channel}"
read id
python scrape_youtube_url.py $(cat $api) $id $type > $url
echo "Specify the name of the directory that you want to store these subtitles in"
read storage
mkdir $storage
storage+='/'
for name in $(cat $url); do youtube-dl --sub-lang en --write-sub --skip-download $name; done

mv *.vtt $storage