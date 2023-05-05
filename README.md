# bazarr-rtl
A `linuxserver.io` mod for `bazarr`
* Installs the bazarr-rtl cli tool on the container

## How to setup:
In your `docker-compose.yml` add the `DOCKER_MODS` environment variable:
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

Next time you start your bazarr container, the mod will be installed.

## Bazarr UI
**Note**: `Settings -> Languages -> Single Language` should be turned off, this mod is not tested when this flag is on 

* Go to `Settings -> Subtitles`
* Make sure the `Reverse RTL` flag is turned off.
* Turn on `Custom Post-Processing` and use the following command:
```bash
bazarr_rtl fix -s "{{subtitles}}" -e "{{episode}}" --lang "{{subtitles_language_code2}}" -k
```
* The `-k` flag keeps the original downloaded subtitles as well, you can drop this flag if you don't want it.
