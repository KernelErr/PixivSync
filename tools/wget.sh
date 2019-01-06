for url in `cat $1`;do
    nohup wget $url --referer="https://www.pixiv.net" >/dev/null 2>&1 &
done
