FROM scratch

# copy local files
COPY root/ /

# copy script & requirements
COPY requirements.txt /opt/rtl_fix/requirements.txt
COPY scripts/rtl_fix.py /opt/rtl_fix/rtl_fix.py
