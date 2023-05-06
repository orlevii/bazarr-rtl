# bazarr-rtl-mod
This is a mod made for bazarr.
It installs a tool called `bazarr-rtl` on the container that is used to correct RTL `.srt` for some video players.

## Motivation
I experienced issues displaying RTL subtitles on certain video players. Recently, I picked Jellyfin as my home media server. For instance, ExoPlayer may encounter display problems like reversed punctuation marks.

On AndroidTV, you have the option of selecting LibVLC as a player, but while the VLC Player app accurately displays the subtitles, the LibVLC player on Jellyfin does not.

Bazarr's "Reverse RTL" feature exists, but it does not resolve all issues. Consequently, I chose to create a customized post-processing script.

It's worth noting that Jellyfin's WebOS player displays subtitles accurately.


## How to setup:
To set up, add the `DOCKER_MODS` environment variable in your `docker-compose.yml` file.

Here's an example of how it should look:
```yaml
version: "3"
services:
  bazarr:
    image: lscr.io/linuxserver/bazarr:latest
    container_name: bazarr
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - DOCKER_MODS=orlevi/bazarr-rtl-mod:latest
    volumes:
      - # your volumes
    ports:
      - "6767:6767"
```

After adding this variable, the mod will be installed when you start the Bazarr container.

## Bazarr UI
**Note** - the mod is not tested when `Settings -> Languages -> Single Language` is turned on.

* Go to `Settings -> Subtitles`.
* Make sure the `Reverse RTL` flag is turned off.
* Turn on `Custom Post-Processing` and use the following command:
```bash
bazarr_rtl fix -s "{{subtitles}}" -e "{{episode}}" --lang "{{subtitles_language_code2}}" -k
```
* The -k flag keeps the original downloaded subtitles, which can be removed if you don't want them.
