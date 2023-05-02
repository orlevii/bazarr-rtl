FROM alpine:3.10 as builder
WORKDIR /docker_mod

# copy local files
COPY root/ .

# copy script & requirements
WORKDIR /docker_mod/opt/rtl_fix
COPY requirements.txt .
COPY scripts/rtl_fix.py .

FROM scratch

COPY --from=builder /docker_mod /
