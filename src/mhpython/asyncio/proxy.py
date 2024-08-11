#  MIT License
#
#  Copyright (c) 2024 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import asyncio

unix_socket = '/tmp/mrmat-asyncio-proxy.sock'


async def unix_server_handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        print("UNIX server handling client connection")
        while True:
            data_raw = await reader.readline()
            data_in = data_raw.decode()
            if data_in.startswith("exit"):
                data_out = 'Goodbye'
                writer.write(data_out.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
                return
            else:
                data_out = f'Echo: {data_in}'
                writer.write(data_out.encode())
                await writer.drain()

    except asyncio.CancelledError:
        print("UNIX server client connection shutting down")
    finally:
        print("UNIX server client connection shut down")


async def unix_server():
    try:
        print("UNIX server starting")
        server = await asyncio.start_unix_server(unix_server_handle_connection,
                                                 path=unix_socket,
                                                 ssl=None)
        async with server:
            print("UNIX server started")
            await server.serve_forever()
    except asyncio.CancelledError:
        print("UNIX Server shutting down")
    finally:
        print("UNIX server shut down")


async def inet_proxy_handle_connection(inet_reader: asyncio.StreamReader,
                                       inet_writer: asyncio.StreamWriter):
    try:
        print("INET server handling client connection")
        unix_reader, unix_writer = await asyncio.open_unix_connection(path=unix_socket,
                                                                      ssl=None)
        while True:
            data_in = await inet_reader.readline()
            unix_writer.write(data_in)
            await unix_writer.drain()

            data_out = await unix_reader.readline()
            inet_writer.write(data_out)
            await inet_writer.drain()
    except ConnectionResetError:
        print("INET server client connection reset")
        inet_writer.close()
        await inet_writer.wait_closed()
    except asyncio.CancelledError:
        print("INET server client connection shutting down")
    finally:
        print("INET server client connection shut down")


async def inet_proxy():
    try:
        print("INET server starting")
        server = await asyncio.start_server(inet_proxy_handle_connection,
                                            host='127.0.0.1',
                                            port=8000,
                                            ssl=None)
        async with server:
            print("INET server started")
            await server.serve_forever()
    except asyncio.CancelledError:
        print("INET server shutting down")
    finally:
        print("INET server shut down")


async def main() -> int:
    try:
        unix_server_task = asyncio.create_task(unix_server())
        inet_proxy_task = asyncio.create_task(inet_proxy())
        await asyncio.gather(*[unix_server_task, inet_proxy_task], return_exceptions=False)
    except asyncio.CancelledError:
        print('Shutting down')
    finally:
        print('Shut down')
    return 0


def run():
    """
    We must start the async run from a normal function when running with a script entry point
    Returns:
        System exit code
    """
    sys.exit(asyncio.run(main()))


if __name__ == '__main__':
    run()
