FROM debian
WORKDIR /code
VOLUME ["/app"]
RUN apt update && apt install iverilog python3 python3-pip -y
RUN python3 -m pip install cocotb pytest